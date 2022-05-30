# -*- coding: utf-8 -*-

'''Заполняет БД самолетами из файлы-справочника типа *.csv

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

# Источник BTSgov
DataFromCSV = pandas.read_csv("804982210_T_ONTIME_REPORTING_2018_1.csv", sep=",")
ListAirLineCodeIATA = DataFromCSV['OP_UNIQUE_CARRIER'].tolist()
ListAirCraft = DataFromCSV['TAIL_NUM'].tolist()  # используется как длина списков
ListFlightNumber = DataFromCSV['OP_CARRIER_FL_NUM'].tolist()
ListAirPortDeparture = DataFromCSV['ORIGIN'].tolist()
ListAirPortArrival = DataFromCSV['DEST'].tolist()


# Добавляем недостающие маршруты

# Обнуляем счетчики
Count = 0
CountAdded = 0
CountFailed = 0
CountNotChecked = 0

while Count < len(ListAirLineCodeIATA):
    # Проверяем наличие аэропорта отправления
    myQueryAirPortSource = "SELECT * FROM dbo.AirPortsTableNew WHERE AirPortCodeIATA = '" + str(ListAirPortDeparture[Count]) + "'"
    seek.execute(myQueryAirPortSource)
    ResultSQLQueryAirPortSource = seek.fetchall()
    if not ResultSQLQueryAirPortSource:
        print("  ... Аэропорта", str(ListAirPortDeparture[Count]), "в БД пока нет, добавить маршрут не получится ...")
    # Проверяем наличие аэропорта прибытия
    myQueryAirPortDestination = "SELECT * FROM dbo.AirPortsTableNew WHERE AirPortCodeIATA = '" + str(ListAirPortArrival[Count]) + "'"
    seek.execute(myQueryAirPortDestination)
    ResultSQLQueryAirPortDestination = seek.fetchall()
    if not ResultSQLQueryAirPortDestination:
        print("  ... Аэропорта", str(ListAirPortArrival[Count]), "в БД пока нет, добавить маршрут не получится ...")
    if ResultSQLQueryAirPortSource and ResultSQLQueryAirPortDestination:
        # В таблице "AirRoutesTableNew" два внешних ключа на один первичный ключ и сделано условие "AirPortSource" не равно "AirPortDescination"
        # Оба аэропорта есть, проверяем наличие маршрута
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
                          WHERE (dbo.AirPortsTableNew.AirPortCodeIATA = '""" + str(ListAirPortDeparture[Count]) + "') AND (AirPortsTableNew_1.AirPortCodeIATA = '" + str(ListAirPortArrival[Count]) + "') COMMIT"
        try:
            seek.execute(myQueryRoute)  # ---- здесь скрипт слетает ---
        except:
            print(" ... -- условие не проверено --")
            Count += 1
            CountNotChecked += 1
            continue
        ResultSQLQueryRoute = seek.fetchall()
        if ResultSQLQueryRoute:
            # Такой маршрут есть
            print("Маршрут есть, не меняем")
        else:
            # Добавляем маршрут
            print("Маршрут в БД не найден, добавляем его")
            myQueryInsert = "BEGIN TRANSACTION "
            myQueryInsert += "INSERT INTO dbo.AirRoutesTableNew (AirPortDeparture, AirPortArrival, Stops, Equipment) VALUES ("
            myQueryInsert += "(SELECT AirPortUniqueNumber FROM dbo.AirPortsTableNew WHERE AirPortCodeIATA = '" + str(ListAirPortDeparture[Count]) + "'), "  # nchar(10)
            myQueryInsert += "(SELECT AirPortUniqueNumber FROM dbo.AirPortsTableNew WHERE AirPortCodeIATA = '" + str(ListAirPortArrival[Count]) + "'), "  # nchar(10)
            #myQueryInsert += str(ListStops[Count_index]) + ", "  # smallint
            myQueryInsert += "0, "  # smallint
            #myQueryInsert += "'" + str(ListEquipment[Count_index]) + "')"  # ntext
            myQueryInsert += "'++ 804982210_T_ONTIME_REPORTING_2018_1.csv ++') "  # ntext
            myQueryInsert += "COMMIT TRANSACTION "
            try:
                seek.execute(myQueryInsert)
                CountAdded += 1
            except:
                print(" ..-- Маршрут не вставился .....")
                CountFailed += 1
    Count += 1

# Снимаем курсор
seek.close()

# Заканчиваем висящие транзакции
cnxn.commit()
# Закрываем соединение
cnxn.close()

# Выводим итоги
print("\n Итоги:\n ----")
print(" Просмотрено", str(Count), "записей в справочном файле")
print(" Добавлено", str(CountAdded), "маршрутов")
print(" Не добавлено", str(CountFailed), "маршрутов")
