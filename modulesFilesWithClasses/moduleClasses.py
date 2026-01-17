#  Interpreter 3.7 -> 3.10 -> 3.12 -> 3.13 -> 3.14


from xml.etree import ElementTree
# todo ветка библиотек Qt - QtCore, QtGui, QtNetwork, QtOpenGL, QtScript, QtSQL (медленнее чем pyodbc), QtDesigner, QtXml
# Руководство по установке см. https://packaging.python.org/tutorials/installing-packages/

# Пользовательская библиотека с классами
from modulesFilesWithClasses.moduleClassServerExchange import ServerExchange
# Задача создания пользовательских структур данных не расматривается -> Только функционал
# Компилируется и кладется в папку __pycache__
# Идея выноса каждого класса в этот отдельный файл, как на Java -> Удобство просмотра типов данных, не особо практично


class FileNames:
    def __init__(self):
        # Имена читаемых и записываемых файлов
        self.InputFileCSV = ' '
        self.OutputFileTXT = ' '
        self.OutputFileTXTErrors = 'LogReport_Errors.txt'
        self.OutputFileLOG = ' '


class Flags:
    def __init__(self):
        # Флаги
        self.useAirCrafts = False  # пишем авиаперелеты в БД самолетов
        self.useAirCraftsDB = True  # используем драйвер
        self.useAirFlightsDB = True  # используем драйвер
        self.useSAX = False
        self.useMSsql = False
        self.useODBCMarkers = False
        self.useSQLServerDriverFormat = False
        self.SetInputDate = False
        self.BeginDate = ' '


class States:
    def __init__(self):
        # Состояния
        self.Connected_AL = False
        self.Connected_RT = False
        self.Connected_A = False


SE = ServerExchange


class ACFN(SE):
    def __init__(self):
        super().__init__(c=None, s=None)
        self.Result = 0
        # AirLine
        self.AirLine_ID = 1
        self.AirLineName = " "
        self.AirLineAlias = " "
        self.AirLineCodeIATA = " "
        self.AirLineCodeICAO = " "
        self.AirLineCallSighn = " "
        self.AirLineCity = " "
        self.AirLineCountry = " "
        self.AirLineStatus = 1
        self.CreationDate = '1990-01-01'
        self.AirLineDescription = " "
        self.Alliance = 4
        self.Position = 1  # Позиция курсора в таблице (в SQL начинается с 1)
        self.cnxn_AL_odbc = None  # подключение
        self.seek_AL_odbc = None  # курсор
        # AirCraft
        self.AirCraftModel = 387  # Unknown Model
        self.BuildDate = '1990-01-01'
        self.RetireDate = '1990-01-01'
        self.AirCraftSourceCSVFile = " "
        self.AirCraftDescription = " "
        self.AirCraftLineNumber_LN = " "
        self.AirCraftLineNumber_MSN = " "
        self.AirCraftSerialNumber_SN = " "
        self.AirCraftCNumber = " "
        self.EndDate = '1990-01-01'
        # Подключения
        self.cnxn_A_mssql = None
        self.cnxn_A_odbc = None
        # Курсоры
        self.seek_A_mssql = None
        self.seek_A_odbc = None
        # AirPort
        self.HyperLinkToWikiPedia = " "
        self.HyperLinkToAirPortSite = " "
        self.HyperLinkToOperatorSite = " "
        self.HyperLinksToOtherSites = " "
        self.AirPortCodeIATA = " "
        self.AirPortCodeICAO = " "
        self.AirPortCodeFAA_LID = " "
        self.AirPortCodeWMO = " "
        self.AirPortName = " "
        self.AirPortCity = " "
        self.AirPortCounty = " "
        self.AirPortCountry = " "
        self.AirPortLatitude = 0
        self.AirPortLongitude = 0
        self.HeightAboveSeaLevel = 0
        self.SourceCSVFile = " "
        self.AirPortDescription = " "
        self.AirPortRunWays = " "
        self.AirPortFacilities = " "
        self.AirPortIncidents = " "
        self.cnxn_RT_odbc = None  # подключение
        self.seek_RT_odbc = None  # курсор
        self.LogCountViewed = 0
        self.LogCountChanged = 0

    def getListDataBasesLocal(self):
        ListDataBases = []
        ListDataBasesAirLines = []
        ListDataBasesAirCrafts = []
        ListDataBasesAirPorts = []
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seek_AL_odbc.execute(SQLQuery)
            SQLQuery = "SELECT name from sys.databases"
            self.seek_AL_odbc.execute(SQLQuery)
            ResultSQL = self.seek_AL_odbc.fetchall()
            self.cnxn_AL_odbc.commit()
            print(" результат запроса = " + str(ResultSQL))
            #список баз данных = [('master',), ('tempdb',), ('model',), ('msdb',), ('AirCraftsDBNew62',), ('AirLinesDBNew62',), ('AirPortsAndRoutesDBNew62',)]
            for line in ResultSQL:
                print(" line = " + str(line[0]))
                if line[0] != 'master' and line[0] != 'tempdb' and line[0] != 'model' and line[0] != 'msdb':
                    ListDataBases.append(line[0])
            print(" список баз = " + str(ListDataBases))
            for string in ListDataBases:
                if 'AirLines' in string:
                    ListDataBasesAirLines.append(string)
                if 'AirCrafts' in string:
                    ListDataBasesAirCrafts.append(string)
                if 'AirPorts' in string:
                    ListDataBasesAirPorts.append(string)
            print(" БД авиакомпаний = " + str(ListDataBasesAirLines))
            print(" БД самолетов = " + str(ListDataBasesAirCrafts))
            print(" БД аэропортов = " + str(ListDataBasesAirPorts))
        except Exception:
            ResultSQL = False
            self.cnxn_AL_odbc.rollback()
        return ListDataBases

    def getListDataBasesRemote(self):
        pass

    class AirLine:
        def __init__(self):
            pass

    def connect_DB_AL_odbc(self, servername, driver, database):
        if self.connect_DB_odbc(servername=servername, driver=driver, database=database):
            self.cnxn_AL_odbc = self.cnxn
            self.seek_AL_odbc = self.seek
            #self.getListDataBasesLocal()
            return True
        else:
            return False

    def disconnect_AL_odbc(self):
        try:
            # Закрываем курсор
            self.seek_AL_odbc.close()
            # Отключаемся от базы данных
            self.cnxn_AL_odbc.close()
            print(" -- БД отключена")
        except Exception:
            print(" -- БД уже отключена")
        #self.disconnect()

    def QueryAlliances(self):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seek_AL_odbc.execute(SQLQuery)
            SQLQuery = "SELECT AllianceUniqueNumber, AllianceName FROM dbo.AlliancesTable"  # Убрал  ORDER BY AllianceName
            self.seek_AL_odbc.execute(SQLQuery)
            ResultSQL = self.seek_AL_odbc.fetchall()
            self.cnxn_AL_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_AL_odbc.rollback()
        return ResultSQL

    def QueryAlliancesSqlAlchemy(self):
        pass

    def QueryAlliancePKByName(self, name):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seek_AL_odbc.execute(SQLQuery)
            SQLQuery = "SELECT AllianceUniqueNumber FROM dbo.AlliancesTable WHERE AllianceName='" + str(name) + "' "  # Убрал  ORDER BY AllianceName
            self.seek_AL_odbc.execute(SQLQuery)
            ResultSQL = self.seek_AL_odbc.fetchone()
            self.cnxn_AL_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_AL_odbc.rollback()
        return ResultSQL[0]

    def QueryAirLineByPK(self, pk):
        # Возвращает строку авиакомпании по первичному ключу
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seek_AL_odbc.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineUniqueNumber = '" + str(pk) + "' "
            self.seek_AL_odbc.execute(SQLQuery)
            ResultSQL = self.seek_AL_odbc.fetchone()
            self.cnxn_AL_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_AL_odbc.rollback()
        return ResultSQL

    def QueryAirLineByIATA(self, iata):
        # Возвращает строку авиакомпании по ее коду IATA
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seek_AL_odbc.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineCodeIATA = '" + str(iata) + "' "
            self.seek_AL_odbc.execute(SQLQuery)
            ResultSQL = self.seek_AL_odbc.fetchone()
            self.cnxn_AL_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_AL_odbc.rollback()
        return ResultSQL

    def QueryAirLineByICAO(self, icao):
        # Возвращает строку авиакомпании по ее коду ICAO
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seek_AL_odbc.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineCodeICAO = '" + str(icao) + "' "
            self.seek_AL_odbc.execute(SQLQuery)
            ResultSQL = self.seek_AL_odbc.fetchone()
            self.cnxn_AL_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_AL_odbc.rollback()
        return ResultSQL

    def QueryAirLineByIATAandICAO(self, iata, icao):
        # Возвращает строку авиакомпании по ее кодам IATA и ICAO
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seek_AL_odbc.execute(SQLQuery)
            if iata is None:
                SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineCodeIATA IS NULL AND AirLineCodeICAO = '" + str(icao) + "' "
            elif icao is None:
                SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineCodeIATA = '" + str(iata) + "' AND AirLineCodeICAO IS NULL "
            elif iata is None and icao is None:
                SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineCodeIATA IS NULL AND AirLineCodeICAO IS NULL "
            else:
                SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineCodeIATA = '" + str(iata) + "' AND AirLineCodeICAO = '" + str(icao) + "' "
            self.seek_AL_odbc.execute(SQLQuery)
            ResultSQL = self.seek_AL_odbc.fetchone()
            self.cnxn_AL_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_AL_odbc.rollback()
        return ResultSQL

    def InsertAirLineByIATAandICAO(self, iata, icao):
        # Вставляем авиакомпанию с кодами IATA и ICAO, альянсом по умолчанию
        # fixme Потом подправить Альанс авиакомпании
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
            self.seek_AL_odbc.execute(SQLQuery)
            if iata is None:
                print(" ICAO=", str(icao))
                SQLQuery = "INSERT INTO dbo.AirLinesTable (AirLineCodeICAO) VALUES ('" + str(icao) + "') "
            elif icao is None:
                print(" IATA=", str(iata))
                SQLQuery = "INSERT INTO dbo.AirLinesTable (AirLineCodeIATA) VALUES ('" + str(iata) + "') "
            elif iata is None and icao is None:
                print(" IATA=", str(iata), " ICAO=", str(icao))
                SQLQuery = "INSERT INTO dbo.AirLinesTable (AirLineCodeIATA, AirLineCodeICAO) VALUES (NULL, NULL) "
                #print("raise Exception")
                #raise Exception
            else:
                print(" IATA=", str(iata), " ICAO=", str(icao))
                SQLQuery = "INSERT INTO dbo.AirLinesTable (AirLineCodeIATA, AirLineCodeICAO) VALUES ('" + str(iata) + "', '" + str(icao) + "') "
            self.seek_AL_odbc.execute(SQLQuery)  # записываем данные по самолету в БД
            ResultSQL = True
            self.cnxn_AL_odbc.commit()  # фиксируем транзакцию, снимаем блокировку с запрошенных диапазонов
        except Exception:
            ResultSQL = False
            self.cnxn_AL_odbc.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
        return ResultSQL

    def UpdateAirLineByIATAandICAO(self, id, name, alias, iata, icao, callsign, city, country, status, date, description, aliance):
        # Обновляет данные авиакомпании в один запрос - БЫСТРЕЕ, НАДЕЖНЕЕ
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"
            self.seek_AL_odbc.execute(SQLQuery)
            SQLQuery = "UPDATE dbo.AirLinesTable SET AirLine_ID = " + str(id) + ", AirLineName = '" + str(name) + "', AirLineAlias = '" + str(alias)
            SQLQuery += "', AirLineCallSighn = '" + str(callsign)
            SQLQuery += "', AirLineCity = '" + str(city) + "', AirLineCountry = '" + str(country) + "', AirLineStatus = " + str(status)
            SQLQuery += ", CreationDate = '" + str(date) + "', AirLineDescription = '" + str(description) + "', Alliance = " + str(aliance)
            if iata is None:
                print(" ICAO=", str(icao))
                SQLQuery += " WHERE AirLineCodeIATA IS NULL AND AirLineCodeICAO = '" + str(icao) + "' "
            elif icao is None:
                print(" IATA=", str(iata))
                SQLQuery += " WHERE AirLineCodeIATA = '" + str(iata) + "' AND AirLineCodeICAO IS NULL "
            elif iata is None and icao is None:
                print(" IATA=", str(iata), " ICAO=", str(icao))
                SQLQuery += " WHERE AirLineCodeIATA IS NULL AND AirLineCodeICAO IS NULL "
            else:
                print(" IATA=", str(iata), " ICAO=", str(icao))
                SQLQuery += " WHERE AirLineCodeIATA = '" + str(iata) + "' AND AirLineCodeICAO = '" + str(icao) + "' "
            self.seek_AL_odbc.execute(SQLQuery)
            ResultSQL = True
            self.cnxn_AL_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_AL_odbc.rollback()
        return ResultSQL

    class AirCraft:
        def __init__(self):
            pass

    def connect_DB_A_odbc(self, servername, driver, database):
        if self.connect_DB_odbc(servername=servername, driver=driver, database=database):
            self.cnxn_A_odbc = self.cnxn
            self.seek_A_odbc = self.seek
            return True
        else:
            return False

    def connect_DB_A_mssql(self, servername, database):
        if self.connect_DB_mssql(servername=servername, database=database):
            self.cnxn_A_mssql = self.cnxn
            self.seek_A_mssql = self.seek
            return True
        else:
            return False

    def connect_DSN_A_odbc(self, dsn):
        if self.connect_DSN_odbc(dsn=dsn):
            self.cnxn_A_odbc = self.cnxn
            self.seek_A_odbc = self.seek
            return True
        else:
            return False

    def disconnect_A_mssql(self):
        try:
            # Отключаемся от базы данных, курсов закрывается
            self.cnxn_A_mssql.close()
            print(" -- БД mssql отключена")
        except Exception:
            print(" -- БД mssql уже отключена")

    def disconnect_A_odbc(self):
        try:
            # Закрываем курсор
            self.seek_A_odbc.close()
            # Отключаемся от базы данных
            self.cnxn_A_odbc.close()
            print(" -- БД pyodbc отключена")
        except Exception:
            print(" -- БД pyodbc уже отключена")

    def QueryAirCraftByRegistration(self, Registration, use_aircrafts_db):
        # Возвращает строку самолета по его регистрации
        if use_aircrafts_db:
            try:
                SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
                self.seek_A_odbc.execute(SQLQuery)
                SQLQuery = "SELECT * FROM dbo.AirCraftsTableNew2XsdIntermediate WHERE AirCraftRegistration = '" + str(Registration) + "' "
                self.seek_A_odbc.execute(SQLQuery)
                ResultSQL = self.seek_A_odbc.fetchone()  # курсор забирает одну строку и сдвигается на строку вниз
                self.cnxn_A_odbc.commit()
            except Exception:
                ResultSQL = False
                self.cnxn_A_odbc.rollback()
        else:
            try:
                SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
                self.seek_A_odbc.execute(SQLQuery)
                SQLQuery = "SELECT * FROM dbo.AirCraftsTable WHERE AirCraftRegistration = '" + str(Registration) + "' "
                self.seek_A_odbc.execute(SQLQuery)
                ResultSQL = self.seek_A_odbc.fetchone()  # курсор забирает одну строку и сдвигается на строку вниз
                self.cnxn_A_odbc.commit()
            except Exception:
                ResultSQL = False
                self.cnxn_A_odbc.rollback()
        return ResultSQL

    def InsertAirCraftByRegistration(self, Registration, ALPK, useAirCrafts):
        # Вставляет строку самолета по его регистрации
        if useAirCrafts:
            try:
                SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
                self.seek_A_odbc.execute(SQLQuery)
                SQLQuery = "INSERT INTO dbo.AirCraftsTableNew2XsdIntermediate (AirCraftRegistration) VALUES ('" + str(Registration) + "') "
                self.seek_A_odbc.execute(SQLQuery)  # записываем данные по самолету в БД
                # todo Дописать авиакомпанию-оператора в поле AirFlightsByAirLines -> не надо (он в начале FlightNumberString)
                ResultSQL = True
                self.cnxn_A_odbc.commit()  # фиксируем транзакцию, снимаем блокировку с запрошенных диапазонов
            except Exception:
                ResultSQL = False
                self.cnxn_A_odbc.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
        else:
            try:
                SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
                self.seek_A_odbc.execute(SQLQuery)
                if ALPK is None:
                    SQLQuery = "INSERT INTO dbo.AirCraftsTable (AirCraftRegistration) VALUES ('" + str(Registration) + "') "
                else:
                    SQLQuery = "INSERT INTO dbo.AirCraftsTable (AirCraftRegistration, AirCraftAirLine) VALUES ('" + str(Registration) + "', " + str(ALPK) + ") "
                self.seek_A_odbc.execute(SQLQuery)  # записываем данные по самолету в БД
                ResultSQL = True
                self.cnxn_A_odbc.commit()  # фиксируем транзакцию, снимаем блокировку с запрошенных диапазонов
            except Exception:
                ResultSQL = False
                self.cnxn_A_odbc.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
        return ResultSQL

    def UpdateAirCraft(self, Registration, ALPK, useAirCrafts):
        # Обновляет строку самолета с регистрацией (только для табличных данных)
        if useAirCrafts:
            return True
        else:
            try:
                SQLQuery = "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"
                self.seek_A_odbc.execute(SQLQuery)
                SQLQuery = "UPDATE dbo.AirCraftsTable SET AirCraftAirLine = " + str(ALPK) + " WHERE AirCraftRegistration = '" + str(Registration) + "' "
                self.seek_A_odbc.execute(SQLQuery)  # записываем данные по самолету в БД
                ResultSQL = True
                self.cnxn_A_odbc.commit()  # фиксируем транзакцию, снимаем блокировку с запрошенных диапазонов
            except Exception:
                ResultSQL = False
                self.cnxn_A_odbc.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
            return ResultSQL

    class AirPort:
        def __init__(self):
            pass

    def connect_DB_RT_odbc(self, servername, driver, database):
        if self.connect_DB_odbc(servername=servername, driver=driver, database=database):
            self.cnxn_RT_odbc = self.cnxn
            self.seek_RT_odbc = self.seek
            return True
        else:
            return False

    def disconnect_RT_odbc(self):
        try:
            # Закрываем курсор
            self.seek_RT_odbc.close()
            # Отключаемся от базы данных
            self.cnxn_RT_odbc.close()
            print(" -- БД отключена")
        except Exception:
            print(" -- БД уже отключена")

    def QueryAirPortByIATA(self, iata):
        # Возвращает строку аэропорта по коду IATA
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seek_RT_odbc.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirPortsTable WHERE AirPortCodeIATA = '" + str(iata) + "' "
            self.seek_RT_odbc.execute(SQLQuery)
            ResultSQL = self.seek_RT_odbc.fetchone()
            self.cnxn_RT_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_RT_odbc.rollback()
        return ResultSQL

    def QueryAirPortByICAO(self, icao):
        # Возвращает строку аэропорта по коду ICAO
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seek_RT_odbc.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirPortsTable WHERE AirPortCodeICAO = '" + str(icao) + "' "
            self.seek_RT_odbc.execute(SQLQuery)
            ResultSQL = self.seek_RT_odbc.fetchone()
            self.cnxn_RT_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_RT_odbc.rollback()
        return ResultSQL

    def QueryAirPortByIATAandICAO(self, iata, icao):
        # Возвращает строку аэропорта по кодам IATA и ICAO
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seek_RT_odbc.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirPortsTable "
            if iata is None:
                SQLQuery += "WHERE AirPortCodeIATA IS NULL AND AirPortCodeICAO = '" + str(icao) + "' "
            elif icao is None:
                SQLQuery += "WHERE AirPortCodeIATA = '" + str(iata) + "' AND AirPortCodeICAO IS NULL "
            elif iata is None and icao is None:
                SQLQuery += "WHERE AirPortCodeIATA IS NULL AND AirPortCodeICAO IS NULL "
            else:
                SQLQuery += "WHERE AirPortCodeIATA = '" + str(iata) + "' AND AirPortCodeICAO = '" + str(icao) + "' "
            self.seek_RT_odbc.execute(SQLQuery)
            ResultSQL = self.seek_RT_odbc.fetchone()  # выбираем первую строку из возможно нескольких
            self.cnxn_RT_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_RT_odbc.rollback()
        return ResultSQL

    def QueryAirPortByFAA_LID(self, faa_lid):
        # Возвращает строку аэропорта по коду ICAO
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seek_RT_odbc.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirPortsTable WHERE AirPortCodeFAA_LID = '" + str(faa_lid) + "' "
            self.seek_RT_odbc.execute(SQLQuery)
            ResultSQL = self.seek_RT_odbc.fetchone()
            self.cnxn_RT_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_RT_odbc.rollback()
        return ResultSQL

    def QueryAirPortByWMO(self, wmo):
        # Возвращает строку аэропорта по коду ICAO
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seek_RT_odbc.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirPortsTable WHERE AirPortCodeWMO = '" + str(wmo) + "' "
            self.seek_RT_odbc.execute(SQLQuery)
            ResultSQL = self.seek_RT_odbc.fetchone()
            self.cnxn_RT_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_RT_odbc.rollback()
        return ResultSQL

    def QueryAirRoute(self, IATADeparture, IATAArrival):
        # Возвращает строку маршрута по кодам IATA аэропортов
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seek_RT_odbc.execute(SQLQuery)
            SQLQuery = """SELECT dbo.AirRoutesTable.AirRouteUniqueNumber                                 
                       FROM dbo.AirRoutesTable INNER JOIN
                       dbo.AirPortsTable ON dbo.AirRoutesTable.AirPortDeparture = dbo.AirPortsTable.AirPortUniqueNumber INNER JOIN
                       dbo.AirPortsTable AS AirPortsTable_1 ON dbo.AirRoutesTable.AirPortArrival = AirPortsTable_1.AirPortUniqueNumber
                       WHERE (dbo.AirPortsTable.AirPortCodeIATA = '""" + str(IATADeparture) + "') AND (AirPortsTable_1.AirPortCodeIATA = '" + str(IATAArrival) + "') "
            self.seek_RT_odbc.execute(SQLQuery)
            ResultSQL = self.seek_RT_odbc.fetchone()
            self.cnxn_RT_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_RT_odbc.rollback()
        return ResultSQL

    def InsertAirPortByIATA(self, iata):
        # fixme дописать функционал, когда код пустой
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
            self.seek_RT_odbc.execute(SQLQuery)
            SQLQuery = "INSERT INTO dbo.AirPortsTable (AirPortCodeIATA) VALUES ('" + str(iata) + "') "
            self.seek_RT_odbc.execute(SQLQuery)
            ResultSQL = True
            self.cnxn_RT_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_RT_odbc.rollback()
        return ResultSQL

    def InsertAirPortByIATAandICAO(self, iata, icao):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
            self.seek_RT_odbc.execute(SQLQuery)
            SQLQuery = "INSERT INTO dbo.AirPortsTable (AirPortCodeIATA, AirPortCodeICAO) VALUES ("
            if iata is None:
                SQLQuery += " NULL, '" + str(icao) + "' "
            elif icao is None:
                SQLQuery += " '" + str(iata) + "', NULL "
            elif iata is None and icao is None:
                SQLQuery += " NULL, NULL "
                #print("raise Exception")
                #raise Exception
            else:
                SQLQuery += " '" + str(iata) + "', '" + str(icao) + "' "
            SQLQuery += ") "
            self.seek_RT_odbc.execute(SQLQuery)
            ResultSQL = True
            self.cnxn_RT_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_RT_odbc.rollback()
        return ResultSQL

    def InsertAirRoute(self, IATADeparture, IATAArrival):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
            self.seek_RT_odbc.execute(SQLQuery)
            SQLQuery = "INSERT INTO dbo.AirRoutesTable (AirPortDeparture, AirPortArrival) VALUES ("
            SQLQuery += str(IATADeparture) + ", "  # bigint
            SQLQuery += str(IATAArrival) + ") "  # bigint
            self.seek_RT_odbc.execute(SQLQuery)
            ResultSQL = True
            self.cnxn_RT_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_RT_odbc.rollback()
        return ResultSQL

    def UpdateAirPortByIATAandICAO(self, csv, hyperlinkWiki, hyperlinkAirPort, hyperlinkOperator, iata, icao, faa_lid, wmo, name, city, county, country, lat, long, height, desc, facilities, incidents):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"
            self.seek_RT_odbc.execute(SQLQuery)
            SQLQuery = "UPDATE dbo.AirPortsTable SET SourceCSVFile = '" + str(csv) + "', HyperLinkToWikiPedia = '" + str(hyperlinkWiki) + "', HyperLinkToAirPortSite = '" + str(hyperlinkAirPort) + "', HyperLinkToOperatorSite = '" + str(hyperlinkOperator)
            SQLQuery += "', AirPortCodeFAA_LID = '" + str(faa_lid) + "', AirPortCodeWMO = '" + str(wmo) + "', AirPortName = '" + str(name) + "', AirPortCity = '" + str(city)
            SQLQuery += "', AirPortCounty = '" + str(county) + "', AirPortCountry = '" + str(country) + "', AirPortLatitude = " + str(lat)
            SQLQuery += ", AirPortLongitude = " + str(long) + ", HeightAboveSeaLevel = " + str(height)
            SQLQuery += ", AirPortDescription = '" + str(desc) + "', AirPortFacilities = '" + str(facilities) + "', AirPortIncidents = '" + str(incidents) + "' "
            SQLGeoQuery = ' '
            # todo И надо пересчитать длины маршрутов, завязанных на этот аэропорт
            if lat is not None and long is not None:
                SQLGeoQuery = "UPDATE dbo.AirPortsTable SET AirPortGeo = geography::STPointFromText(CONCAT('POINT(', " + str(long) + ", ' ', " + str(lat) + ", ') '), 4326) "
            else:
                SQLQuery = "UPDATE dbo.AirPortsTable SET AirPortGeo = geography::STPointFromText(CONCAT('POINT(', " + str(0) + ", ' ', " + str(0) + ", ') '), 4326) "
            if iata is None:
                Append = " WHERE AirPortCodeIATA IS NULL AND AirPortCodeICAO = '" + str(icao) + "' "
                SQLQuery += Append
                SQLGeoQuery += Append
            elif icao is None:
                Append = " WHERE AirPortCodeIATA = '" + str(iata) + "' AND AirPortCodeICAO IS NULL "
                SQLQuery += Append
                SQLGeoQuery += Append
            elif iata is None and icao is None:
                Append = " WHERE AirPortCodeIATA IS NULL AND AirPortCodeICAO IS NULL "
                SQLQuery += Append
                SQLGeoQuery += Append
                #print("raise Exception")
                #raise Exception
            else:
                Append = " WHERE AirPortCodeIATA = '" + str(iata) + "' AND AirPortCodeICAO = '" + str(icao) + "' "
                SQLQuery += Append
                SQLGeoQuery += Append
            self.seek_RT_odbc.execute(SQLQuery)
            self.seek_RT_odbc.execute(SQLGeoQuery)
            ResultSQL = True
            self.cnxn_RT_odbc.commit()
        except Exception:
            ResultSQL = False
            self.cnxn_RT_odbc.rollback()
        return ResultSQL

    def IncrementLogCountViewedAirPort(self, iata, icao, host, user, dtn):
        try:
            Query = "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"
            self.seek_RT_odbc.execute(Query)
            SQLQuery = "SELECT LogCountViewed FROM dbo.AirPortsTable"
            XMLQuery = "SELECT LogDateAndTimeViewed FROM dbo.AirPortsTable"
            if iata is None:
                Append = " WHERE AirPortCodeIATA IS NULL AND AirPortCodeICAO = '" + str(icao) + "' "
                SQLQuery += Append
                XMLQuery += Append
            elif icao is None:
                Append = " WHERE AirPortCodeIATA = '" + str(iata) + "' AND AirPortCodeICAO IS NULL "
                SQLQuery += Append
                XMLQuery += Append
            elif iata is None and icao is None:
                Append = " WHERE AirPortCodeIATA IS NULL AND AirPortCodeICAO IS NULL "
                SQLQuery += Append
                XMLQuery += Append
            else:
                Append = " WHERE AirPortCodeIATA = '" + str(iata) + "' AND AirPortCodeICAO = '" + str(icao) + "' "
                SQLQuery += Append
                XMLQuery += Append
            self.seek_RT_odbc.execute(SQLQuery)
            ResultSQL = self.seek_RT_odbc.fetchone()  # выбираем первую строку из возможно нескольких
            self.seek_RT_odbc.execute(XMLQuery)
            ResultXML = self.seek_RT_odbc.fetchone()
            Count = 1
            #host = 'WorkCompTest1'
            #user = 'ArtemTest20'
            print(" ResultXML = " + str(ResultXML[0]))
            DateTime = ElementTree.Element('DateTime', From=str(host))
            DateTime.text = str(dtn)
            User = ElementTree.Element('User', Name=str(user))
            User.append(DateTime)
            if ResultXML[0] is None:
                root_tag = ElementTree.Element('Viewed')
                root_tag.append(User)
            else:
                Count += ResultSQL[0]
                root_tag = ElementTree.fromstring(ResultXML[0])  # указатель на XML-ную структуру - Element
                Search = root_tag.findall(".//User")
                print(" Search = " + str(Search))
                added = False
                for node in Search:
                    if node.attrib['Name'] == str(user):
                        node.append(DateTime)
                        added = True
                if not added:
                    root_tag.append(User)
                xQuery = ".//User[@Name='" + str(user) + "'] "
                print(" xQuery = " + str(xQuery))
            print("LogCountViewed = " + str(Count))
            xml_to_String = ElementTree.tostring(root_tag, method='xml').decode(encoding="utf-8")  # XML-ная строка
            SQLQuery = "UPDATE dbo.AirPortsTable SET LogCountViewed = " + str(Count)
            XMLQuery = "UPDATE dbo.AirPortsTable SET LogDateAndTimeViewed = '" + str(xml_to_String) + "' "
            if iata is None:
                Append = " WHERE AirPortCodeIATA IS NULL AND AirPortCodeICAO = '" + str(icao) + "' "
                SQLQuery += Append
                XMLQuery += Append
            elif icao is None:
                Append = " WHERE AirPortCodeIATA = '" + str(iata) + "' AND AirPortCodeICAO IS NULL "
                SQLQuery += Append
                XMLQuery += Append
            elif iata is None and icao is None:
                Append = " WHERE AirPortCodeIATA IS NULL AND AirPortCodeICAO IS NULL "
                SQLQuery += Append
                XMLQuery += Append
            else:
                Append = " WHERE AirPortCodeIATA = '" + str(iata) + "' AND AirPortCodeICAO = '" + str(icao) + "' "
                SQLQuery += Append
                XMLQuery += Append
            self.seek_RT_odbc.execute(SQLQuery)
            self.seek_RT_odbc.execute(XMLQuery)
            self.cnxn_RT_odbc.commit()
            Result = True
        except Exception:
            Result = False
            self.cnxn_RT_odbc.rollback()
        return Result

    def IncrementLogCountChangedAirPort(self, iata, icao, host, user, dtn):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"
            self.seek_RT_odbc.execute(SQLQuery)
            SQLQuery = "SELECT LogCountChanged FROM dbo.AirPortsTable"
            XMLQuery = "SELECT LogDateAndTimeChanged FROM dbo.AirPortsTable"
            if iata is None:
                Append = " WHERE AirPortCodeIATA IS NULL AND AirPortCodeICAO = '" + str(icao) + "' "
                SQLQuery += Append
                XMLQuery += Append
            elif icao is None:
                Append = " WHERE AirPortCodeIATA = '" + str(iata) + "' AND AirPortCodeICAO IS NULL "
                SQLQuery += Append
                XMLQuery += Append
            elif iata is None and icao is None:
                Append = " WHERE AirPortCodeIATA IS NULL AND AirPortCodeICAO IS NULL "
                SQLQuery += Append
                XMLQuery += Append
            else:
                Append = " WHERE AirPortCodeIATA = '" + str(iata) + "' AND AirPortCodeICAO = '" + str(icao) + "' "
                SQLQuery += Append
                XMLQuery += Append
            self.seek_RT_odbc.execute(SQLQuery)
            ResultSQL = self.seek_RT_odbc.fetchone()  # выбираем первую строку из возможно нескольких
            self.seek_RT_odbc.execute(XMLQuery)
            ResultXML = self.seek_RT_odbc.fetchone()
            Count = 1
            DateTime = ElementTree.Element('DateTime', From=str(host))
            DateTime.text = str(dtn)
            User = ElementTree.Element('User', Name=str(user))
            User.append(DateTime)
            if ResultXML[0] is None:
                root_tag = ElementTree.Element('Changed')
                root_tag.append(User)
            else:
                Count += ResultSQL[0]
                root_tag = ElementTree.fromstring(ResultXML[0])
                Search = root_tag.findall(".//User")
                added = False
                for node in Search:
                    if node.attrib['Name'] == str(user):
                        node.append(DateTime)
                        added = True
                if not added:
                    root_tag.append(User)
            print("LogCountChanged = " + str(Count))
            xml_to_String = ElementTree.tostring(root_tag, method='xml').decode(encoding="utf-8")
            print(" xml_to_String = " + str(xml_to_String))
            SQLQuery = "UPDATE dbo.AirPortsTable SET LogCountChanged = " + str(Count)
            XMLQuery = "UPDATE dbo.AirPortsTable SET LogDateAndTimeChanged = '" + str(xml_to_String) + "' "
            if iata is None:
                Append = " WHERE AirPortCodeIATA IS NULL AND AirPortCodeICAO = '" + str(icao) + "' "
                SQLQuery += Append
                XMLQuery += Append
            elif icao is None:
                Append = " WHERE AirPortCodeIATA = '" + str(iata) + "' AND AirPortCodeICAO IS NULL "
                SQLQuery += Append
                XMLQuery += Append
            elif iata is None and icao is None:
                Append = " WHERE AirPortCodeIATA IS NULL AND AirPortCodeICAO IS NULL "
                SQLQuery += Append
                XMLQuery += Append
            else:
                Append = " WHERE AirPortCodeIATA = '" + str(iata) + "' AND AirPortCodeICAO = '" + str(icao) + "' "
                SQLQuery += Append
                XMLQuery += Append
            self.seek_RT_odbc.execute(SQLQuery)
            self.seek_RT_odbc.execute(XMLQuery)
            self.cnxn_RT_odbc.commit()
            Result = True
        except Exception:
            Result = False
            self.cnxn_RT_odbc.rollback()
        return Result

    def ModifyAirFlightTable(self, ac, al, fn, dep, arr, flightdate, begindate, use_aircrafts_db):
        db_air_route = self.QueryAirRoute(dep, arr).AirRouteUniqueNumber
        if db_air_route is not None:
            db_air_craft = self.QueryAirCraftByRegistration(ac, use_aircrafts_db).AirCraftUniqueNumber
            if db_air_craft is not None:
                try:
                    SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
                    self.seek_A_odbc.execute(SQLQuery)
                    SQLQuery = "SELECT * FROM dbo.AirFlightsTable WITH (UPDLOCK) WHERE FlightNumberString = '" + str(al) + str(fn) + "' AND AirRoute = "
                    SQLQuery += str(db_air_route) + " AND AirCraft = " + str(db_air_craft) + " AND FlightDate = '" + str(flightdate) + "' AND BeginDate = '" + str(begindate) + "' "
                    self.seek_A_odbc.execute(SQLQuery)
                    ResultQuery = self.seek_A_odbc.fetchone()
                    if ResultQuery is None:
                        SQLQuery = "INSERT INTO dbo.AirFlightsTable (AirRoute, AirCraft, FlightNumberString, QuantityCounted, FlightDate, BeginDate) VALUES ("
                        SQLQuery += str(db_air_route) + ", "  # bigint
                        SQLQuery += str(db_air_craft) + ", '"  # bigint
                        SQLQuery += str(al) + str(fn) + "', "  # nvarchar(50)
                        SQLQuery += str(1) + ", '" + str(flightdate) + "', '" + str(begindate) + "') "  # bigint
                        self.Result = 1
                    elif ResultQuery is not None:
                        quantity = ResultQuery.QuantityCounted + 1
                        SQLQuery = "UPDATE dbo.AirFlightsTable SET QuantityCounted = " + str(quantity)
                        SQLQuery += " WHERE FlightNumberString = '" + str(al) + str(fn) + "' AND AirRoute = " + str(db_air_route)
                        SQLQuery += " AND AirCraft = " + str(db_air_craft) + " AND FlightDate = '" + str(flightdate) + "' AND BeginDate = '" + str(begindate) + "' "
                        self.Result = 2
                    else:
                        pass
                    self.seek_A_odbc.execute(SQLQuery)
                    self.cnxn_A_odbc.commit()
                except Exception:
                    self.cnxn_A_odbc.rollback()
                    self.Result = 0
                finally:
                    pass
            elif db_air_craft is None:
                self.Result = 0
            else:
                self.Result = 0
        elif db_air_route is None:
            self.Result = 0
        else:
            self.Result = 0
        # Коды возврата: 0 - несработка, 1 - вставили, 2 - сплюсовали
        return self.Result

    def ModifyAirFlightXML(self, ac, al, fn, dep, arr, flightdate, begindate, use_aircrafts_db, use_sax, use_ms_sql, use_markers, use_sql_server_driver_format):
        db_air_route = self.QueryAirRoute(dep, arr).AirRouteUniqueNumber
        if db_air_route is not None:
            db_air_craft = self.QueryAirCraftByRegistration(ac, use_aircrafts_db).AirCraftUniqueNumber
            if db_air_craft is not None:
                if use_sax:
                    # Парсим XML-ное поле как SAX: используем функционал XML-ного поля, использует XML-ные индексы todo см. статью https://learn.microsoft.com/ru-ru/sql/relational-databases/xml/xml-indexes-sql-server?view=sql-server-ver16
                    try:
                        SP = 'SPFlightInsertOrUpdate'
                        SPTest = 'SPFlightTest'
                        parameters = (str(ac), str(al) + str(fn), db_air_route, str(flightdate), str(begindate), )
                        print("\n parameters = " + str(parameters))
                        if use_ms_sql:
                            # fixme см. статью https://kontext.tech/article/893/call-sql-server-procedure-in-python
                            #  https://github.com/tds-fdw/tds_fdw/issues/262
                            #  https://github.com/mkleehammer/pyodbc/issues/184
                            self.seek_A_mssql.callproc(SP, parameters=parameters)
                            Data = self.seek_A_mssql.fetchall()  # fetchval() - pyodbc convenience method similar to cursor.fetchone()[0]
                            self.cnxn_A_mssql.commit()
                        else:
                            # todo --> Пробуем DSN-ы с разными драйверами
                            #  - Native Client,
                            #  - SQL Server,
                            #  - ODBC 11-ый,
                            #  - ODBC 13-ый,
                            #  - ODBC 17-ый (самый надежный и быстрый),
                            #  - ODBC 18-ый
                            #  и напрямую через драйвер SQL Server-а -> работает нормально
                            # fixme см. статью https://stackoverflow.com/questions/28635671/using-sql-server-stored-procedures-from-python-pyodbc
                            #  https://code.google.com/archive/p/pyodbc/wikis/Cursor.wiki
                            if use_markers:
                                # fixme см. статью https://stackoverflow.com/questions/34228152/python-execute-stored-procedure-with-parameters
                                #  https://www.sqlservercentral.com/articles/sql-server-and-python-tutorial
                                #  https://github.com/mkleehammer/pyodbc/wiki/Calling-Stored-Procedures
                                if use_sql_server_driver_format:
                                    # SQL Server Driver format with markers
                                    SQLQuery = "DECLARE @return_status INT = 5 \n"
                                    #SQLQuery += "EXECUTE @return_status = dbo." + SPTest + " ?, ?, ?, ?, ? \n"
                                    SQLQuery += "EXECUTE @return_status = dbo." + SP + " ?, ?, ?, ?, ? \n"
                                    SQLQuery += "SELECT @return_status AS 'return_status' "
                                else:
                                    # ODBC Driver format with markers
                                    #SQLQuery = "{CALL dbo." + SPTest + " (?, ?, ?, ?, ?)} "
                                    SQLQuery = "{CALL dbo." + SP + " (?, ?, ?, ?, ?)} "
                                print(" SQLQuery: \n ----\n" + str(SQLQuery))
                                self.seek_A_odbc.fast_executemany = True
                                self.seek_A_odbc.execute(SQLQuery, parameters)
                            else:
                                if use_sql_server_driver_format:
                                    # SQL Server Driver format
                                    SQLQuery = "DECLARE @return_status INT = 5 \n"
                                    #SQLQuery += "EXECUTE @return_status = dbo." + SPTest + " '" + str(ac) + "', '" + str(al) + str(fn) + "Test', " + str(db_air_route) + ", '" + str(flightdate) + "', '" + str(begindate) + "' \n"
                                    SQLQuery += "EXECUTE @return_status = dbo." + SP + " '" + str(ac) + "', '" + str(al) + str(fn) + "', " + str(db_air_route) + ", '" + str(flightdate) + "', '" + str(begindate) + "' \n"
                                    SQLQuery += "SELECT @return_status AS 'return_status' "
                                else:
                                    # ODBC Driver format
                                    #SQLQuery = "{CALL dbo." + SPTest + " ('" + str(ac) + "', '" + str(al) + str(fn) + "', " + str(db_air_route) + ", '" + str(flightdate) + "', '" + str(begindate) + "')} "
                                    SQLQuery = "{CALL dbo." + SP + " ('" + str(ac) + "', '" + str(al) + str(fn) + "', " + str(db_air_route) + ", '" + str(flightdate) + "', '" + str(begindate) + "')} "
                                print(" SQLQuery: \n ----\n" + str(SQLQuery))
                                #self.seek_AC_odbc.fast_executemany = True
                                self.seek_A_odbc.execute(SQLQuery)
                            # todo см. статью https://learn.microsoft.com/en-us/sql/relational-databases/stored-procedures/return-data-from-a-stored-procedure?view=sql-server-ver16
                            #  https://github.com/mkleehammer/pyodbc/wiki/Tips-and-Tricks-by-Database-Platform#passing-row-oriented-parameter-data-as-a-json-string
                            Data = self.seek_A_odbc.fetchall()  # fetchval() - pyodbc convenience method similar to cursor.fetchone()[0]
                            self.cnxn_A_odbc.commit()
                        if Data:
                            print(" Data = " + str(Data))
                            self.Result = Data[0][5]
                            print(" Результат хранимой процедуры = " + str(self.Result))
                        else:
                            self.Result = 0
                    except Exception as exception:
                        print(" exception = " + str(exception))
                        if use_ms_sql:
                            self.cnxn_A_mssql.rollback()
                        else:
                            self.cnxn_A_odbc.rollback()
                        self.Result = 0
                else:
                    # Парсим XML-ное поле как DOM
                    # fixme при полной модели восстановления БД на первых 5-ти загрузках файл журнала стал в 1000 раз больше файла данных -> сделал простую
                    try:
                        SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
                        self.seek_A_odbc.execute(SQLQuery)
                        XMLQuery = "SELECT FlightsByRoutes FROM dbo.AirCraftsTableNew2XsdIntermediate WITH (UPDLOCK) WHERE AirCraftRegistration = '" + str(ac) + "' "
                        self.seek_A_odbc.execute(XMLQuery)
                        ResultXML = self.seek_A_odbc.fetchone()
                        QuantityCounted = 1  # количество таких авиаперелетов за этот день
                        QuantityOnThisRoute = 1  # количестов авиаперелетов этого авиарейса по этому маршруту
                        QuantityOnThisFlight = 1  # количество авиаперелетов этого авиарейса
                        QuantityTotal = 1  # количество авиапрелетов с этой регистрацией
                        step = ElementTree.Element('step', FlightDate=str(flightdate), BeginDate=str(begindate))
                        Route = ElementTree.Element('Route', RouteFK=str(db_air_route))
                        Flight = ElementTree.Element('Flight', FlightNumberString=str(al) + str(fn))
                        root_tag_FlightsByRoutes = ElementTree.Element('FlightsByRoutes')
                        paddedStep = False
                        addedStep = False
                        addedRoute = False
                        addedFlight = False
                        if ResultXML[0] is None:
                            step.text = str(QuantityCounted)
                            Route.append(step)
                            #Flight.text = str(1)
                            Flight.append(Route)
                            #root_tag_FlightsByRoutes.text = str(1)
                            root_tag_FlightsByRoutes.append(Flight)
                            #Route.text = str(QuantityOnThisRoute)  # fixme в SSMS с этого места выводит в одну строчку (строка всегда в одну строчку)
                            addedStep = True
                            addedRoute = True
                            addedFlight = True
                            self.Result = 3
                        else:
                            root_tag_FlightsByRoutes = ElementTree.fromstring(ResultXML[0])
                            SearchFlight = root_tag_FlightsByRoutes.findall(".//Flight")
                            # fixme в БД наблюдаются дубликаты FlightNumberString, Route, step (цикл for ... break else ... работает не так, как ожидалось) -> добавил флаги added... , заменил else на if not added...
                            for nodeFlight in SearchFlight:
                                if nodeFlight.attrib['FlightNumberString'] == str(al) + str(fn):
                                    SearchRoute = nodeFlight.findall(".//Route")
                                    for nodeRoute in SearchRoute:
                                        if nodeRoute.attrib['RouteFK'] == str(db_air_route):
                                            SearchStep = nodeRoute.findall(".//step")
                                            for nodeStep in SearchStep:
                                                if nodeStep.attrib['FlightDate'] == str(flightdate) and not paddedStep:
                                                    QuantityCounted = int(nodeStep.text) + 1
                                                    nodeStep.text = str(QuantityCounted)
                                                    paddedStep = True
                                                    self.Result = 2
                                            if not paddedStep:
                                                step.text = str(QuantityCounted)
                                                nodeRoute.append(step)
                                                addedStep = True
                                                self.Result = 1
                                    if not paddedStep and not addedStep:
                                        step.text = str(QuantityCounted)
                                        Route.append(step)
                                        nodeFlight.append(Route)
                                        addedRoute = True
                                        self.Result = 1
                            if not paddedStep and not addedStep and not addedRoute:
                                step.text = str(QuantityCounted)
                                Route.append(step)
                                Flight.append(Route)
                                root_tag_FlightsByRoutes.append(Flight)
                                addedFlight = True
                                self.Result = 1
                        xml_FlightsByRoutes_to_String = ElementTree.tostring(root_tag_FlightsByRoutes, method='xml').decode(encoding="utf-8")  # XML-ная строка
                        XMLQuery = "UPDATE dbo.AirCraftsTableNew2XsdIntermediate SET FlightsByRoutes = '" + str(xml_FlightsByRoutes_to_String) + "' WHERE AirCraftRegistration = '" + str(ac) + "' "
                        self.seek_A_odbc.execute(XMLQuery)
                        self.cnxn_A_odbc.commit()
                    except Exception as exception:
                        print(" exception = " + str(exception))
                        self.cnxn_A_odbc.rollback()
                        self.Result = 0
            elif db_air_craft is None:
                self.Result = 0
            else:
                self.Result = 0
        elif db_air_route is None:
            self.Result = 0
        else:
            self.Result = 0
        # Коды возврата: 0 - несработка, 1 - вставили, 2 - сплюсовали, 3 - первая запись в еще пустую ячейку
        return self.Result

    def checkConnection(self):
        #if self.cnxn_AL_odbc.is_connected() and (self.cnxn_AC_odbc.is_connected() or self.cnxn_ACFN_odbc.is_connected()) and self.cnxn_RT_odbc.is_connected():  # mysql
        if self.cnxn_AL_odbc and self.cnxn_A_odbc and self.cnxn_RT_odbc:
            return True
        else:
            return False
