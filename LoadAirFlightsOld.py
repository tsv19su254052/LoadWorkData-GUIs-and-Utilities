# -*- coding: utf-8 -*-
# Версия интерпретатора 3.6 (на 3.7 работает так же)

'''Проверяем и добавляем в БД:
  - самолеты,
  - маршруты,
  - авиарейсы
  из файлы-справочника типа *.csv
  У каждого самолета один код регистрацииД
  Допускается, что сторонними обработками могли быть внесены самолеты других моделей с тем же кодом регистрации
  У маршрута может быть несколько разноименных авиарейсов
  У авиарейса может быть несколько маршрутов
'''

#import pymssql - работает тяжелее
import pyodbc
import pandas
import itertools
import datetime
import time
import os

__Version__ = 4.41  # Версия обработки

# Открываем соединение с БД
__Driver__ = "SQL Server"  # список доступных драйверов выводит команда pyodbc.drivers()
__Server__ = "Data-Server"
__DataBase__ = "AirFlightsDBNew42"
__mydsn__ = "AirFlightsDBNew4_DSN"
# Через системный DSN (для всех пользователей) - все настроено и протестировано в DSN
#cnxn = pyodbc.connect(__mydsn__)
# Через драйвер ODBC
cnxn = pyodbc.connect(driver=__Driver__, server=__Server__, database=__DataBase__)
#cnxn.set_attr(pyodbc.SQL_ATTR_TXN_ISOLATION, pyodbc.SQL_TXN_SERIALIZABLE) - устарелая операция, ошибка
# Разрешаем транзакции и вызываем функцию commit() при необходимости в явном виде
cnxn.autocommit = False  # Значение AUTOCOMMIT в СУБД по умолчанию FALSE
# Ставим курсор на начало
seek = cnxn.cursor()
__DebugOutPut__ = False
"""
Файл текстового вывода
Или делать вывод в отдельную БД
"""
__OutputFileTXT__ = "LogReport_DBNew4"


def QueryAirCraft(Registration):
    '''Возвращает данные самолета по его регистрации
       Считаем, что у одного самолета любой модели, в том числе неизвестной одна регистрация - это неверно
       Но дубликаты могут быть, так как при переходе самолета от одной компании-владельца к другой регистрация как правило меняется
       и однозначно определить самолет можно по сочетанию его заводских номеров
       Регистрация через несколько лет может передаваться от утилизированного самолета к новому без привязки к изготовителю и модели
       Выводим первую найденную строку
    '''
    SQLQuery = "SELECT * FROM dbo.AirCraftsTable WHERE AirCraftRegistration = '" + str(Registration) + "' ORDER BY AirCraftAirLine, AirCraftRegistration"
    if __DebugOutPut__:
        seek.execute(SQLQuery)  # где-то в ОЗУ висит результат выборки по запросу
        print("\n  самолет ", str(seek.fetchall()))
    seek.execute(SQLQuery)
    ResultSQL = seek.fetchone()  # курсор забирает одну строку и сдвигается на строку вниз
    if ResultSQL:
        return ResultSQL
    else:
        return False  # NULL (пустая строка таблицы) в SQL => (None,) в Python-е -> условия с None не работает, функция не возвращает None -> ошибка, скрипт слетает


def QueryAirLine(IATA):
    '''Возвращает данные авиакомпании по ее коду IATA
       Считаем, что одному коду соответствует одна авиакомпания
       Дубликаты есть (221 шт.)
       Выводим первую найденную строку
    '''
    SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineCodeIATA = '" + str(IATA) + "' ORDER BY AirLineName"
    if __DebugOutPut__:
        seek.execute(SQLQuery)
        print("\n  авиакомпания ", str(seek.fetchall()))
    seek.execute(SQLQuery)
    ResultSQL = seek.fetchone()
    if ResultSQL:
        return ResultSQL
    else:
        return False


def QueryAirLine2(UN):
    '''Возвращает данные авиакомпании по ее первичному ключу
       Дубликатов быть не может
    '''
    SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineUniqueNumber = '" + str(UN) + "' "
    seek.execute(SQLQuery)
    ResultSQL = seek.fetchone()
    if ResultSQL:
        return ResultSQL
    else:
        return False


def QueryAirPort(IATA):
    '''Возвращает данные аэропортов отправления и прибытия по их кодам IATA
       Считаем, что каждому коду соответствует один аэропорт
       Дубликаты есть (2 шт.) - убрал
       Выводим первую найденную строку
    '''
    SQLQuery = "SELECT * FROM dbo.AirPortsTable WHERE AirPortCodeIATA = '" + str(IATA) + "' ORDER BY AirPortCountry, AirPortCity, AirPortCodeIATA"
    if __DebugOutPut__:
        seek.execute(SQLQuery)
        print("\n  аэропорт ", str(seek.fetchall()))
    seek.execute(SQLQuery)
    ResultSQL = seek.fetchone()
    if ResultSQL:
        return ResultSQL
    else:
        return False


def QueryAirRoute(IATADeparture, IATAArrival):
    '''Возвращает данные маршрута по кодам IATA аэропортов
       Считаем, что от одного до другого аэропорта может быть только один маршрут
       Если несколько, выводим первый найденный маршрут
    '''
    SQLQuery = """SELECT dbo.AirRoutesTable.AirRouteUniqueNumber                                 
               FROM dbo.AirRoutesTable INNER JOIN
               dbo.AirPortsTable ON dbo.AirRoutesTable.AirPortDeparture = dbo.AirPortsTable.AirPortUniqueNumber INNER JOIN
               dbo.AirPortsTable AS AirPortsTable_1 ON dbo.AirRoutesTable.AirPortArrival = AirPortsTable_1.AirPortUniqueNumber
               WHERE (dbo.AirPortsTable.AirPortCodeIATA = '""" + str(IATADeparture) + "') AND (AirPortsTable_1.AirPortCodeIATA = '" + str(IATAArrival) + "') "
    if __DebugOutPut__:
        seek.execute(SQLQuery)
        print("\n  маршрут ", str(seek.fetchall()))
    seek.execute(SQLQuery)
    ResultSQL = seek.fetchone()
    if ResultSQL:
        return ResultSQL
    else:
        return False


def QueryTransactionIsolationLevel():
    """Возвращает уровень изоляции транзакций для данного подключения
       Для представления последовательных операций внутри транзакций СУБД поддерживает четыре уровня изоляции транзакции.
       Драйвер ODBC SQL Server-а поддерживает:
        - SQL_TXN_READ_COMMITTED_SNAPSHOT
        - SQL_TXN_SERIALIZABLE (многострочный запрос к одной таблице несколько раз за одну транзакцию)
        - SQL_TXN_REPEATABLE_READ (многострочный запрос к одной таблице один раз за одну транзакцию)
        - SQL_TXN_READ_COMMITTED (однострочный запрос к одной таблице один раз, не накапливаем данные, не вычисляем) - по умолчанию
        - SQL_TXN_READ_UNCOMMITTED
    """
    SQLQuery = """SELECT CASE transaction_isolation_level
                     WHEN 0 THEN 'UNSPECIFIED'
                     WHEN 1 THEN 'READ UNCOMMITTED'
                     WHEN 2 THEN 'READ COMMITTED'
                     WHEN 3 THEN 'REPEATABLE READ'
                     WHEN 4 THEN 'SERIALIZABLE'
                     WHEN 5 THEN 'SNAPSHOT'
                     END AS TIL
           FROM sys.dm_exec_sessions
           WHERE session_id = @@SPID"""
    seek.execute(SQLQuery)
    ResultSQL = seek.fetchone()
    if ResultSQL:
        return ResultSQL.TIL
    else:
        return False


def SetTransactionIsolationLevel(Level):
    """ Устанавливает уровень изоляции транзакций
        Берет на вход его название на SQL в виде строки
        READ COMMITTED (Чтение зафиксированных данных) - (по умолчанию) инструкции не могут считывать данные, которые были изменены и еще не зафиксированы другими транзакциями
                        Другие транзакции могут изменять и вставлять данные, читаемые текущей транзакцией
        REPEATABLE READ (Повторяемость чтения) - еще плюс Другие транзакции могут только вставлять данные, читаемые текущей транзакцией
        SERIALIZABLE (Упорядочиваемость) - еще плюс Другие транзакции не могут изменять и вставлять данные в диапазон, читаемые текущей транзакцией

       Одновременно может быть установлен только один параметр уровня изоляции, который продолжает действовать для текущего соединения до тех пор,
       пока не будет явно изменен. Все операции считывания, выполняемые в рамках транзакции, функционируют в соответствии с правилами уровня изоляции,
       если только табличное указание в предложении FROM инструкции не задает другое поведение блокировки или управления версиями строк для таблицы.

       Уровни изоляции транзакции определяют тип блокировки, применяемый к операциям считывания. Совмещаемые блокировки,
       применяемые для READ COMMITTED или REPEATABLE READ, как правило, являются блокировками строк, но при этом,
       если в процессе считывания идет обращение к большому числу строк, блокировка строк может быть расширена до блокировки страниц или таблиц.
       Если строка была изменена транзакцией после считывания, для защиты такой строки транзакция применяет монопольную блокировку,
       которая сохраняется до завершения транзакции.
       Например, если транзакция REPEATABLE READ имеет разделяемую блокировку строки и при этом изменяет ее, совмещаемая блокировка преобразуется в монопольную.

       В любой момент транзакции можно переключиться с одного уровня изоляции на другой, однако есть одно исключение.
       Это смена уровня изоляции на уровень изоляции SNAPSHOT. Такая смена приводит к ошибке и откату транзакции.
       Однако для транзакции, которая была начата с уровнем изоляции SNAPSHOT, можно установить любой другой уровень изоляции.

       Когда для транзакции изменяется уровень изоляции, ресурсы, которые считываются после изменения, защищаются в соответствии с правилами нового уровня.
       Ресурсы, которые считываются до изменения, остаются защищенными в соответствии с правилами предыдущего уровня.
       Например, если для транзакции уровень изоляции изменяется с READ COMMITTED на SERIALIZABLE,
       то совмещаемые блокировки, полученные после изменения, будут удерживаться до завершения транзакции.

       Если инструкция SET TRANSACTION ISOLATION LEVEL использовалась в хранимой процедуре или триггере,
       то при возврате управления из них уровень изоляции будет изменен на тот, который действовал на момент их вызова.
       Например, если уровень изоляции REPEATABLE READ устанавливается в пакете, а пакет затем вызывает хранимую процедуру,
       которая меняет уровень изоляции на SERIALIZABLE, при возвращении хранимой процедурой управления пакету,
       настройки уровня изоляции меняются назад на REPEATABLE READ

       The default transaction isolation level in SQL Server is READ COMMITTED.
       Unless the database is configured to support SNAPSHOT isolation by default,
       a write operation within a transaction under READ COMMITTED isolation will place transaction-scoped locks on the rows that were updated.
       Under conditions of high concurrency, DEADLOCKS CAN OCCUR if multiple processes generate conflicting locks.
       If those processes use long-lived transactions that generate a large number of such locks then the chances of a deadlock are greater.

       Setting autocommit=True will avoid the deadlocks because each individual SQL statement will be automatically committed,
       thus ending the transaction (which was automatically started when that statement began executing) and releasing any locks on the updated rows
    """
    SQLQuery = "SET TRANSACTION ISOLATION LEVEL "
    SQLQuery += str(Level)
    seek.execute(SQLQuery)


# Источник BTSgov
# Убать из файла все косые, запятые и кавычки
print("БД ", __DataBase__)
print("Имя входного файла типа *.csv = ", end=" ")
__InputFileCSV__ = str(input())

print(" Делать диагностический вывод для отладки? (работает медленнее) [y/n] ", end=" ")
if str(input()) == 'y':
    __DebugOutPut__ = True
else:
    __DebugOutPut__ = False
print("  Чтение и перепаковка входного файла")
print("  Ожидайте ...")

# Читаем входной файл и перепаковываем его в DataFrame (кодировка UTF-8, шапка таблицы на столбцы, разделитель - ,)
DataFrameFromCSV = pandas.read_csv(__InputFileCSV__ + ".csv", sep=",")
# В исходном файле *.csv подписаны столбцы -> в DataFrame можно перемещаться по именам столбцов -> Разбираем на столбцы и работаем с ними
ListAirLineCodeIATA = DataFrameFromCSV['OP_UNIQUE_CARRIER'].tolist()
ListAirCraft = DataFrameFromCSV['TAIL_NUM'].tolist()
ListFlightNumber = DataFrameFromCSV['OP_CARRIER_FL_NUM'].tolist()
ListAirPortDeparture = DataFrameFromCSV['ORIGIN'].tolist()
ListAirPortArrival = DataFrameFromCSV['DEST'].tolist()
print(" готово")

# Помечаем файл как в работе
try:
    os.rename(__InputFileCSV__ + ".csv", __InputFileCSV__ + "_" + __DataBase__ + ".csv")
#    __InputFileCSV__ += "_"
except:
    print(" -- имя входного файла", __InputFileCSV__, " не пометилось..... ")

# Счетчики
CountRoutesAdded = 0
CountRoutesFailed = 0
CountFlightsAdded = 0
CountFlightsPadded = 0
CountFlightsFailed = 0

# Немножко машинного обучения по задержкам
print("Предел ожидания сервера (Рекомендуется 225), секунд = ", end=" ")
MaxDelay = int(input())  # Предел ожидания, секунд
if MaxDelay <= 35:
    MaxDelay = 35
elif MaxDelay > 250:
    MaxDelay = 250
# Распределение плотности задержки на самолеты, маршрутам, авиарейсам
DistributionDensityAirCrafts = []
DistributionDensityAirRoutes = []
DistributionDensityAirFlights = []
Index = 0
while Index <= MaxDelay:  # MaxDelay + 1 ячеек
    DistributionDensityAirCrafts.append(0)
    DistributionDensityAirRoutes.append(0)
    DistributionDensityAirFlights.append(0)
    Index += 1

# Списки самолетов
ListAirCraftsAdded = []
ListAirCraftsUpdated = []
ListAirCraftsFailed = []

# Список ненайденных аэропортов
ListAirPortsNotFounded = []

# Дата и время сейчас
Now = time.time()
DateTime = time.ctime(Now)

OutputString = "\n\nЗагрузка рабочих данных (версия обработки - " + str(__Version__) + ") \n"
OutputString += " Источник входных данных - " + str(__InputFileCSV__) + " \n"
OutputString += " Загрузка начата " + str(DateTime) + " \n"

# Пишем в журнал
try:
    OutPutFile = open(__OutputFileTXT__ + ".txt", 'a')
    OutPutFile.write(OutputString)
except IOError:
    print(" -- ошибка дозаписи в " + str(__OutputFileTXT__) + "..... ")
finally:
    OutPutFile.close()

# Отметка времени начала загрузки
__StartTime__ = datetime.datetime.now()

# Один внешний цикл и три вложенных цикла
# Между вложенными циклами результаты запросов не переходят, перезапрашиваем снова
for AC, AL, FN, Dep, Arr in zip(ListAirCraft, ListAirLineCodeIATA, ListFlightNumber, ListAirPortDeparture, ListAirPortArrival):
    # Входная проверка - Если есть регистрация самолета, в том числе UNKNOWN и nan
    if AC and AL:
        if __DebugOutPut__:
            print("\n\n")
        print("Самолет", str(AC), end=" ")
        CurrentMax_i = 0  # Текущий максимум, секунд -> Обнуляем
        SetTransactionIsolationLevel("SERIALIZABLE")
        # Цикл попыток
        for i in range(2, MaxDelay):
            if CurrentMax_i < i:
                CurrentMax_i = i
            # Начинаем транзакцию и блокируем запрашиваемые диапазоны
            DBAirCraft = QueryAirCraft(AC)
            DBAirLine = QueryAirLine(AL)
            if DBAirCraft:
                DBAirLine2 = QueryAirLine2(DBAirCraft.AirCraftAirLine)
                # Если самолет есть в БД, и если нет авиакомпании или неизвестная авиакомпания
                if not DBAirCraft.AirCraftAirLine or DBAirLine2.AirLineCodeIATA == ('nan' or 'Unknown'):
                    # Вставляем (только один раз) авиакомпанию-оператора самолета
                    SQLUpdateAirCraft = "UPDATE dbo.AirCraftsTable SET AirCraftAirLine = " + str(DBAirLine.AirLineUniqueNumber) + " WHERE AirCraftRegistration = '" + str(AC) + "' "
                    try:
                        seek.execute(SQLUpdateAirCraft)  # записываем данные по самолету в БД
                    except:
                        print("*", end=" ")
                    else:
                        ListAirCraftsUpdated.append(AC)
                        print("вставилась авиакомпания-оператор", end=" ")
                        break
                    finally:
                        pass  # выполняется всегда
                else:
                    break
            # Если самолета нет в БД
            else:
                SQLInsertAirCraft = "INSERT INTO dbo.AirCraftsTable (AirCraftRegistration, AirCraftAirLine, SourceCSVFile) VALUES ("
                SQLInsertAirCraft += "'" + str(AC) + "', "  # nvarchar(50)
                SQLInsertAirCraft += str(DBAirLine.AirLineUniqueNumber) + ", "  # bigint
                SQLInsertAirCraft += "'" + str(__InputFileCSV__) + "') "  # ntext
                try:
                    seek.execute(SQLInsertAirCraft)  # записываем данные по самолету в БД
                except:
                    # без самолета авиарейс с неизвестным самолетом
                    print("+", end=" ")
                else:
                    ListAirCraftsAdded.append(AC)
                    print("добавился", end=" ")
                    break
                finally:
                    pass  # выполняется всегда
            cnxn.commit()  # снимаем блокировку с запрошенных диапазонов
            time.sleep(i)  # уходим от взаимоблокировки
        else:
            ListAirCraftsFailed.append(AC)
        cnxn.commit()  # фиксируем транзакцию
        print(" ")
        DistributionDensityAirCrafts[CurrentMax_i] += 1
    # Входная проверка - Если есть оба аэропорта и они разные
    if Dep and Arr and Dep != Arr:
        print(" Маршрут", str(Dep), "-", str(Arr), end=" ")
        CurrentMax_i = 0  # Текущий максимум, секунд -> Обнуляем
        SetTransactionIsolationLevel("REPEATABLE READ")
        # Цикл попыток
        for i in range(2, MaxDelay):
            if CurrentMax_i < i:
                CurrentMax_i = i
            # Начинаем транзакцию и блокируем запрашиваемые диапазоны
            DBAirPortDep = QueryAirPort(Dep)
            DBAirPortArr = QueryAirPort(Arr)
            DBAirRoute = QueryAirRoute(Dep, Arr)
            # Для вставки аэропортов нужны полностью проверенные вручную данные, поэтому здесь аэропорты только проверяются
            # Если есть оба аэропорта и нет маршрута
            if DBAirPortDep and DBAirPortArr and not DBAirRoute:
                SQLInsertRoute = "INSERT INTO dbo.AirRoutesTable (AirPortDeparture, AirPortArrival, SourceCSVFile) VALUES ("
                SQLInsertRoute += str(DBAirPortDep.AirPortUniqueNumber) + ", "  # bigint
                SQLInsertRoute += str(DBAirPortArr.AirPortUniqueNumber) + ", "  # bigint
                SQLInsertRoute += "'" + str(__InputFileCSV__) + "') "  # ntext
                try:
                    seek.execute(SQLInsertRoute)  # записываем маршрут в БД
                except:
                    print("+", end=" ")
                else:
                    CountRoutesAdded += 1
                    print("добавился", end=" ")
                    break
                finally:
                    pass  # выполняется всегда
            elif not DBAirPortDep:
                ListAirPortsNotFounded.append(Dep)
                break
            elif not DBAirPortArr:
                ListAirPortsNotFounded.append(Arr)
                break
            else:
                break
            cnxn.commit()  # снимаем блокировку с запрошенных диапазонов
            time.sleep(i)  # уходим от взаимоблокировки
        else:
            CountRoutesFailed += 1
        cnxn.commit()  # фиксируем транзакцию
        print(" ")
        DistributionDensityAirRoutes[CurrentMax_i] += 1
    # Входная проверка - Если есть регистрация самолета, код IATA авиакомпании и номер авиарейса
    if AC and AL and FN:
        print(" Авиарейс", str(AL) + str(FN), end=" ")
        CurrentMax_i = 0  # Текущий максимум, секунд -> Обнуляем
        SetTransactionIsolationLevel("SERIALIZABLE")
        # Цикл попыток
        for i in range(2, MaxDelay):
            if CurrentMax_i < i:
                CurrentMax_i = i
            # Начинаем транзакцию и блокируем запрашиваемые диапазоны
            DBAirLine = QueryAirLine(AL)
            DBAirRoute = QueryAirRoute(Dep, Arr)
            # Если есть:
            # - маршрут (должен быть),
            # - авиакомпания,
            # - не пустой номер авиарейса в файле,
            # - регистрация самолета
            if DBAirLine and DBAirRoute:
                DBAirCraft = QueryAirCraft(AC)
                SQLExpression = "(FlightNumberString = '" + str(AL) + str(FN) + "') AND ((AirRoute = " + str(DBAirRoute.AirRouteUniqueNumber) + ") AND (AirCraft = " + str(DBAirCraft.AirCraftUniqueNumber) + "))"
                SQLQueryFlight = "SELECT * FROM dbo.AirFlightsTable WHERE " + str(SQLExpression) + " ORDER BY  AirRoute, AirCraft, FlightNumberString"
                seek.execute(SQLQueryFlight)  # много транзакций, подвисает, проигрыш при взаимоблокировке, сервер отбрасывает подключение -> скрипт слетает
                DBAirFlight = seek.fetchone()
                # Авиарейс с таким маршрутом есть
                if DBAirFlight:
                    # Плюсуем авиарейс
                    if DBAirFlight.QuantityCounted:
                        Quantity = DBAirFlight.QuantityCounted
                    else:
                        Quantity = 0  # NULL (пустая ячейка таблицы) в SQL => None в Python-е -> выражение с None не работает, функция не может вернуть None -> ошибка, скрипт слетает
                    Quantity += 1  # отдельно плюсуем на 1 для наглядности
                    SQLUpdateFlight = "UPDATE dbo.AirFlightsTable SET QuantityCounted = " + str(Quantity) + " WHERE " + str(SQLExpression) + " "
                    try:
                        seek.execute(SQLUpdateFlight)  # записываем сплюсованный авиарейс в БД
                    except:
                        print("*", end=" ")
                    else:
                        CountFlightsPadded += 1
                        print("сплюсовался", end=" ")
                        break
                    finally:
                        pass  # выполняется всегда
                else:
                    # Добавляем авиарейс
                    SQLInsertFlight = "INSERT INTO dbo.AirFlightsTable (AirRoute, AirCraft, FlightNumberString, QuantityCounted, SourceCSVFile) VALUES ("
                    SQLInsertFlight += str(DBAirRoute.AirRouteUniqueNumber) + ", "  # bigint
                    SQLInsertFlight += str(DBAirCraft.AirCraftUniqueNumber) + ", "  # bigint
                    SQLInsertFlight += "'" + str(AL) + str(FN) + "', "  # nvarchar(50)
                    SQLInsertFlight += str(1) + ", "  # bigint
                    SQLInsertFlight += "'" + str(__InputFileCSV__) + "') "  # ntext
                    try:
                        seek.execute(SQLInsertFlight)  # записываем добавленный авиарейс в БД
                    except:
                        print("+", end=" ")
                    else:
                        CountFlightsAdded += 1
                        print("добавился", end=" ")
                        break
                    finally:
                        pass  # выполняется всегда
            else:
                break
            cnxn.commit()  # снимаем блокировку с запрошенных диапазонов
            time.sleep(i)  # уходим от взаимоблокировки
        else:
            CountFlightsFailed += 1
        cnxn.commit()  # фиксируем транзакцию
        print(" ")
        DistributionDensityAirFlights[CurrentMax_i] += 1

# Снимаем курсор
seek.close()

# Фиксируем зависшие и безхозные транзакции
cnxn.commit()
# Закрываем соединение
cnxn.close()

# Собираем три списка в DataFrame
DataFrameDistributionDensity = pandas.DataFrame([DistributionDensityAirCrafts,
                                                 DistributionDensityAirRoutes,
                                                 DistributionDensityAirFlights],
                                                index=["AirCrafts", "AirRoutes", "AirFlights"])
DataFrameDistributionDensity.index.name = "Categories"

# Формируем итоги
OutputString = " Итоги:\n ---- \n"

# Отметка времени окончания загрузки
__EndTime__ = datetime.datetime.now()

if ListAirCraftsAdded:
    OutputString += " Добавлены самолеты:\n"
    OutputString += str(set(ListAirCraftsAdded))
    OutputString += " \n"
if ListAirCraftsUpdated:
    OutputString += "  Добавлены данные по самолетам:\n"
    OutputString += str(set(ListAirCraftsUpdated))
    # Убираем только повторы, идущие подряд, но с сохранением исходного порядка
    OutPutNew = [el for el, _ in itertools.groupby(ListAirCraftsUpdated)]
    OutputString += " \n"
if ListAirCraftsFailed:
    OutputString += "  не добавлены данные по самолетам:\n"
    OutputString += str(set(ListAirCraftsFailed))
    OutputString += " \n"
if CountRoutesAdded:
    OutputString += " Добавлено " + str(CountRoutesAdded) + " маршрутов \n"
if CountRoutesFailed:
    OutputString += " Не добавлено " + str(CountRoutesFailed) + " маршрутов\n"
    OutputString += " \n"
if ListAirPortsNotFounded:
    OutputString += " Не найдены аэропорты:\n"
    OutputString += str(set(ListAirPortsNotFounded))
    OutputString += " \n"
if CountFlightsAdded:
    OutputString += " Добавлено " + str(CountFlightsAdded) + " авиарейсов \n"
if CountFlightsFailed:
    OutputString += " Не добавлено " + str(CountFlightsFailed) + " авиарейсов (нет маршрута, авиакомпании или пустой номер авиарейса) \n"
if CountFlightsPadded:
    OutputString += " Сплюсовано " + str(CountFlightsPadded) + " авиарейсов \n"
OutputString += " ---- \n"
OutputString += "   Длительность загрузки - " + str(__EndTime__ - __StartTime__) + " \n"
OutputString += " Распределения плотности задержки сервера, секунд: \n" + str(DistributionDensityAirCrafts) + "\n" + str(DistributionDensityAirRoutes) + "\n" + str(DistributionDensityAirFlights) + "\n"
print(OutputString)

# Дописываем итоги в журнал
try:
    OutPutFile = open(__OutputFileTXT__ + ".txt", 'a')
    OutPutFile.write(OutputString)
except IOError:
    print(" -- ошибка дозаписи в " + str(__OutputFileTXT__) + "..... ")
finally:
    OutPutFile.close()

"""
Помечаем файл, как отработанный (добавляем плюс в имени файла)
try:
    os.rename(__InputFileCSV__ + ".csv", __InputFileCSV__ + "_+" + ".csv")
except:
    print(" -- имя входного файла", __InputFileCSV__, " не пометилось..... ")

"""
