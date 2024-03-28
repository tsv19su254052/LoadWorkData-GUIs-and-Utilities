#  Interpreter 3.7 -> 3.10


# QtSQL медленнее, чем pyodbc
import pyodbc
import sys
from PyQt5 import QtWidgets, QtCore
import io
import folium
from PyQt5.QtWebEngineWidgets import QWebEngineView  # pip install PyQtWebEngine -> поставил

# Импорт пользовательской библиотеки (файла *.py в этой же папке)
import Classes


# Делаем экземпляры
A = Classes.AirPort()
S = Classes.Servers()
# Добавляем аттрибуты
#S.ServerName = "data-server-1.movistar.vrn.skylink.local"  # указал ресурсную запись из DNS
S.ServerName = "localhost\mssqlserver15"  # указал инстанс
#S.ServerName = "localhost\sqldeveloper"  # указал инстанс
S.Connected_AL = False
S.Connected_AC = False
S.Connected_RT = False
S.Connected_FN = False


# Основная функция
def myApplication():
    # Одно прикладное приложение
    # todo Делаем сопряжение экземпляров классов с SQL-ными базами данных - семантическими противоположностями ООП, примеров мало
    # fixme Сделать скрипт, который копирует данные таблицы по коду IATA строку за строкой из одной базы в другую
    myApp = QtWidgets.QApplication(sys.argv)
    # Делаем экземпляры
    # fixme Правильно сделать экземпляр с композицией
    myDialog = Classes.Ui_DialogCorrectAirPortsWithMap()
    myDialog.setupUi(Dialog=myDialog)  # надо вызывать явно
    myDialog.setFixedSize(920, 780)
    myDialog.setWindowTitle('АэроПорты')
    # Дополняем функционал экземпляра главного диалога
    # Переводим в исходное состояние
    myDialog.comboBox_Driver.setToolTip("предпочтительно - драйвер ODBC для SDK SQL Server-а \n(работает во всех режимах, полностью функционален, расходует больше ресурсов сервера) \nдля просмотра и внесения исправлений компл. драйвер SQL Server-а \n (не отрабатывает вложенные обработки исключений)")
    myDialog.pushButton_ConnectDB.setToolTip("После подключения нажмите кнопку Поиск")
    myDialog.pushButton_DisconnectDB.setToolTip("Перед закрытием диалога отключиться от базы данных")
    myDialog.pushButton_DisconnectDB.setEnabled(False)
    # Параметры соединения с сервером
    myDialog.lineEdit_Server.setEnabled(False)
    myDialog.lineEdit_Driver.setEnabled(False)
    myDialog.lineEdit_ODBCversion.setEnabled(False)
    myDialog.lineEdit_DSN.setEnabled(False)
    myDialog.lineEdit_Schema.setEnabled(False)
    myDialog.lineEdit_AirPortCodeIATA.setEnabled(False)
    myDialog.lineEdit_AirPortCodeICAO.setEnabled(False)
    myDialog.lineEdit_AirPortCodeFAA_LID.setEnabled(False)
    myDialog.pushButton_HyperLinksChange.setToolTip("Изменение адресов ссылок")
    myDialog.pushButton_HyperLinksChange.setEnabled(False)
    myDialog.pushButton_SearchByIATA.setToolTip("Поиск по коду IATA (дубликаты не предусматриваются)")
    myDialog.pushButton_SearchByIATA.setEnabled(False)
    myDialog.pushButton_SearchByICAO.setToolTip("Поиск по коду ICAO (дубликаты не предусматриваются)")
    myDialog.pushButton_SearchByICAO.setEnabled(False)
    myDialog.pushButton_Insert.setToolTip("Поиск и вставка по коду IATA\nЕсли код IATA пустой - это вероятно просто аэродром, без инфраструктуры")
    myDialog.pushButton_Insert.setEnabled(False)
    myDialog.textEdit_AirPortName.setEnabled(False)
    myDialog.textEdit_AirPortCity.setEnabled(False)
    myDialog.textEdit_AirPortCounty.setEnabled(False)
    myDialog.textEdit_AirPortCountry.setEnabled(False)
    myDialog.lineEdit_AirPortLatitude.setEnabled(False)
    myDialog.lineEdit_AirPortLongitude.setEnabled(False)
    myDialog.lineEdit_HeightAboveSeaLevel.setEnabled(False)
    myDialog.textEdit_SourceCSVFile.setEnabled(False)
    myDialog.textBrowser_HyperLinks.setOpenExternalLinks(True)
    myDialog.textBrowser_HyperLinks.setReadOnly(True)
    myDialog.textBrowser_HyperLinks.setEnabled(False)
    myDialog.tabWidget.setTabText(0, "Описание")
    myDialog.tabWidget.setTabText(1, "Сооружения")
    myDialog.tabWidget.setTabText(2, "Случаи")
    myDialog.tabWidget.setTabText(3, "На карте")
    myDialog.tabWidget.setTabText(4, "Дополнительно")
    myDialog.tab_1.setToolTip("Общее описание аэропорта. История развития")
    myDialog.tab_2.setToolTip("Инфраструктура аэропорта, сооружения, хабы, арендаторы, склады, ангары")
    myDialog.tab_3.setToolTip("Случаи и инциденты")
    myDialog.tab_4.setToolTip("Расположение объекта на карте")
    myDialog.tab_5.setToolTip("Оснащение аппаратурой взаимодействия с самолетами (пока в разработке)")
    myDialog.textEdit_AirPortDescription.setEnabled(False)
    myDialog.textEdit_AirPortFacilities.setEnabled(False)
    myDialog.textEdit_Incidents.setEnabled(False)
    myDialog.verticalLayout.setEnabled(False)
    myDialog.pushButton_Begin.setToolTip("После нажатия использовать Поиск")
    myDialog.pushButton_Begin.setEnabled(False)
    myDialog.pushButton_Update.setToolTip("Запись внесенных изменений в БД \n Перед нажатием правильно заполнить и проверить введенные данные")
    myDialog.pushButton_Update.setEnabled(False)
    # Добавляем атрибут ввода
    myDialog.lineEditCodeIATA = QtWidgets.QLineEdit()
    myDialog.lineEditCodeICAO = QtWidgets.QLineEdit()
    #myDialog.lineEditReserveDB = QtWidgets.QLineEdit()
    # Добавляем базы данных в выпадающий список
    myDialog.comboBox_DB.addItem("AirPortsAndRoutesDBNew62")
    # Получаем список драйверов баз данных
    # Добавляем атрибут DriversODBC по ходу действия
    S.DriversODBC = pyodbc.drivers()
    if S.DriversODBC:
        for DriverODBC in S.DriversODBC:
            if not DriverODBC:
                break
            myDialog.comboBox_Driver.addItem(str(DriverODBC))
    # Привязки обработчиков
    myDialog.pushButton_ConnectDB.clicked.connect(lambda: PushButtonConnectDB())
    myDialog.pushButton_DisconnectDB.clicked.connect(lambda: PushButtonDisconnect())
    myDialog.pushButton_HyperLinksChange.clicked.connect(lambda: PushButtonChangeHyperLinks())
    myDialog.pushButton_SearchByIATA.clicked.connect(lambda: PushButtonSearchByIATA())
    myDialog.pushButton_SearchByICAO.clicked.connect(lambda: PushButtonSearchByICAO())
    myDialog.pushButton_Insert.clicked.connect(lambda: PushButtonInsert())
    myDialog.pushButton_Update.clicked.connect(lambda: PushButtonUpdate())

    def PushButtonConnectDB():
        if not S.Connected_RT:
            # Переводим в неактивное состояние
            myDialog.pushButton_ConnectDB.setEnabled(False)
            # Подключаемся к базе данных по выбранному источнику
            ChoiceDB = myDialog.comboBox_DB.currentText()
            ChoiceDriver = myDialog.comboBox_Driver.currentText()
            # Добавляем атрибуты DataBase, DriverODBC
            S.DataBase = str(ChoiceDB)
            S.DriverODBC = str(ChoiceDriver)
            try:
                # Добавляем атрибут cnxn
                # через драйвер СУБД + клиентский API-курсор
                S.cnxnAL = pyodbc.connect(driver=S.DriverODBC, server=S.ServerName, database=S.DataBase)
                S.cnxnAC = pyodbc.connect(driver=S.DriverODBC, server=S.ServerName, database=S.DataBase)
                S.cnxnRT = pyodbc.connect(driver=S.DriverODBC, server=S.ServerName, database=S.DataBase)
                S.cnxnFN = pyodbc.connect(driver=S.DriverODBC, server=S.ServerName, database=S.DataBase)
                print("  База данных ", S.DataBase, " подключена")
                S.Connected_AL = True
                S.Connected_AC = True
                S.Connected_RT = True
                S.Connected_FN = True
                # Разрешаем транзакции и вызываем функцию commit() при необходимости в явном виде, в СУБД по умолчанию FALSE
                S.cnxnAL.autocommit = False
                S.cnxnAC.autocommit = False
                S.cnxnRT.autocommit = False
                S.cnxnFN.autocommit = False
                print("autocommit is disabled")
                # Ставим набор курсоров
                # КУРСОР нужен для перехода функционального языка формул на процедурный или для вставки процедурных кусков в функциональный скрипт.
                # Способы реализации курсоров:
                #  - SQL, Transact-SQL,
                #  - серверные API-курсоры (OLE DB, ADO, ODBC),
                #  - клиентские API-курсоры (выборка кэшируется на клиенте)
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
                # Добавляем атрибуты seek...
                S.seekAL = S.cnxnAL.cursor()
                S.seekAC = S.cnxnAC.cursor()
                S.seekRT = S.cnxnRT.cursor()
                S.seekFN = S.cnxnFN.cursor()
                print("seeks is on")
                # Переводим в рабочее состояние (продолжение)
                myDialog.comboBox_DB.setEnabled(False)
                myDialog.comboBox_Driver.setEnabled(False)
                myDialog.pushButton_DisconnectDB.setEnabled(True)
                myDialog.pushButton_Begin.setEnabled(True)  # кнопка "Начало"
                # SQL Server
                myDialog.lineEdit_Server.setText(S.cnxnRT.getinfo(pyodbc.SQL_SERVER_NAME))
                myDialog.lineEdit_Server.setEnabled(True)
                # Драйвер
                myDialog.lineEdit_Driver.setText(S.cnxnRT.getinfo(pyodbc.SQL_DRIVER_NAME))
                myDialog.lineEdit_Driver.setEnabled(True)
                # версия ODBC
                myDialog.lineEdit_ODBCversion.setText(S.cnxnRT.getinfo(pyodbc.SQL_ODBC_VER))
                myDialog.lineEdit_ODBCversion.setEnabled(True)
                # Источник данных
                myDialog.lineEdit_DSN.setText(S.cnxnRT.getinfo(pyodbc.SQL_DATA_SOURCE_NAME))
                myDialog.lineEdit_DSN.setEnabled(True)
                # Схема (если из-под другой учетки, то выводит имя учетки)
                # todo Схема по умолчанию - dbo
                myDialog.lineEdit_Schema.setText(S.cnxnRT.getinfo(pyodbc.SQL_USER_NAME))
                myDialog.lineEdit_Schema.setEnabled(True)
            except Exception:
                # Переводим в рабочее состояние
                myDialog.pushButton_ConnectDB.setEnabled(True)
                message = QtWidgets.QMessageBox()
                message.setText("Нет подключения к базе данных аэропортов")
                message.setIcon(QtWidgets.QMessageBox.Warning)
                message.exec_()
            else:
                pass
            finally:
                pass
        # переводим в рабочее состояние (окончание)
        myDialog.lineEdit_AirPortCodeIATA.setEnabled(True)  # применям Решение 4 Проблемы 1
        myDialog.lineEdit_AirPortCodeICAO.setEnabled(True)
        myDialog.lineEdit_AirPortCodeFAA_LID.setEnabled(True)  # код FAA пока не используется - поле ввода неактивное
        myDialog.pushButton_HyperLinksChange.setEnabled(True)
        myDialog.pushButton_SearchByIATA.setEnabled(True)
        myDialog.pushButton_SearchByICAO.setEnabled(True)
        myDialog.pushButton_Insert.setEnabled(True)
        myDialog.textEdit_AirPortName.setEnabled(True)
        myDialog.textEdit_AirPortCity.setEnabled(True)
        myDialog.textEdit_AirPortCounty.setEnabled(True)
        myDialog.textEdit_AirPortCountry.setEnabled(True)
        myDialog.lineEdit_AirPortLatitude.setEnabled(True)
        myDialog.lineEdit_AirPortLongitude.setEnabled(True)
        myDialog.lineEdit_HeightAboveSeaLevel.setEnabled(True)
        myDialog.textEdit_SourceCSVFile.setEnabled(True)
        myDialog.textBrowser_HyperLinks.setEnabled(True)
        myDialog.textEdit_AirPortDescription.setEnabled(True)
        myDialog.textEdit_AirPortFacilities.setEnabled(True)
        myDialog.textEdit_Incidents.setEnabled(True)
        myDialog.verticalLayout.setEnabled(True)
        myDialog.pushButton_Begin.setEnabled(False)
        myDialog.pushButton_Update.setEnabled(True)
        A.Position = 1

    def PushButtonDisconnect():
        # кнопка 'Отключиться от базы данных' нажата
        if S.Connected_RT:
            # Снимаем курсоры
            S.seekAL.close()
            S.seekAC.close()
            S.seekRT.close()
            S.seekFN.close()
            # Отключаемся от базы данных
            S.cnxnAL.close()
            S.cnxnAC.close()
            S.cnxnRT.close()
            S.cnxnFN.close()
            # Снимаем флаги
            S.Connected_AL = False
            S.Connected_AC = False
            S.Connected_RT = False
            S.Connected_FN = False
            # Переключаем в исходное состояние
            myDialog.comboBox_DB.setEnabled(True)
            myDialog.comboBox_Driver.setEnabled(True)
            myDialog.pushButton_ConnectDB.setEnabled(True)
            myDialog.pushButton_DisconnectDB.setEnabled(False)
            # Параметры соединения с сервером
            myDialog.lineEdit_Server.setEnabled(False)
            myDialog.lineEdit_Driver.setEnabled(False)
            myDialog.lineEdit_ODBCversion.setEnabled(False)
            myDialog.lineEdit_DSN.setEnabled(False)
            myDialog.lineEdit_Schema.setEnabled(False)
            myDialog.lineEdit_AirPortCodeIATA.setEnabled(False)
            myDialog.lineEdit_AirPortCodeICAO.setEnabled(False)
            myDialog.lineEdit_AirPortCodeFAA_LID.setEnabled(False)
            myDialog.pushButton_HyperLinksChange.setEnabled(False)
            myDialog.pushButton_SearchByIATA.setEnabled(False)
            myDialog.pushButton_SearchByICAO.setEnabled(False)
            myDialog.pushButton_Insert.setEnabled(False)
            myDialog.textEdit_AirPortName.setEnabled(False)
            myDialog.textEdit_AirPortCity.setEnabled(False)
            myDialog.textEdit_AirPortCounty.setEnabled(False)
            myDialog.textEdit_AirPortCountry.setEnabled(False)
            myDialog.lineEdit_AirPortLatitude.setEnabled(False)
            myDialog.lineEdit_AirPortLongitude.setEnabled(False)
            myDialog.lineEdit_HeightAboveSeaLevel.setEnabled(False)
            myDialog.textEdit_SourceCSVFile.setEnabled(False)
            myDialog.textBrowser_HyperLinks.setEnabled(False)
            myDialog.textEdit_AirPortDescription.setEnabled(False)
            myDialog.textEdit_AirPortFacilities.setEnabled(False)
            myDialog.textEdit_Incidents.setEnabled(False)
            myDialog.verticalLayout.setEnabled(False)
            myDialog.pushButton_Begin.setEnabled(False)
            myDialog.pushButton_Update.setEnabled(False)

    def SetFields():
        # Выводим запись
        myDialog.lineEdit_AirPortCodeIATA.setText(str(A.AirPortCodeIATA))
        #myDialog.lineEdit_AirPortCodeIATA.setEnabled(False)
        myDialog.lineEdit_AirPortCodeICAO.setText(str(A.AirPortCodeICAO))
        myDialog.textEdit_AirPortName.clear()
        myDialog.textEdit_AirPortName.append(str(A.AirPortName))
        myDialog.textEdit_AirPortCity.clear()
        myDialog.textEdit_AirPortCity.append(str(A.AirPortCity))
        myDialog.textEdit_AirPortCounty.clear()
        myDialog.textEdit_AirPortCounty.append(str(A.AirPortCounty))
        myDialog.textEdit_AirPortCountry.clear()
        myDialog.textEdit_AirPortCountry.append(str(A.AirPortCountry))
        myDialog.lineEdit_AirPortLatitude.setText(str(A.AirPortLatitude))
        myDialog.lineEdit_AirPortLongitude.setText(str(A.AirPortLongitude))
        myDialog.lineEdit_HeightAboveSeaLevel.setText(str(A.HeightAboveSeaLevel))
        myDialog.textEdit_SourceCSVFile.clear()
        myDialog.textEdit_SourceCSVFile.append(str(A.SourceCSVFile))
        myDialog.textBrowser_HyperLinks.clear()
        myDialog.textBrowser_HyperLinks.append("<a href=" + str(A.SourceCSVFile) + ">Wikipedia</a>")
        myDialog.textBrowser_HyperLinks.append("<a href=" + str(A.SourceCSVFile) + ">Сайт аэропорта или аэродрома</a>")
        myDialog.textBrowser_HyperLinks.append("<a href=" + str(A.SourceCSVFile) + ">Сайт оператора аэропорта</a>")
        myDialog.textEdit_AirPortDescription.clear()
        myDialog.textEdit_AirPortDescription.append(str(A.AirPortDescription))
        myDialog.textEdit_AirPortFacilities.clear()
        myDialog.textEdit_AirPortFacilities.append(A.AirPortFacilities)
        myDialog.textEdit_Incidents.clear()
        myDialog.textEdit_Incidents.append(A.AirPortIncidents)
        coordinates = (A.AirPortLatitude, A.AirPortLongitude)
        # Варианты карт: OpenStreetMap (подробная цветная), CartoDB Positron (серенькая), CartoDB Voyager (аскетичная, мало подписей и меток), NASAGIBS Blue Marble (пока не отрисовывается)
        m = folium.Map(tiles='OpenStreetMap',
                       zoom_start=13,
                       location=coordinates)
        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)
        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        if myDialog.verticalLayout is not None:
            while myDialog.verticalLayout.count():
                child = myDialog.verticalLayout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    myDialog.verticalLayout.clearLayout(child.layout())
        myDialog.verticalLayout.addWidget(webView)

    def PushButtonChangeHyperLinks():
        pass

    def PushButtonSearchByIATA():
        # Кнопка "Поиск" нажата
        LineCodeIATA, ok = QtWidgets.QInputDialog.getText(myDialog, "Код IATA", "Введите код IATA")
        if ok:
            myDialog.lineEditCodeIATA.setText(str(LineCodeIATA))
            Code = myDialog.lineEditCodeIATA.text()
            DBAirPort = S.QueryAirPortByIATA(Code)
            # fixme Решение 3 - не перезаписывать код IATA (Недостаток - можно сделать дубликат по коду ICAO, их много, возможно это НОРМА, исправлять только вручную)
            # fixme Решение 4 - код IATA всегда неактивный, он вводится только при вставке
            if DBAirPort is not None:
                A.Position = DBAirPort.AirPortUniqueNumber
                A.AirPortCodeIATA = DBAirPort.AirPortCodeIATA
                A.AirPortCodeICAO = DBAirPort.AirPortCodeICAO
                A.AirPortName = DBAirPort.AirPortName
                A.AirPortCity = DBAirPort.AirPortCity
                A.AirPortCounty = DBAirPort.AirPortCounty
                A.AirPortCountry = DBAirPort.AirPortCountry
                A.AirPortLatitude = DBAirPort.AirPortLatitude
                A.AirPortLongitude = DBAirPort.AirPortLongitude
                A.HeightAboveSeaLevel = DBAirPort.HeightAboveSeaLevel
                A.SourceCSVFile = DBAirPort.SourceCSVFile
                A.AirPortDescription = DBAirPort.AirPortDescription
                A.AirPortFacilities = DBAirPort.AirPortFacilities
                A.AirPortIncidents = DBAirPort.AirPortIncidents
            elif DBAirPort is None:
                message = QtWidgets.QMessageBox()
                message.setText("Запись не найдена. Можете вставить новую запись")
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.exec_()
                # Вставка новой записи
                PushButtonInsert()
            else:
                pass
            SetFields()

    def PushButtonSearchByICAO():
        # Кнопка "Поиск" нажата
        LineCodeICAO, ok = QtWidgets.QInputDialog.getText(myDialog, "Код ICAO", "Введите код ICAO")
        if ok:
            myDialog.lineEditCodeICAO.setText(str(LineCodeICAO))
            Code = myDialog.lineEditCodeICAO.text()
            DBAirPort = S.QueryAirPortByICAO(Code)
            if DBAirPort is not None:
                A.Position = DBAirPort.AirPortUniqueNumber
                A.AirPortCodeIATA = DBAirPort.AirPortCodeIATA
                A.AirPortCodeICAO = DBAirPort.AirPortCodeICAO
                A.AirPortName = DBAirPort.AirPortName
                A.AirPortCity = DBAirPort.AirPortCity
                A.AirPortCounty = DBAirPort.AirPortCounty
                A.AirPortCountry = DBAirPort.AirPortCountry
                A.AirPortLatitude = DBAirPort.AirPortLatitude
                A.AirPortLongitude = DBAirPort.AirPortLongitude
                A.HeightAboveSeaLevel = DBAirPort.HeightAboveSeaLevel
                A.SourceCSVFile = DBAirPort.SourceCSVFile
                A.AirPortDescription = DBAirPort.AirPortDescription
                A.AirPortFacilities = DBAirPort.AirPortFacilities
                A.AirPortIncidents = DBAirPort.AirPortIncidents
            elif DBAirPort is None:
                message = QtWidgets.QMessageBox()
                message.setText("Запись не найдена")
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.exec_()
            else:
                pass
            SetFields()

    def PushButtonInsert():
        # кнопка 'Вставить новый' нажата
        LineCodeIATA, ok = QtWidgets.QInputDialog.getText(myDialog, "Код IATA", "Введите новый код IATA")
        if ok:
            myDialog.lineEditCodeIATA.setText(str(LineCodeIATA))
            Code = myDialog.lineEditCodeIATA.text()
            DBAirPort = S.QueryAirPortByIATA(Code)

            def Transfer():
                A.Position = DBAirPort.AirPortUniqueNumber
                A.AirPortCodeIATA = DBAirPort.AirPortCodeIATA
                A.AirPortCodeICAO = DBAirPort.AirPortCodeICAO
                A.AirPortName = DBAirPort.AirPortName
                A.AirPortCity = DBAirPort.AirPortCity
                A.AirPortCounty = DBAirPort.AirPortCounty
                A.AirPortCountry = DBAirPort.AirPortCountry
                A.AirPortLatitude = DBAirPort.AirPortLatitude
                A.AirPortLongitude = DBAirPort.AirPortLongitude
                A.HeightAboveSeaLevel = DBAirPort.HeightAboveSeaLevel
                A.SourceCSVFile = DBAirPort.SourceCSVFile
                A.AirPortDescription = DBAirPort.AirPortDescription
                A.AirPortFacilities = DBAirPort.AirPortFacilities
                A.AirPortIncidents = DBAirPort.AirPortIncidents
                SetFields()

            if DBAirPort is not None:
                # Переходим на найденную запись
                Transfer()
                message = QtWidgets.QMessageBox()
                message.setText("Такая запись есть. Вставляйте через поиск")
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.exec_()
            elif DBAirPort is None:
                # Вставка новой строки
                ResultInsert = S.InsertAirPortByIATA(Code)
                if ResultInsert:
                    DBAirPort = S.QueryAirPortByIATA(Code)
                    if DBAirPort is not None:
                        Transfer()
                    else:
                        message = QtWidgets.QMessageBox()
                        message.setText("Запись не прочиталась. Посмотрите ее через поиск")
                        message.setIcon(QtWidgets.QMessageBox.Warning)
                        message.exec_()
                else:
                    message = QtWidgets.QMessageBox()
                    message.setText("Запись не вставилась")
                    message.setIcon(QtWidgets.QMessageBox.Warning)
                    message.exec_()

    def CommonPart():
        DBAirPort = S.QueryAirPortByPK(A.Position)
        if DBAirPort is not None:
            A.AirPortCodeIATA = DBAirPort.AirPortCodeIATA
            A.AirPortCodeICAO = DBAirPort.AirPortCodeICAO
            A.AirPortName = DBAirPort.AirPortName
            A.AirPortCity = DBAirPort.AirPortCity
            A.AirPortCounty = DBAirPort.AirPortCounty
            A.AirPortCountry = DBAirPort.AirPortCountry
            A.AirPortLatitude = DBAirPort.AirPortLatitude
            A.AirPortLongitude = DBAirPort.AirPortLongitude
            A.HeightAboveSeaLevel = DBAirPort.HeightAboveSeaLevel
            A.SourceCSVFile = DBAirPort.SourceCSVFile
            A.AirPortDescription = DBAirPort.AirPortDescription
            A.AirPortFacilities = DBAirPort.AirPortFacilities
            A.AirPortIncidents = DBAirPort.AirPortIncidents
            SetFields()
            return True
        elif DBAirPort is None:
            message = QtWidgets.QMessageBox()
            message.setText("Запись не найдена")
            message.setIcon(QtWidgets.QMessageBox.Information)
            message.exec_()
            return False
        else:
            message = QtWidgets.QMessageBox()
            message.setText("Запись не прочиталась")
            message.setIcon(QtWidgets.QMessageBox.Warning)
            message.exec_()
            return False

    def PushButtonUpdate():
        # Кнопка "Записать"
        # todo вставить диалог выбора и проверки сертификата (ЭЦП) и условный переход с проверкой
        A.AirPortCodeICAO = myDialog.lineEdit_AirPortCodeICAO.text()
        A.AirPortName = myDialog.textEdit_AirPortName.toPlainText()
        A.AirPortCity = myDialog.textEdit_AirPortCity.toPlainText()
        A.AirPortCounty = myDialog.textEdit_AirPortCounty.toPlainText()
        A.AirPortCountry = myDialog.textEdit_AirPortCountry.toPlainText()
        A.AirPortLatitude = myDialog.lineEdit_AirPortLatitude.text()
        A.AirPortLongitude = myDialog.lineEdit_AirPortLongitude.text()
        A.HeightAboveSeaLevel = myDialog.lineEdit_HeightAboveSeaLevel.text()
        A.SourceCSVFile = myDialog.textEdit_SourceCSVFile.toPlainText()
        A.AirPortDescription = myDialog.textEdit_AirPortDescription.toPlainText()
        A.AirPortFacilities = myDialog.textEdit_AirPortFacilities.toPlainText()
        A.AirPortIncidents = myDialog.textEdit_Incidents.toPlainText()
        # Вносим изменение
        ResultUpdate = S.UpdateAirPort(A.AirPortCodeIATA,
                                       A.AirPortCodeICAO,
                                       A.AirPortName,
                                       A.AirPortCity,
                                       A.AirPortCounty,
                                       A.AirPortCountry,
                                       A.AirPortLatitude,
                                       A.AirPortLongitude,
                                       A.HeightAboveSeaLevel,
                                       A.SourceCSVFile,
                                       A.AirPortDescription,
                                       A.AirPortFacilities,
                                       A.AirPortIncidents)
        if not ResultUpdate:
            message = QtWidgets.QMessageBox()
            message.setText("Запись не переписалась")
            message.setIcon(QtWidgets.QMessageBox.Warning)
            message.exec_()
    # Отрисовка первого окна
    myDialog.show()
    # Правильное закрытие окна
    sys.exit(myApp.exec_())


# Точка входа
# __name__ — это специальная переменная, которая будет равна __main__, только если файл запускается как основная программа,
# в остальных случаях - имени модуля при импорте в качестве модуля
if __name__ == "__main__":
    myApplication()
