# -*- coding: utf-8 -*-

'''Заполняем строки в БД из файлы-справочника типа *.csv
   открываем строку файла и ищем авиакомпанию с кодом ICAO
   Если такой еще нет, передаем ее характеристики на вход процедуре
   SPAirLineInsertion
   Процедура за одну транзакцию вставляет одну строку в справочную таблицу
'''


import pyodbc
import pandas


myDriver = "SQL Server"
myServer = "Data-Server"
myDataBase = "AirFlightsDB"

# Открываем соединение с БД. Значение AUTOCOMMIT берет из БД (там по-умолчанию FALSE)
cnxn = pyodbc.connect(driver=myDriver, server=myServer, database=myDataBase)

# Ставим курсор на начало
seek = cnxn.cursor()

# Читаем справочный файл типа *.csv (разделитель - |, шапка таблицы) и перепаковываем его в DataFrame
# Источник OpenFlights
DataFrameFromCSV = pandas.read_csv("++AirLines.csv", sep="|")
# Столбцы из справочного файла
ListID = DataFrameFromCSV['AirLine_ID'].tolist()
ListName = DataFrameFromCSV['Name'].tolist()
ListAlias = DataFrameFromCSV['Alias'].tolist()
ListIATA = DataFrameFromCSV['IATA'].tolist()
ListICAO = DataFrameFromCSV['ICAO'].tolist()
ListCallSighn = DataFrameFromCSV['CallSighn'].tolist()
ListCountry = DataFrameFromCSV['Country'].tolist()

'''
# Источник BTSgov
DataFromCSV = pandas.read_csv("L_CARRIERS.csv", sep=",")
# Столбцы из справочного файла
ListICAO = DataFromCSV['ICAO'].tolist()
ListName = DataFromCSV['Name'].tolist()'''

# Счетчики
CountAdded = 0
CountFailed = 0


# Делаем проход по таблице - ищем такой же код IATA
# Если такой уже есть, переходим на следующую строку DataFrame-а
for ID, Name, Alias, IATA, ICAO, CallSighn, Country in zip(ListID, ListName, ListAlias, ListIATA, ListICAO, ListCallSighn, ListCountry):
    # Становимся на строку с номером Count_index
    myQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineCodeICAO = '" + str(ICAO) + "' ORDER BY AirLineCodeICAO"
    seek.execute(myQuery)
    ResultSQL = seek.fetchall()
    if ResultSQL:
        print("Код ", ICAO, " есть, не меняем")
    else:
        print("...Код ", ICAO, " не найден, добавляем его")
        # Вызываем процедуру и даем ей на вход характеристики аэропорта с этим кодом IATA
        myInsertion = "SPAirLineInsertion "
        myInsertion += str(int(ID)) + ", "  # bigint
        myInsertion += "'" + str(Name) + "', "  # nvarchar(50)
        myInsertion += "'" + str(Alias) + "', "  # nvarchar(50)
        myInsertion += "'" + str(IATA) + "', "  # nchar(10)
        myInsertion += "'" + str(ICAO) + "', "  # nchar(10)
        myInsertion += "'" + str(CallSighn) + "', "  # nvarchar(50)
        myInsertion += "'" + str(Country) + "' "  # nvarchar(50)
        try:
            seek.execute(myInsertion) # если параметры не подготовлены, вылетает
            CountAdded += 1
        except:
            print("..-- Код ", str(ICAO), " не обработан .....") # не получается
            CountFailed += 1

# Снимаем курсор
seek.close()

# Заканчиваем висящие транзакции
cnxn.commit()

# Закрываем соединение
cnxn.close()

# Итоги
print("\n Итоги:\n ----")
print(" Добавлено ", str(CountAdded), " авиакомпаний")
print(" Не добавлено ", str(CountFailed), " авиакомпаний")
