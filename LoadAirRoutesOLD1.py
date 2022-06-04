# -*- coding: utf-8 -*-

'''Заполняет БД маршрутами из файлы-справочника типа *.csv
   Читаем строку справочного файла и проверяем аэропорты.
   Если все есть, то смотрим в БД такой маршрут по кодам IATA аэропортов.
   Если такого маршрута нет, добавляем его.
   Прежние маршруты остаются без изменений

   --- На больших входных файлах наблюдается постепенная значительная утечка ОЗУ ---
'''


import pyodbc
import pandas


myDriver = "SQL Server"
myServer = "Data-Server"
myDataBase = "AirLines"

# Открываем соединение с БД. Значение AUTOCOMMIT берет из БД (там по-умолчанию FALSE)
cnxn = pyodbc.connect(driver=myDriver, server=myServer, database=myDataBase)

# Ставим курсор на начало
seek = cnxn.cursor()

# Читаем справочный файл типа *.csv (UTF-8, шапка таблицы, разделитель - |) и перепаковываем его в DataFrame
# В исходном файле *.csv подписаны столбцы -> в DataFrame можно пока обращаться к именам столбцов

'''
# Источник OpenFlights
DataFrameFromCSV = pandas.read_csv("Routes.csv", sep="|")
ListAirLine = DataFrameFromCSV['AirLine'].tolist()
ListAirPortSource = DataFrameFromCSV['AirPortSource'].tolist()  # используется как длина списков
ListAirPortDestination = DataFrameFromCSV['AirPortDestination'].tolist()
ListStops = DataFrameFromCSV['Stops'].tolist()
ListEquipment = DataFrameFromCSV['Equipment'].tolist()'''

# Источник BTSgov
DataFromCSV = pandas.read_csv("1007531840_T_DB1B_COUPON.csv", sep=",")
ListAirPortSource = DataFromCSV['ORIGIN'].tolist()
ListAirPortDestination = DataFromCSV['DEST'].tolist()

# Счетчики
Count_index = 0
CountNotChecked = 0
CountAdded = 0
CountFailed = 0

# Делаем проход по таблице Если такой уже есть, переходим на следующую строку DataFrame-а
while Count_index < len(ListAirPortSource):
    # Становимся на строку с номером Count_index
    myQueryAirPortSource = "SELECT * FROM dbo.AirPortsTableNew WHERE AirPortCodeIATA = '" + str(ListAirPortSource[Count_index]) + "'"
    seek.execute(myQueryAirPortSource)
    ResultSQLQueryAirPortSource = seek.fetchall()
    if not ResultSQLQueryAirPortSource:
        print("  ... Аэропорта ", str(ListAirPortSource[Count_index]), " в БД пока нет, добавить маршрут не получится ...")
    myQueryAirPortDestination = "SELECT * FROM dbo.AirPortsTableNew WHERE AirPortCodeIATA = '" + str(ListAirPortDestination[Count_index]) + "'"
    seek.execute(myQueryAirPortDestination)
    ResultSQLQueryAirPortDestination = seek.fetchall()
    if not ResultSQLQueryAirPortDestination:
        print("  ... Аэропорта ", str(ListAirPortDestination[Count_index]), " в БД пока нет, добавить маршрут не получится ...")
    if ResultSQLQueryAirPortSource and ResultSQLQueryAirPortDestination:
        # В таблице "AirRoutesTableNew" два внешних ключа на один первичный ключ и сделано условие "AirPortSource" не равно "AirPortDestination"
        myQueryRoute = """SELECT dbo.AirRoutesTableNew.AirRouteUniqueNumber AS AIRROUTE,
                                 dbo.AirPortsTableNew.AirPortName AS DEPARTURE,
                                 AirPortsTableNew_1.AirPortName AS ARRIVAL,
                                 dbo.AirRoutesTableNew.CodeShape,
                                 dbo.AirRoutesTableNew.Stops,
                                 dbo.AirRoutesTableNew.Equipment,
                                 dbo.AirPortsTableNew.AirPortCodeIATA AS Departure_IATA,
                                 AirPortsTableNew_1.AirPortCodeIATA AS Arrival_IATA                                 
                          FROM dbo.AirRoutesTableNew INNER JOIN
                               dbo.AirPortsTableNew ON dbo.AirRoutesTableNew.AirPortDeparture = dbo.AirPortsTableNew.AirPortUniqueNumber INNER JOIN
                               dbo.AirPortsTableNew AS AirPortsTableNew_1 ON dbo.AirRoutesTableNew.AirPortArrival = AirPortsTableNew_1.AirPortUniqueNumber
                          WHERE (dbo.AirPortsTableNew.AirPortCodeIATA = '""" + str(ListAirPortSource[Count_index]) + "') AND (AirPortsTableNew_1.AirPortCodeIATA = '" + str(ListAirPortDestination[Count_index]) + "') COMMIT"
        try:
            seek.execute(myQueryRoute)  # ---- здесь скрипт слетает ---
        except:
            print(" ... -- условие не проверено --")
            Count_index += 1
            CountNotChecked += 1
            continue
        ResultSQLQueryRoute = seek.fetchall()
        if ResultSQLQueryRoute:
            # Такой маршрут есть в БД
            print("Маршрут есть, не меняем")
        else:
            # Такого маршрута нет в БД. Добавляем его
            print("Маршрут в БД не найден, добавляем его")
            myQueryInsert = "BEGIN TRANSACTION "
            myQueryInsert += "INSERT INTO dbo.AirRoutesTableNew (AirPortDeparture, AirPortArrival, Stops, Equipment) VALUES ("
            myQueryInsert += "(SELECT AirPortUniqueNumber FROM dbo.AirPortsTableNew WHERE AirPortCodeIATA = '" + str(ListAirPortSource[Count_index]) + "'), "  # nchar(10)
            myQueryInsert += "(SELECT AirPortUniqueNumber FROM dbo.AirPortsTableNew WHERE AirPortCodeIATA = '" + str(ListAirPortDestination[Count_index]) + "'), "  # nchar(10)
            #myQueryInsert += str(ListStops[Count_index]) + ", "  # smallint
            myQueryInsert += "0, "  # smallint
            #myQueryInsert += "'" + str(ListEquipment[Count_index]) + "')"  # ntext
            myQueryInsert += "'-+- OpenFlights -+-') "  # ntext
            myQueryInsert += "COMMIT TRANSACTION "
            try:
                seek.execute(myQueryInsert)
                CountAdded += 1
            except:
                print(" ..-- Маршрут не вставился .....")
                CountFailed += 1
    Count_index += 1

# Если заполение велось с помощью этой обработки, повторов не будет

# Снимаем курсор
seek.close()

# Заканчиваем висящие транзакции
cnxn.commit()
# Закрываем соединение
cnxn.close()

# Выводим итоги
print("\n Итоги:\n ----")
print(" Просмотрено ", str(Count_index), " записей в справочном файле")
print(" Не проверено ", str(CountNotChecked), " записей")
print(" Добавлено ", str(CountAdded), " авиалиний")
print(" Не добавлено", str(CountFailed), " авиалиний")
