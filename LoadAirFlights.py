# Interpreter 3.6 -> 3.7 (работает так же)
# Interpreter 3.8 (пока не проверяли)
# Interpreter 3.9 (требуется Windows 10 или Windows Server 2012)

"""
Проверяем и добавляем в БД:
  - самолеты,
  - маршруты,
  - авиарейсы
  из файлы-справочника типа *.csv
  У каждого самолета один код регистрацииД
  Допускается, что сторонними обработками могли быть внесены самолеты других моделей с тем же кодом регистрации
  У маршрута может быть несколько разноименных авиарейсов
  У авиарейса может быть несколько маршрутов
"""


#import pymssql - работает тяжелее
import pyodbc
import pandas
import itertools
import datetime
import time
import os
import json


__myOwnDevelopVersion__ = 4.87  # Версия обработки

# Библиотеки Python для ввода-вывода в файл:
# - Pandas (анализ данных, лучше чем NumPy),
# - math (математические функции),
# - SciPy (математика),
# - SymPy,
# - MatPlotLib (графики на плоскости),
# - Pickle (пишут, что ненадежен -> лучше json),
# - dbm,
# - shelve (чтение и запись в файл),
# - sys (система),
# - os (операционная система),
# - time, datetime (дата и время)

# Обмен данными между программами до SQL-ных баз данных:
# - двоичный файл типа *.dat,
# - текстовый файл типа *.txt,
# - файл с разделителями и переводом строки типа *.csv,
# - файл с тэгами и иерархией типа *.xml (xml.dom, xml.sax) или *.html,
#    XQuery - вложение в SQL для подддержки запросов XML
#    XQuery XPath (выведен из SQL и OQL) и XSLT (выведен из SGML с его языком таблиц стилей DSSSL) берут на вход файл XML,
#        обрабатывают его по формуле и выводят файл XML, XHTML, HTML
#        XPath выбирает узлы из исходного дерева,
#        XSLT создает узлы дерева результата
#    XSLT для документно-ориентированного XML
#    XQuery для информационно-ориентированного XML
#    XSLT может переводить XML в формат представления HTML или PDF
#    Инструкции XSLT вызывают выражения XPath
#    Схемы:
#     - схема XDR с заметками (устаревшая в SQLXML 4.0)
#     - схема XSD (полнее, чем XDR) с заметками,  файл типа *.xsd
#     - типы данных XPath,
#     - типы данных XDR,
#     - типы данных XSD
# - файл кодера-декодера исходный текст типа *.json,
# - файл типа *.yaml
# - файл MsgPack, Protocol Buffers, Avro, Thrift
# - с помощью модуля pickle,
# - научный формат HDF5,
# - БД с помощью DB-API (функционал - connect, cursor, execute, fetch) нет своего функционала для прямой работы с таблицами SQL Server-а
# (для выборки вызываем скрипт на SQL или хранимую процедуру с параметрами на входе),
# - файл формта dbm (словарь),
# - python-memcached,
# - сервер структурных данных Redis.

# Главная трудоемкость математики - это скалярное <-> векторное преобразование - решена в Python и в R, но не в SQL-ных БД (кроме старой Informix).
# В языке R все величины векторые, в том числе одноразмерные

# Перед передачей данных из Python-а на вход хранимой процедуры надо преобразовать их в типы данных SQL.
# Возможности типов данных Python-а намного богаче типов полей таблиц SQL-ных БД.
# Поэтому происходит потеря данных и их разнообразия.
# Можно сделать сложный иерархический наращиваемый пользовательский тип данных,
# который намного превышает возможности таблиц SQL-ных БД.
# Как вариант можно сохранить его файлом, но у файла нет способа множественного доступа на межпрограммном уровне с транзакциями и по нескольким учеткам,
# кроме старой ORACLE Solaris локально, которая сейчас уже не в ходу

# Поэтому центром вычислительной активности в прикладных проектах является Microsoft SQL Server
# Он содержит в составе своей аппаратуры наилучшее оснащение
# К нему по мере необходимости подключаются клиенты из-под разных учетных записей в виде например скриптов

# Нет практической пользы писать одну многопоточную программу на C++ которая содержит в себе весь необходимый функционал
# делая все и которая ведет свои какие-то записи в свой файл данных типа *.dat, который понимает только она
# И которая живет сама по себе вне зависимости от инфраструктуры, заменяя собой инфраструктуру
# Сейчас есть столбцовые БД где-то там на облаках типа Vertica, SandBridge, Amazon RedShift и другие
# Есть Oracle локально или на облаке :) С бесплатным начальным периодом :) Никто ничего на них не гарантирует :)
# А Microsoft SQL Server всегда по рукой и все серьезные SoftWare-ные компании выдают ПО, которое успешно работает с ним в том числе :)


# fixme Сделать формочку для поиска и исправления дубликатов в таблицах (внутри SSMS) - СДЕЛАл через SSMS
# todo Попробовать dplyr и tidyr для Python-а
# todo Каждое действие с БД внутри обработки исключения, кроме изменения уровня изоляции транзакции - СДЕЛАЛ
# todo Делать транзакции поменьше и почаще, в конце commit или rollback - СДЕЛАЛ
# todo Указать уровень изоляции транзакции точнее (обновление - REPEATABLE READ, вставка - SERIALIZABLE, выборка и все остальное - READ COMMITTED)
# todo Подключать и отключать библиотеки по мере надобности (статические -> динамические библиотеки)
# todo Чем быстрее отвечает СУБД, тем больше обращений она отбрасывает, тем больше вероятность наскочить на взаимоблокировку


def QueryAirCraft(Registration):
    """Возвращает данные самолета по его коду регистрации
    Считаем, что у одного самолета любой модели, в том числе неизвестной один код регистрации
    Но дубликаты могут быть, так как при переходе самолета от одной компании-владельца к другой код регистрации как правило меняется
    и однозначно определить самолет можно по сочетанию его MSN (SN) и коду регистрации
    Код регистрации через несколько лет может передаваться от утилизированного самолета к новому без привязки к изготовителю и модели
    Выводим первую найденную строку
    """
    SQLQuery = "SELECT * FROM dbo.AirCraftsTable WHERE AirCraftRegistration = '" + str(Registration) + "' ORDER BY AirCraftAirLine, AirCraftRegistration"
    if __DebugOutPut__:
        seekSubs.execute(SQLQuery)  # где-то в памяти висит результат выборки по запросу
        print("\n  самолет ", str(seekSubs.fetchall()))
    seekSubs.execute(SQLQuery)
    ResultSQL = seekSubs.fetchone()  # курсор забирает одну строку и сдвигается на строку вниз
    # в SQL пустая ячейка в таблице -  NULL -> в Python-е - (None,) -> условия с None не работает, функция не возвращает None -> ошибка, скрипт слетает
    if ResultSQL:
        return ResultSQL
    else:
        return False


def QueryAirLine(IATA):
    """Возвращает данные авиакомпании по ее коду IATA
    Считаем, что одному коду соответствует одна авиакомпания
    Дубликаты есть (221 шт.)
    Выводим первую найденную строку
    """
    SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineCodeIATA = '" + str(IATA) + "' ORDER BY AirLineName"
    if __DebugOutPut__:
        seekSubs.execute(SQLQuery)
        print("\n  авиакомпания ", str(seekSubs.fetchall()))
    seekSubs.execute(SQLQuery)
    ResultSQL = seekSubs.fetchone()
    if ResultSQL:
        return ResultSQL
    else:
        return False


def QueryAirLine2(UN):
    """Возвращает данные авиакомпании по ее первичному ключу
    Дубликатов быть не может
    """
    SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineUniqueNumber = '" + str(UN) + "' "
    seekSubs.execute(SQLQuery)
    ResultSQL = seekSubs.fetchone()
    if ResultSQL:
        return ResultSQL
    else:
        return False


def QueryAirPort(IATA):
    """Возвращает данные аэропортов отправления и прибытия по их кодам IATA
    Считаем, что каждому коду соответствует один аэропорт
    Дубликаты есть (2 шт.)
    Выводим первую найденную строку
    """
    SQLQuery = "SELECT * FROM dbo.AirPortsTable WHERE AirPortCodeIATA = '" + str(IATA) + "' ORDER BY AirPortCountry, AirPortCity, AirPortCodeIATA"
    if __DebugOutPut__:
        seekSubs.execute(SQLQuery)
        print("\n  аэропорт ", str(seekSubs.fetchall()))
    seekSubs.execute(SQLQuery)
    ResultSQL = seekSubs.fetchone()
    if ResultSQL:
        return ResultSQL
    else:
        return False


def QueryAirRoute(IATADeparture, IATAArrival):
    """Возвращает данные маршрута по кодам IATA аэропортов
    Считаем, что от одного до другого аэропорта может быть только один маршрут
    Если несколько, выводим первый найденный маршрут"""
    SQLQuery = """SELECT dbo.AirRoutesTable.AirRouteUniqueNumber                                 
               FROM dbo.AirRoutesTable INNER JOIN
               dbo.AirPortsTable ON dbo.AirRoutesTable.AirPortDeparture = dbo.AirPortsTable.AirPortUniqueNumber INNER JOIN
               dbo.AirPortsTable AS AirPortsTable_1 ON dbo.AirRoutesTable.AirPortArrival = AirPortsTable_1.AirPortUniqueNumber
               WHERE (dbo.AirPortsTable.AirPortCodeIATA = '""" + str(IATADeparture) + "') AND (AirPortsTable_1.AirPortCodeIATA = '" + str(IATAArrival) + "') "
    if __DebugOutPut__:
        seekSubs.execute(SQLQuery)
        print("\n  маршрут ", str(seekSubs.fetchall()))
    seekSubs.execute(SQLQuery)
    ResultSQL = seekSubs.fetchone()
    if ResultSQL:
        return ResultSQL
    else:
        return False


def QueryTransactionIsolationLevel():
    """ Возвращает уровень изоляции транзакций для данного подключения
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
    seekSubs.execute(SQLQuery)
    ResultSQL = seekSubs.fetchone()
    if ResultSQL:
        return ResultSQL.TIL
    else:
        return False


def SetTransactionIsolationLevel(Level):
     # Устанавливает уровень изоляции транзакций
     #    Берет на вход его название на SQL в виде строки
     #    READ COMMITTED (Чтение зафиксированных данных) - (по умолчанию) инструкции не могут считывать данные, которые были изменены и еще не зафиксированы другими транзакциями
     #                    Другие транзакции могут изменять и вставлять данные, читаемые текущей транзакцией
     #    REPEATABLE READ (Повторяемость чтения) - еще плюс Другие транзакции могут только вставлять данные, читаемые текущей транзакцией
     #    SERIALIZABLE (Упорядочиваемость) - еще плюс Другие транзакции не могут изменять и вставлять данные в диапазон, читаемые текущей транзакцией
     #
     #   Одновременно может быть установлен только один параметр уровня изоляции, который продолжает действовать для текущего соединения до тех пор,
     #   пока не будет явно изменен. Все операции считывания, выполняемые в рамках транзакции, функционируют в соответствии с правилами уровня изоляции,
     #   если только табличное указание в предложении FROM инструкции не задает другое поведение блокировки или управления версиями строк для таблицы.
     #
     #   Уровни изоляции транзакции определяют тип блокировки, применяемый к операциям считывания. Совмещаемые блокировки,
     #   применяемые для READ COMMITTED или REPEATABLE READ, как правило, являются блокировками строк, но при этом,
     #   если в процессе считывания идет обращение к большому числу строк, блокировка строк может быть расширена до блокировки страниц или таблиц.
     #   Если строка была изменена транзакцией после считывания, для защиты такой строки транзакция применяет монопольную блокировку,
     #   которая сохраняется до завершения транзакции.
     #   Например, если транзакция REPEATABLE READ имеет разделяемую блокировку строки и при этом изменяет ее, совмещаемая блокировка преобразуется в монопольную.
     #
     #   В любой момент транзакции можно переключиться с одного уровня изоляции на другой, однако есть одно исключение.
     #   Это смена уровня изоляции на уровень изоляции SNAPSHOT. Такая смена приводит к ошибке и откату транзакции.
     #   Однако для транзакции, которая была начата с уровнем изоляции SNAPSHOT, можно установить любой другой уровень изоляции.
     #
     #   Когда для транзакции изменяется уровень изоляции, ресурсы, которые считываются после изменения, защищаются в соответствии с правилами нового уровня.
     #   Ресурсы, которые считываются до изменения, остаются защищенными в соответствии с правилами предыдущего уровня.
     #   Например, если для транзакции уровень изоляции изменяется с READ COMMITTED на SERIALIZABLE,
     #   то совмещаемые блокировки, полученные после изменения, будут удерживаться до завершения транзакции.
     #
     #   Если инструкция SET TRANSACTION ISOLATION LEVEL использовалась в хранимой процедуре или триггере,
     #   то при возврате управления из них уровень изоляции будет изменен на тот, который действовал на момент их вызова.
     #   Например, если уровень изоляции REPEATABLE READ устанавливается в пакете, а пакет затем вызывает хранимую процедуру,
     #   которая меняет уровень изоляции на SERIALIZABLE, при возвращении хранимой процедурой управления пакету,
     #   настройки уровня изоляции меняются назад на REPEATABLE READ
     #
     #   The default transaction isolation level in SQL Server is READ COMMITTED.
     #   Unless the database is configured to support SNAPSHOT isolation by default,
     #   a write operation within a transaction under READ COMMITTED isolation will place transaction-scoped locks on the rows that were updated.
     #   Under conditions of high concurrency, DEADLOCKS CAN OCCUR if multiple processes generate conflicting locks.
     #   If those processes use long-lived transactions that generate a large number of such locks then the chances of a deadlock are greater.
     #
     #   Setting autocommit=True will avoid the deadlocks because each individual SQL statement will be automatically committed,
     #   thus ending the transaction (which was automatically started when that statement began executing) and releasing any locks on the updated rows
    SQLQuery = "SET TRANSACTION ISOLATION LEVEL "
    SQLQuery += str(Level)
    seekSubs.execute(SQLQuery)


print("Обработка v", str(__myOwnDevelopVersion__), "загрузки рабочих данных в БД SQL Server-а")
print("Разработал Тарасов Сергей tsv19su@yandex.ru")
print("Пользователь = ", str(os.getlogin()))

# Драйверы СУБД
print(" ")
__DriversODBC__ = pyodbc.drivers()
if __DriversODBC__:
    print("Драйверы СУБД:")
    for DriverODBC in __DriversODBC__:
        if not DriverODBC:
            break
        print(DriverODBC)
else:
    print("Драйверов СУБД нет")

# Базы данных
__DataBase__ = " "
__myDSN__ = " "
__OutputFileTXT__ = " "
print(" ")
# todo * Сделать формочку с переключателями баз данных и кнопкой "Записать и закрыть" (редактор графических форм - tkinter, gtk, pyGTK, pyQT) - СДЕЛАЛ

print("Базы данных (в квадратных скобках варианты выбора):")
print(" - AirFlightsDBNew42 [42],")
print(" - AirFlightsDBNew42Test [4],")
print(" - AirFlightsDBNew52 [52],")
print(" - AirFlightsDBNew52Test [5]")
#print("  Выберите базу данных = ", end=" ")
# Введенный вариант преобразуем в текстовую строку
# todo Добавить права на изменение для учетки, из-под которой запускается скрипт
__ChoiceDB__ = str(input("  Выберите базу данных = "))
if __ChoiceDB__ == "42":
    __DataBase__ = "AirFlightsDBNew42"
    __myDSN__ = "AirFlightsDBNew4_DSN"
    __OutputFileTXT__ = "LogReport_DBNew4"
elif __ChoiceDB__ == "4":
    __DataBase__ = "AirFlightsDBNew42Test"
    __myDSN__ = "AirFlightsDBNew4Test_DSN"
    __OutputFileTXT__ = "LogReport_DBNew4Test"
elif __ChoiceDB__ == "52":
    __DataBase__ = "AirFlightsDBNew52"
    __myDSN__ = "AirFlightsDBNew5_DSN"
    __OutputFileTXT__ = "LogReport_DBNew5"
elif __ChoiceDB__ == "5":
    __DataBase__ = "AirFlightsDBNew52Test"
    __myDSN__ = "AirFlightsDBNew5Test_DSN"
    __OutputFileTXT__ = "LogReport_DBNew5Test"
else:
    print("БД не выбрана. Выход из обработки.")
    exit(0)

# Cистемные или пользовательские DSN-ы
# fixme Сделать, чтобы выводились и драйверы СУБД тоже, как словарь - СДЕЛАЛ
print(" ")
__DSNs__ = pyodbc.dataSources()  # добавленные DSN-ы
if __DSNs__:
    print("Доступные DSN-ы:")
    for DSN in __DSNs__.items():
        if not DSN:
            break
        print(DSN)
    __jsonDSNs__ = json.dumps(__DSNs__)
    # print(__jsonDSNs__)
else:
    print("Доступных DSN-ов нет")

# todo Схема по умолчанию - dbo, другая схема указывается в явном виде
# Открываем соединение с БД
if __DSNs__:
    # через DSN + клиентский API-курсор (все настроено и протестировано в DSN)
    #print("  Можете уточнить DSN (см. список, пусто - оставить выбранный) = ", end=" ")
    CmyDSN = str(input("  Можете уточнить DSN (см. список, пусто - оставить выбранный) = "))
    if CmyDSN:
        __OutputFileTXT__ = "LogReport_DBNewCommon"
        __myDSN__ = CmyDSN
    cnxn = pyodbc.connect("DSN=" + __myDSN__)  # если DSN введен неправильно, то в этом месте сервер возвращает ошибку и обработка слетает
else:
    # через драйвер СУБД + клиентский API-курсор
    Driver = "SQL Server"
    Server = "Data-Server"
    cnxn = pyodbc.connect(driver=Driver, server=Server, database=__DataBase__)

# Разрешаем транзакции и вызываем функцию commit() при необходимости в явном виде, в СУБД по умолчанию FALSE
cnxn.autocommit = False

# КУРСОР нужен для перехода функционального языка формул на процедурный или для вставки процедурных кусков в функциональный скрипт.
#
# Способы реализации курсоров:
#  - SQL, Transact-SQL,
#  - серверные API-курсоры (OLE DB, ADO, ODBC),
#  - клиентские (выборка кэшируется на клиенте)
#
# API-курсоры ODBC по SQLSetStmtAttr:
#  - тип SQL_ATTR_CURSOR_TYPE:
#    - однопроходный (последовательный доступ),
#    - статический (копия в tempdb),
#    - управляемый набор ключей,
#    - динамический,
#    - смешанный
#  - режим работы в стиле ISO:
#    - прокручиваемый SQL_ATTR_CURSOR_SCROLLABLE,
#    - обновляемый (чувствительный) SQL_ATTR_CURSOR_SENSITIVITY
# Клиентские однопроходные , статические API-курсоры ODBC.
seekSubs = cnxn.cursor()
seekAC = cnxn.cursor()
seekRT = cnxn.cursor()
seekFN = cnxn.cursor()

SetTransactionIsolationLevel("READ COMMITTED")
# SQL Server
print(" ")
print("Сервер СУБД = ", cnxn.getinfo(pyodbc.SQL_SERVER_NAME))
# Драйвер
print("Драйвер = ", cnxn.getinfo(pyodbc.SQL_DRIVER_NAME))
# версия ODBC
print("Версия ODBC = ", cnxn.getinfo(pyodbc.SQL_ODBC_VER))
# Источник данных
print("DSN = ", cnxn.getinfo(pyodbc.SQL_DATA_SOURCE_NAME))
# Схема
print("Схема = ", cnxn.getinfo(pyodbc.SQL_USER_NAME))

__DebugOutPut__ = False
#print("  Делать диагностический вывод для отладки? (работает медленнее) [y/n] = ", end=" ")
if str(input("  Делать диагностический вывод для отладки? (работает медленнее) [y/n] = ")) == 'y':
    __DebugOutPut__ = True
else:
    __DebugOutPut__ = False


# Источник BTSgov
# Убать из файла все косые, запятые и кавычки
#print("  Имя входного файла типа *.csv = ", end=" ")
__InputFileCSV__ = str(input("  Имя входного файла типа *.csv = "))
print("  чтение и перепаковка входного файла")
print("  ожидайте ...")

# Читаем входной файл и перепаковываем его в DataFrame (кодировка UTF-8, шапка таблицы на столбцы, разделитель - ,)
DataFrameFromCSV = pandas.read_csv(__InputFileCSV__ + ".csv", sep=",")
# todo Пересчитать в промежуточный DataFrame (взять в исходном DataFrameFromCSV все строки с оовпадающими
# В исходном файле *.csv подписаны столбцы -> в DataFrame можно перемещаться по именам столбцов -> Разбираем на столбцы и работаем с ними
ListAirLineCodeIATA = DataFrameFromCSV['OP_UNIQUE_CARRIER'].tolist()
ListAirCraft = DataFrameFromCSV['TAIL_NUM'].tolist()
ListFlightNumber = DataFrameFromCSV['OP_CARRIER_FL_NUM'].tolist()
ListAirPortDeparture = DataFrameFromCSV['ORIGIN'].tolist()
ListAirPortArrival = DataFrameFromCSV['DEST'].tolist()
print(" готово")

# Помечаем файл как в работе
try:
    if __DSNs__:
        # Дописываем в имя файла DSN
        os.rename(__InputFileCSV__ + ".csv", __InputFileCSV__ + "_" + __myDSN__ + ".csv")
    else:
        # Дописываем в имя файла имя базы
        os.rename(__InputFileCSV__ + ".csv", __InputFileCSV__ + "_" + __DataBase__ + ".csv")
#    __InputFileCSV__ += "_"
except Exception:
    print(" -- имя входного файла не пометилось")
except:
    print(" -- Имя входного файла не пометилось")

# Счетчики
CountRoutesAdded = 0
CountRoutesFailed = 0
CountFlightsAdded = 0
CountFlightsPadded = 0
CountFlightsFailed = 0

# Немножко машинного обучения по задержкам
#print("Предел ожидания (рекомендуется 225), секунд = ", end=" ")
MaxDelay = int(input("Предел ожидания (рекомендуется 1750), секунд = "))  # Предел ожидания, секунд
if MaxDelay <= 35:
    MaxDelay = 35
elif MaxDelay > 1750:
    MaxDelay = 1750
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

OutputString = "\n\n"
OutputString += "Загрузка рабочих данных (версия обработки - " + str(__myOwnDevelopVersion__) + ") начата " + str(DateTime) + " \n"
OutputString += " Источник входных данных = " + str(__InputFileCSV__) + " \n"
OutputString += " Сервер СУБД = " + str(cnxn.getinfo(pyodbc.SQL_SERVER_NAME)) + " \n"
OutputString += " Драйвер = " + str(cnxn.getinfo(pyodbc.SQL_DRIVER_NAME)) + " \n"
OutputString += " Версия ODBC = " + str(cnxn.getinfo(pyodbc.SQL_ODBC_VER)) + " \n"
OutputString += " DSN = " + str(cnxn.getinfo(pyodbc.SQL_DATA_SOURCE_NAME)) + " \n"
OutputString += " Схема = " + str(cnxn.getinfo(pyodbc.SQL_USER_NAME)) + " \n"

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
# Между вложенными циклами результаты запросов не переходят, все перезапрашиваем снова
for AC, AL, FN, Dep, Arr in zip(ListAirCraft, ListAirLineCodeIATA, ListFlightNumber, ListAirPortDeparture, ListAirPortArrival):
    # Если есть код регистрации самолета, в том числе UNKNOWN и nan
    if AC and AL:
        if __DebugOutPut__:
            print("\n\n")
        print("Самолет", str(AC), end=" ")
        CurrentMax_i = 0  # Текущий максимум, секунд -> Обнуляем
        SetTransactionIsolationLevel("READ COMMITTED")
        # Цикл попыток
        for i in range(2, MaxDelay):
            if CurrentMax_i < i:
                CurrentMax_i = i
            try:
                # Начинаем транзакцию и блокируем запрашиваемые диапазоны
                DBAirCraft = QueryAirCraft(AC)
                DBAirLine = QueryAirLine(AL)
                cnxn.commit()
            except Exception:
                print("AC1>", end=" ")
                cnxn.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
                continue  # цикл с начала
            else:
                pass
            finally:
                pass  # выполняется всегда
            if DBAirCraft:
                try:
                    DBAirLine2 = QueryAirLine2(DBAirCraft.AirCraftAirLine)
                    cnxn.commit()
                except Exception:
                    print("AC2>", end=" ")
                    cnxn.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
                    continue  # цикл с начала
                else:
                    pass
                finally:
                    pass  # выполняется всегда
                # Если самолет есть в БД, и если нет авиакомпании или неизвестная авиакомпания
                if not DBAirCraft.AirCraftAirLine or DBAirLine2.AirLineCodeIATA == ('nan' or 'Unknown'):
                    # Вставляем (только один раз) авиакомпанию-оператора самолета
                    SQLUpdateAirCraft = "UPDATE dbo.AirCraftsTable SET AirCraftAirLine = " + str(DBAirLine.AirLineUniqueNumber) + " WHERE AirCraftRegistration = '" + str(AC) + "' "
                    try:
                        SetTransactionIsolationLevel("REPEATABLE READ")
                        seekAC.execute(SQLUpdateAirCraft)  # записываем данные по самолету в БД
                        cnxn.commit()  # фиксируем транзакцию, снимаем блокировку с запрошенных диапазонов
                        ListAirCraftsUpdated.append(AC)
                        print("вставилась авиакомпания-оператор", end=" ")
                        break
                    except Exception:
                        print("*", end=" ")
                        cnxn.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
                    finally:
                        SetTransactionIsolationLevel("READ COMMITTED")
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
                    SetTransactionIsolationLevel("SERIALIZABLE")
                    seekAC.execute(SQLInsertAirCraft)  # записываем данные по самолету в БД
                    cnxn.commit()  # фиксируем транзакцию, снимаем блокировку с запрошенных диапазонов
                    ListAirCraftsAdded.append(AC)
                    print("добавился", end=" ")
                    break
                except Exception:
                    # без самолета авиарейс с неизвестным самолетом
                    print("+", end=" ")
                    cnxn.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
                finally:
                    SetTransactionIsolationLevel("READ COMMITTED")
                    pass  # выполняется всегда
            #time.sleep(i)  # пытаемся уйти от взаимоблокировки
        else:
            ListAirCraftsFailed.append(AC)
        print(" ")
        DistributionDensityAirCrafts[CurrentMax_i] += 1

    # Если есть оба аэропорта и они разные
    if Dep and Arr and Dep != Arr:
        print(" Маршрут", str(Dep), "-", str(Arr), end=" ")
        CurrentMax_i = 0  # Текущий максимум, секунд -> Обнуляем
        SetTransactionIsolationLevel("READ COMMITTED")
        # Цикл попыток
        for i in range(2, MaxDelay):
            if CurrentMax_i < i:
                CurrentMax_i = i
            try:
                # Начинаем транзакцию и блокируем запрашиваемые диапазоны
                DBAirPortDep = QueryAirPort(Dep)
                DBAirPortArr = QueryAirPort(Arr)
                DBAirRoute = QueryAirRoute(Dep, Arr)
                cnxn.commit()
            except Exception:
                print("RT>", end=" ")
                cnxn.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
                continue  # цикл с начала
            else:
                pass
            finally:
                pass  # выполняется всегда
            # Для вставки аэропортов нужны полностью проверенные вручную данные, поэтому здесь аэропорты только проверяются
            # Если есть оба аэропорта и нет маршрута
            if DBAirPortDep and DBAirPortArr and not DBAirRoute:
                SQLInsertRoute = "INSERT INTO dbo.AirRoutesTable (AirPortDeparture, AirPortArrival, SourceCSVFile) VALUES ("
                SQLInsertRoute += str(DBAirPortDep.AirPortUniqueNumber) + ", "  # bigint
                SQLInsertRoute += str(DBAirPortArr.AirPortUniqueNumber) + ", "  # bigint
                SQLInsertRoute += "'" + str(__InputFileCSV__) + "') "  # ntext
                try:
                    SetTransactionIsolationLevel("SERIALIZABLE")
                    seekRT.execute(SQLInsertRoute)  # записываем маршрут в БД
                    cnxn.commit()  # фиксируем транзакцию, снимаем блокировку с запрошенных диапазонов
                    CountRoutesAdded += 1
                    print("добавился", end=" ")
                    break
                except Exception:
                    print("+", end=" ")
                    cnxn.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
                finally:
                    SetTransactionIsolationLevel("READ COMMITTED")
                    pass  # выполняется всегда
            elif not DBAirPortDep:
                ListAirPortsNotFounded.append(Dep)
                break
            elif not DBAirPortArr:
                ListAirPortsNotFounded.append(Arr)
                break
            else:
                break
            #time.sleep(i)  # пытаемся уйти от взаимоблокировки
        else:
            CountRoutesFailed += 1
        print(" ")
        DistributionDensityAirRoutes[CurrentMax_i] += 1

    # fixme в этом месте загрузки велись неправильно (читались коды IATA, сравнивали по коду ICAO) - версии 4 и 5 с ошибками загрузки, исправил 6-ой версии базы данных
    # Новая версия - все действия внутри обработки исключения
    # Если есть регистрационный номер самолета, код IATA авиакомпании и номер авиарейса
    if AC and AL and FN:
        print(" Авиарейс", str(AL) + str(FN), end=" ")
        CurrentMax_i = 0  # Текущий максимум, секунд -> Обнуляем
        SetTransactionIsolationLevel("READ COMMITTED")
        # Цикл попыток
        for i in range(2, MaxDelay):
            if CurrentMax_i < i:
                CurrentMax_i = i
            # Обработка исключения отсюда
            try:
                # Начинаем транзакцию и блокируем запрашиваемые диапазоны
                DBAirLine = QueryAirLine(AL)
                DBAirRoute = QueryAirRoute(Dep, Arr)
                cnxn.commit()
            except Exception:
                print("FN1>", end=" ")
                cnxn.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
                continue  # цикл с начала
            else:
                pass
            finally:
                pass  # выполняется всегда
            # Если есть:
            # - маршрут (должен быть),
            # - авиакомпания,
            # - не пустой номер авиарейса в файле,
            # - код регистрации самолета
            if DBAirLine and DBAirRoute:
                try:
                    DBAirCraft = QueryAirCraft(AC)
                    SQLExpression = "(FlightNumberString = '" + str(AL) + str(FN) + "') AND ((AirRoute = " + str(DBAirRoute.AirRouteUniqueNumber) + ") AND (AirCraft = " + str(DBAirCraft.AirCraftUniqueNumber) + "))"
                    SQLQueryFlight = "SELECT * FROM dbo.AirFlightsTable WHERE " + str(SQLExpression) + " ORDER BY  AirRoute, AirCraft, FlightNumberString"
                    seekFN.execute(SQLQueryFlight)  # много транзакций, подвисает, проигрыш при взаимоблокировке, сервер отбрасывает подключение -> скрипт слетает
                    DBAirFlight = seekFN.fetchone()
                    cnxn.commit()
                except Exception:
                    print("FN2>", end=" ")
                    cnxn.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
                    continue  # цикл с начала
                else:
                    pass
                finally:
                    pass  # выполняется всегда
                # Авиарейс с таким маршрутом есть
                if DBAirFlight:
                    # Плюсуем авиарейс
                    if DBAirFlight.QuantityCounted:
                        Quantity = DBAirFlight.QuantityCounted
                    else:
                        Quantity = 0  # NULL (пустая ячейка таблицы) в SQL => None (неопределенное вещественное число) в Python-е, NaN в R -> выражение с None не работает, функция не может вернуть None -> ошибка, скрипт слетает
                    Quantity += 1  # отдельно плюсуем на 1 для наглядности
                    SQLUpdateFlight = "UPDATE dbo.AirFlightsTable SET QuantityCounted = " + str(Quantity) + " WHERE " + str(SQLExpression) + " "  # fixme ошибка (используется устаревший ответ на запрос)
                    try:
                        SetTransactionIsolationLevel("REPEATABLE READ")
                        seekFN.execute(SQLUpdateFlight)  # записываем сплюсованный авиарейс в БД
                        cnxn.commit()  # фиксируем транзакцию, снимаем блокировку с запрошенных диапазонов
                        CountFlightsPadded += 1
                        print("сплюсовался", end=" ")
                        break
                    except Exception:
                        print("*", end=" ")
                        cnxn.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
                    finally:
                        SetTransactionIsolationLevel("READ COMMITTED")
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
                        SetTransactionIsolationLevel("SERIALIZABLE")
                        seekFN.execute(SQLInsertFlight)  # записываем добавленный авиарейс в БД
                        cnxn.commit()  # фиксируем транзакцию, снимаем блокировку с запрошенных диапазонов
                        CountFlightsAdded += 1
                        print("добавился", end=" ")
                        break
                    except Exception:
                        print("+", end=" ")
                        cnxn.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
                    else:
                        pass
                    finally:
                        SetTransactionIsolationLevel("READ COMMITTED")
                        pass  # выполняется всегда
            else:
                break
            #time.sleep(i)  # пытаемся уйти от взаимоблокировки
        else:
            CountFlightsFailed += 1
        print(" ")
        DistributionDensityAirFlights[CurrentMax_i] += 1

    #  Старая версия с взаимоблокировками
    # # Если есть регистрационный номер самолета, код IATA авиакомпании и номер авиарейса
    # if AC and AL and FN:
    #     print(" Авиарейс", str(AL) + str(FN), end=" ")
    #     CurrentMax_i = 0  # Текущий максимум, секунд -> Обнуляем
    #     SetTransactionIsolationLevel("READ COMMITTED")
    #     # Цикл попыток
    #     for i in range(2, MaxDelay):
    #         if CurrentMax_i < i:
    #             CurrentMax_i = i
    #         # Обработка исключения отсюда
    #         # Начинаем транзакцию и блокируем запрашиваемые диапазоны
    #         DBAirLine = QueryAirLine(AL)
    #         DBAirRoute = QueryAirRoute(Dep, Arr)
    #         # Если есть:
    #         # - маршрут (должен быть),
    #         # - авиакомпания,
    #         # - не пустой номер авиарейса в файле,
    #         # - код регистрации самолета
    #         if DBAirLine and DBAirRoute:
    #             DBAirCraft = QueryAirCraft(AC)
    #             SQLExpression = "(FlightNumberString = '" + str(AL) + str(FN) + "') AND ((AirRoute = " + str(DBAirRoute.AirRouteUniqueNumber) + ") AND (AirCraft = " + str(DBAirCraft.AirCraftUniqueNumber) + "))"
    #             SQLQueryFlight = "SELECT * FROM dbo.AirFlightsTable WHERE " + str(SQLExpression) + " ORDER BY  AirRoute, AirCraft, FlightNumberString"
    #             seekFN.execute(SQLQueryFlight)  # много транзакций, подвисает, проигрыш при взаимоблокировке, сервер отбрасывает подключение -> скрипт слетает
    #             DBAirFlight = seekFN.fetchone()
    #             # Авиарейс с таким маршрутом есть
    #             if DBAirFlight:
    #                 # Плюсуем авиарейс
    #                 if DBAirFlight.QuantityCounted:
    #                     Quantity = DBAirFlight.QuantityCounted
    #                 else:
    #                     Quantity = 0  # NULL (пустая ячейка таблицы) в SQL => None (неопределенное вещественное число) в Python-е, NaN в R -> выражение с None не работает, функция не может вернуть None -> ошибка, скрипт слетает
    #                 Quantity += 1  # отдельно плюсуем на 1 для наглядности
    #                 SQLUpdateFlight = "UPDATE dbo.AirFlightsTable SET QuantityCounted = " + str(Quantity) + " WHERE " + str(SQLExpression) + " "
    #                 try:
    #                     SetTransactionIsolationLevel("REPEATABLE READ")
    #                     seekFN.execute(SQLUpdateFlight)  # записываем сплюсованный авиарейс в БД
    #                     cnxn.commit()  # фиксируем транзакцию, снимаем блокировку с запрошенных диапазонов
    #                 except:
    #                     print("*", end=" ")
    #                     cnxn.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
    #                 else:
    #                     CountFlightsPadded += 1
    #                     print("сплюсовался", end=" ")
    #                     break
    #                 finally:
    #                     SetTransactionIsolationLevel("READ COMMITTED")
    #                     pass  # выполняется всегда
    #             else:
    #                 # Добавляем авиарейс
    #                 SQLInsertFlight = "INSERT INTO dbo.AirFlightsTable (AirRoute, AirCraft, FlightNumberString, QuantityCounted, SourceCSVFile) VALUES ("
    #                 SQLInsertFlight += str(DBAirRoute.AirRouteUniqueNumber) + ", "  # bigint
    #                 SQLInsertFlight += str(DBAirCraft.AirCraftUniqueNumber) + ", "  # bigint
    #                 SQLInsertFlight += "'" + str(AL) + str(FN) + "', "  # nvarchar(50)
    #                 SQLInsertFlight += str(1) + ", "  # bigint
    #                 SQLInsertFlight += "'" + str(__InputFileCSV__) + "') "  # ntext
    #                 try:
    #                     SetTransactionIsolationLevel("SERIALIZABLE")
    #                     seekFN.execute(SQLInsertFlight)  # записываем добавленный авиарейс в БД
    #                     cnxn.commit()  # фиксируем транзакцию, снимаем блокировку с запрошенных диапазонов
    #                 except:
    #                     print("+", end=" ")
    #                     cnxn.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
    #                 else:
    #                     CountFlightsAdded += 1
    #                     print("добавился", end=" ")
    #                     break
    #                 finally:
    #                     SetTransactionIsolationLevel("READ COMMITTED")
    #                     pass  # выполняется всегда
    #         else:
    #             break
    #         #cnxn.commit()  # снимаем блокировку с запрошенных диапазонов - старая версия
    #         time.sleep(i)  # пытаемся уйти от взаимоблокировки
    #     else:
    #         CountFlightsFailed += 1
    #     #cnxn.commit()  # фиксируем транзакцию - старая версия
    #     print(" ")
    #     DistributionDensityAirFlights[CurrentMax_i] += 1

# Снимаем курсоры
seekSubs.close()
seekAC.close()
seekRT.close()
seekFN.close()

# Фиксируем зависшие и безхозные транзакции
#cnxn.commit()  # старая версия
# Закрываем соединение
cnxn.close()

# Собираем три списка в DataFrame
DataFrameDistributionDensity = pandas.DataFrame(
    [DistributionDensityAirCrafts,
     DistributionDensityAirRoutes,
     DistributionDensityAirFlights],
    index=["AirCrafts", "AirRoutes", "AirFlights"]
)
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
OutputString += "   Пользователь = " + str(os.getlogin()) + " \n"
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

# Помечаем файл, как отработанный (добавляем плюс в имени файла)
# try:
#     os.rename(__InputFileCSV__ + ".csv", __InputFileCSV__ + "_+" + ".csv")
# except:
#     print(" -- имя входного файла", __InputFileCSV__, " не пометилось..... ")
