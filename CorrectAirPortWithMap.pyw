#  Interpreter 3.7 -> 3.10 -> 3.11 (+) -> 3.12 -> 3.13 (+) -> 3.14 (-)


import datetime
import sys
import io
import os
import socket
import json
import pyodbc
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets  # pip install PyQtWebEngine -> поставил 02.06.2024
import folium
from folium.plugins.draw import Draw
#from PyQt5.QtWebEngineWidgets import QWebEngineView  # pip install PyQtWebEngine
from configparser import ConfigParser

# Импорт модулей библиотек индивидуальной разработки (файла *.py в этой же папке)
from modulesFilesWithClasses.moduleClasses import FileNames, Flags, States, ACFN
from modulesFilesWithClasses.moduleClassesUIsSources import Ui_DialogCorrectAirPortsWithMap, Ui_DialogInputIATAandICAO


# Делаем экземпляры
config_from_cfg = ConfigParser()
config_from_cfg.read('configCommon.cfg')

F = FileNames()
Fl = Flags()
St = States()
acfn = ACFN()


# Основная функция
def myApplication():
    # Одно прикладное приложение
    # todo Делаем сопряжение экземпляров классов с SQL-ными базами данных - семантическими противоположностями ООП, примеров мало
    # fixme Сделать скрипт, который копирует данные таблицы по коду IATA строку за строкой из одной базы в другую -> Сделал на курсоре (нужно проверять правильность сработки скрипта)
    myApp = QtWidgets.QApplication(sys.argv)
    # Делаем экземпляры
    # fixme Правильно сделать экземпляр с композицией
    myDialog = Ui_DialogCorrectAirPortsWithMap()
    myDialog.setupUi(Dialog=myDialog)  # надо вызывать явно
    myDialog.setFixedSize(920, 780)
    myDialog.setWindowTitle('АэроПорты')
    myDialogInputIATAandICAO = Ui_DialogInputIATAandICAO()
    myDialogInputIATAandICAO.setupUi(Dialog=myDialogInputIATAandICAO)
    myDialogInputIATAandICAO.setFixedSize(240, 245)
    # Дополняем функционал экземпляра главного диалога
    # Переводим в исходное состояние
    myDialog.pushButton_ConnectDB.setToolTip("После подключения нажмите кнопку Поиск")
    myDialog.pushButton_UpdateDB.setToolTip("Запись внесенных изменений в БД \n Перед нажатием правильно заполнить и проверить введенные данные")
    myDialog.pushButton_UpdateDB.setEnabled(False)
    myDialog.pushButton_DisconnectDB.setToolTip("Перед закрытием диалога отключиться от базы данных")
    myDialog.pushButton_DisconnectDB.setEnabled(False)
    # Параметры соединения с сервером
    myDialog.lineEdit_Server.setEnabled(False)
    myDialog.lineEdit_Driver.setEnabled(False)
    myDialog.lineEdit_ODBCversion.setEnabled(False)
    myDialog.lineEdit_Schema.setEnabled(False)
    # Добавляем базы данных в выпадающий список
    listdbs = sorted(config_from_cfg.get(section='DataBases', option='AirPorts').split(','))
    if listdbs:
        for point in listdbs:
            #point = point.lstrip(' ')
            stripped_point = point.strip()
            myDialog.comboBox_DB.addItem(stripped_point)
    # Получаем список драйверов баз данных
    # Добавляем атрибут DriversODBC по ходу действия
    DriversODBC = sorted(pyodbc.drivers())
    if DriversODBC:
        for DriverODBC in DriversODBC:
            myDialog.comboBox_Driver.addItem(str(DriverODBC))
    myDialog.textEdit_SourceCSVFile.setEnabled(False)
    myDialog.label_hyperlink_to_WikiPedia.setEnabled(False)
    myDialog.label_HyperLink_to_AirPort.setEnabled(False)
    myDialog.label_HyperLink_to_Operator.setEnabled(False)
    myDialog.textBrowser_HyperLinks.setToolTip("Пока в разработке")
    myDialog.pushButton_HyperLinkChange_Wikipedia.setEnabled(False)
    myDialog.pushButton_HyperLinkChange_AirPort.setEnabled(False)
    myDialog.pushButton_HyperLinkChange_Operator.setEnabled(False)
    myDialog.lineEdit_AirPortCodeFAA_LID.setEnabled(False)
    myDialog.lineEdit_AirPortCodeWMO.setEnabled(False)
    myDialog.pushButton_SearchByIATA.setToolTip("Поиск по коду IATA\n (выводит первую запись из БД, дубликаты не предусматриваются)")
    myDialog.pushButton_SearchByIATA.setEnabled(False)
    myDialog.pushButton_SearchByICAO.setToolTip("Поиск по коду ICAO\n (выводит первую запись из БД, дубликаты не предусматриваются)")
    myDialog.pushButton_SearchByICAO.setEnabled(False)
    myDialog.pushButton_SearchByFAALID.setToolTip("Поиск по коду FAA LID\n (выводит первую запись из БД, дубликаты не предусматриваются)")
    myDialog.pushButton_SearchByFAALID.setEnabled(False)
    myDialog.pushButton_SearchByWMO.setToolTip("Поиск по коду WMO\n (выводит первую запись из БД, дубликаты не предусматриваются)")
    myDialog.pushButton_SearchByWMO.setEnabled(False)
    myDialog.pushButton_SearchAndInsertByIATAandICAO.setToolTip("Считаем, что аэропорт или аэродром однозначно определяются сочетанием кодов IATA и ICAO\nКоды FAA LID (легкомоторная авиация) и WMO дописываются дополнительно\nЕсли код IATA пустой, то вероятно просто аэродром или взлетная полоса без инфраструктуры")
    myDialog.pushButton_SearchAndInsertByIATAandICAO.setEnabled(False)
    myDialog.textEdit_AirPortName.setEnabled(False)
    myDialog.textEdit_AirPortCity.setEnabled(False)
    myDialog.textEdit_AirPortCounty.setEnabled(False)
    myDialog.textEdit_AirPortCountry.setEnabled(False)
    myDialog.lineEdit_AirPortLatitude.setEnabled(False)
    myDialog.lineEdit_AirPortLongitude.setEnabled(False)
    myDialog.lineEdit_HeightAboveSeaLevel.setEnabled(False)
    myDialog.textBrowser_HyperLinks.setOpenExternalLinks(True)
    myDialog.textBrowser_HyperLinks.setReadOnly(True)
    myDialog.textBrowser_HyperLinks.setEnabled(False)
    myDialog.pushButton_HyperLinksChange.setToolTip("Изменение адресов ссылок")
    myDialog.pushButton_HyperLinksChange.setEnabled(False)
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
    myDialog.verticalLayout_Map.setEnabled(False)
    myDialogInputIATAandICAO.lineEdit_CodeIATA.setToolTip("Введите код IATA или поставьте галочку, если его нет")
    myDialogInputIATAandICAO.lineEdit_CodeICAO.setToolTip("Введите код ICAO или поставьте галочку, если его нет")
    myDialogInputIATAandICAO.checkBox_Status_IATA.setToolTip("Пустая ячейка в БД (не считается, как пустая строка)")
    myDialogInputIATAandICAO.checkBox_Status_ICAO.setToolTip("Пустая ячейка в БД (не считается, как пустая строка)")
    myDialogInputIATAandICAO.pushButton_SearchInsert.setToolTip("Внимательно проверить введенные данные. Исправления после вставки не предусматриваются")
    # Добавляем атрибут ввода
    myDialog.lineEditCodeIATA = QtWidgets.QLineEdit()
    myDialog.lineEditCodeICAO = QtWidgets.QLineEdit()
    myDialog.lineEditCodeFAA_LID = QtWidgets.QLineEdit()
    myDialog.lineEditCodeWMO = QtWidgets.QLineEdit()
    # Привязки обработчиков
    myDialog.pushButton_ConnectDB.clicked.connect(lambda: PushButtonConnectDB())
    myDialog.pushButton_UpdateDB.clicked.connect(lambda: PushButtonUpdateDB())
    myDialog.pushButton_DisconnectDB.clicked.connect(lambda: PushButtonDisconnect())
    myDialog.pushButton_HyperLinkChange_Wikipedia.clicked.connect(lambda: PushButtonChangeHyperLinkWikiPedia())
    myDialog.pushButton_HyperLinkChange_AirPort.clicked.connect(lambda: PushButtonChangeHyperLinkAirPort())
    myDialog.pushButton_HyperLinkChange_Operator.clicked.connect(lambda: PushButtonChangeHyperLinkOperator())
    myDialog.pushButton_SearchByIATA.clicked.connect(lambda: PushButtonSearchByIATA())
    myDialog.pushButton_SearchByICAO.clicked.connect(lambda: PushButtonSearchByICAO())
    myDialog.pushButton_SearchByFAALID.clicked.connect(lambda: PushButtonSearchByFAA_LID())
    myDialog.pushButton_SearchByWMO.clicked.connect(lambda: PushButtonSearchByWMO())
    myDialog.pushButton_SearchAndInsertByIATAandICAO.clicked.connect(lambda: PushButtonInsertByIATAandICAO())
    myDialog.pushButton_HyperLinksChange.clicked.connect(lambda: PushButtonChangeHyperLinks())
    myDialogInputIATAandICAO.pushButton_SearchInsert.clicked.connect(lambda: PushButtonInput())
    myDialogInputIATAandICAO.checkBox_Status_IATA.clicked.connect(lambda: Check_IATA())
    myDialogInputIATAandICAO.checkBox_Status_ICAO.clicked.connect(lambda: Check_ICAO())

    def ClearMap():
        # очищаем предыдущую отрисовку см. https://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt/78674901#78674901
        if myDialog.verticalLayout_Map is not None:
            while myDialog.verticalLayout_Map.count():
                child = myDialog.verticalLayout_Map.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    myDialog.verticalLayout_Map.clearLayout(child.layout())

    def SwitchingGUI(Key):
        myDialog.comboBox_DB.setEnabled(not Key)
        myDialog.comboBox_Driver.setEnabled(not Key)
        myDialog.lineEdit_Server.setEnabled(Key)
        myDialog.lineEdit_Driver.setEnabled(Key)
        myDialog.lineEdit_ODBCversion.setEnabled(Key)
        myDialog.lineEdit_Schema.setEnabled(Key)
        myDialog.textEdit_SourceCSVFile.setEnabled(Key)
        myDialog.label_hyperlink_to_WikiPedia.setEnabled(Key)
        myDialog.label_HyperLink_to_AirPort.setEnabled(Key)
        myDialog.label_HyperLink_to_Operator.setEnabled(Key)
        myDialog.pushButton_HyperLinkChange_Wikipedia.setEnabled(Key)
        myDialog.pushButton_HyperLinkChange_AirPort.setEnabled(Key)
        myDialog.pushButton_HyperLinkChange_Operator.setEnabled(Key)
        myDialog.lineEdit_AirPortCodeFAA_LID.setEnabled(Key)
        myDialog.lineEdit_AirPortCodeWMO.setEnabled(Key)
        myDialog.pushButton_SearchByIATA.setEnabled(Key)
        myDialog.pushButton_SearchByICAO.setEnabled(Key)
        myDialog.pushButton_SearchByFAALID.setEnabled(Key)
        myDialog.pushButton_SearchByWMO.setEnabled(Key)
        myDialog.pushButton_SearchAndInsertByIATAandICAO.setEnabled(Key)
        myDialog.textEdit_AirPortName.setEnabled(Key)
        myDialog.textEdit_AirPortCity.setEnabled(Key)
        myDialog.textEdit_AirPortCounty.setEnabled(Key)
        myDialog.textEdit_AirPortCountry.setEnabled(Key)
        myDialog.lineEdit_AirPortLatitude.setEnabled(Key)
        myDialog.lineEdit_AirPortLongitude.setEnabled(Key)
        myDialog.lineEdit_HeightAboveSeaLevel.setEnabled(Key)
        myDialog.textBrowser_HyperLinks.setEnabled(Key)
        myDialog.pushButton_HyperLinksChange.setEnabled(Key)
        myDialog.textEdit_AirPortDescription.setEnabled(Key)
        myDialog.textEdit_AirPortFacilities.setEnabled(Key)
        myDialog.textEdit_Incidents.setEnabled(Key)
        ClearMap()
        myDialog.verticalLayout_Map.setEnabled(Key)

    def ReadingQuery(ResultQuery):
        acfn.SourceCSVFile = ResultQuery.SourceCSVFile
        acfn.HyperLinkToWikiPedia = ResultQuery.HyperLinkToWikiPedia
        acfn.HyperLinkToAirPortSite = ResultQuery.HyperLinkToAirPortSite
        acfn.HyperLinkToOperatorSite = ResultQuery.HyperLinkToOperatorSite
        acfn.AirPortCodeIATA = ResultQuery.AirPortCodeIATA
        acfn.AirPortCodeICAO = ResultQuery.AirPortCodeICAO
        acfn.AirPortCodeFAA_LID = ResultQuery.AirPortCodeFAA_LID
        acfn.AirPortCodeWMO = ResultQuery.AirPortCodeWMO
        acfn.AirPortName = ResultQuery.AirPortName
        acfn.AirPortCity = ResultQuery.AirPortCity
        acfn.AirPortCounty = ResultQuery.AirPortCounty
        acfn.AirPortCountry = ResultQuery.AirPortCountry
        acfn.AirPortLatitude = ResultQuery.AirPortLatitude
        acfn.AirPortLongitude = ResultQuery.AirPortLongitude
        acfn.HeightAboveSeaLevel = ResultQuery.HeightAboveSeaLevel
        acfn.AirPortDescription = ResultQuery.AirPortDescription
        acfn.AirPortFacilities = ResultQuery.AirPortFacilities
        acfn.AirPortIncidents = ResultQuery.AirPortIncidents
        acfn.LogCountViewed = ResultQuery.LogCountViewed
        acfn.LogCountChanged = ResultQuery.LogCountChanged
        acfn.IncrementLogCountViewedAirPort(acfn.AirPortCodeIATA, acfn.AirPortCodeICAO, socket.gethostname(), os.getlogin(), datetime.datetime.now())

    @QtCore.pyqtSlot("QWebEngineDownloadItem*")
    def ExportGeoJSON(self, item):
        print(" выбираем путь записи файла *.geojson")
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, caption="Записать файл геоданных", directory=' ', filter=item.suggestedFileName())
        if path:
            print(str(path))
            item.setPath(path)
            item.accept()

    def SetFields():
        # Выводим записи
        myDialog.textEdit_SourceCSVFile.clear()
        myDialog.textEdit_SourceCSVFile.append(str(acfn.SourceCSVFile))
        myDialog.label_hyperlink_to_WikiPedia.setText("<a href=" + str(acfn.HyperLinkToWikiPedia) + ">Wikipedia</a>")
        myDialog.label_hyperlink_to_WikiPedia.setToolTip(str(acfn.HyperLinkToWikiPedia))
        myDialog.label_hyperlink_to_WikiPedia.setOpenExternalLinks(True)
        myDialog.label_HyperLink_to_AirPort.setText("<a href=" + str(acfn.HyperLinkToAirPortSite) + ">Сайт аэропорта или аэродрома</a>")
        myDialog.label_HyperLink_to_AirPort.setToolTip(str(acfn.HyperLinkToAirPortSite))
        myDialog.label_HyperLink_to_AirPort.setOpenExternalLinks(True)
        myDialog.label_HyperLink_to_Operator.setText("<a href=" + str(acfn.HyperLinkToOperatorSite) + ">Сайт оператора аэропорта</a>")
        myDialog.label_HyperLink_to_Operator.setToolTip(str(acfn.HyperLinkToOperatorSite))
        myDialog.label_HyperLink_to_Operator.setOpenExternalLinks(True)
        if acfn.AirPortCodeIATA is None:
            myDialog.label_CodeIATA.setText(" ")
        else:
            myDialog.label_CodeIATA.setText(str(acfn.AirPortCodeIATA))
        if acfn.AirPortCodeICAO is None:
            myDialog.label_CodeICAO.setText(" ")
        else:
            myDialog.label_CodeICAO.setText(acfn.AirPortCodeICAO)
        myDialog.lineEdit_AirPortCodeFAA_LID.setText(str(acfn.AirPortCodeFAA_LID))
        myDialog.lineEdit_AirPortCodeWMO.setText(str(acfn.AirPortCodeWMO))
        myDialog.textEdit_AirPortName.clear()
        myDialog.textEdit_AirPortName.append(str(acfn.AirPortName))
        myDialog.textEdit_AirPortCity.clear()
        myDialog.textEdit_AirPortCity.append(str(acfn.AirPortCity))
        myDialog.textEdit_AirPortCounty.clear()
        myDialog.textEdit_AirPortCounty.append(str(acfn.AirPortCounty))
        myDialog.textEdit_AirPortCountry.clear()
        myDialog.textEdit_AirPortCountry.append(str(acfn.AirPortCountry))
        myDialog.lineEdit_AirPortLatitude.setText(str(acfn.AirPortLatitude))
        myDialog.lineEdit_AirPortLongitude.setText(str(acfn.AirPortLongitude))
        myDialog.lineEdit_HeightAboveSeaLevel.setText(str(acfn.HeightAboveSeaLevel))
        myDialog.textBrowser_HyperLinks.clear()
        #myDialog.textBrowser_HyperLinks.append("<a href=" + str(A.SourceCSVFile) + ">Wikipedia</a>")
        #myDialog.textBrowser_HyperLinks.append("<a href=" + str(A.SourceCSVFile) + ">Сайт аэропорта или аэродрома</a>")
        #myDialog.textBrowser_HyperLinks.append("<a href=" + str(A.SourceCSVFile) + ">Сайт оператора аэропорта</a>")
        myDialog.textEdit_AirPortDescription.clear()
        myDialog.textEdit_AirPortDescription.append(str(acfn.AirPortDescription))
        myDialog.textEdit_AirPortFacilities.clear()
        myDialog.textEdit_AirPortFacilities.append(acfn.AirPortFacilities)
        myDialog.textEdit_Incidents.clear()
        myDialog.textEdit_Incidents.append(acfn.AirPortIncidents)
        ClearMap()
        if acfn.AirPortLatitude is not None and acfn.AirPortLongitude is not None:
            coordinates = (acfn.AirPortLatitude, acfn.AirPortLongitude)
            # Варианты карт:
            #  - OpenStreetMap (подробная цветная),
            #  - CartoDB Positron (серенькая),
            #  - CartoDB Voyager (аскетичная, мало подписей и меток),
            #  - NASAGIBS Blue Marble (пока не отрисовывается),
            #  - Stamen Terrain - не работает,
            #  - Esri - не работает,
            #  - OpenWeatherMap - не работает,
            zoom = 13
            Map = folium.Map(tiles=None, zoom_start=zoom, location=coordinates)
            try:
                folium.TileLayer("CartoDB Positron").add_to(Map)
            except Exception:
                message = QtWidgets.QMessageBox()
                message.setText("CartoDB Positron не отвечает")
                message.setIcon(QtWidgets.QMessageBox.Warning)
                message.exec_()
            try:
                folium.TileLayer("CartoDB Voyager").add_to(Map)
            except Exception:
                message = QtWidgets.QMessageBox()
                message.setText("CartoDB Voyager не отвечает")
                message.setIcon(QtWidgets.QMessageBox.Warning)
                message.exec_()
            try:
                folium.TileLayer("NASAGIBS Blue Marble").add_to(Map)
            except Exception:
                message = QtWidgets.QMessageBox()
                message.setText("NASAGIBS Blue Marble не отвечает")
                message.setIcon(QtWidgets.QMessageBox.Warning)
                message.exec_()
            try:
                folium.TileLayer("OpenStreetMap").add_to(Map)
            except Exception:
                message = QtWidgets.QMessageBox()
                message.setText("OpenStreetMap не отвечает")
                message.setIcon(QtWidgets.QMessageBox.Warning)
                message.exec_()
            try:
                folium.raster_layers.TileLayer(tiles='http://mt1.google.com/vt/lyrs=m&h1=p1Z&x={x}&y={y}&z={z}', name='Google Roadmap', attr='Google Map', ).add_to(Map)
            except Exception:
                message = QtWidgets.QMessageBox()
                message.setText("Google Roadmap не отвечает")
                message.setIcon(QtWidgets.QMessageBox.Warning)
                message.exec_()
            try:
                folium.raster_layers.TileLayer(tiles='http://mt1.google.com/vt/lyrs=s&h1=p1Z&x={x}&y={y}&z={z}', name='Google Satellite', attr='Google Map', ).add_to(Map)
            except Exception:
                message = QtWidgets.QMessageBox()
                message.setText("Google Satellite не отвечает")
                message.setIcon(QtWidgets.QMessageBox.Warning)
                message.exec_()
            try:
                folium.raster_layers.TileLayer(tiles='http://mt1.google.com/vt/lyrs=y&h1=p1Z&x={x}&y={y}&z={z}', name='Google Hybrid', attr='Google Map', ).add_to(Map)
            except Exception:
                message = QtWidgets.QMessageBox()
                message.setText("Google Hybrid не отвечает")
                message.setIcon(QtWidgets.QMessageBox.Warning)
                message.exec_()
            folium.TileLayer(show=True).add_to(Map)
            folium.LayerControl().add_to(Map)
            Map.add_child(folium.LatLngPopup())
            # fixme Export не работает -> см. https://stackoverflow.com/questions/64402959/cant-export-coordinates-on-folium-draw-polygon-in-pyqt5-app
            Draw(export=True,
                 filename="my_data.geojson",
                 position="topleft",
                 draw_options={"polyline": True, "rectangle": True, "circle": True, "circlemarker": True, },
                 edit_options={"poly": {"allowIntersection": False}}, ).add_to(Map)
            # save map data to data object
            data = io.BytesIO()
            Map.save(data, close_file=False)

            class WebEnginePage(QtWebEngineWidgets.QWebEnginePage):
                def javaScriptConsoleMessage(self, level, msg, line, sourceID):
                    coords_dict = json.loads(msg)
                    coords = coords_dict['geometry']['coordinates'][0]
                    print(str(coords))

            webView = QtWebEngineWidgets.QWebEngineView()
            webView.page().profile().downloadRequested.connect(lambda: ExportGeoJSON)  # fixme функция-обработчик не срабатывает, connect не работает
            page = WebEnginePage(webView)
            webView.setPage(page)
            webView.setHtml(data.getvalue().decode())
            # новая отрисовка
            myDialog.verticalLayout_Map.addWidget(webView)

    def PushButtonConnectDB():
        if not St.Connected_RT:
            # Переводим в неактивное состояние
            myDialog.pushButton_ConnectDB.setEnabled(False)
            # Подключаемся к базе данных по выбранному источнику
            ChoiceDB = myDialog.comboBox_DB.currentText()
            ChoiceDriver = myDialog.comboBox_Driver.currentText()
            # Добавляем атрибуты DataBase, DriverODBC
            DataBase = str(ChoiceDB)
            DriverODBC = str(ChoiceDriver)
            if acfn.connect_DB_RT_odbc(servername=config_from_cfg.get(section='Servers', option='ServerNameRemote'), driver=DriverODBC, database=DataBase):
                print("  База данных ", DataBase, " подключена")
                Data = acfn.getSQLData_odbc()
                print(" Data = " + str(Data))
                St.Connected_RT = True
                # SQL Server
                myDialog.lineEdit_Server.setText(str(Data[0]))
                myDialog.lineEdit_Server.setReadOnly(True)
                # Драйвер
                myDialog.lineEdit_Driver.setText(str(Data[1]))
                myDialog.lineEdit_Driver.setReadOnly(True)
                # версия ODBC
                myDialog.lineEdit_ODBCversion.setText(str(Data[2]))
                myDialog.lineEdit_ODBCversion.setReadOnly(True)
                # Схема (если из-под другой учетки, то выводит имя учетки)
                # todo Схема по умолчанию - dbo
                myDialog.lineEdit_Schema.setText(str(Data[4]))
                myDialog.lineEdit_Schema.setReadOnly(True)
                # Переводим в рабочее состояние (продолжение)
                SwitchingGUI(True)
                myDialog.pushButton_DisconnectDB.setEnabled(True)
            else:
                # Переводим в рабочее состояние
                myDialog.pushButton_ConnectDB.setEnabled(True)
                message = QtWidgets.QMessageBox()
                message.setText("Нет подключения к базе данных аэропортов")
                message.setIcon(QtWidgets.QMessageBox.Warning)
                message.exec_()

    def PushButtonDisconnect():
        # кнопка 'Отключиться от базы данных' нажата
        if St.Connected_RT:
            acfn.disconnect_RT_odbc()
            # Переводим в неактивное состояние
            myDialog.pushButton_DisconnectDB.setEnabled(False)
            # Снимаем флаги
            St.Connected_RT = False
            # Переводим в рабочее состояние (продолжение)
            SwitchingGUI(False)
            myDialog.pushButton_UpdateDB.setEnabled(False)  # возможно пока не тут
            myDialog.pushButton_ConnectDB.setEnabled(True)

    def PushButtonUpdateDB():
        acfn.SourceCSVFile = myDialog.textEdit_SourceCSVFile.toPlainText()
        #A.AirPortCodeIATA = myDialog.lineEdit_AirPortCodeIATA.text()
        #A.AirPortCodeICAO = myDialog.lineEdit_AirPortCodeICAO.text()
        acfn.AirPortCodeFAA_LID = myDialog.lineEdit_AirPortCodeFAA_LID.text()
        acfn.AirPortCodeWMO = myDialog.lineEdit_AirPortCodeWMO.text()
        acfn.AirPortName = myDialog.textEdit_AirPortName.toPlainText()
        acfn.AirPortCity = myDialog.textEdit_AirPortCity.toPlainText()
        acfn.AirPortCounty = myDialog.textEdit_AirPortCounty.toPlainText()
        acfn.AirPortCountry = myDialog.textEdit_AirPortCountry.toPlainText()
        acfn.AirPortLatitude = myDialog.lineEdit_AirPortLatitude.text()
        acfn.AirPortLongitude = myDialog.lineEdit_AirPortLongitude.text()
        acfn.HeightAboveSeaLevel = myDialog.lineEdit_HeightAboveSeaLevel.text()
        acfn.AirPortDescription = myDialog.textEdit_AirPortDescription.toPlainText()
        acfn.AirPortFacilities = myDialog.textEdit_AirPortFacilities.toPlainText()
        acfn.AirPortIncidents = myDialog.textEdit_Incidents.toPlainText()
        DBAirPort = acfn.QueryAirPortByIATAandICAO(iata=acfn.AirPortCodeIATA, icao=acfn.AirPortCodeICAO)
        LogCountChangedCurrent = DBAirPort.LogCountChanged
        if LogCountChangedCurrent is None or (acfn.LogCountChanged is not None and LogCountChangedCurrent is not None and acfn.LogCountChanged == LogCountChangedCurrent):
            # Вносим изменение
            ResultUpdate = acfn.UpdateAirPortByIATAandICAO(acfn.SourceCSVFile,
                                                      acfn.HyperLinkToWikiPedia,
                                                      acfn.HyperLinkToAirPortSite,
                                                      acfn.HyperLinkToOperatorSite,
                                                      acfn.AirPortCodeIATA,
                                                      acfn.AirPortCodeICAO,
                                                      acfn.AirPortCodeFAA_LID,
                                                      acfn.AirPortCodeWMO,
                                                      acfn.AirPortName,
                                                      acfn.AirPortCity,
                                                      acfn.AirPortCounty,
                                                      acfn.AirPortCountry,
                                                      acfn.AirPortLatitude,
                                                      acfn.AirPortLongitude,
                                                      acfn.HeightAboveSeaLevel,
                                                      acfn.AirPortDescription,
                                                      acfn.AirPortFacilities,
                                                      acfn.AirPortIncidents)
            if ResultUpdate:
                # fixme Пользователи без права на изменение не фиксируются
                acfn.IncrementLogCountChangedAirPort(acfn.AirPortCodeIATA, acfn.AirPortCodeICAO, socket.gethostname(), os.getlogin(), datetime.datetime.now())
                DBAirPort = acfn.QueryAirPortByIATAandICAO(acfn.AirPortCodeIATA, acfn.AirPortCodeICAO)
                acfn.LogCountChanged = DBAirPort.LogCountChanged
            else:
                message = QtWidgets.QMessageBox()
                message.setText("Запись не переписалась")
                message.setIcon(QtWidgets.QMessageBox.Warning)
                message.exec_()
        else:
            qm = QtWidgets.QMessageBox()
            qm.setText("Перечитайте данные (уже изменены)")
            qm.setIcon(QtWidgets.QMessageBox.Warning)
            qm.exec_()

    def PushButtonChangeHyperLinkWikiPedia():
        Link, ok = QtWidgets.QInputDialog.getText(myDialog, "Ссылка", "Введите адрес сайта")
        if ok:
            acfn.HyperLinkToWikiPedia = Link
            print(str(Link))
            myDialog.label_hyperlink_to_WikiPedia.setText("<a href=" + str(acfn.HyperLinkToWikiPedia) + ">Wikipedia</a>")
            myDialog.label_hyperlink_to_WikiPedia.setToolTip(str(acfn.HyperLinkToWikiPedia))
            myDialog.label_hyperlink_to_WikiPedia.setOpenExternalLinks(True)

    def PushButtonChangeHyperLinkAirPort():
        Link, ok = QtWidgets.QInputDialog.getText(myDialog, "Ссылка", "Введите адрес сайта")
        if ok:
            acfn.HyperLinkToAirPortSite = Link
            print(str(Link))
            myDialog.label_HyperLink_to_AirPort.setText("<a href=" + str(acfn.HyperLinkToAirPortSite) + ">Сайт аэропорта или аэродрома</a>")
            myDialog.label_HyperLink_to_AirPort.setToolTip(str(acfn.HyperLinkToAirPortSite))
            myDialog.label_HyperLink_to_AirPort.setOpenExternalLinks(True)

    def PushButtonChangeHyperLinkOperator():
        Link, ok = QtWidgets.QInputDialog.getText(myDialog, "Ссылка", "Введите адрес сайта")
        if ok:
            acfn.HyperLinkToOperatorSite = Link
            print(str(Link))
            myDialog.label_HyperLink_to_Operator.setText("<a href=" + str(acfn.HyperLinkToOperatorSite) + ">Сайт оператора аэропорта</a>")
            myDialog.label_HyperLink_to_Operator.setToolTip(str(acfn.HyperLinkToOperatorSite))
            myDialog.label_HyperLink_to_Operator.setOpenExternalLinks(True)

    def PushButtonChangeHyperLinks():
        message = QtWidgets.QMessageBox()
        message.setText("Пока в разработке")
        message.setIcon(QtWidgets.QMessageBox.Information)
        message.exec_()

    def PushButtonSearchByIATA():
        # Кнопка "Поиск" нажата
        Code, ok = QtWidgets.QInputDialog.getText(myDialog, "Код IATA", "Введите код IATA")
        if ok:
            DBAirPort = acfn.QueryAirPortByIATA(Code)
            # fixme Решение 3 - не перезаписывать код IATA (Недостаток - можно сделать дубликат по коду ICAO, их много, возможно это НОРМА, исправлять только вручную)
            # fixme Решение 4 - код IATA всегда неактивный, он вводится только при вставке
            if DBAirPort is None:
                message = QtWidgets.QMessageBox()
                message.setText("Запись не найдена")
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.exec_()
            else:
                ReadingQuery(DBAirPort)
                SetFields()
                myDialog.pushButton_UpdateDB.setEnabled(True)

    def PushButtonSearchByICAO():
        # Кнопка "Поиск" нажата
        Code, ok = QtWidgets.QInputDialog.getText(myDialog, "Код ICAO", "Введите код ICAO")
        if ok:
            DBAirPort = acfn.QueryAirPortByICAO(Code)
            if DBAirPort is None:
                message = QtWidgets.QMessageBox()
                message.setText("Запись не найдена")
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.exec_()
            else:
                ReadingQuery(DBAirPort)
                SetFields()
                myDialog.pushButton_UpdateDB.setEnabled(True)

    def PushButtonSearchByFAA_LID():
        # Кнопка "Поиск" нажата
        Code, ok = QtWidgets.QInputDialog.getText(myDialog, "Код FAA LID", "Введите код FAA LID")
        if ok:
            DBAirPort = acfn.QueryAirPortByFAA_LID(Code)
            if DBAirPort is None:
                message = QtWidgets.QMessageBox()
                message.setText("Запись не найдена")
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.exec_()
            else:
                ReadingQuery(DBAirPort)
                SetFields()
                myDialog.pushButton_UpdateDB.setEnabled(True)

    def PushButtonSearchByWMO():
        # Кнопка "Поиск" нажата
        Code, ok = QtWidgets.QInputDialog.getText(myDialog, "Код WMO", "Введите код WMO")
        if ok:
            DBAirPort = acfn.QueryAirPortByWMO(Code)
            if DBAirPort is None:
                message = QtWidgets.QMessageBox()
                message.setText("Запись не найдена")
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.exec_()
            else:
                ReadingQuery(DBAirPort)
                SetFields()
                myDialog.pushButton_UpdateDB.setEnabled(True)

    def Check_IATA():
        if myDialogInputIATAandICAO.checkBox_Status_IATA.isChecked():
            myDialogInputIATAandICAO.lineEdit_CodeIATA.setEnabled(False)
        else:
            myDialogInputIATAandICAO.lineEdit_CodeIATA.setEnabled(True)

    def Check_ICAO():
        if myDialogInputIATAandICAO.checkBox_Status_ICAO.isChecked():
            myDialogInputIATAandICAO.lineEdit_CodeICAO.setEnabled(False)
        else:
            myDialogInputIATAandICAO.lineEdit_CodeICAO.setEnabled(True)

    def PushButtonInput():
        if myDialogInputIATAandICAO.checkBox_Status_IATA.isChecked():
            Code_IATA = None
        else:
            Code_IATA = myDialogInputIATAandICAO.lineEdit_CodeIATA.text()
        if myDialogInputIATAandICAO.checkBox_Status_ICAO.isChecked():
            Code_ICAO = None
        else:
            Code_ICAO = myDialogInputIATAandICAO.lineEdit_CodeICAO.text()
        DBAirPort = acfn.QueryAirPortByIATAandICAO(iata=Code_IATA, icao=Code_ICAO)
        myDialogInputIATAandICAO.close()

        if DBAirPort is None:
            # Вставляем новую запись fixme вставилась запись с Code_IATA = NULL и Code_ICAO = "None"
            ResultInsert = acfn.InsertAirPortByIATAandICAO(Code_IATA, Code_ICAO)
            if ResultInsert:
                DBAirPort = acfn.QueryAirPortByIATAandICAO(Code_IATA, Code_ICAO)
                if DBAirPort is None:
                    message = QtWidgets.QMessageBox()
                    message.setText("Запись не прочиталась. Попробуйте прочитать ее через поиск")
                    message.setIcon(QtWidgets.QMessageBox.Warning)
                    message.exec_()
                else:
                    ReadingQuery(DBAirPort)
                    SetFields()
                    # fixme Пользователи без права на изменение не фиксируются
                    acfn.IncrementLogCountChangedAirPort(Code_IATA, Code_ICAO, socket.gethostname(), os.getlogin(), datetime.datetime.now())
                    DBAirPort = acfn.QueryAirPortByIATAandICAO(acfn.AirPortCodeIATA, acfn.AirPortCodeICAO)
                    acfn.LogCountChanged = DBAirPort.LogCountChanged
            else:
                message = QtWidgets.QMessageBox()
                message.setText("Запись не вставилась")
                message.setIcon(QtWidgets.QMessageBox.Warning)
                message.exec_()
        else:
            # Переходим на найденную запись
            ReadingQuery(DBAirPort)
            SetFields()
            message = QtWidgets.QMessageBox()
            message.setText("Такая запись есть")
            message.setIcon(QtWidgets.QMessageBox.Information)
            message.exec_()

    def PushButtonInsertByIATAandICAO():
        # кнопка "Поиск и Вставка"
        # Отрисовка диалога ввода
        myDialogInputIATAandICAO.setWindowTitle("Диалог ввода")
        myDialogInputIATAandICAO.setWindowModality(QtCore.Qt.ApplicationModal)
        myDialogInputIATAandICAO.show()

    # Отрисовка первого окна
    myDialog.show()
    # Правильное закрытие окна
    sys.exit(myApp.exec_())


# Точка входа
# __name__ — это специальная переменная, которая будет равна __main__, только если файл запускается как основная программа,
# в остальных случаях - имени модуля при импорте в качестве модуля
if __name__ == "__main__":
    myApplication()
