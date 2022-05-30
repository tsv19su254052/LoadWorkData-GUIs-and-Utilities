# -*- coding: utf-8 -*-

# Обработка добавляет в БД аэропорты по коду IATA из файла-справочника типа *.csv
import pyodbc
import pandas

myDriver = "SQL Server"
myServer = "Data-Server"
myDataBase = "AirLines"

# Открываем соединение с БД. Значение AUTOCOMMIT берет из БД (там по-умолчанию FALSE)
#cnxn = pyodbc.connect("Driver={SQL Server}; Server=" + __Server__ + "; Database=" + __DataBase__ + "; Trusted_Connection=yes;")
cnxn = pyodbc.connect(driver=myDriver, server=myServer, database=myDataBase)

# Ставим курсор на начало
seek = cnxn.cursor()

# Читаем справочный файл типа *.csv (разделитель - |, строка 1 - шапка таблицы) и перепаковываем его в DataFrame


# Источник ApInfoRu
DataFrameFromCSV = pandas.read_csv("++ApInfoRu.csv", sep="|")
# Столбцы из справочного файла
ListIATA = DataFrameFromCSV['IATA'].tolist()
ListICAO = DataFrameFromCSV['ICAO'].tolist()
ListName = DataFrameFromCSV['Name'].tolist()
ListCity = DataFrameFromCSV['City'].tolist()
ListCountry = DataFrameFromCSV['Country'].tolist()
ListLatitude = DataFrameFromCSV['Latitude'].tolist()
ListLongitude = DataFrameFromCSV['Longitude'].tolist()

'''
# Источник  OpenFlights
DataFrameFromCSV = pandas.read_csv("AirPorts.csv", sep="|")
# Столбцы из справочного файла
ListIATA = DataFrameFromCSV['IATA'].tolist()
ListName = DataFrameFromCSV['Name'].tolist()
ListLatitude = DataFrameFromCSV['Latitude'].tolist()
ListLongitude = DataFrameFromCSV['Longitude'].tolist()'''

'''
# Источник  Bureau of Transportation Statistics
DataFromCSV = pandas.read_csv("L_AIRPORT.csv", sep="|")
# Столбцы из справочного файла
ListIATA = DataFromCSV['IATA'].tolist()
ListCity = DataFromCSV['City'].tolist()
ListName = DataFromCSV['Name'].tolist()'''

# Счетчики
CountAdded = 0
CountFailed = 0

# Делаем проход по таблице - ищем такой же код IATA
# Если такой уже есть, переходим на следующую строку DataFrame-а
for IATA, ICAO, Name, City, Country, Latitude, Longitude in zip(ListIATA, ListICAO, ListName, ListCity, ListCountry, ListLatitude, ListLongitude):
    # Становимся на строку с номером Count_index
    myQuery = "SELECT * FROM dbo.AirPortsTableNew WHERE AirPortCodeIATA = '" + IATA + "' ORDER BY AirPortCodeIATA"
    seek.execute(myQuery)
    ResultSQL = seek.fetchall()
    if ResultSQL:
        print("Код ", IATA, " есть, не меняем")
    else:
        print("...Код ", IATA, " не найден, добавляем его")
        # Вызываем процедуру и даем ей на вход характеристики аэропорта с этим кодом IATA
        myInsertion = "SPAirPortsInsertion "
        myInsertion += "'" + str(IATA) + "', "  # nchar(10)
        myInsertion += "'" + str(ICAO) + "', "  # nchar(10)
        myInsertion += "'" + str(Name) + "', "  # nvarchar(50)
        myInsertion += "'" + str(City) + "', "  # nvarchar(50)
        myInsertion += "'" + str(Country) + "', "  # nvarchar(50)
        myInsertion += str(float(Latitude)) + ", "  # float
        myInsertion += str(float(Longitude)) + ", 0"  # Longitude, Height - float, float
        try:
            seek.execute(myInsertion) # некорректные строки не вставляются
            CountAdded += 1
        except:
            print("..-- Код ", str(IATA), " не обработан .....")
            CountFailed += 1

myQuery = """SELECT [AirPortCodeIATA], [AirPortCodeICAO], [AirPortName], [AirPortCity], [AirPortCountry], [AirPortLatitude], [AirPortLongitude]
             FROM [AirLines].[dbo].[AirPortsTableNew]
             ORDER BY AirPortCodeIATA"""
DataFromSQL = pandas.read_sql(myQuery, cnxn)
DataFromSQL.to_csv("DataSQL.csv", sep="|")
DataFromSQL.to_json("DataSQL.json")
DataFromSQL.to_html("DataSQL.html")

# Снимаем курсор
seek.close()

# Заканчиваем висящие транзакции
cnxn.commit()
# Закрываем соединение
cnxn.close()

# Выводим итоги
print("\n Итоги:\n ----")
print(" Просмотрено ", str(len(IATA)), " записей в справочном файле")
print(" Добавлено ", str(CountAdded), " аэропортов")
print(" Не добавлено ", str(CountFailed), " аэропортов")
