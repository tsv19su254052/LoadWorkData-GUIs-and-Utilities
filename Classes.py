#  Interpreter 3.7 -> 3.10


from PyQt5 import QtWidgets, QtCore, QtGui  # оставили 5-ую версию, потому что много наработок еще завязаны на нее
# todo ветка библиотек Qt - QtCore, QtGui, QtNetwork, QtOpenGL, QtScript, QtSQL (медленнее чем pyodbc), QtDesigner, QtXml
# Руководство по установке см. https://packaging.python.org/tutorials/installing-packages/

# Пользовательская библиотека с классами
# Задача создания пользовательских структур данных не расматривается -> Только функционал
# Компилируется и кладется в папку __pycache__
# Идея выноса каждого класса в этот отдельный файл, как на Java -> Удобство просмотра типов данных, не особо практично
# Qt Designer (см. https://build-system.fman.io/qt-designer-download)
# Запуск Qt Designer из библиотеки pyQt5_tools (3.10 и более ранние) командой в терминале
# > pyqt5-tools designer
# или из библиотеки pyQt6_tools (3.11) командой в терминале
# > pyqt6-tools designer
# todo Вероятно придется много переделать, чтобы не вызывать по 2 раза. Не работает с XML-ными полями см. https://docs.sqlalchemy.org/en/20/dialects/mssql.html#sqlalchemy.dialects.mssql.XML
from sqlalchemy import create_engine



# Делаем предка
class AirLine:
    # fixme правильно писать конструктор
    # todo Объявления внутри класса с конструктором и без
    # todo Пакет библиотек с __init.py__ и без
    def __init__(self):
        self.AirLine_ID = 1
        self.AirLineName = " "
        self.AirLineAlias = " "
        self.AirLineCodeIATA = " "
        self.AirLineCodeICAO = " "
        self.AirLineCallSighn = " "
        self.AirLineCity = " "
        self.AirLineCountry = " "
        self.AirLineStatus = 1
        self.CreationDate = '1920-01-01'
        self.AirLineDescription = " "
        self.Alliance = 4
        self.Position = 1  # Позиция курсора в таблице (в SQL начинается с 1)


# Делаем предка
class AirCraft:
    # fixme правильно писать конструктор
    def __init__(self):
        self.AirCraftModel = 387  # Unknown Model
        self.BuildDate = '1920-01-01'
        self.RetireDate = '1920-01-01'
        self.SourceCSVFile = " "
        self.AirCraftDescription = " "
        self.AirCraftLineNumber_LN = " "
        self.AirCraftLineNumber_MSN = " "
        self.AirCraftSerialNumber_SN = " "
        self.AirCraftCNumber = " "
        self.EndDate = '1920-01-01'
        self.Position = 1  # Позиция курсора в таблице (в SQL начинается с 1)


# Делаем предка
class AirPort:
    # fixme правильно писать конструктор
    def __init__(self):
        self.AirPortCodeIATA = " "
        self.AirPortCodeICAO = " "
        self.AirPortName = " "
        self.AirPortCity = " "
        self.AirPortCounty = " "
        self.AirPortCountry = " "
        self.AirPortLatitude = 0
        self.AirPortLongitude = 0
        self.HeightAboveSeaLevel = 0
        self.SourceCSVFile = " "
        self.AirPortDescription = " "
        self.AirPortFacilities = " "
        self.AirPortIncidents = " "
        self.Position = 1  # Позиция курсора в таблице (в SQL начинается с 1)


# Делаем предка
class Servers:
    # fixme Написать конструктор правильно
    def __init__(self):
        pass
        # Получаем список DSN-ов - тут выдает ошибки, лучше делать в экземпляре
        # Server.DSNs = pyodbc.dataSources()  # добавленные DSN-ы
        # Получаем список драйверов баз данных
        # Server.DriversODBC = pyodbc.drivers()

    """
    Библиотеки Python для ввода-вывода в файл:
     - Pandas (анализ данных, лучше чем NumPy),
     - math (математические функции),
     - SciPy (математика),
     - SymPy,
     - MatPlotLib (графики на плоскости),
     - Pickle (пишут, что ненадежен -> лучше json),
     - dbm,
     - shelve (чтение и запись в файл),
     - sys (система),
     - os (операционная система),
     - time, datetime (дата и время)

    Обмен данными между программами:
     - двоичный файл типа *.dat,
     - текстовый файл типа *.txt,
     - файл с разделителями и переводом строки типа *.csv,
     - файл с тэгами и иерархией типа *.xml (xml.dom, xml.sax) или *.html (XML-RPC, WDDX, WSDL),
        XQuery для информационно-ориентированного XML
        XSLT для документно-ориентированного XML (может переводить XML в формат представления HTML или PDF)
        Схемы:
         - схема XDR с заметками (устаревшая до SQLXML 4.0)
         - схема XSD (полнее, чем XDR) с заметками,  файл типа *.xsd
         - типы данных и операторы XPath & XQuery,
         - типы данных XDR,
         - типы данных XSD
     - файл кодера-декодера исходный текст типа *.json,
     - файл типа *.yaml
     - файл MsgPack, Protocol Buffers, Avro, Thrift
     - с помощью модуля pickle,
     - научный формат HDF5,
     - БД с помощью DB-API (функционал - connect, cursor, execute, fetch) нет своего функционала для прямой работы с таблицами SQL Server-а
     (для выборки вызываем скрипт на SQL или хранимую процедуру с параметрами на входе),
     - файл формата dbm (словарь),
     - python-memcached,
     - сервер структурных данных Redis,

    Выборка и все остальное - READ COMMITTED (Чтение зафиксированных данных - в настройках по умолчанию) инструкции не могут считывать данные,
    которые были изменены и еще не зафиксированы другими транзакциями.
    Другие транзакции могут изменять и вставлять данные, читаемые текущей транзакцией.
    
    Обновление - REPEATABLE READ (Повторяемость чтения) - Другие транзакции могут только вставлять данные, читаемые текущей транзакцией
    
    Вставка - SERIALIZABLE (Упорядочиваемость) - Другие транзакции не могут изменять и вставлять данные в диапазон, читаемые текущей транзакцией

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

    ----
    Уровень изоляции транзакций по умолчанию в SQL Server — READ COMMITTED.
     Если база данных не настроена на поддержку изоляции SNAPSHOT по умолчанию,
     операция записи внутри транзакции в режиме изоляции READ COMMITTED устанавливает блокировки на уровне транзакции для обновленных строк.
     В условиях высокой параллельности МОГУТ ПРОИЗОЙТИ БЛОКИРОВКИ, если несколько процессов генерируют конфликтующие блокировки.
     Если эти процессы используют долгоживущие транзакции, генерирующие большое количество таких блокировок, вероятность возникновения взаимоблокировки возрастает.
    
     Установка autocommit=True позволит избежать взаимоблокировок, поскольку каждый отдельный оператор SQL будет автоматически зафиксирован.
     тем самым завершая транзакцию (которая автоматически запускалась, когда этот оператор начал выполняться) и снимая все блокировки обновленных строк.
    """
    # fixme Возможно надо возвращать из функций сработку (OPC-server) и результат (SQL Server) отдельно
    # todo Функции запроса при пустом ответе возвращают (None,) или None, при несработке - False
    # todo Функции обновления и вставки при сработке возвращают True, при несработке - False
    def QueryAirLineByIATA(self, iata):
        # Возвращает строку авиакомпании по ее коду IATA
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seekAL.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineCodeIATA = '" + str(iata) + "' "
            self.seekAL.execute(SQLQuery)
            ResultSQL = self.seekAL.fetchone()
            self.cnxnAL.commit()
        except Exception:
            ResultSQL = False
            self.cnxnAL.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def QueryAirLineByIATA_SQLAlchemy(self, iata):
        # todo В процессе разработки
        pass

    def QueryAirLineByICAO(self, icao):
        # Возвращает строку авиакомпании по ее коду ICAO
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seekAL.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineCodeICAO = '" + str(icao) + "' "
            self.seekAL.execute(SQLQuery)
            ResultSQL = self.seekAL.fetchone()
            self.cnxnAL.commit()
        except Exception:
            ResultSQL = False
            self.cnxnAL.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def QueryAirLineByICAO_SQLAlchemy(self, icao):
        # todo В процессе разработки
        pass

    def QueryAirLineByIATAandICAO(self, iata, icao):
        # Возвращает строку авиакомпании по ее кодам IATA и ICAO
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seekAL.execute(SQLQuery)
            if iata is None:
                SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineCodeIATA IS NULL AND AirLineCodeICAO = '" + str(icao) + "' "
            elif icao is None:
                SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineCodeIATA = '" + str(iata) + "' AND AirLineCodeICAO IS NULL "
            elif iata is None and icao is None:
                SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineCodeIATA IS NULL AND AirLineCodeICAO IS NULL "
            else:
                SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineCodeIATA = '" + str(iata) + "' AND AirLineCodeICAO = '" + str(icao) + "' "
            self.seekAL.execute(SQLQuery)
            ResultSQL = self.seekAL.fetchone()
            self.cnxnAL.commit()
        except Exception:
            ResultSQL = False
            self.cnxnAL.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def QueryAirLineByIATAandICAO_SQLAlchemy(self, iata, icao):
        # todo В процессе разработки
        pass

    def QueryAirLineByPK(self, pk):
        # Возвращает строку авиакомпании по первичному ключу
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seekAL.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirLinesTable WHERE AirLineUniqueNumber = '" + str(pk) + "' "
            self.seekAL.execute(SQLQuery)
            ResultSQL = self.seekAL.fetchone()
            self.cnxnAL.commit()
        except Exception:
            ResultSQL = False
            self.cnxnAL.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def QueryAirLineByPK_SQLAlchemy(self, pk):
        pass

    def QueryAlliances(self):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seekAL.execute(SQLQuery)
            SQLQuery = "SELECT AllianceUniqueNumber, AllianceName FROM dbo.AlliancesTable"  # Убрал  ORDER BY AlianceName
            self.seekAL.execute(SQLQuery)
            ResultSQL = self.seekAL.fetchall()
            self.cnxnAL.commit()
        except Exception:
            ResultSQL = False
            self.cnxnAL.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def QueryAlliances_SQLAlchemy(self):
        # todo В процессе разработки
        pass

    def QueryAlliancePKByName(self, name):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seekAL.execute(SQLQuery)
            SQLQuery = "SELECT AllianceUniqueNumber FROM dbo.AlliancesTable WHERE AllianceName='" + str(name) + "' "  # Убрал  ORDER BY AlianceName
            self.seekAL.execute(SQLQuery)
            ResultSQL = self.seekAL.fetchone()
            self.cnxnAL.commit()
        except Exception:
            ResultSQL = False
            self.cnxnAL.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def QueryAlliancePKByName_SQLAlchemy(self, name):
        # todo В процессе разработки
        pass

    def UpdateAirLineByIATAandICAO(self, id, name, alias, iata, icao, callsign, city, country, status, date, description, aliance):
        # Обновляет данные авиакомпании в один запрос - БЫСТРЕЕ, НАДЕЖНЕЕ
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"
            self.seekAL.execute(SQLQuery)
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
                #print("raise Exception")
                #raise Exception
            else:
                print(" IATA=", str(iata), " ICAO=", str(icao))
                SQLQuery += " WHERE AirLineCodeIATA = '" + str(iata) + "' AND AirLineCodeICAO = '" + str(icao) + "' "
            self.seekAL.execute(SQLQuery)
            ResultSQL = True
            self.cnxnAL.commit()
        except Exception:
            ResultSQL = False
            self.cnxnAL.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def UpdateAirLineByIATAandICAO_SQLAlchemy(self, id, name, alias, iata, icao, callsign, city, country, status, date, description, aliance):
        # todo В процессе разработки
        pass

    def InsertAirLineByIATAandICAO(self, iata, icao):
        # Вставляем авиакомпанию с кодами IATA и ICAO, альянсом по умолчанию
        # fixme Потом подправить Альанс авиакомпании
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
            self.seekAL.execute(SQLQuery)
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
            self.seekAL.execute(SQLQuery)  # записываем данные по самолету в БД
            ResultSQL = True
            self.cnxnAL.commit()  # фиксируем транзакцию, снимаем блокировку с запрошенных диапазонов
        except Exception:
            ResultSQL = False
            self.cnxnAL.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
        else:
            pass
        finally:
            return ResultSQL

    def InsertAirLineByIATAandICAO_SQLAlchemy(self, iata, icao):
        # todo В процессе разработки
        pass

    def QueryAirCraftManufacturers(self):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seekAC.execute(SQLQuery)
            SQLQuery = "SELECT Name FROM dbo.AirCraftManufacturersTable"
            self.seekAC.execute(SQLQuery)
            ResultSQL = self.seekAC.fetchall()
            self.cnxnAC.commit()
        except Exception:
            ResultSQL = False
            self.cnxnAC.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def QueryAirCraftManufacturers_SQLAlchemy(self):
        # todo В процессе разработки
        pass

    def QueryManufacturerNumberByModelNumber(self, model_number):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seekAC.execute(SQLQuery)
            SQLQuery = "SELECT Manufacturer FROM dbo.AirCraftModelsTable WHERE AirCraftModelUniqueNumber =" + str(model_number) + " "
            self.seekAC.execute(SQLQuery)
            ResultSQL = self.seekAC.fetchone()
            self.cnxnAC.commit()
        except Exception:
            ResultSQL = False
            self.cnxnAC.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def QueryManufacturerNumberByModelNumber_SQLAlchemy(self, model_number):
        # todo В процессе разработки
        pass

    def QueryAirCraftModels(self):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seekAC.execute(SQLQuery)
            SQLQuery = "SELECT ModelName FROM dbo.AirCraftModelsTable"
            self.seekAC.execute(SQLQuery)
            ResultSQL = self.seekAC.fetchall()
            self.cnxnAC.commit()
        except Exception:
            ResultSQL = False
            self.cnxnAC.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def QueryAirCraftModels_SQLAlchemy(self):
        # todo В процессе разработки
        pass

    def QueryAirCraftByRegistration(self, Registration):
        # Возвращает строку самолета по его регистрации
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seekAC.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirCraftsTable WHERE AirCraftRegistration = '" + str(Registration) + "' "
            self.seekAC.execute(SQLQuery)
            ResultSQL = self.seekAC.fetchone()  # курсор забирает одну строку и сдвигается на строку вниз
            self.cnxnAC.commit()
        except Exception:
            ResultSQL = False
            self.cnxnAC.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def QueryAirCraftByRegistration_SQLAlchemy(self, Registration):
        # todo В процессе разработки
        pass

    def QueryAirCraftByLN(self, ln):
        # Возвращает строку самолета по его LN
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seekAC.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirCraftsTable WHERE AirCraftLineNumber_LN = '" + str(ln) + "' "
            self.seekAC.execute(SQLQuery)
            ResultSQL = self.seekAC.fetchone()  # курсор забирает одну строку и сдвигается на строку вниз
            self.cnxnAC.commit()
        except Exception:
            ResultSQL = False
            self.cnxnAC.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def QueryAirCraftByLN_SQLAlchemy(self, ln):
        # todo В процессе разработки
        pass

    def QueryAirCraftByMSN(self, msn):
        # Возвращает строку самолета по его MSN
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seekAC.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirCraftsTable WHERE AirCraftLineNumber_MSN = '" + str(msn) + "' "
            self.seekAC.execute(SQLQuery)
            ResultSQL = self.seekAC.fetchone()  # курсор забирает одну строку и сдвигается на строку вниз
            self.cnxnAC.commit()
        except Exception:
            ResultSQL = False
            self.cnxnAC.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def QueryAirCraftByMSN_SQLAlchemy(self, msn):
        # todo В процессе разработки
        pass

    def QueryAirCraftByPK(self, pk):
        # Возвращает строку самолета по его первичному ключу
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seekAC.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirCraftsTable WHERE AirCraftUniqueNumber = '" + str(pk) + "' "
            self.seekAC.execute(SQLQuery)
            ResultSQL = self.seekAC.fetchone()  # курсор забирает одну строку и сдвигается на строку вниз
            self.cnxnAC.commit()
        except Exception:
            ResultSQL = False
            self.cnxnAC.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def QueryAirCraftByPK_SQLAlchemy(self, pk):
        # todo В процессе разработки
        pass

    def UpdateAirCraft(self, Registration, ALPK):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"
            self.seekAC.execute(SQLQuery)
            SQLQuery = "UPDATE dbo.AirCraftsTable SET AirCraftAirLine = " + str(ALPK) + " WHERE AirCraftRegistration = '" + str(Registration) + "' "
            self.seekAC.execute(SQLQuery)  # записываем данные по самолету в БД
            ResultSQL = True
            self.cnxnAC.commit()  # фиксируем транзакцию, снимаем блокировку с запрошенных диапазонов
        except Exception:
            ResultSQL = False
            self.cnxnAC.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
        else:
            pass
        finally:
            return ResultSQL

    def UpdateAirCraftOperator(self, RegistartionXML):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"
            self.seekAC.execute(SQLQuery)
            ResultSQL = True
            self.cnxnAC.commit()  # фиксируем транзакцию, снимаем блокировку с запрошенных диапазонов
        except Exception:
            ResultSQL = False
            self.cnxnAC.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
        else:
            pass
        finally:
            return ResultSQL
        pass

    def UpdateAirCraft_SQLAlchemy(self, Registration, ALPK):
        # todo В процессе разработки
        pass

    def InsertAirCraftByRegistration(self, Registration, ALPK):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
            self.seekAC.execute(SQLQuery)
            if ALPK is None:
                SQLQuery = "INSERT INTO dbo.AirCraftsTable (AirCraftRegistration) VALUES ('"
                SQLQuery += str(Registration) + "') "  # nvarchar(50)
            else:
                SQLQuery = "INSERT INTO dbo.AirCraftsTable (AirCraftRegistration, AirCraftAirLine) VALUES ('"
                SQLQuery += str(Registration) + "', "  # nvarchar(50)
                SQLQuery += str(ALPK) + ") "  # bigint
            self.seekAC.execute(SQLQuery)  # записываем данные по самолету в БД
            ResultSQL = True
            self.cnxnAC.commit()  # фиксируем транзакцию, снимаем блокировку с запрошенных диапазонов
        except Exception:
            ResultSQL = False
            self.cnxnAC.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
        else:
            pass
        finally:
            return ResultSQL

    def InsertAirCraftByRegistration_SQLAlchemy(self, Registration, ALPK):
        # todo В процессе разработки
        pass

    def InsertAirCraftByMSN(self, msn):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
            self.seekAC.execute(SQLQuery)
            SQLQuery = "INSERT INTO dbo.AirCraftsTable (AirCraftLineNumber_MSN) VALUES ('" + str(msn) + "') "  # nvarchar(50)
            self.seekAC.execute(SQLQuery)  # записываем данные по самолету в БД
            ResultSQL = True
            self.cnxnAC.commit()  # фиксируем транзакцию, снимаем блокировку с запрошенных диапазонов
        except Exception:
            ResultSQL = False
            self.cnxnAC.rollback()  # откатываем транзакцию, снимаем блокировку с запрошенных диапазонов
        else:
            pass
        finally:
            return ResultSQL

    def InsertAirCraftByMSN_SQLAlchemy(self, msn):
        # todo В процессе разработки
        pass

    def QueryAirPortByIATA(self, iata):
        # Возвращает строку аэропорта по коду IATA
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seekRT.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirPortsTable WHERE AirPortCodeIATA = '" + str(iata) + "' "
            self.seekRT.execute(SQLQuery)
            ResultSQL = self.seekRT.fetchone()
            self.cnxnRT.commit()
        except Exception:
            ResultSQL = False
            self.cnxnRT.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def QueryAirPortByIATA_SQLAlchemy(self, iata):
        # todo В процессе разработки
        pass

    def QueryAirPortByICAO(self, icao):
        # Возвращает строку аэропорта по коду ICAO
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seekRT.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirPortsTable WHERE AirPortCodeICAO = '" + str(icao) + "' "
            self.seekRT.execute(SQLQuery)
            ResultSQL = self.seekRT.fetchone()
            self.cnxnRT.commit()
        except Exception:
            ResultSQL = False
            self.cnxnRT.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def QueryAirPortByICAO_SQLAlchemy(self, icao):
        # todo В процессе разработки
        pass

    def QueryAirPortByPK(self, pk):
        # Возвращает строку аэропорта по первичному ключу
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seekRT.execute(SQLQuery)
            SQLQuery = "SELECT * FROM dbo.AirPortsTable WHERE dbo.AirPortsTable.AirPortUniqueNumber=" + str(pk)  # можно убрать лишнее
            self.seekRT.execute(SQLQuery)
            ResultSQL = self.seekRT.fetchone()
            self.cnxnRT.commit()
        except Exception:
            ResultSQL = False
            self.cnxnRT.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def QueryAirPortByPK_SQLAlchemy(self, pk):
        # todo В процессе разработки
        pass

    def UpdateAirPort(self, iata, icao, name, city, county, country, lat, long, height, csv, desc, facilities, incidents):
        # Обновляет данные аэропорта по его коду IATA в один запрос - БЫСТРЕЕ, НАДЕЖНЕЕ
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ"
            self.seekRT.execute(SQLQuery)
            SQLQuery = "UPDATE dbo.AirPortsTable SET AirPortCodeICAO = '" + str(icao) + "', AirPortName = '" + str(name) + "', AirPortCity = '" + str(city)
            SQLQuery += "', AirPortCounty = '" + str(county) + "', AirPortCountry = '" + str(country) + "', AirPortLatitude = " + str(lat)
            SQLQuery += ", AirPortLongitude = " + str(long) + ", HeightAboveSeaLevel = " + str(height) + ", SourceCSVFile = '" + str(csv)
            SQLQuery += "', AirPortDescription = '" + str(desc) + "', AirPortFacilities = '" + str(facilities) + "', AirPortIncidents = '" + str(incidents) + "' WHERE AirPortCodeIATA = '" + str(iata) + "' "
            self.seekRT.execute(SQLQuery)
            ResultSQL = True
            self.cnxnRT.commit()
        except Exception:
            ResultSQL = False
            self.cnxnRT.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def UpdateAirPort_SQLAlchemy(self, iata, icao, name, city, county, country, lat, long, height, csv, desc, facilities, incidents):
        # todo В процессе разработки
        pass

    def InsertAirPortByIATA(self, iata):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
            self.seekRT.execute(SQLQuery)
            SQLQuery = "INSERT INTO dbo.AirPortsTable (AirPortCodeIATA) VALUES ('" + str(iata) + "') "
            self.seekRT.execute(SQLQuery)
            ResultSQL = True
            self.cnxnRT.commit()
        except Exception:
            ResultSQL = False
            self.cnxnRT.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def InsertAirPortByIATA_SQLAlchemy(self, iata):
        # todo В процессе разработки
        pass

    def QueryAirRoute(self, IATADeparture, IATAArrival):
        # Возвращает строку маршрута по кодам IATA аэропортов
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL READ COMMITTED"
            self.seekRT.execute(SQLQuery)
            SQLQuery = """SELECT dbo.AirRoutesTable.AirRouteUniqueNumber                                 
                       FROM dbo.AirRoutesTable INNER JOIN
                       dbo.AirPortsTable ON dbo.AirRoutesTable.AirPortDeparture = dbo.AirPortsTable.AirPortUniqueNumber INNER JOIN
                       dbo.AirPortsTable AS AirPortsTable_1 ON dbo.AirRoutesTable.AirPortArrival = AirPortsTable_1.AirPortUniqueNumber
                       WHERE (dbo.AirPortsTable.AirPortCodeIATA = '""" + str(IATADeparture) + "') AND (AirPortsTable_1.AirPortCodeIATA = '" + str(IATAArrival) + "') "
            self.seekRT.execute(SQLQuery)
            ResultSQL = self.seekRT.fetchone()
            self.cnxnRT.commit()
        except Exception:
            ResultSQL = False
            self.cnxnRT.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def QueryAirRoute_SQLAlchemy(self, IATADeparture, IATAArrival):
        # todo В процессе разработки
        pass

    def InsertAirRoute(self, IATADeparture, IATAArrival):
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
            self.seekRT.execute(SQLQuery)
            SQLQuery = "INSERT INTO dbo.AirRoutesTable (AirPortDeparture, AirPortArrival) VALUES ("
            SQLQuery += str(IATADeparture) + ", "  # bigint
            SQLQuery += str(IATAArrival) + ") "  # bigint
            self.seekRT.execute(SQLQuery)
            ResultSQL = True
            self.cnxnRT.commit()
        except Exception:
            ResultSQL = False
            self.cnxnRT.rollback()
        else:
            pass
        finally:
            return ResultSQL

    def InsertAirRoute_SQLAlchemy(self, IATADeparture, IATAArrival):
        # todo В процессе разработки
        pass

    def ModifyAirFlight(self, ac, al, fn, dep, arr, flightdate, begindate):
        db_air_route = self.QueryAirRoute(dep, arr).AirRouteUniqueNumber
        if db_air_route is not None:
            db_air_craft = self.QueryAirCraftByRegistration(ac).AirCraftUniqueNumber
            if db_air_craft is not None:
                try:
                    SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
                    self.seekFN.execute(SQLQuery)
                    SQLQuery = "SELECT * FROM dbo.AirFlightsTable WITH (UPDLOCK) WHERE FlightNumberString = '" + str(al) + str(fn) + "' AND AirRoute = "
                    SQLQuery += str(db_air_route) + " AND AirCraft = " + str(db_air_craft) + " AND FlightDate = '" + str(flightdate) + "' AND BeginDate = '" + str(begindate) + "' "
                    self.seekFN.execute(SQLQuery)
                    ResultQuery = self.seekFN.fetchone()
                    if ResultQuery is None:
                        SQLQuery = "INSERT INTO dbo.AirFlightsTable (AirRoute, AirCraft, FlightNumberString, QuantityCounted, FlightDate, BeginDate) VALUES ("
                        SQLQuery += str(db_air_route) + ", "  # bigint
                        SQLQuery += str(db_air_craft) + ", '"  # bigint
                        SQLQuery += str(al) + str(fn) + "', "  # nvarchar(50)
                        SQLQuery += str(1) + ", '" + str(flightdate) + "', '" + str(begindate) + "') "  # bigint
                        ResultSQL = 1  # вставили
                    elif ResultQuery is not None:
                        quantity = ResultQuery.QuantityCounted + 1
                        SQLQuery = "UPDATE dbo.AirFlightsTable SET QuantityCounted = " + str(quantity)
                        SQLQuery += " WHERE FlightNumberString = '" + str(al) + str(fn) + "' AND AirRoute = " + str(db_air_route)
                        SQLQuery += " AND AirCraft = " + str(db_air_craft) + " AND FlightDate = '" + str(flightdate) + "' AND BeginDate = '" + str(begindate) + "' "
                        ResultSQL = 2  # сплюсовали
                    else:
                        pass
                    self.seekFN.execute(SQLQuery)
                    self.cnxnFN.commit()
                except Exception:
                    ResultSQL = 0  # не сработка
                    self.cnxnFN.rollback()
                finally:
                    pass
            elif db_air_craft is None:
                ResultSQL = 0
            else:
                ResultSQL = 0
        elif db_air_route is None:
            ResultSQL = 0
        else:
            ResultSQL = 0
        return ResultSQL

    def ModifyAirFlight_SQLAlchemy(self, ac, al, fn, dep, arr, flightdate, begindate):
        # todo В процессе разработки
        pass

    def QueryCount(self):
        # Возвращает количество строк в таблице аэропортов
        try:
            SQLQuery = "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"
            self.seekRT.execute(SQLQuery)
            SQLQuery = "SELECT COUNT(*) AS COUNT FROM dbo.AirPortsTable"
            self.seekRT.execute(SQLQuery)
            ResultSQL = self.seekRT.fetchone()
            self.cnxnRT.commit()
        except Exception:
            ResultSQL = False
            self.cnxnRT.rollback()
        else:
            pass
        finally:
            return ResultSQL[0]


# Конвертация ресурсного файла *.ui -> *.py в терминале командой (командной строке)
# > pyuic5 Qt_Designer_CorrectDialogAirPort.ui -o Qt_Designer_CorrectDialogAirPort.py
class Ui_DialogCorrectAirPorts(QtWidgets.QDialog):
    def __init__(self):
        # просто сразу вызываем конструктор предка
        super(Ui_DialogCorrectAirPorts, self).__init__()  # конструктор предка
        # а потом остальное
        pass

    # Начало вставки тела конвертированного ресурсного файла
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(740, 810)
        self.label_12 = QtWidgets.QLabel(Dialog)
        self.label_12.setGeometry(QtCore.QRect(20, 220, 91, 16))
        self.label_12.setObjectName("label_12")
        self.lineEdit_DSN = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_DSN.setGeometry(QtCore.QRect(120, 280, 181, 20))
        self.lineEdit_DSN.setObjectName("lineEdit_DSN")
        self.lineEdit_ODBCversion = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_ODBCversion.setGeometry(QtCore.QRect(120, 250, 181, 20))
        self.lineEdit_ODBCversion.setObjectName("lineEdit_ODBCversion")
        self.label_16 = QtWidgets.QLabel(Dialog)
        self.label_16.setGeometry(QtCore.QRect(340, 60, 111, 16))
        self.label_16.setObjectName("label_16")
        self.label_13 = QtWidgets.QLabel(Dialog)
        self.label_13.setGeometry(QtCore.QRect(20, 280, 91, 16))
        self.label_13.setObjectName("label_13")
        self.label_11 = QtWidgets.QLabel(Dialog)
        self.label_11.setGeometry(QtCore.QRect(20, 190, 91, 16))
        self.label_11.setObjectName("label_11")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(11, 20, 171, 151))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("../Example pyQt (Hramushin2 - DevelopServer)/tproger-square-192.png"))
        self.label_4.setObjectName("label_4")
        self.pushButton_SelectDB = QtWidgets.QPushButton(Dialog)
        self.pushButton_SelectDB.setGeometry(QtCore.QRect(400, 110, 181, 23))
        self.pushButton_SelectDB.setObjectName("pushButton_SelectDB")
        self.lineEdit_Driver = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Driver.setGeometry(QtCore.QRect(120, 220, 181, 20))
        self.lineEdit_Driver.setObjectName("lineEdit_Driver")
        self.lineEdit_Schema = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Schema.setGeometry(QtCore.QRect(120, 310, 181, 20))
        self.lineEdit_Schema.setObjectName("lineEdit_Schema")
        self.label_14 = QtWidgets.QLabel(Dialog)
        self.label_14.setGeometry(QtCore.QRect(20, 250, 91, 16))
        self.label_14.setObjectName("label_14")
        self.comboBox_DB = QtWidgets.QComboBox(Dialog)
        self.comboBox_DB.setGeometry(QtCore.QRect(330, 30, 251, 22))
        self.comboBox_DB.setObjectName("comboBox_DB")
        self.comboBox_Driver = QtWidgets.QComboBox(Dialog)
        self.comboBox_Driver.setGeometry(QtCore.QRect(330, 80, 251, 22))
        self.comboBox_Driver.setObjectName("comboBox_Driver")
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(340, 10, 111, 16))
        self.label_8.setObjectName("label_8")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(190, 20, 131, 151))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_15 = QtWidgets.QLabel(Dialog)
        self.label_15.setGeometry(QtCore.QRect(20, 310, 91, 16))
        self.label_15.setObjectName("label_15")
        self.lineEdit_Server = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Server.setGeometry(QtCore.QRect(120, 190, 181, 20))
        self.lineEdit_Server.setObjectName("lineEdit_Server")
        self.pushButton_Disconnect = QtWidgets.QPushButton(Dialog)
        self.pushButton_Disconnect.setGeometry(QtCore.QRect(400, 140, 181, 23))
        self.pushButton_Disconnect.setObjectName("pushButton_Disconnect")
        self.pushButton_Update = QtWidgets.QPushButton(Dialog)
        self.pushButton_Update.setEnabled(True)
        self.pushButton_Update.setGeometry(QtCore.QRect(530, 780, 91, 23))
        self.pushButton_Update.setObjectName("pushButton_Update")
        self.label_17 = QtWidgets.QLabel(Dialog)
        self.label_17.setGeometry(QtCore.QRect(30, 720, 111, 21))
        self.label_17.setObjectName("label_17")
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(140, 780, 221, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.lineEdit_Position = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Position.setGeometry(QtCore.QRect(450, 780, 71, 21))
        self.lineEdit_Position.setObjectName("lineEdit_Position")
        self.lineEdit_HeightAboveSeaLevel = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_HeightAboveSeaLevel.setGeometry(QtCore.QRect(20, 780, 111, 20))
        self.lineEdit_HeightAboveSeaLevel.setObjectName("lineEdit_HeightAboveSeaLevel")
        self.pushButton_Begin = QtWidgets.QPushButton(Dialog)
        self.pushButton_Begin.setGeometry(QtCore.QRect(640, 20, 91, 23))
        self.pushButton_Begin.setObjectName("pushButton_Begin")
        self.lineEdit_AirPortCodeIATA = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_AirPortCodeIATA.setGeometry(QtCore.QRect(20, 350, 113, 20))
        self.lineEdit_AirPortCodeIATA.setObjectName("lineEdit_AirPortCodeIATA")
        self.lineEdit_AirPortLongitude = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_AirPortLongitude.setGeometry(QtCore.QRect(140, 740, 113, 20))
        self.lineEdit_AirPortLongitude.setObjectName("lineEdit_AirPortLongitude")
        self.textEdit_AirPortCity = QtWidgets.QTextEdit(Dialog)
        self.textEdit_AirPortCity.setGeometry(QtCore.QRect(20, 550, 281, 51))
        self.textEdit_AirPortCity.setObjectName("textEdit_AirPortCity")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(30, 660, 181, 16))
        self.label_7.setObjectName("label_7")
        self.textEdit_SourceCSVFile = QtWidgets.QTextEdit(Dialog)
        self.textEdit_SourceCSVFile.setGeometry(QtCore.QRect(310, 190, 271, 61))
        self.textEdit_SourceCSVFile.setObjectName("textEdit_SourceCSVFile")
        self.textEdit_AirPortName = QtWidgets.QTextEdit(Dialog)
        self.textEdit_AirPortName.setGeometry(QtCore.QRect(20, 480, 281, 51))
        self.textEdit_AirPortName.setObjectName("textEdit_AirPortName")
        self.pushButton_SearchByIATA = QtWidgets.QPushButton(Dialog)
        self.pushButton_SearchByIATA.setGeometry(QtCore.QRect(200, 350, 91, 23))
        self.pushButton_SearchByIATA.setObjectName("pushButton_SearchByIATA")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(30, 600, 181, 16))
        self.label_6.setObjectName("label_6")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 460, 111, 16))
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(30, 530, 111, 16))
        self.label_5.setObjectName("label_5")
        self.label_18 = QtWidgets.QLabel(Dialog)
        self.label_18.setGeometry(QtCore.QRect(390, 780, 51, 20))
        self.label_18.setObjectName("label_18")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(140, 380, 47, 13))
        self.label_2.setObjectName("label_2")
        self.lineEdit_AirPortLatitude = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_AirPortLatitude.setGeometry(QtCore.QRect(20, 740, 113, 20))
        self.lineEdit_AirPortLatitude.setObjectName("lineEdit_AirPortLatitude")
        self.label_19 = QtWidgets.QLabel(Dialog)
        self.label_19.setGeometry(QtCore.QRect(150, 720, 111, 21))
        self.label_19.setObjectName("label_19")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(140, 350, 51, 16))
        self.label.setObjectName("label")
        self.lineEdit_AirPortCodeICAO = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_AirPortCodeICAO.setGeometry(QtCore.QRect(20, 380, 113, 20))
        self.lineEdit_AirPortCodeICAO.setObjectName("lineEdit_AirPortCodeICAO")
        self.label_21 = QtWidgets.QLabel(Dialog)
        self.label_21.setGeometry(QtCore.QRect(330, 170, 161, 21))
        self.label_21.setObjectName("label_21")
        self.textEdit_AirPortCounty = QtWidgets.QTextEdit(Dialog)
        self.textEdit_AirPortCounty.setGeometry(QtCore.QRect(20, 620, 281, 41))
        self.textEdit_AirPortCounty.setObjectName("textEdit_AirPortCounty")
        self.pushButton_Next = QtWidgets.QPushButton(Dialog)
        self.pushButton_Next.setGeometry(QtCore.QRect(640, 80, 91, 23))
        self.pushButton_Next.setObjectName("pushButton_Next")
        self.textEdit_AirPortCountry = QtWidgets.QTextEdit(Dialog)
        self.textEdit_AirPortCountry.setGeometry(QtCore.QRect(20, 680, 281, 41))
        self.textEdit_AirPortCountry.setObjectName("textEdit_AirPortCountry")
        self.label_22 = QtWidgets.QLabel(Dialog)
        self.label_22.setGeometry(QtCore.QRect(30, 760, 131, 21))
        self.label_22.setObjectName("label_22")
        self.pushButton_Previous = QtWidgets.QPushButton(Dialog)
        self.pushButton_Previous.setGeometry(QtCore.QRect(640, 50, 91, 23))
        self.pushButton_Previous.setObjectName("pushButton_Previous")
        self.label_23 = QtWidgets.QLabel(Dialog)
        self.label_23.setGeometry(QtCore.QRect(150, 760, 111, 21))
        self.label_23.setObjectName("label_23")
        self.label_24 = QtWidgets.QLabel(Dialog)
        self.label_24.setGeometry(QtCore.QRect(140, 410, 47, 13))
        self.label_24.setObjectName("label_24")
        self.lineEdit_AirPortCodeFAA_LID = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_AirPortCodeFAA_LID.setGeometry(QtCore.QRect(20, 410, 113, 20))
        self.lineEdit_AirPortCodeFAA_LID.setObjectName("lineEdit_AirPortCodeFAA_LID")
        self.pushButton_SearchByICAO = QtWidgets.QPushButton(Dialog)
        self.pushButton_SearchByICAO.setGeometry(QtCore.QRect(200, 380, 91, 23))
        self.pushButton_SearchByICAO.setObjectName("pushButton_SearchByICAO")
        self.pushButton_Insert = QtWidgets.QPushButton(Dialog)
        self.pushButton_Insert.setGeometry(QtCore.QRect(120, 440, 171, 23))
        self.pushButton_Insert.setObjectName("pushButton_Insert")
        self.label_25 = QtWidgets.QLabel(Dialog)
        self.label_25.setGeometry(QtCore.QRect(10, 20, 171, 151))
        self.label_25.setText("")
        self.label_25.setPixmap(QtGui.QPixmap("Значки (Иконки)/tproger-square-192.png"))
        self.label_25.setObjectName("label_25")
        self.label_26 = QtWidgets.QLabel(Dialog)
        self.label_26.setGeometry(QtCore.QRect(590, 20, 41, 41))
        self.label_26.setText("")
        self.label_26.setPixmap(QtGui.QPixmap("Значки (Иконки)/a_25.ico"))
        self.label_26.setObjectName("label_26")
        self.label_27 = QtWidgets.QLabel(Dialog)
        self.label_27.setGeometry(QtCore.QRect(590, 70, 41, 41))
        self.label_27.setText("")
        self.label_27.setPixmap(QtGui.QPixmap("Значки (Иконки)/a_21.ico"))
        self.label_27.setObjectName("label_27")
        self.label_28 = QtWidgets.QLabel(Dialog)
        self.label_28.setGeometry(QtCore.QRect(350, 120, 41, 41))
        self.label_28.setText("")
        self.label_28.setPixmap(QtGui.QPixmap("Значки (Иконки)/a_22.ico"))
        self.label_28.setObjectName("label_28")
        self.label_29 = QtWidgets.QLabel(Dialog)
        self.label_29.setGeometry(QtCore.QRect(590, 120, 131, 141))
        self.label_29.setText("")
        self.label_29.setPixmap(QtGui.QPixmap("Значки (Иконки)/internal_drive_alt_13801.ico"))
        self.label_29.setObjectName("label_29")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(310, 260, 421, 511))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.textEdit_AirPortDescription = QtWidgets.QTextEdit(self.tab_1)
        self.textEdit_AirPortDescription.setGeometry(QtCore.QRect(10, 10, 401, 471))
        self.textEdit_AirPortDescription.setObjectName("textEdit_AirPortDescription")
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.textEdit_AirPortFacilities = QtWidgets.QTextEdit(self.tab_2)
        self.textEdit_AirPortFacilities.setGeometry(QtCore.QRect(10, 10, 401, 471))
        self.textEdit_AirPortFacilities.setObjectName("textEdit_AirPortFacilities")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.textEdit_Incidents = QtWidgets.QTextEdit(self.tab_3)
        self.textEdit_Incidents.setGeometry(QtCore.QRect(10, 10, 401, 471))
        self.textEdit_Incidents.setObjectName("textEdit_Incidents")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.tabWidget.addTab(self.tab_5, "")

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(4)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_12.setText(_translate("Dialog", "Драйвер СУБД"))
        self.label_16.setText(_translate("Dialog", "Драйвер СУБД"))
        self.label_13.setText(_translate("Dialog", "DSN"))
        self.label_11.setText(_translate("Dialog", "Сервер СУБД"))
        self.pushButton_SelectDB.setText(_translate("Dialog", "Подключиться к БД или к DSN"))
        self.label_14.setText(_translate("Dialog", "Версия ODBC"))
        self.label_8.setText(_translate("Dialog", "База данных"))
        self.label_15.setText(_translate("Dialog", "Схема"))
        self.pushButton_Disconnect.setText(_translate("Dialog", "Отключиться от БД или от DSN"))
        self.pushButton_Update.setText(_translate("Dialog", "Записать"))
        self.label_17.setText(_translate("Dialog", "Широта, градусы"))
        self.pushButton_Begin.setText(_translate("Dialog", "Начало"))
        self.label_7.setText(_translate("Dialog", "Страна"))
        self.pushButton_SearchByIATA.setText(_translate("Dialog", "Поиск"))
        self.label_6.setText(_translate("Dialog", "Область, округ, провинция"))
        self.label_3.setText(_translate("Dialog", "Наименование"))
        self.label_5.setText(_translate("Dialog", "Город"))
        self.label_18.setText(_translate("Dialog", "Позиция"))
        self.label_2.setText(_translate("Dialog", "ICAO"))
        self.label_19.setText(_translate("Dialog", "Долгота, градусы"))
        self.label.setText(_translate("Dialog", "IATA"))
        self.label_21.setText(_translate("Dialog", "Источник информации"))
        self.pushButton_Next.setText(_translate("Dialog", "Следующий"))
        self.label_22.setText(_translate("Dialog", "Абс. отм., м"))
        self.pushButton_Previous.setText(_translate("Dialog", "Предыдущий"))
        self.label_23.setText(_translate("Dialog", "Выполнение"))
        self.label_24.setText(_translate("Dialog", "FAA LID"))
        self.pushButton_SearchByICAO.setText(_translate("Dialog", "Поиск"))
        self.pushButton_Insert.setText(_translate("Dialog", "Поиск и Вставка по IATA"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("Dialog", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Tab 2"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", "Страница"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Dialog", "Страница"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("Dialog", "Страница"))

    # Окончание вставки тела конвертированного ресурсного файла

        # Добавляем функционал класса главного диалога

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Предупреждение', "Закрыть диалог?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


# Конвертация ресурсного файла *.ui -> *.py в терминале командой (командной строке)
# > pyuic5 Qt_Designer_LoadDialog.ui -o Qt_Designer_LoadDialog.py
class Ui_DialogLoadAirFlights(QtWidgets.QDialog):
    def __init__(self):
        # просто сразу вызываем конструктор предка
        super(Ui_DialogLoadAirFlights, self).__init__()  # конструктор предка
        # а потом остальное
        pass

    # Начало вставки тела конвертированного ресурсного файла
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(768, 380)
        self.label_12 = QtWidgets.QLabel(Dialog)
        self.label_12.setGeometry(QtCore.QRect(50, 220, 81, 20))
        self.label_12.setObjectName("label_12")
        self.lineEdit_DSN_FN = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_DSN_FN.setGeometry(QtCore.QRect(560, 310, 201, 20))
        self.lineEdit_DSN_FN.setObjectName("lineEdit_DSN_FN")
        self.lineEdit_ODBCversion_FN = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_ODBCversion_FN.setGeometry(QtCore.QRect(560, 250, 201, 20))
        self.lineEdit_ODBCversion_FN.setObjectName("lineEdit_ODBCversion_FN")
        self.label_16 = QtWidgets.QLabel(Dialog)
        self.label_16.setGeometry(QtCore.QRect(570, 60, 181, 16))
        self.label_16.setObjectName("label_16")
        self.label_11 = QtWidgets.QLabel(Dialog)
        self.label_11.setGeometry(QtCore.QRect(20, 140, 81, 20))
        self.label_11.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_11.setObjectName("label_11")
        self.comboBox_DSN_FN = QtWidgets.QComboBox(Dialog)
        self.comboBox_DSN_FN.setGeometry(QtCore.QRect(560, 130, 201, 22))
        self.comboBox_DSN_FN.setObjectName("comboBox_DSN_FN")
        self.label_9 = QtWidgets.QLabel(Dialog)
        self.label_9.setGeometry(QtCore.QRect(570, 110, 181, 16))
        self.label_9.setObjectName("label_9")
        self.pushButton_Connect_FN = QtWidgets.QPushButton(Dialog)
        self.pushButton_Connect_FN.setGeometry(QtCore.QRect(580, 160, 181, 23))
        self.pushButton_Connect_FN.setObjectName("pushButton_Connect_FN")
        self.lineEdit_Driver_FN = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Driver_FN.setGeometry(QtCore.QRect(560, 220, 201, 20))
        self.lineEdit_Driver_FN.setObjectName("lineEdit_Driver_FN")
        self.lineEdit_Schema_FN = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Schema_FN.setGeometry(QtCore.QRect(560, 280, 201, 20))
        self.lineEdit_Schema_FN.setObjectName("lineEdit_Schema_FN")
        self.label_14 = QtWidgets.QLabel(Dialog)
        self.label_14.setGeometry(QtCore.QRect(50, 250, 81, 20))
        self.label_14.setObjectName("label_14")
        self.comboBox_DB_FN = QtWidgets.QComboBox(Dialog)
        self.comboBox_DB_FN.setGeometry(QtCore.QRect(560, 30, 201, 22))
        self.comboBox_DB_FN.setObjectName("comboBox_DB_FN")
        self.comboBox_Driver_FN = QtWidgets.QComboBox(Dialog)
        self.comboBox_Driver_FN.setGeometry(QtCore.QRect(560, 80, 201, 22))
        self.comboBox_Driver_FN.setObjectName("comboBox_Driver_FN")
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(570, 10, 181, 16))
        self.label_8.setObjectName("label_8")
        self.label_15 = QtWidgets.QLabel(Dialog)
        self.label_15.setGeometry(QtCore.QRect(50, 280, 81, 20))
        self.label_15.setObjectName("label_15")
        self.pushButton_Disconnect_FN = QtWidgets.QPushButton(Dialog)
        self.pushButton_Disconnect_FN.setGeometry(QtCore.QRect(580, 190, 181, 23))
        self.pushButton_Disconnect_FN.setObjectName("pushButton_Disconnect_FN")
        self.pushButton_GetStarted = QtWidgets.QPushButton(Dialog)
        self.pushButton_GetStarted.setGeometry(QtCore.QRect(10, 190, 121, 21))
        self.pushButton_GetStarted.setObjectName("pushButton_GetStarted")
        self.pushButton_ChooseTXTFile = QtWidgets.QPushButton(Dialog)
        self.pushButton_ChooseTXTFile.setGeometry(QtCore.QRect(40, 350, 91, 23))
        self.pushButton_ChooseTXTFile.setObjectName("pushButton_ChooseTXTFile")
        self.lineEdit_TXTFile = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_TXTFile.setGeometry(QtCore.QRect(140, 350, 291, 20))
        self.lineEdit_TXTFile.setReadOnly(False)
        self.lineEdit_TXTFile.setObjectName("lineEdit_TXTFile")
        self.lineEdit_CSVFile = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_CSVFile.setGeometry(QtCore.QRect(140, 320, 291, 20))
        self.lineEdit_CSVFile.setReadOnly(False)
        self.lineEdit_CSVFile.setObjectName("lineEdit_CSVFile")
        self.pushButton_ChooseCSVFile = QtWidgets.QPushButton(Dialog)
        self.pushButton_ChooseCSVFile.setGeometry(QtCore.QRect(40, 320, 91, 23))
        self.pushButton_ChooseCSVFile.setObjectName("pushButton_ChooseCSVFile")
        self.comboBox_Driver_RT = QtWidgets.QComboBox(Dialog)
        self.comboBox_Driver_RT.setGeometry(QtCore.QRect(310, 80, 191, 22))
        self.comboBox_Driver_RT.setObjectName("comboBox_Driver_RT")
        self.label_18 = QtWidgets.QLabel(Dialog)
        self.label_18.setGeometry(QtCore.QRect(320, 10, 171, 20))
        self.label_18.setObjectName("label_18")
        self.comboBox_DB_RT = QtWidgets.QComboBox(Dialog)
        self.comboBox_DB_RT.setGeometry(QtCore.QRect(310, 30, 191, 22))
        self.comboBox_DB_RT.setObjectName("comboBox_DB_RT")
        self.label_19 = QtWidgets.QLabel(Dialog)
        self.label_19.setGeometry(QtCore.QRect(320, 60, 111, 16))
        self.label_19.setObjectName("label_19")
        self.lineEdit_ODBCversion_RT = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_ODBCversion_RT.setGeometry(QtCore.QRect(340, 250, 161, 20))
        self.lineEdit_ODBCversion_RT.setObjectName("lineEdit_ODBCversion_RT")
        self.lineEdit_Driver_RT = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Driver_RT.setGeometry(QtCore.QRect(340, 220, 161, 20))
        self.lineEdit_Driver_RT.setObjectName("lineEdit_Driver_RT")
        self.lineEdit_Schema_RT = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Schema_RT.setGeometry(QtCore.QRect(340, 280, 161, 20))
        self.lineEdit_Schema_RT.setObjectName("lineEdit_Schema_RT")
        self.pushButton_Disconnect_RT = QtWidgets.QPushButton(Dialog)
        self.pushButton_Disconnect_RT.setGeometry(QtCore.QRect(370, 140, 131, 23))
        self.pushButton_Disconnect_RT.setObjectName("pushButton_Disconnect_RT")
        self.pushButton_Connect_RT = QtWidgets.QPushButton(Dialog)
        self.pushButton_Connect_RT.setGeometry(QtCore.QRect(370, 110, 131, 23))
        self.pushButton_Connect_RT.setObjectName("pushButton_Connect_RT")
        self.label_25 = QtWidgets.QLabel(Dialog)
        self.label_25.setGeometry(QtCore.QRect(0, 20, 131, 121))
        self.label_25.setText("")
        self.label_25.setPixmap(QtGui.QPixmap("Значки (Иконки)/2059278.png"))
        self.label_25.setObjectName("label_25")
        self.lineEdit_Schema_AL = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Schema_AL.setGeometry(QtCore.QRect(140, 280, 161, 20))
        self.lineEdit_Schema_AL.setObjectName("lineEdit_Schema_AL")
        self.lineEdit_Driver_AL = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Driver_AL.setGeometry(QtCore.QRect(140, 220, 161, 20))
        self.lineEdit_Driver_AL.setObjectName("lineEdit_Driver_AL")
        self.lineEdit_ODBCversion_AL = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_ODBCversion_AL.setGeometry(QtCore.QRect(140, 250, 161, 20))
        self.lineEdit_ODBCversion_AL.setObjectName("lineEdit_ODBCversion_AL")
        self.comboBox_DB_AL = QtWidgets.QComboBox(Dialog)
        self.comboBox_DB_AL.setGeometry(QtCore.QRect(140, 30, 161, 22))
        self.comboBox_DB_AL.setObjectName("comboBox_DB_AL")
        self.label_20 = QtWidgets.QLabel(Dialog)
        self.label_20.setGeometry(QtCore.QRect(150, 60, 141, 20))
        self.label_20.setObjectName("label_20")
        self.pushButton_Disconnect_AL = QtWidgets.QPushButton(Dialog)
        self.pushButton_Disconnect_AL.setGeometry(QtCore.QRect(160, 140, 141, 23))
        self.pushButton_Disconnect_AL.setObjectName("pushButton_Disconnect_AL")
        self.comboBox_Driver_AL = QtWidgets.QComboBox(Dialog)
        self.comboBox_Driver_AL.setGeometry(QtCore.QRect(140, 80, 161, 22))
        self.comboBox_Driver_AL.setObjectName("comboBox_Driver_AL")
        self.pushButton_Connect_AL = QtWidgets.QPushButton(Dialog)
        self.pushButton_Connect_AL.setGeometry(QtCore.QRect(160, 110, 141, 23))
        self.pushButton_Connect_AL.setObjectName("pushButton_Connect_AL")
        self.lineEdit_Server = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Server.setGeometry(QtCore.QRect(10, 160, 121, 20))
        self.lineEdit_Server.setObjectName("lineEdit_Server")
        self.label_21 = QtWidgets.QLabel(Dialog)
        self.label_21.setGeometry(QtCore.QRect(150, 10, 141, 20))
        self.label_21.setObjectName("label_21")
        self.label_28 = QtWidgets.QLabel(Dialog)
        self.label_28.setGeometry(QtCore.QRect(510, 70, 41, 41))
        self.label_28.setText("")
        self.label_28.setPixmap(QtGui.QPixmap("Значки (Иконки)/a_22.ico"))
        self.label_28.setObjectName("label_28")
        self.label_29 = QtWidgets.QLabel(Dialog)
        self.label_29.setGeometry(QtCore.QRect(510, 220, 41, 41))
        self.label_29.setText("")
        self.label_29.setPixmap(QtGui.QPixmap("Значки (Иконки)/a_23.ico"))
        self.label_29.setObjectName("label_29")
        self.radioButton_DB = QtWidgets.QRadioButton(Dialog)
        self.radioButton_DB.setGeometry(QtCore.QRect(510, 30, 41, 18))
        self.radioButton_DB.setObjectName("radioButton_DB")
        self.radioButton_DSN = QtWidgets.QRadioButton(Dialog)
        self.radioButton_DSN.setGeometry(QtCore.QRect(510, 130, 41, 18))
        self.radioButton_DSN.setObjectName("radioButton_DSN")
        self.dateEdit_BeginDate = QtWidgets.QDateEdit(Dialog)
        self.dateEdit_BeginDate.setGeometry(QtCore.QRect(440, 350, 110, 22))
        self.dateEdit_BeginDate.setObjectName("dateEdit_BeginDate")
        self.label_30 = QtWidgets.QLabel(Dialog)
        self.label_30.setGeometry(QtCore.QRect(320, 110, 41, 41))
        self.label_30.setText("")
        self.label_30.setPixmap(QtGui.QPixmap("Значки (Иконки)/a_21.ico"))
        self.label_30.setObjectName("label_30")
        self.checkBox_SetInputDate = QtWidgets.QCheckBox(Dialog)
        self.checkBox_SetInputDate.setGeometry(QtCore.QRect(560, 350, 191, 18))
        self.checkBox_SetInputDate.setObjectName("checkBox_SetInputDate")
        self.label_23 = QtWidgets.QLabel(Dialog)
        self.label_23.setGeometry(QtCore.QRect(150, 170, 81, 21))
        self.label_23.setObjectName("label_23")
        self.progressBar_completion = QtWidgets.QProgressBar(Dialog)
        self.progressBar_completion.setGeometry(QtCore.QRect(140, 190, 411, 23))
        self.progressBar_completion.setProperty("value", 24)
        self.progressBar_completion.setObjectName("progressBar_completion")
        self.label_10 = QtWidgets.QLabel(Dialog)
        self.label_10.setGeometry(QtCore.QRect(460, 310, 91, 20))
        self.label_10.setObjectName("label_10")
        self.label_Version = QtWidgets.QLabel(Dialog)
        self.label_Version.setGeometry(QtCore.QRect(10, 0, 131, 20))
        self.label_Version.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_Version.setObjectName("label_Version")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_12.setText(_translate("Dialog", "Драйвер СУБД"))
        self.label_16.setText(_translate("Dialog", "Драйвер СУБД"))
        self.label_11.setText(_translate("Dialog", "Сервер СУБД"))
        self.label_9.setText(_translate("Dialog", "DSN авиарейсов"))
        self.pushButton_Connect_FN.setText(_translate("Dialog", "Подключиться к БД или к DSN"))
        self.label_14.setText(_translate("Dialog", "Версия ODBC"))
        self.label_8.setText(_translate("Dialog", "База данных авиарейсов"))
        self.label_15.setText(_translate("Dialog", "Схема"))
        self.pushButton_Disconnect_FN.setText(_translate("Dialog", "Отключиться от БД или от DSN"))
        self.pushButton_GetStarted.setText(_translate("Dialog", "Начатьзагрузку"))
        self.pushButton_ChooseTXTFile.setText(_translate("Dialog", "Файл журнала"))
        self.pushButton_ChooseCSVFile.setText(_translate("Dialog", "Файл данных"))
        self.label_18.setText(_translate("Dialog", "База данных аэропортов"))
        self.label_19.setText(_translate("Dialog", "Драйвер СУБД"))
        self.pushButton_Disconnect_RT.setText(_translate("Dialog", "Отключиться от БД"))
        self.pushButton_Connect_RT.setText(_translate("Dialog", "Подключиться к БД"))
        self.label_20.setText(_translate("Dialog", "Драйвер СУБД"))
        self.pushButton_Disconnect_AL.setText(_translate("Dialog", "Отключиться от БД"))
        self.pushButton_Connect_AL.setText(_translate("Dialog", "Подключиться к БД"))
        self.label_21.setText(_translate("Dialog", "База данных авиакомпаний"))
        self.radioButton_DB.setText(_translate("Dialog", "БД"))
        self.radioButton_DSN.setText(_translate("Dialog", "DSN"))
        self.checkBox_SetInputDate.setText(_translate("Dialog", "Перенос даты из файла данных"))
        self.label_23.setText(_translate("Dialog", "Выполнение"))
        self.label_10.setText(_translate("Dialog", "DSN авиарейсов"))
        self.label_Version.setText(_translate("Dialog", "Сервер СУБД"))

    # Окончание вставки тела конвертированного ресурсного файла

        # Добавляем функционал класса главного диалога

    # def closeEvent(self, event):
    #     reply = QtWidgets.QMessageBox.question(self, 'Предупреждение', "Закрыть диалог?",
    #                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
    #                                            QtWidgets.QMessageBox.No)
    #     if reply == QtWidgets.QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()


class Ui_DialogLoadAirFlightsWithAirCrafts(QtWidgets.QDialog):
    def __init__(self):
        # просто сразу вызываем конструктор предка
        super(Ui_DialogLoadAirFlightsWithAirCrafts, self).__init__()  # конструктор предка
        # а потом остальное
        pass

    # Начало вставки тела конвертированного ресурсного файла
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(940, 375)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.label_12 = QtWidgets.QLabel(Dialog)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QtCore.QRect(50, 230, 81, 20))
        self.lineEdit_DSN_FN = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_DSN_FN.setObjectName(u"lineEdit_DSN_FN")
        self.lineEdit_DSN_FN.setGeometry(QtCore.QRect(520, 280, 201, 20))
        self.lineEdit_ODBCversion_FN = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_ODBCversion_FN.setObjectName(u"lineEdit_ODBCversion_FN")
        self.lineEdit_ODBCversion_FN.setGeometry(QtCore.QRect(520, 220, 201, 20))
        self.label_16 = QtWidgets.QLabel(Dialog)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QtCore.QRect(530, 40, 181, 16))
        self.label_11 = QtWidgets.QLabel(Dialog)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QtCore.QRect(150, 40, 251, 20))
        self.label_11.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboBox_DSN_FN = QtWidgets.QComboBox(Dialog)
        self.comboBox_DSN_FN.setObjectName(u"comboBox_DSN_FN")
        self.comboBox_DSN_FN.setGeometry(QtCore.QRect(520, 100, 201, 22))
        self.label_9 = QtWidgets.QLabel(Dialog)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QtCore.QRect(530, 80, 181, 16))
        self.pushButton_Connect_FN = QtWidgets.QPushButton(Dialog)
        self.pushButton_Connect_FN.setObjectName(u"pushButton_Connect_FN")
        self.pushButton_Connect_FN.setGeometry(QtCore.QRect(540, 130, 181, 23))
        self.lineEdit_Driver_FN = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Driver_FN.setObjectName(u"lineEdit_Driver_FN")
        self.lineEdit_Driver_FN.setGeometry(QtCore.QRect(520, 190, 201, 20))
        self.lineEdit_Schema_FN = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Schema_FN.setObjectName(u"lineEdit_Schema_FN")
        self.lineEdit_Schema_FN.setGeometry(QtCore.QRect(520, 250, 201, 20))
        self.label_14 = QtWidgets.QLabel(Dialog)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QtCore.QRect(50, 260, 81, 20))
        self.comboBox_DB_FN = QtWidgets.QComboBox(Dialog)
        self.comboBox_DB_FN.setObjectName(u"comboBox_DB_FN")
        self.comboBox_DB_FN.setGeometry(QtCore.QRect(520, 20, 201, 22))
        self.comboBox_Driver_FN = QtWidgets.QComboBox(Dialog)
        self.comboBox_Driver_FN.setObjectName(u"comboBox_Driver_FN")
        self.comboBox_Driver_FN.setGeometry(QtCore.QRect(520, 60, 201, 22))
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QtCore.QRect(530, 0, 221, 20))
        self.label_15 = QtWidgets.QLabel(Dialog)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QtCore.QRect(50, 290, 81, 20))
        self.pushButton_Disconnect_FN = QtWidgets.QPushButton(Dialog)
        self.pushButton_Disconnect_FN.setObjectName(u"pushButton_Disconnect_FN")
        self.pushButton_Disconnect_FN.setGeometry(QtCore.QRect(540, 160, 181, 23))
        self.pushButton_GetStarted = QtWidgets.QPushButton(Dialog)
        self.pushButton_GetStarted.setObjectName(u"pushButton_GetStarted")
        self.pushButton_GetStarted.setGeometry(QtCore.QRect(820, 350, 111, 21))
        self.pushButton_ChooseTXTFile = QtWidgets.QPushButton(Dialog)
        self.pushButton_ChooseTXTFile.setObjectName(u"pushButton_ChooseTXTFile")
        self.pushButton_ChooseTXTFile.setGeometry(QtCore.QRect(40, 350, 91, 23))
        self.lineEdit_TXTFile = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_TXTFile.setObjectName(u"lineEdit_TXTFile")
        self.lineEdit_TXTFile.setGeometry(QtCore.QRect(140, 350, 341, 20))
        self.lineEdit_TXTFile.setReadOnly(False)
        self.lineEdit_CSVFile = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_CSVFile.setObjectName(u"lineEdit_CSVFile")
        self.lineEdit_CSVFile.setGeometry(QtCore.QRect(140, 320, 341, 20))
        self.lineEdit_CSVFile.setReadOnly(False)
        self.pushButton_ChooseCSVFile = QtWidgets.QPushButton(Dialog)
        self.pushButton_ChooseCSVFile.setObjectName(u"pushButton_ChooseCSVFile")
        self.pushButton_ChooseCSVFile.setGeometry(QtCore.QRect(40, 320, 91, 23))
        self.comboBox_Driver_RT = QtWidgets.QComboBox(Dialog)
        self.comboBox_Driver_RT.setObjectName(u"comboBox_Driver_RT")
        self.comboBox_Driver_RT.setGeometry(QtCore.QRect(320, 140, 191, 22))
        self.label_18 = QtWidgets.QLabel(Dialog)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setGeometry(QtCore.QRect(330, 80, 171, 20))
        self.comboBox_DB_RT = QtWidgets.QComboBox(Dialog)
        self.comboBox_DB_RT.setObjectName(u"comboBox_DB_RT")
        self.comboBox_DB_RT.setGeometry(QtCore.QRect(320, 100, 191, 22))
        self.label_19 = QtWidgets.QLabel(Dialog)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setGeometry(QtCore.QRect(330, 120, 111, 16))
        self.lineEdit_ODBCversion_RT = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_ODBCversion_RT.setObjectName(u"lineEdit_ODBCversion_RT")
        self.lineEdit_ODBCversion_RT.setGeometry(QtCore.QRect(320, 260, 191, 20))
        self.lineEdit_Driver_RT = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Driver_RT.setObjectName(u"lineEdit_Driver_RT")
        self.lineEdit_Driver_RT.setGeometry(QtCore.QRect(320, 230, 191, 20))
        self.lineEdit_Schema_RT = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Schema_RT.setObjectName(u"lineEdit_Schema_RT")
        self.lineEdit_Schema_RT.setGeometry(QtCore.QRect(320, 290, 191, 20))
        self.pushButton_Disconnect_RT = QtWidgets.QPushButton(Dialog)
        self.pushButton_Disconnect_RT.setObjectName(u"pushButton_Disconnect_RT")
        self.pushButton_Disconnect_RT.setGeometry(QtCore.QRect(380, 200, 131, 23))
        self.pushButton_Connect_RT = QtWidgets.QPushButton(Dialog)
        self.pushButton_Connect_RT.setObjectName(u"pushButton_Connect_RT")
        self.pushButton_Connect_RT.setGeometry(QtCore.QRect(380, 170, 131, 23))
        self.label_25 = QtWidgets.QLabel(Dialog)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setGeometry(QtCore.QRect(10, 30, 121, 121))
        self.label_25.setPixmap(QtGui.QPixmap(u"\u0417\u043d\u0430\u0447\u043a\u0438 (\u0418\u043a\u043e\u043d\u043a\u0438)/2059278.png"))
        self.lineEdit_Schema_AL = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Schema_AL.setObjectName(u"lineEdit_Schema_AL")
        self.lineEdit_Schema_AL.setGeometry(QtCore.QRect(140, 290, 171, 20))
        self.lineEdit_Driver_AL = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Driver_AL.setObjectName(u"lineEdit_Driver_AL")
        self.lineEdit_Driver_AL.setGeometry(QtCore.QRect(140, 230, 171, 20))
        self.lineEdit_ODBCversion_AL = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_ODBCversion_AL.setObjectName(u"lineEdit_ODBCversion_AL")
        self.lineEdit_ODBCversion_AL.setGeometry(QtCore.QRect(140, 260, 171, 20))
        self.comboBox_DB_AL = QtWidgets.QComboBox(Dialog)
        self.comboBox_DB_AL.setObjectName(u"comboBox_DB_AL")
        self.comboBox_DB_AL.setGeometry(QtCore.QRect(140, 100, 171, 22))
        self.label_20 = QtWidgets.QLabel(Dialog)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setGeometry(QtCore.QRect(150, 120, 111, 20))
        self.pushButton_Disconnect_AL = QtWidgets.QPushButton(Dialog)
        self.pushButton_Disconnect_AL.setObjectName(u"pushButton_Disconnect_AL")
        self.pushButton_Disconnect_AL.setGeometry(QtCore.QRect(170, 200, 141, 23))
        self.comboBox_Driver_AL = QtWidgets.QComboBox(Dialog)
        self.comboBox_Driver_AL.setObjectName(u"comboBox_Driver_AL")
        self.comboBox_Driver_AL.setGeometry(QtCore.QRect(140, 140, 171, 22))
        self.pushButton_Connect_AL = QtWidgets.QPushButton(Dialog)
        self.pushButton_Connect_AL.setObjectName(u"pushButton_Connect_AL")
        self.pushButton_Connect_AL.setGeometry(QtCore.QRect(170, 170, 141, 23))
        self.lineEdit_Server = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Server.setObjectName(u"lineEdit_Server")
        self.lineEdit_Server.setGeometry(QtCore.QRect(140, 60, 371, 20))
        self.label_21 = QtWidgets.QLabel(Dialog)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setGeometry(QtCore.QRect(150, 80, 141, 20))
        self.label_28 = QtWidgets.QLabel(Dialog)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setGeometry(QtCore.QRect(120, 170, 41, 41))
        self.label_28.setPixmap(QtGui.QPixmap(u"\u0417\u043d\u0430\u0447\u043a\u0438 (\u0418\u043a\u043e\u043d\u043a\u0438)/a_22.ico"))
        self.label_29 = QtWidgets.QLabel(Dialog)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setGeometry(QtCore.QRect(330, 170, 41, 41))
        self.label_29.setPixmap(QtGui.QPixmap(u"\u0417\u043d\u0430\u0447\u043a\u0438 (\u0418\u043a\u043e\u043d\u043a\u0438)/a_23.ico"))
        self.dateEdit_BeginDate = QtWidgets.QDateEdit(Dialog)
        self.dateEdit_BeginDate.setObjectName(u"dateEdit_BeginDate")
        self.dateEdit_BeginDate.setGeometry(QtCore.QRect(490, 320, 110, 22))
        self.label_30 = QtWidgets.QLabel(Dialog)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setGeometry(QtCore.QRect(750, 130, 41, 41))
        self.label_30.setPixmap(QtGui.QPixmap(u"\u0417\u043d\u0430\u0447\u043a\u0438 (\u0418\u043a\u043e\u043d\u043a\u0438)/a_21.ico"))
        self.checkBox_SetInputDate = QtWidgets.QCheckBox(Dialog)
        self.checkBox_SetInputDate.setObjectName(u"checkBox_SetInputDate")
        self.checkBox_SetInputDate.setGeometry(QtCore.QRect(490, 350, 191, 18))
        self.label_Version = QtWidgets.QLabel(Dialog)
        self.label_Version.setObjectName(u"label_Version")
        self.label_Version.setGeometry(QtCore.QRect(10, 0, 121, 20))
        self.label_Version.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_Disconnect_AC = QtWidgets.QPushButton(Dialog)
        self.pushButton_Disconnect_AC.setObjectName(u"pushButton_Disconnect_AC")
        self.pushButton_Disconnect_AC.setGeometry(QtCore.QRect(800, 160, 131, 23))
        self.label_13 = QtWidgets.QLabel(Dialog)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QtCore.QRect(740, 80, 181, 16))
        self.pushButton_Connect_AC = QtWidgets.QPushButton(Dialog)
        self.pushButton_Connect_AC.setObjectName(u"pushButton_Connect_AC")
        self.pushButton_Connect_AC.setGeometry(QtCore.QRect(800, 130, 131, 23))
        self.comboBox_DSN_AC = QtWidgets.QComboBox(Dialog)
        self.comboBox_DSN_AC.setObjectName(u"comboBox_DSN_AC")
        self.comboBox_DSN_AC.setGeometry(QtCore.QRect(730, 100, 201, 22))
        self.lineEdit_DSN_AC = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_DSN_AC.setObjectName(u"lineEdit_DSN_AC")
        self.lineEdit_DSN_AC.setGeometry(QtCore.QRect(730, 280, 201, 20))
        self.lineEdit_Schema_AC = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Schema_AC.setObjectName(u"lineEdit_Schema_AC")
        self.lineEdit_Schema_AC.setGeometry(QtCore.QRect(730, 250, 201, 20))
        self.lineEdit_Driver_AC = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Driver_AC.setObjectName(u"lineEdit_Driver_AC")
        self.lineEdit_Driver_AC.setGeometry(QtCore.QRect(730, 190, 201, 20))
        self.lineEdit_ODBCversion_AC = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_ODBCversion_AC.setObjectName(u"lineEdit_ODBCversion_AC")
        self.lineEdit_ODBCversion_AC.setGeometry(QtCore.QRect(730, 220, 201, 20))
        self.lineEdit_Server_remote = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Server_remote.setObjectName(u"lineEdit_Server_remote")
        self.lineEdit_Server_remote.setGeometry(QtCore.QRect(140, 20, 371, 20))
        self.label_17 = QtWidgets.QLabel(Dialog)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QtCore.QRect(150, 0, 261, 20))
        self.label_17.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QtCore.QRect(750, 0, 181, 81))
        self.radioButton_DSN = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_DSN.setObjectName(u"radioButton_DSN")
        self.radioButton_DSN.setGeometry(QtCore.QRect(10, 50, 41, 18))
        self.radioButton_DB = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_DB.setObjectName(u"radioButton_DB")
        self.radioButton_DB.setGeometry(QtCore.QRect(10, 20, 151, 18))
        self.label_execute = QtWidgets.QLabel(Dialog)
        self.label_execute.setObjectName(u"label_execute")
        self.label_execute.setGeometry(QtCore.QRect(670, 320, 261, 20))
        self.label_22 = QtWidgets.QLabel(Dialog)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setGeometry(QtCore.QRect(610, 320, 51, 20))

        self.retranslateUi(Dialog)

        QtCore.QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtCore.QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_12.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0414\u0440\u0430\u0439\u0432\u0435\u0440 \u0421\u0423\u0411\u0414", None))
        self.label_16.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0414\u0440\u0430\u0439\u0432\u0435\u0440 \u0421\u0423\u0411\u0414", None))
        self.label_11.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0421\u0435\u0440\u0432\u0435\u0440 \u0421\u0423\u0411\u0414 \u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a\u043e\u0432", None))
        self.label_9.setText(QtCore.QCoreApplication.translate("Dialog", u"DSN \u0430\u0432\u0438\u0430\u043f\u0435\u0440\u0435\u043b\u0435\u0442\u043e\u0432", None))
        self.pushButton_Connect_FN.setText(QtCore.QCoreApplication.translate("Dialog", u"\u041f\u043e\u0434\u043a\u043b\u044e\u0447\u0438\u0442\u044c\u0441\u044f \u043a \u0411\u0414 \u0438\u043b\u0438 \u043a DSN", None))
        self.label_14.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0412\u0435\u0440\u0441\u0438\u044f ODBC", None))
        self.label_8.setText(QtCore.QCoreApplication.translate("Dialog", u"\u041e\u043f\u0435\u0440\u0430\u0442\u0438\u0432\u043d\u044b\u0435 \u0434\u0430\u043d\u043d\u044b\u0435 \u043f\u043e \u0430\u0432\u0438\u0430\u043f\u0435\u0440\u0435\u043b\u0435\u0442\u0430\u043c", None))
        self.label_15.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0421\u0445\u0435\u043c\u0430", None))
        self.pushButton_Disconnect_FN.setText(QtCore.QCoreApplication.translate("Dialog", u"\u041e\u0442\u043a\u043b\u044e\u0447\u0438\u0442\u044c\u0441\u044f \u043e\u0442 \u0411\u0414 \u0438\u043b\u0438 \u043e\u0442 DSN", None))
        self.pushButton_GetStarted.setText(QtCore.QCoreApplication.translate("Dialog", u"\u041d\u0430\u0447\u0430\u0442\u044c\u0437\u0430\u0433\u0440\u0443\u0437\u043a\u0443", None))
        self.pushButton_ChooseTXTFile.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0424\u0430\u0439\u043b \u0436\u0443\u0440\u043d\u0430\u043b\u0430", None))
        self.pushButton_ChooseCSVFile.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0424\u0430\u0439\u043b \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.label_18.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0421\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a \u0430\u044d\u0440\u043e\u043f\u043e\u0440\u0442\u043e\u0432", None))
        self.label_19.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0414\u0440\u0430\u0439\u0432\u0435\u0440 \u0421\u0423\u0411\u0414", None))
        self.pushButton_Disconnect_RT.setText(QtCore.QCoreApplication.translate("Dialog", u"\u041e\u0442\u043a\u043b\u044e\u0447\u0438\u0442\u044c\u0441\u044f \u043e\u0442 \u0411\u0414", None))
        self.pushButton_Connect_RT.setText(QtCore.QCoreApplication.translate("Dialog", u"\u041f\u043e\u0434\u043a\u043b\u044e\u0447\u0438\u0442\u044c\u0441\u044f \u043a \u0411\u0414", None))
        self.label_25.setText("")
        self.label_20.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0414\u0440\u0430\u0439\u0432\u0435\u0440 \u0421\u0423\u0411\u0414", None))
        self.pushButton_Disconnect_AL.setText(QtCore.QCoreApplication.translate("Dialog", u"\u041e\u0442\u043a\u043b\u044e\u0447\u0438\u0442\u044c\u0441\u044f \u043e\u0442 \u0411\u0414", None))
        self.pushButton_Connect_AL.setText(QtCore.QCoreApplication.translate("Dialog", u"\u041f\u043e\u0434\u043a\u043b\u044e\u0447\u0438\u0442\u044c\u0441\u044f \u043a \u0411\u0414", None))
        self.label_21.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0421\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a \u0430\u0432\u0438\u0430\u043a\u043e\u043c\u043f\u0430\u043d\u0438\u0439", None))
        self.label_28.setText("")
        self.label_29.setText("")
        self.label_30.setText("")
        self.checkBox_SetInputDate.setText(QtCore.QCoreApplication.translate("Dialog", u"\u041f\u0435\u0440\u0435\u043d\u043e\u0441 \u0434\u0430\u0442\u044b \u0438\u0437 \u0444\u0430\u0439\u043b\u0430 \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.label_Version.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0412\u0435\u0440\u0441\u0438\u044f \u0437\u0430\u0433\u0440\u0443\u0437\u043a\u0438", None))
        self.pushButton_Disconnect_AC.setText(QtCore.QCoreApplication.translate("Dialog", u"\u041e\u0442\u043a\u043b\u044e\u0447\u0438\u0442\u044c\u0441\u044f \u043e\u0442 DSN", None))
        self.label_13.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0421\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a \u043f\u043e \u0441\u0430\u043c\u043e\u043b\u0435\u0442\u0430\u043c", None))
        self.pushButton_Connect_AC.setText(QtCore.QCoreApplication.translate("Dialog", u"\u041f\u043e\u0434\u043a\u043b\u044e\u0447\u0438\u0442\u044c\u0441\u044f \u043a DSN", None))
        self.label_17.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0421\u0435\u0440\u0432\u0435\u0440 \u0421\u0423\u0411\u0414 \u043e\u043f\u0435\u0440\u0430\u0442\u0438\u0432\u043d\u044b\u0445 \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.groupBox.setTitle(QtCore.QCoreApplication.translate("Dialog", u"\u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a \u043e\u043f\u0435\u0440\u0430\u0442\u0438\u0432\u043d\u044b\u0445 \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.radioButton_DSN.setText(QtCore.QCoreApplication.translate("Dialog", u"DSN", None))
        self.radioButton_DB.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0411\u0430\u0437\u0430 \u0434\u0430\u043d\u043d\u044b\u0445 \u0438 \u0414\u0440\u0430\u0439\u0432\u0435\u0440", None))
        self.label_execute.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0412\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435 = ", None))
        self.label_22.setText(QtCore.QCoreApplication.translate("Dialog", u"\u0421\u0442\u0430\u0442\u0443\u0441:", None))
    # retranslateUi

    # Окончание вставки тела конвертированного ресурсного файла

        # Добавляем функционал класса главного диалога

    # def closeEvent(self, event):
    #     reply = QtWidgets.QMessageBox.question(self, 'Предупреждение', "Закрыть диалог?",
    #                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
    #                                            QtWidgets.QMessageBox.No)
    #     if reply == QtWidgets.QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()


# Конвертация ресурсного файла *.ui -> *.py в терминале командой (командной строке)
# > pyuic5 Qt_Designer_ReverseDialog.ui -o Qt_Designer_ReverseDialog.py
class Ui_DialogReverse(QtWidgets.QDialog):
    def __init__(self):
        # просто сразу вызываем конструктор предка
        super(Ui_DialogReverse, self).__init__()  # конструктор предка
        # а потом остальное
        pass

    # Начало вставки тела конвертированного ресурсного файла
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(560, 340)
        self.label_12 = QtWidgets.QLabel(Dialog)
        self.label_12.setGeometry(QtCore.QRect(20, 220, 91, 16))
        self.label_12.setObjectName("label_12")
        self.lineEdit_DSN = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_DSN.setGeometry(QtCore.QRect(120, 280, 181, 20))
        self.lineEdit_DSN.setObjectName("lineEdit_DSN")
        self.lineEdit_ODBCversion = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_ODBCversion.setGeometry(QtCore.QRect(120, 250, 181, 20))
        self.lineEdit_ODBCversion.setObjectName("lineEdit_ODBCversion")
        self.label_16 = QtWidgets.QLabel(Dialog)
        self.label_16.setGeometry(QtCore.QRect(340, 60, 111, 16))
        self.label_16.setObjectName("label_16")
        self.label_13 = QtWidgets.QLabel(Dialog)
        self.label_13.setGeometry(QtCore.QRect(20, 280, 91, 16))
        self.label_13.setObjectName("label_13")
        self.label_11 = QtWidgets.QLabel(Dialog)
        self.label_11.setGeometry(QtCore.QRect(20, 190, 91, 16))
        self.label_11.setObjectName("label_11")
        self.comboBox_DSN = QtWidgets.QComboBox(Dialog)
        self.comboBox_DSN.setGeometry(QtCore.QRect(330, 160, 221, 22))
        self.comboBox_DSN.setObjectName("comboBox_DSN")
        self.label_9 = QtWidgets.QLabel(Dialog)
        self.label_9.setGeometry(QtCore.QRect(340, 140, 211, 16))
        self.label_9.setObjectName("label_9")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(11, 20, 171, 151))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("../Example pyQt (Hramushin2 - DevelopServer)/tproger-square-192.png"))
        self.label_4.setObjectName("label_4")
        self.pushButton_SelectDB = QtWidgets.QPushButton(Dialog)
        self.pushButton_SelectDB.setGeometry(QtCore.QRect(350, 190, 181, 23))
        self.pushButton_SelectDB.setObjectName("pushButton_SelectDB")
        self.lineEdit_Driver = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Driver.setGeometry(QtCore.QRect(120, 220, 181, 20))
        self.lineEdit_Driver.setObjectName("lineEdit_Driver")
        self.lineEdit_Schema = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Schema.setGeometry(QtCore.QRect(120, 310, 181, 20))
        self.lineEdit_Schema.setObjectName("lineEdit_Schema")
        self.label_14 = QtWidgets.QLabel(Dialog)
        self.label_14.setGeometry(QtCore.QRect(20, 250, 91, 16))
        self.label_14.setObjectName("label_14")
        self.comboBox_DB = QtWidgets.QComboBox(Dialog)
        self.comboBox_DB.setGeometry(QtCore.QRect(330, 30, 221, 22))
        self.comboBox_DB.setObjectName("comboBox_DB")
        self.comboBox_Driver = QtWidgets.QComboBox(Dialog)
        self.comboBox_Driver.setGeometry(QtCore.QRect(330, 80, 221, 22))
        self.comboBox_Driver.setObjectName("comboBox_Driver")
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(340, 10, 111, 16))
        self.label_8.setObjectName("label_8")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(140, 20, 131, 151))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_15 = QtWidgets.QLabel(Dialog)
        self.label_15.setGeometry(QtCore.QRect(20, 310, 91, 16))
        self.label_15.setObjectName("label_15")
        self.lineEdit_Server = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Server.setGeometry(QtCore.QRect(120, 190, 181, 20))
        self.lineEdit_Server.setObjectName("lineEdit_Server")
        self.pushButton_Disconnect = QtWidgets.QPushButton(Dialog)
        self.pushButton_Disconnect.setGeometry(QtCore.QRect(350, 280, 181, 23))
        self.pushButton_Disconnect.setObjectName("pushButton_Disconnect")
        self.pushButton_BackUp = QtWidgets.QPushButton(Dialog)
        self.pushButton_BackUp.setEnabled(True)
        self.pushButton_BackUp.setGeometry(QtCore.QRect(380, 220, 111, 23))
        self.pushButton_BackUp.setObjectName("pushButton_BackUp")
        self.pushButton_Restore = QtWidgets.QPushButton(Dialog)
        self.pushButton_Restore.setEnabled(True)
        self.pushButton_Restore.setGeometry(QtCore.QRect(380, 250, 111, 23))
        self.pushButton_Restore.setObjectName("pushButton_Restore")
        self.label_25 = QtWidgets.QLabel(Dialog)
        self.label_25.setGeometry(QtCore.QRect(10, 10, 121, 131))
        self.label_25.setText("")
        self.label_25.setPixmap(QtGui.QPixmap("Значки (Иконки)/FolderOut06.jpg"))
        self.label_25.setObjectName("label_25")
        self.label_26 = QtWidgets.QLabel(Dialog)
        self.label_26.setGeometry(QtCore.QRect(330, 230, 41, 41))
        self.label_26.setText("")
        self.label_26.setPixmap(QtGui.QPixmap("Значки (Иконки)/a_25.ico"))
        self.label_26.setObjectName("label_26")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_12.setText(_translate("Dialog", "Драйвер СУБД"))
        self.label_16.setText(_translate("Dialog", "Драйвер СУБД"))
        self.label_13.setText(_translate("Dialog", "DSN"))
        self.label_11.setText(_translate("Dialog", "Сервер СУБД"))
        self.label_9.setText(_translate("Dialog", "DSN (сист. или пользов.)"))
        self.pushButton_SelectDB.setText(_translate("Dialog", "Подключиться к БД или к DSN"))
        self.label_14.setText(_translate("Dialog", "Версия ODBC"))
        self.label_8.setText(_translate("Dialog", "База данных"))
        self.label_15.setText(_translate("Dialog", "Схема"))
        self.pushButton_Disconnect.setText(_translate("Dialog", "Отключиться от БД или от DSN"))
        self.pushButton_BackUp.setText(_translate("Dialog", "Резервная копия"))
        self.pushButton_Restore.setText(_translate("Dialog", "Восстановить"))

    # Окончание вставки тела конвертированного ресурсного файла

        # Добавляем функционал класса главного диалога

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Предупреждение', "отключились от БД?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


# Конвертация ресурсного файла *.ui -> *.py в терминале командой (командной строке)
# Вставка картинки https://stackoverflow.com/questions/28536306/inserting-an-image-in-gui-using-qt-designer
# > pyuic5 Qt_Designer_CorrectDialogAirLines.ui -o Qt_Designer_CorrectDialogAirLines.py
class Ui_DialogCorrectAirLine(QtWidgets.QDialog):
    def __init__(self):
        # просто сразу вызываем конструктор предка
        super(Ui_DialogCorrectAirLine, self).__init__()  # конструктор предка
        # а потом остальное
        pass

    # Начало вставки тела конвертированного ресурсного файла
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(862, 830)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.label_12 = QtWidgets.QLabel(Dialog)
        self.label_12.setGeometry(QtCore.QRect(20, 220, 91, 16))
        self.label_12.setObjectName("label_12")
        self.lineEdit_DSN = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_DSN.setGeometry(QtCore.QRect(120, 280, 181, 20))
        self.lineEdit_DSN.setObjectName("lineEdit_DSN")
        self.lineEdit_ODBCversion = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_ODBCversion.setGeometry(QtCore.QRect(120, 250, 181, 20))
        self.lineEdit_ODBCversion.setObjectName("lineEdit_ODBCversion")
        self.label_13 = QtWidgets.QLabel(Dialog)
        self.label_13.setGeometry(QtCore.QRect(20, 280, 91, 16))
        self.label_13.setObjectName("label_13")
        self.label_11 = QtWidgets.QLabel(Dialog)
        self.label_11.setGeometry(QtCore.QRect(20, 190, 91, 16))
        self.label_11.setObjectName("label_11")
        self.pushButton_SelectDB = QtWidgets.QPushButton(Dialog)
        self.pushButton_SelectDB.setGeometry(QtCore.QRect(400, 110, 181, 23))
        self.pushButton_SelectDB.setObjectName("pushButton_SelectDB")
        self.lineEdit_Driver = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Driver.setGeometry(QtCore.QRect(120, 220, 181, 20))
        self.lineEdit_Driver.setObjectName("lineEdit_Driver")
        self.lineEdit_Schema = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Schema.setGeometry(QtCore.QRect(120, 310, 181, 20))
        self.lineEdit_Schema.setObjectName("lineEdit_Schema")
        self.label_14 = QtWidgets.QLabel(Dialog)
        self.label_14.setGeometry(QtCore.QRect(20, 250, 91, 16))
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(Dialog)
        self.label_15.setGeometry(QtCore.QRect(20, 310, 91, 16))
        self.label_15.setObjectName("label_15")
        self.lineEdit_Server = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Server.setGeometry(QtCore.QRect(120, 190, 181, 20))
        self.lineEdit_Server.setObjectName("lineEdit_Server")
        self.pushButton_Disconnect = QtWidgets.QPushButton(Dialog)
        self.pushButton_Disconnect.setGeometry(QtCore.QRect(400, 140, 181, 23))
        self.pushButton_Disconnect.setObjectName("pushButton_Disconnect")
        self.pushButton_Update = QtWidgets.QPushButton(Dialog)
        self.pushButton_Update.setEnabled(True)
        self.pushButton_Update.setGeometry(QtCore.QRect(460, 800, 91, 23))
        self.pushButton_Update.setObjectName("pushButton_Update")
        self.label_17 = QtWidgets.QLabel(Dialog)
        self.label_17.setGeometry(QtCore.QRect(30, 780, 111, 21))
        self.label_17.setObjectName("label_17")
        self.lineEdit_Position = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Position.setGeometry(QtCore.QRect(380, 800, 71, 21))
        self.lineEdit_Position.setObjectName("lineEdit_Position")
        self.pushButton_Begin = QtWidgets.QPushButton(Dialog)
        self.pushButton_Begin.setGeometry(QtCore.QRect(640, 20, 91, 23))
        self.pushButton_Begin.setObjectName("pushButton_Begin")
        self.lineEdit_AirLineCodeIATA = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_AirLineCodeIATA.setGeometry(QtCore.QRect(20, 350, 113, 20))
        self.lineEdit_AirLineCodeIATA.setObjectName("lineEdit_AirLineCodeIATA")
        self.lineEdit_AirLineAlias = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_AirLineAlias.setGeometry(QtCore.QRect(140, 800, 231, 20))
        self.lineEdit_AirLineAlias.setObjectName("lineEdit_AirLineAlias")
        self.textEdit_AirLineCity = QtWidgets.QTextEdit(Dialog)
        self.textEdit_AirLineCity.setGeometry(QtCore.QRect(20, 560, 281, 51))
        self.textEdit_AirLineCity.setObjectName("textEdit_AirLineCity")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(30, 690, 101, 16))
        self.label_7.setObjectName("label_7")
        self.textEdit_AirLineName = QtWidgets.QTextEdit(Dialog)
        self.textEdit_AirLineName.setGeometry(QtCore.QRect(20, 480, 281, 51))
        self.textEdit_AirLineName.setObjectName("textEdit_AirLineName")
        self.pushButton_SearchByIATA = QtWidgets.QPushButton(Dialog)
        self.pushButton_SearchByIATA.setGeometry(QtCore.QRect(200, 350, 101, 23))
        self.pushButton_SearchByIATA.setObjectName("pushButton_SearchByIATA")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(30, 620, 181, 16))
        self.label_6.setObjectName("label_6")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(30, 460, 111, 16))
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(30, 540, 151, 16))
        self.label_5.setObjectName("label_5")
        self.label_18 = QtWidgets.QLabel(Dialog)
        self.label_18.setGeometry(QtCore.QRect(390, 780, 61, 20))
        self.label_18.setObjectName("label_18")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(140, 380, 47, 13))
        self.label_2.setObjectName("label_2")
        self.lineEdit_AirLineID = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_AirLineID.setGeometry(QtCore.QRect(20, 800, 113, 20))
        self.lineEdit_AirLineID.setObjectName("lineEdit_AirLineID")
        self.label_19 = QtWidgets.QLabel(Dialog)
        self.label_19.setGeometry(QtCore.QRect(150, 780, 111, 21))
        self.label_19.setObjectName("label_19")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(140, 350, 51, 16))
        self.label.setObjectName("label")
        self.lineEdit_AirLineCodeICAO = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_AirLineCodeICAO.setGeometry(QtCore.QRect(20, 380, 113, 20))
        self.lineEdit_AirLineCodeICAO.setObjectName("lineEdit_AirLineCodeICAO")
        self.pushButton_Next = QtWidgets.QPushButton(Dialog)
        self.pushButton_Next.setGeometry(QtCore.QRect(640, 80, 91, 23))
        self.pushButton_Next.setObjectName("pushButton_Next")
        self.textEdit_AirLineCountry = QtWidgets.QTextEdit(Dialog)
        self.textEdit_AirLineCountry.setGeometry(QtCore.QRect(20, 710, 281, 31))
        self.textEdit_AirLineCountry.setObjectName("textEdit_AirLineCountry")
        self.pushButton_Previous = QtWidgets.QPushButton(Dialog)
        self.pushButton_Previous.setGeometry(QtCore.QRect(640, 50, 91, 23))
        self.pushButton_Previous.setObjectName("pushButton_Previous")
        self.label_24 = QtWidgets.QLabel(Dialog)
        self.label_24.setGeometry(QtCore.QRect(240, 410, 51, 20))
        self.label_24.setObjectName("label_24")
        self.lineEdit_CallSign = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_CallSign.setGeometry(QtCore.QRect(20, 410, 211, 20))
        self.lineEdit_CallSign.setObjectName("lineEdit_CallSign")
        self.pushButton_SearchByICAO = QtWidgets.QPushButton(Dialog)
        self.pushButton_SearchByICAO.setGeometry(QtCore.QRect(200, 380, 101, 23))
        self.pushButton_SearchByICAO.setObjectName("pushButton_SearchByICAO")
        self.pushButton_Insert = QtWidgets.QPushButton(Dialog)
        self.pushButton_Insert.setGeometry(QtCore.QRect(100, 440, 201, 23))
        self.pushButton_Insert.setObjectName("pushButton_Insert")
        self.label_25 = QtWidgets.QLabel(Dialog)
        self.label_25.setGeometry(QtCore.QRect(10, 20, 131, 141))
        self.label_25.setText("")
        self.label_25.setPixmap(QtGui.QPixmap("Значки (Иконки)/folder.ico"))
        self.label_25.setObjectName("label_25")
        self.label_26 = QtWidgets.QLabel(Dialog)
        self.label_26.setGeometry(QtCore.QRect(590, 20, 41, 41))
        self.label_26.setText("")
        self.label_26.setPixmap(QtGui.QPixmap("Значки (Иконки)/a_25.ico"))
        self.label_26.setObjectName("label_26")
        self.label_27 = QtWidgets.QLabel(Dialog)
        self.label_27.setGeometry(QtCore.QRect(590, 70, 41, 41))
        self.label_27.setText("")
        self.label_27.setPixmap(QtGui.QPixmap("Значки (Иконки)/a_21.ico"))
        self.label_27.setObjectName("label_27")
        self.label_28 = QtWidgets.QLabel(Dialog)
        self.label_28.setGeometry(QtCore.QRect(350, 120, 41, 41))
        self.label_28.setText("")
        self.label_28.setPixmap(QtGui.QPixmap("Значки (Иконки)/a_22.ico"))
        self.label_28.setObjectName("label_28")
        self.label_29 = QtWidgets.QLabel(Dialog)
        self.label_29.setGeometry(QtCore.QRect(150, 20, 131, 141))
        self.label_29.setText("")
        self.label_29.setPixmap(QtGui.QPixmap("Значки (Иконки)/Device_Drive_Internal_alt_24444.ico"))
        self.label_29.setObjectName("label_29")
        self.checkBox_Status = QtWidgets.QCheckBox(Dialog)
        self.checkBox_Status.setGeometry(QtCore.QRect(20, 440, 71, 18))
        self.checkBox_Status.setObjectName("checkBox_Status")
        self.dateEdit_CreateDate = QtWidgets.QDateEdit(Dialog)
        self.dateEdit_CreateDate.setGeometry(QtCore.QRect(20, 640, 110, 22))
        self.dateEdit_CreateDate.setObjectName("dateEdit_CreateDate")
        self.graphicsView_Logo = QtWidgets.QGraphicsView(Dialog)
        self.graphicsView_Logo.setGeometry(QtCore.QRect(140, 620, 161, 81))
        self.graphicsView_Logo.setObjectName("graphicsView_Logo")
        self.label_10 = QtWidgets.QLabel(Dialog)
        self.label_10.setGeometry(QtCore.QRect(30, 740, 211, 16))
        self.label_10.setObjectName("label_10")
        self.comboBox_Alliance = QtWidgets.QComboBox(Dialog)
        self.comboBox_Alliance.setGeometry(QtCore.QRect(20, 760, 251, 22))
        self.comboBox_Alliance.setObjectName("comboBox_Alliance")
        self.label_22 = QtWidgets.QLabel(Dialog)
        self.label_22.setGeometry(QtCore.QRect(30, 670, 101, 16))
        self.label_22.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_22.setObjectName("label_22")
        self.label_16 = QtWidgets.QLabel(Dialog)
        self.label_16.setGeometry(QtCore.QRect(340, 60, 111, 16))
        self.label_16.setObjectName("label_16")
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(340, 10, 111, 16))
        self.label_8.setObjectName("label_8")
        self.comboBox_Driver = QtWidgets.QComboBox(Dialog)
        self.comboBox_Driver.setGeometry(QtCore.QRect(290, 80, 291, 22))
        self.comboBox_Driver.setObjectName("comboBox_Driver")
        self.comboBox_DB = QtWidgets.QComboBox(Dialog)
        self.comboBox_DB.setGeometry(QtCore.QRect(290, 30, 291, 22))
        self.comboBox_DB.setObjectName("comboBox_DB")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(310, 170, 541, 611))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.textEdit_AirLineDescription = QtWidgets.QTextEdit(self.tab_1)
        self.textEdit_AirLineDescription.setGeometry(QtCore.QRect(10, 10, 521, 571))
        self.textEdit_AirLineDescription.setObjectName("textEdit_AirLineDescription")
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tab_2_tableWidget_1 = QtWidgets.QTableWidget(self.tab_2)
        self.tab_2_tableWidget_1.setGeometry(QtCore.QRect(10, 10, 521, 571))
        self.tab_2_tableWidget_1.setObjectName("tab_2_tableWidget_1")
        self.tab_2_tableWidget_1.setColumnCount(0)
        self.tab_2_tableWidget_1.setRowCount(0)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tab_3_treeWidget_Hubs = QtWidgets.QTreeWidget(self.tab_3)
        self.tab_3_treeWidget_Hubs.setGeometry(QtCore.QRect(10, 10, 521, 571))
        self.tab_3_treeWidget_Hubs.setObjectName("tab_3_treeWidget_Hubs")
        self.tab_3_treeWidget_Hubs.headerItem().setText(0, "1")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tab_4_listWidget_1 = QtWidgets.QListWidget(self.tab_4)
        self.tab_4_listWidget_1.setGeometry(QtCore.QRect(10, 10, 521, 571))
        self.tab_4_listWidget_1.setObjectName("tab_4_listWidget_1")
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.tab_5_toolBox_1 = QtWidgets.QToolBox(self.tab_5)
        self.tab_5_toolBox_1.setGeometry(QtCore.QRect(20, 10, 57, 561))
        self.tab_5_toolBox_1.setObjectName("tab_5_toolBox_1")
        self.page_1 = QtWidgets.QWidget()
        self.page_1.setGeometry(QtCore.QRect(0, 0, 96, 26))
        self.page_1.setObjectName("page_1")
        self.tab_5_toolBox_1.addItem(self.page_1, "")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 96, 26))
        self.page.setObjectName("page")
        self.tab_5_toolBox_1.addItem(self.page, "")
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setGeometry(QtCore.QRect(0, 0, 96, 26))
        self.page_3.setObjectName("page_3")
        self.tab_5_toolBox_1.addItem(self.page_3, "")
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setGeometry(QtCore.QRect(0, 0, 96, 26))
        self.page_4.setObjectName("page_4")
        self.tab_5_toolBox_1.addItem(self.page_4, "")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 96, 26))
        self.page_2.setObjectName("page_2")
        self.tab_5_toolBox_1.addItem(self.page_2, "")
        self.tab_5_treeView_1 = QtWidgets.QTreeView(self.tab_5)
        self.tab_5_treeView_1.setGeometry(QtCore.QRect(85, 10, 441, 571))
        self.tab_5_treeView_1.setObjectName("tab_5_treeView_1")
        self.tabWidget.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.tab_6_tableView_1 = QtWidgets.QTableView(self.tab_6)
        self.tab_6_tableView_1.setGeometry(QtCore.QRect(10, 10, 521, 571))
        self.tab_6_tableView_1.setObjectName("tab_6_tableView_1")
        self.tabWidget.addTab(self.tab_6, "")

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.tab_5_toolBox_1.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_12.setText(_translate("Dialog", "Драйвер СУБД"))
        self.label_13.setText(_translate("Dialog", "DSN"))
        self.label_11.setText(_translate("Dialog", "Сервер СУБД"))
        self.pushButton_SelectDB.setText(_translate("Dialog", "Подключиться к БД"))
        self.label_14.setText(_translate("Dialog", "Версия ODBC"))
        self.label_15.setText(_translate("Dialog", "Схема"))
        self.pushButton_Disconnect.setText(_translate("Dialog", "Отключиться от БД"))
        self.pushButton_Update.setText(_translate("Dialog", "Записать"))
        self.label_17.setText(_translate("Dialog", "ID"))
        self.pushButton_Begin.setText(_translate("Dialog", "Начало"))
        self.label_7.setText(_translate("Dialog", "Страна"))
        self.pushButton_SearchByIATA.setText(_translate("Dialog", "Поиск"))
        self.label_6.setText(_translate("Dialog", "Дата основания"))
        self.label_3.setText(_translate("Dialog", "Наименование"))
        self.label_5.setText(_translate("Dialog", "Город (Штаб-квартира)"))
        self.label_18.setText(_translate("Dialog", "Позиция"))
        self.label_2.setText(_translate("Dialog", "ICAO"))
        self.label_19.setText(_translate("Dialog", "Псевдоним"))
        self.label.setText(_translate("Dialog", "IATA"))
        self.pushButton_Next.setText(_translate("Dialog", "Следующий"))
        self.pushButton_Previous.setText(_translate("Dialog", "Предыдущий"))
        self.label_24.setText(_translate("Dialog", "Позывной"))
        self.pushButton_SearchByICAO.setText(_translate("Dialog", "Поиск"))
        self.pushButton_Insert.setText(_translate("Dialog", "Поиск и Вставка по IATA и по ICAO"))
        self.checkBox_Status.setText(_translate("Dialog", "Статус"))
        self.label_10.setText(_translate("Dialog", "Альянс"))
        self.label_22.setText(_translate("Dialog", "Логотип"))
        self.label_16.setText(_translate("Dialog", "Драйвер СУБД"))
        self.label_8.setText(_translate("Dialog", "База данных"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("Dialog", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Tab 2"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", "Страница"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Dialog", "Страница"))
        self.tab_5_toolBox_1.setItemText(self.tab_5_toolBox_1.indexOf(self.page_1), _translate("Dialog", "Page 1"))
        self.tab_5_toolBox_1.setItemText(self.tab_5_toolBox_1.indexOf(self.page), _translate("Dialog", "Страница"))
        self.tab_5_toolBox_1.setItemText(self.tab_5_toolBox_1.indexOf(self.page_3), _translate("Dialog", "Страница"))
        self.tab_5_toolBox_1.setItemText(self.tab_5_toolBox_1.indexOf(self.page_4), _translate("Dialog", "Страница"))
        self.tab_5_toolBox_1.setItemText(self.tab_5_toolBox_1.indexOf(self.page_2), _translate("Dialog", "Page 2"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("Dialog", "Страница"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _translate("Dialog", "Страница"))

    # Окончание вставки тела конвертированного ресурсного файла

        # Добавляем функционал класса главного диалога

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Предупреждение', "Закрыть диалог?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

# Конвертация ресурсного файла *.ui -> *.py в терминале командой (командной строке)
# > pyuic5 Qt_Designer_CorrectDialogAirLinesInput.ui -o Qt_Designer_CorrectDialogAirLinesInput.py
class Ui_DialogCorrectAirLineInput(QtWidgets.QDialog):
    def __init__(self):
        # просто сразу вызываем конструктор предка
        super(Ui_DialogCorrectAirLineInput, self).__init__()  # конструктор предка
        # а потом остальное
        pass

    # Начало вставки тела конвертированного ресурсного файла
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(240, 245)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(130, 30, 31, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(130, 60, 31, 16))
        self.label_2.setObjectName("label_2")
        self.lineEdit_AirLineCodeIATA = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_AirLineCodeIATA.setGeometry(QtCore.QRect(10, 30, 113, 20))
        self.lineEdit_AirLineCodeIATA.setObjectName("lineEdit_AirLineCodeIATA")
        self.lineEdit_AirLineCodeICAO = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_AirLineCodeICAO.setGeometry(QtCore.QRect(10, 60, 113, 20))
        self.lineEdit_AirLineCodeICAO.setObjectName("lineEdit_AirLineCodeICAO")
        self.checkBox_Status_IATA = QtWidgets.QCheckBox(Dialog)
        self.checkBox_Status_IATA.setGeometry(QtCore.QRect(170, 30, 61, 18))
        self.checkBox_Status_IATA.setObjectName("checkBox_Status_IATA")
        self.pushButton_SearchInsert = QtWidgets.QPushButton(Dialog)
        self.pushButton_SearchInsert.setGeometry(QtCore.QRect(150, 90, 81, 23))
        self.pushButton_SearchInsert.setObjectName("pushButton_SearchInsert")
        self.checkBox_Status_ICAO = QtWidgets.QCheckBox(Dialog)
        self.checkBox_Status_ICAO.setGeometry(QtCore.QRect(170, 60, 61, 18))
        self.checkBox_Status_ICAO.setObjectName("checkBox_Status_ICAO")
        self.label_25 = QtWidgets.QLabel(Dialog)
        self.label_25.setGeometry(QtCore.QRect(10, 90, 131, 141))
        self.label_25.setText("")
        self.label_25.setPixmap(QtGui.QPixmap("Значки (Иконки)/edit.ico"))
        self.label_25.setObjectName("label_25")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "IATA"))
        self.label_2.setText(_translate("Dialog", "ICAO"))
        self.checkBox_Status_IATA.setText(_translate("Dialog", "Пусто"))
        self.pushButton_SearchInsert.setText(_translate("Dialog", "Вставка"))
        self.checkBox_Status_ICAO.setText(_translate("Dialog", "Пусто"))

    # Окончание вставки тела конвертированного ресурсного файла

        # Добавляем функционал класса главного диалога


# Конвертация ресурсного файла *.ui -> *.py в терминале командой (командной строке)
# > pyuic5 Qt_Designer_CorrectDialogAirCraft.ui -o Qt_Designer_CorrectDialogAirCraft.py
class Ui_DialogCorrectAirCraft(QtWidgets.QDialog):
    def __init__(self):
        # просто сразу вызываем конструктор предка
        super(Ui_DialogCorrectAirCraft, self).__init__()  # конструктор предка
        # а потом остальное
        pass

    # Начало вставки тела конвертированного ресурсного файла
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(740, 830)
        self.label_12 = QtWidgets.QLabel(Dialog)
        self.label_12.setGeometry(QtCore.QRect(20, 220, 91, 16))
        self.label_12.setObjectName("label_12")
        self.lineEdit_DSN = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_DSN.setGeometry(QtCore.QRect(120, 280, 181, 20))
        self.lineEdit_DSN.setObjectName("lineEdit_DSN")
        self.lineEdit_ODBCversion = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_ODBCversion.setGeometry(QtCore.QRect(120, 250, 181, 20))
        self.lineEdit_ODBCversion.setObjectName("lineEdit_ODBCversion")
        self.label_13 = QtWidgets.QLabel(Dialog)
        self.label_13.setGeometry(QtCore.QRect(20, 280, 91, 16))
        self.label_13.setObjectName("label_13")
        self.label_11 = QtWidgets.QLabel(Dialog)
        self.label_11.setGeometry(QtCore.QRect(20, 190, 91, 16))
        self.label_11.setObjectName("label_11")
        self.pushButton_SelectDB = QtWidgets.QPushButton(Dialog)
        self.pushButton_SelectDB.setGeometry(QtCore.QRect(390, 190, 181, 23))
        self.pushButton_SelectDB.setObjectName("pushButton_SelectDB")
        self.lineEdit_Driver = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Driver.setGeometry(QtCore.QRect(120, 220, 181, 20))
        self.lineEdit_Driver.setObjectName("lineEdit_Driver")
        self.lineEdit_Schema = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Schema.setGeometry(QtCore.QRect(120, 310, 181, 20))
        self.lineEdit_Schema.setObjectName("lineEdit_Schema")
        self.label_14 = QtWidgets.QLabel(Dialog)
        self.label_14.setGeometry(QtCore.QRect(20, 250, 91, 16))
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(Dialog)
        self.label_15.setGeometry(QtCore.QRect(20, 310, 91, 16))
        self.label_15.setObjectName("label_15")
        self.lineEdit_Server = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Server.setGeometry(QtCore.QRect(120, 190, 181, 20))
        self.lineEdit_Server.setObjectName("lineEdit_Server")
        self.pushButton_Disconnect = QtWidgets.QPushButton(Dialog)
        self.pushButton_Disconnect.setGeometry(QtCore.QRect(390, 220, 181, 23))
        self.pushButton_Disconnect.setObjectName("pushButton_Disconnect")
        self.pushButton_Update = QtWidgets.QPushButton(Dialog)
        self.pushButton_Update.setEnabled(True)
        self.pushButton_Update.setGeometry(QtCore.QRect(640, 240, 91, 23))
        self.pushButton_Update.setObjectName("pushButton_Update")
        self.lineEdit_Position = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Position.setGeometry(QtCore.QRect(180, 440, 121, 21))
        self.lineEdit_Position.setObjectName("lineEdit_Position")
        self.pushButton_Begin = QtWidgets.QPushButton(Dialog)
        self.pushButton_Begin.setGeometry(QtCore.QRect(640, 10, 91, 23))
        self.pushButton_Begin.setObjectName("pushButton_Begin")
        self.lineEdit_LN = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_LN.setGeometry(QtCore.QRect(20, 350, 113, 20))
        self.lineEdit_LN.setObjectName("lineEdit_LN")
        self.textEdit_Description = QtWidgets.QTextEdit(Dialog)
        self.textEdit_Description.setGeometry(QtCore.QRect(310, 350, 421, 261))
        self.textEdit_Description.setObjectName("textEdit_Description")
        self.pushButton_SearchByLN = QtWidgets.QPushButton(Dialog)
        self.pushButton_SearchByLN.setGeometry(QtCore.QRect(200, 350, 101, 23))
        self.pushButton_SearchByLN.setObjectName("pushButton_SearchByLN")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(20, 470, 101, 16))
        self.label_6.setObjectName("label_6")
        self.label_18 = QtWidgets.QLabel(Dialog)
        self.label_18.setGeometry(QtCore.QRect(220, 420, 61, 20))
        self.label_18.setObjectName("label_18")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(140, 380, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(140, 350, 51, 16))
        self.label.setObjectName("label")
        self.lineEdit_MSN = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_MSN.setGeometry(QtCore.QRect(20, 380, 113, 20))
        self.lineEdit_MSN.setObjectName("lineEdit_MSN")
        self.label_21 = QtWidgets.QLabel(Dialog)
        self.label_21.setGeometry(QtCore.QRect(330, 330, 161, 21))
        self.label_21.setObjectName("label_21")
        self.pushButton_Next = QtWidgets.QPushButton(Dialog)
        self.pushButton_Next.setGeometry(QtCore.QRect(640, 70, 91, 23))
        self.pushButton_Next.setObjectName("pushButton_Next")
        self.pushButton_Previous = QtWidgets.QPushButton(Dialog)
        self.pushButton_Previous.setGeometry(QtCore.QRect(640, 40, 91, 23))
        self.pushButton_Previous.setObjectName("pushButton_Previous")
        self.pushButton_SearchByMSN = QtWidgets.QPushButton(Dialog)
        self.pushButton_SearchByMSN.setGeometry(QtCore.QRect(200, 380, 101, 23))
        self.pushButton_SearchByMSN.setObjectName("pushButton_SearchByMSN")
        self.pushButton_Insert = QtWidgets.QPushButton(Dialog)
        self.pushButton_Insert.setGeometry(QtCore.QRect(630, 210, 101, 23))
        self.pushButton_Insert.setObjectName("pushButton_Insert")
        self.label_25 = QtWidgets.QLabel(Dialog)
        self.label_25.setGeometry(QtCore.QRect(40, 20, 131, 131))
        self.label_25.setText("")
        self.label_25.setPixmap(QtGui.QPixmap("Значки (Иконки)/research.ico"))
        self.label_25.setObjectName("label_25")
        self.label_26 = QtWidgets.QLabel(Dialog)
        self.label_26.setGeometry(QtCore.QRect(590, 10, 41, 41))
        self.label_26.setText("")
        self.label_26.setPixmap(QtGui.QPixmap("Значки (Иконки)/a_25.ico"))
        self.label_26.setObjectName("label_26")
        self.label_27 = QtWidgets.QLabel(Dialog)
        self.label_27.setGeometry(QtCore.QRect(590, 60, 41, 41))
        self.label_27.setText("")
        self.label_27.setPixmap(QtGui.QPixmap("Значки (Иконки)/a_21.ico"))
        self.label_27.setObjectName("label_27")
        self.label_28 = QtWidgets.QLabel(Dialog)
        self.label_28.setGeometry(QtCore.QRect(340, 200, 41, 41))
        self.label_28.setText("")
        self.label_28.setPixmap(QtGui.QPixmap("Значки (Иконки)/a_22.ico"))
        self.label_28.setObjectName("label_28")
        self.dateEdit_BuildDate = QtWidgets.QDateEdit(Dialog)
        self.dateEdit_BuildDate.setGeometry(QtCore.QRect(10, 490, 91, 22))
        self.dateEdit_BuildDate.setObjectName("dateEdit_BuildDate")
        self.label_10 = QtWidgets.QLabel(Dialog)
        self.label_10.setGeometry(QtCore.QRect(30, 520, 211, 16))
        self.label_10.setObjectName("label_10")
        self.comboBox_Model = QtWidgets.QComboBox(Dialog)
        self.comboBox_Model.setGeometry(QtCore.QRect(20, 540, 251, 22))
        self.comboBox_Model.setObjectName("comboBox_Model")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(220, 10, 361, 171))
        self.groupBox.setObjectName("groupBox")
        self.comboBox_DSN = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_DSN.setGeometry(QtCore.QRect(100, 140, 251, 22))
        self.comboBox_DSN.setObjectName("comboBox_DSN")
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setGeometry(QtCore.QRect(110, 120, 211, 16))
        self.label_9.setObjectName("label_9")
        self.radioButton_DSN = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_DSN.setGeometry(QtCore.QRect(10, 140, 82, 18))
        self.radioButton_DSN.setObjectName("radioButton_DSN")
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setGeometry(QtCore.QRect(110, 20, 111, 16))
        self.label_8.setObjectName("label_8")
        self.comboBox_Driver = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_Driver.setGeometry(QtCore.QRect(100, 90, 251, 22))
        self.comboBox_Driver.setObjectName("comboBox_Driver")
        self.label_16 = QtWidgets.QLabel(self.groupBox)
        self.label_16.setGeometry(QtCore.QRect(110, 70, 111, 16))
        self.label_16.setObjectName("label_16")
        self.comboBox_DB = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_DB.setGeometry(QtCore.QRect(100, 40, 251, 22))
        self.comboBox_DB.setObjectName("comboBox_DB")
        self.radioButton_DB = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_DB.setGeometry(QtCore.QRect(10, 40, 82, 18))
        self.radioButton_DB.setObjectName("radioButton_DB")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(140, 410, 47, 13))
        self.label_4.setObjectName("label_4")
        self.lineEdit_SN = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_SN.setGeometry(QtCore.QRect(20, 410, 113, 20))
        self.lineEdit_SN.setObjectName("lineEdit_SN")
        self.label_20 = QtWidgets.QLabel(Dialog)
        self.label_20.setGeometry(QtCore.QRect(140, 440, 47, 13))
        self.label_20.setObjectName("label_20")
        self.lineEdit_CN = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_CN.setGeometry(QtCore.QRect(20, 440, 113, 20))
        self.lineEdit_CN.setObjectName("lineEdit_CN")
        self.dateEdit_RetireDate = QtWidgets.QDateEdit(Dialog)
        self.dateEdit_RetireDate.setGeometry(QtCore.QRect(110, 490, 91, 22))
        self.dateEdit_RetireDate.setObjectName("dateEdit_RetireDate")
        self.label_22 = QtWidgets.QLabel(Dialog)
        self.label_22.setGeometry(QtCore.QRect(120, 470, 101, 16))
        self.label_22.setObjectName("label_22")
        self.label_23 = QtWidgets.QLabel(Dialog)
        self.label_23.setGeometry(QtCore.QRect(30, 560, 211, 16))
        self.label_23.setObjectName("label_23")
        self.comboBox_Manufacturer = QtWidgets.QComboBox(Dialog)
        self.comboBox_Manufacturer.setGeometry(QtCore.QRect(20, 580, 251, 22))
        self.comboBox_Manufacturer.setObjectName("comboBox_Manufacturer")
        self.pushButton_Registration = QtWidgets.QPushButton(Dialog)
        self.pushButton_Registration.setGeometry(QtCore.QRect(10, 620, 101, 23))
        self.pushButton_Registration.setObjectName("pushButton_Registration")
        self.pushButton_Owner = QtWidgets.QPushButton(Dialog)
        self.pushButton_Owner.setGeometry(QtCore.QRect(250, 620, 101, 23))
        self.pushButton_Owner.setObjectName("pushButton_Owner")
        self.pushButton_Operator = QtWidgets.QPushButton(Dialog)
        self.pushButton_Operator.setGeometry(QtCore.QRect(490, 620, 101, 23))
        self.pushButton_Operator.setObjectName("pushButton_Operator")
        self.textEdit_SourceCSVFile = QtWidgets.QTextEdit(Dialog)
        self.textEdit_SourceCSVFile.setGeometry(QtCore.QRect(310, 270, 421, 61))
        self.textEdit_SourceCSVFile.setObjectName("textEdit_SourceCSVFile")
        self.label_24 = QtWidgets.QLabel(Dialog)
        self.label_24.setGeometry(QtCore.QRect(330, 250, 161, 21))
        self.label_24.setObjectName("label_24")
        self.treeView_Registration = QtWidgets.QTreeView(Dialog)
        self.treeView_Registration.setGeometry(QtCore.QRect(10, 650, 231, 171))
        self.treeView_Registration.setObjectName("treeView_Registration")
        self.treeView_Owner = QtWidgets.QTreeView(Dialog)
        self.treeView_Owner.setGeometry(QtCore.QRect(250, 650, 231, 171))
        self.treeView_Owner.setObjectName("treeView_Owner")
        self.treeView_Operator = QtWidgets.QTreeView(Dialog)
        self.treeView_Operator.setGeometry(QtCore.QRect(490, 650, 241, 171))
        self.treeView_Operator.setObjectName("treeView_Operator")
        self.label_30 = QtWidgets.QLabel(Dialog)
        self.label_30.setGeometry(QtCore.QRect(220, 470, 101, 16))
        self.label_30.setObjectName("label_30")
        self.dateEdit_EndDate = QtWidgets.QDateEdit(Dialog)
        self.dateEdit_EndDate.setGeometry(QtCore.QRect(210, 490, 91, 22))
        self.dateEdit_EndDate.setObjectName("dateEdit_EndDate")
        self.label_29 = QtWidgets.QLabel(Dialog)
        self.label_29.setGeometry(QtCore.QRect(590, 110, 131, 91))
        self.label_29.setText("")
        self.label_29.setPixmap(QtGui.QPixmap("Значки (Иконки)/floppy.ico"))
        self.label_29.setObjectName("label_29")
        self.groupBox.raise_()
        self.label_12.raise_()
        self.lineEdit_DSN.raise_()
        self.lineEdit_ODBCversion.raise_()
        self.label_13.raise_()
        self.label_11.raise_()
        self.pushButton_SelectDB.raise_()
        self.lineEdit_Driver.raise_()
        self.lineEdit_Schema.raise_()
        self.label_14.raise_()
        self.label_15.raise_()
        self.lineEdit_Server.raise_()
        self.pushButton_Disconnect.raise_()
        self.pushButton_Update.raise_()
        self.lineEdit_Position.raise_()
        self.pushButton_Begin.raise_()
        self.lineEdit_LN.raise_()
        self.textEdit_Description.raise_()
        self.pushButton_SearchByLN.raise_()
        self.label_6.raise_()
        self.label_18.raise_()
        self.label_2.raise_()
        self.label.raise_()
        self.lineEdit_MSN.raise_()
        self.label_21.raise_()
        self.pushButton_Next.raise_()
        self.pushButton_Previous.raise_()
        self.pushButton_SearchByMSN.raise_()
        self.pushButton_Insert.raise_()
        self.label_25.raise_()
        self.label_26.raise_()
        self.label_27.raise_()
        self.label_28.raise_()
        self.dateEdit_BuildDate.raise_()
        self.label_10.raise_()
        self.comboBox_Model.raise_()
        self.label_4.raise_()
        self.lineEdit_SN.raise_()
        self.label_20.raise_()
        self.lineEdit_CN.raise_()
        self.dateEdit_RetireDate.raise_()
        self.label_22.raise_()
        self.label_23.raise_()
        self.comboBox_Manufacturer.raise_()
        self.pushButton_Registration.raise_()
        self.pushButton_Owner.raise_()
        self.pushButton_Operator.raise_()
        self.textEdit_SourceCSVFile.raise_()
        self.label_24.raise_()
        self.treeView_Registration.raise_()
        self.treeView_Owner.raise_()
        self.treeView_Operator.raise_()
        self.label_30.raise_()
        self.dateEdit_EndDate.raise_()
        self.label_29.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_12.setText(_translate("Dialog", "Драйвер СУБД"))
        self.label_13.setText(_translate("Dialog", "DSN"))
        self.label_11.setText(_translate("Dialog", "Сервер СУБД"))
        self.pushButton_SelectDB.setText(_translate("Dialog", "Подключиться к БД или к DSN"))
        self.label_14.setText(_translate("Dialog", "Версия ODBC"))
        self.label_15.setText(_translate("Dialog", "Схема"))
        self.pushButton_Disconnect.setText(_translate("Dialog", "Отключиться от БД или от DSN"))
        self.pushButton_Update.setText(_translate("Dialog", "Записать"))
        self.pushButton_Begin.setText(_translate("Dialog", "Начало"))
        self.pushButton_SearchByLN.setText(_translate("Dialog", "Поиск"))
        self.label_6.setText(_translate("Dialog", "Дата сборки"))
        self.label_18.setText(_translate("Dialog", "Позиция"))
        self.label_2.setText(_translate("Dialog", "MSN"))
        self.label.setText(_translate("Dialog", "LN"))
        self.label_21.setText(_translate("Dialog", "Описание"))
        self.pushButton_Next.setText(_translate("Dialog", "Следующий"))
        self.pushButton_Previous.setText(_translate("Dialog", "Предыдущий"))
        self.pushButton_SearchByMSN.setText(_translate("Dialog", "Поиск"))
        self.pushButton_Insert.setText(_translate("Dialog", "Вставить новый"))
        self.label_10.setText(_translate("Dialog", "Модель"))
        self.groupBox.setTitle(_translate("Dialog", "Способ подключения к базе данных самолетов"))
        self.label_9.setText(_translate("Dialog", "DSN (сист. или пользов.)"))
        self.radioButton_DSN.setText(_translate("Dialog", "через DSN"))
        self.label_8.setText(_translate("Dialog", "База данных"))
        self.label_16.setText(_translate("Dialog", "Драйвер СУБД"))
        self.radioButton_DB.setText(_translate("Dialog", "через БД"))
        self.label_4.setText(_translate("Dialog", "SN"))
        self.label_20.setText(_translate("Dialog", "СN"))
        self.label_22.setText(_translate("Dialog", "Дата разборки"))
        self.label_23.setText(_translate("Dialog", "Фирма-изготовитель"))
        self.pushButton_Registration.setText(_translate("Dialog", "Регистрация"))
        self.pushButton_Owner.setText(_translate("Dialog", "Владелец"))
        self.pushButton_Operator.setText(_translate("Dialog", "Оператор"))
        self.label_24.setText(_translate("Dialog", "Источник информации"))
        self.label_30.setText(_translate("Dialog", "Дата окончания"))

    # Окончание вставки тела конвертированного ресурсного файла

        # Добавляем функционал класса главного диалога

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Предупреждение', "Закрыть диалог?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
