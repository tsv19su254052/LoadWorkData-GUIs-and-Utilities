# -*- coding: utf-8 -*-

'''Заполняем строки в БД из файлы-справочника типа *.csv
   данными по самолетам
   Вставить имя файла и номер модели самолета
'''


import pyodbc
import pandas
import time
import datetime


__version__ = 5.1  # столько плюсов ставим в имени отработанного файла спереди
# Отметка времени начала загрузки
StartTime = datetime.datetime.now()

# Открываем соединение с БД. Значение AUTOCOMMIT берет из БД (там по-умолчанию FALSE)
myDriver = "SQL Server"
myServer = "Data-Server"
myDataBase = "AirFlightsDBNew3"

# Открываем соединение с БД. Значение AUTOCOMMIT берет из БД (там по-умолчанию FALSE)
cnxn = pyodbc.connect(driver=myDriver, server=myServer, database=myDataBase)

# Ставим курсор на начало
seek = cnxn.cursor()

# Читаем справочный файл типа *.csv (разделитель - |, шапка таблицы) и перепаковываем его в DataFrame

# Источник PlaneList.net
# Убать из файла все косые, запятые и кавычки
myCSVFile = "Tu-334.csv"
Model = 201  # модель самолета в таблице

# Перепаковываем его в DataFrame (шапка таблицы над столбцами, разделитель - ,)
DataFrameFromCSV = pandas.read_csv(myCSVFile, sep="|")
# В исходном файле *.csv подписаны столбцы -> в DataFrame можно перемещаться по именам столбцов -> Разбираем на столбцы и работаем по ним
ListCN = DataFrameFromCSV['CN'].tolist()
ListLN = DataFrameFromCSV['LN'].tolist()
ListRegistration = DataFrameFromCSV['Registration'].tolist()
ListOwner = DataFrameFromCSV['AirLineOwner'].tolist()
ListDD = DataFrameFromCSV['DD'].tolist()
ListType = DataFrameFromCSV['Type'].tolist()
ListSt = DataFrameFromCSV['St'].tolist()
ListRemarks = DataFrameFromCSV['FateRemarks'].tolist()

# Счетчики
CountAirCraftsAdded = 0
CountAirCraftsUpdated = 0
CountAirCraftsFailed = 0
CountAirCraftsNotUpdated = 0

# Список недобавленных самолетов
ListAirCraftsFailed = []

# Делаем проход по таблице - ищем такой же код IATA
for CN, LN, AC, Owner, DD, Type, St, Remarks in zip(ListCN, ListLN, ListRegistration, ListOwner, ListDD, ListType, ListSt, ListRemarks):
    myQuery = "SELECT * FROM dbo.AirCraftsTable WHERE AirCraftRegistration = '" + str(AC) + "' COMMIT"
    seek.execute(myQuery)
    ResultSQL = seek.fetchone()
    if ResultSQL:
        print("\n  ++ Самолет ", AC, " есть", end=" ")
        if ResultSQL.AirCraftModel == 186 or ResultSQL.AirCraftModel != Model:  # 186 зарезервировано в БД как неизвестная или нестандартная модель
            myUpdate = "UPDATE dbo.AirCraftsTable SET AirCraftModel = " + str(Model) + " WHERE AirCraftRegistration = '" + str(AC) + "' "
            try:
                seek.execute(myUpdate)
                print(", модель обновили", end=" ")
            except:
                print(", модель не обновили", end=" ")
        if ResultSQL.AirCraftModel == Model:  # чтобы не затереть другой самолет, например, другой модели с возможно таким же кодом регистрации
            if not ResultSQL.SourceCSVFile:
                myUpdate = "UPDATE dbo.AirCraftsTable SET SourceCSVFile = '" + str(myCSVFile) + "' WHERE AirCraftRegistration = '" + str(AC) + "' "
                try:
                    seek.execute(myUpdate)
                    print(" источник обновили", end=" ")
                except:
                    print(" источник не обновили", end=" ")
            if not ResultSQL.AirCraftDescription:
                myUpdate = "UPDATE dbo.AirCraftsTable SET AirCraftDescription = '" + str(Remarks) + "' WHERE AirCraftRegistration = '" + str(AC) + "' "
                try:
                    seek.execute(myUpdate)
                    print(", описание обновили", end=" ")
                except:
                    print(", описание не обновили", end=" ")
            if not ResultSQL.AirCraftLineNumber_LN_MSN:
                myUpdate = "UPDATE dbo.AirCraftsTable SET AirCraftLineNumber_LN_MSN = '" + str(LN) + "' WHERE AirCraftRegistration = '" + str(AC) + "' "
                try:
                    seek.execute(myUpdate)
                    print(", LN MSN обновили", end=" ")
                except:
                    print(", LN MSN не обновили", end=" ")
            if not ResultSQL.AirCraftCNumber:
                myUpdate = "UPDATE dbo.AirCraftsTable SET AirCraftCNumber = '" + str(CN) + "' WHERE AirCraftRegistration = '" + str(AC) + "' "
                try:
                    seek.execute(myUpdate)
                    print(", CN обновили", end=" ")
                except:
                    print(", CN не обновили", end=" ")
            if not ResultSQL.Owner1:
                myUpdate = "UPDATE dbo.AirCraftsTable SET Owner1 = '" + str(Owner) + "' WHERE AirCraftRegistration = '" + str(AC) + "' "
                try:
                    seek.execute(myUpdate)
                    print(", владельца обновили", end=" ")
                except:
                    print(", владельца не обновили", end=" ")
            if not ResultSQL.Type:
                myUpdate = "UPDATE dbo.AirCraftsTable SET Type = '" + str(Type) + "' WHERE AirCraftRegistration = '" + str(AC) + "' "
                try:
                    seek.execute(myUpdate)
                    print(", модификацию обновили", end=" ")
                except:
                    print(", модификацию не обновили", end=" ")
            if not ResultSQL.State:
                myUpdate = "UPDATE dbo.AirCraftsTable SET State = '" + str(St) + "' WHERE AirCraftRegistration = '" + str(AC) + "' "
                try:
                    seek.execute(myUpdate)
                    print(", состояние обновили", end=" ")
                except:
                    print(", состояние не обновили", end=" ")
    else:
        print("\nДобавляем самолет ", AC, "+++ ->", end=" ")
        myInsert = "INSERT INTO dbo.AirCraftsTable (AirCraftRegistration, AirCraftModel, SourceCSVFile, AirCraftDescription, AirCraftLineNumber_LN_MSN, AirCraftCNumber, Owner1, Type, State) VALUES ("
        myInsert += "'" + str(AC) + "', "  # nvarchar(50)
        myInsert += str(Model) + ", "  # bigint
        myInsert += "'" + str(myCSVFile) + "', "  # ntext
        myInsert += "'" + str(Remarks) + "', "  # ntext
        myInsert += "'" + str(LN) + "', "  # nvarchar(50)
        myInsert += "'" + str(CN) + "', "  # nvarchar(50)
        myInsert += "'" + str(Owner) + "', "  # nvarchar(50)
        myInsert += "'" + str(Type) + "', "  # nvarchar(50)
        myInsert += "'" + str(St) + "') "  # nvarchar(50)
        try:
            seek.execute(myInsert)
            CountAirCraftsAdded += 1
            print(" готово")
        except:
            CountAirCraftsFailed += 1
            ListAirCraftsFailed.append(AC)
            print(" не добавился .....")
    cnxn.commit()

# Снимаем курсор
seek.close()

# Заканчиваем висящие транзакции
cnxn.commit()
# Закрываем соединение
cnxn.close()

# Отметка времени окончания загрузки
EndTime = datetime.datetime.now()
# Дата и время сейчас
Now = time.time()
DateTime = time.ctime(Now)

# Итоги
print("\n Итоги:\n ----")
print(" Источник - ", str(myCSVFile))
if CountAirCraftsAdded:
    print(" Добавлено ", str(CountAirCraftsAdded), " самолетов")
if CountAirCraftsFailed:
    print(" Не добавлено ", str(CountAirCraftsFailed), " самолетов")
    if ListAirCraftsFailed:
        print(ListAirCraftsFailed)
print(" ----")
print("   Длительность загрузки", EndTime - StartTime)
print("   Дата и время", DateTime)
