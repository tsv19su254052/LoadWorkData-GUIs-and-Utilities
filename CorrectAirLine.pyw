#  Interpreter 3.7 -> 3.10 -> 3.12 -> 3.13 -> 3.14


# QtSQL медленнее, чем pyodbc
import sys
from PyQt5 import QtWidgets, QtCore
from configparser import ConfigParser

# Импорт пользовательской библиотеки (файла *.py в этой же папке)
from modulesFilesWithClasses.moduleClasses import Flags, States, ACFN
from modulesFilesWithClasses.moduleClassesUIsSources import Ui_DialogCorrectAirLine, Ui_DialogInputIATAandICAO


# Делаем экземпляры
config_from_cfg = ConfigParser()
config_from_cfg.read('configCommon.cfg')

acfn = ACFN()
Fl = Flags()
St = States()


# Основная функция
def myApplication():
    # Одно прикладное приложение
    # todo Делаем сопряжение экземпляров классов с SQL-ными базами данных - семантическими противоположностями ООП, примеров мало
    myApp = QtWidgets.QApplication(sys.argv)
    # fixme Правильно делать экземпляр с композицией
    # Делаем экземпляры
    myDialog = Ui_DialogCorrectAirLine()
    myDialog.setupUi(Dialog=myDialog)  # надо вызывать явно
    myDialog.setFixedSize(862, 830)
    myDialog.setWindowTitle('АвиаКомпании')
    myDialogInputIATAandICAO = Ui_DialogInputIATAandICAO()
    myDialogInputIATAandICAO.setupUi(Dialog=myDialogInputIATAandICAO)
    myDialogInputIATAandICAO.setFixedSize(240, 245)
    # Переводим в исходное состояние
    #myDialogInput.checkBox_Status_IATA.isChecked(False)
    #myDialogInput.checkBox_Status_ICAO.isChecked(False)
    # Дополняем функционал экземпляра главного диалога
    # Переводим в исходное состояние
    myDialog.comboBox_Driver.setToolTip("Драйвер ODBC для SDK SQL Server-а")
    myDialog.pushButton_SelectDB.setToolTip("После подключения нажмите кнопку Начало, далее - Поиск")
    myDialog.pushButton_Disconnect.setToolTip("Перед закрытием диалога отключиться от базы данных")
    myDialog.pushButton_Disconnect.setEnabled(False)
    # Параметры соединения с сервером
    myDialog.lineEdit_Server.setEnabled(False)
    myDialog.lineEdit_Driver.setEnabled(False)
    myDialog.lineEdit_ODBCversion.setEnabled(False)
    myDialog.lineEdit_Schema.setEnabled(False)
    myDialog.lineEdit_AirLineCodeIATA.setEnabled(False)
    myDialog.lineEdit_AirLineCodeIATA.setFrame(True)
    myDialog.lineEdit_AirLineCodeICAO.setEnabled(False)
    myDialog.lineEdit_AirLineCodeICAO.setFrame(True)
    myDialog.lineEdit_CallSign.setEnabled(False)
    myDialog.pushButton_SearchByIATA.setToolTip("Поиск по коду IATA (дубликаты не предусматриваются)")
    myDialog.pushButton_SearchByIATA.setEnabled(False)
    myDialog.pushButton_SearchByICAO.setToolTip("Поиск по коду ICAO (дубликаты не предусматриваются)")
    myDialog.pushButton_SearchByICAO.setEnabled(False)
    myDialog.pushButton_Insert.setToolTip("Поиск и вставка по кодам IATA и ICAO, \n которые вводятся один раз и далее не изменяются. \nАвиакомпания однозначно определяется по их сочетанию")
    myDialog.pushButton_Insert.setEnabled(False)
    myDialog.checkBox_Status.setToolTip("Действующая авиакомпания")
    myDialog.checkBox_Status.setEnabled(False)
    myDialog.textEdit_AirLineName.setEnabled(False)
    myDialog.textEdit_AirLineCity.setToolTip("Штаб-квартира, хабы (в скобках - коды IATA аэропортов)")
    myDialog.textEdit_AirLineCity.setEnabled(False)
    myDialog.dateEdit_CreateDate.setEnabled(False)
    myDialog.textEdit_AirLineCountry.setEnabled(False)
    myDialog.comboBox_Alliance.setToolTip("Альянсы вставляются с помощью хранимой процедуры \nПосле вставки закрыть и снова открыть этот диалог")
    myDialog.comboBox_Alliance.setEditable(True)
    myDialog.comboBox_Alliance.setEnabled(False)
    myDialog.lineEdit_AirLineID.setEnabled(False)
    myDialog.lineEdit_AirLineAlias.setEnabled(False)
    myDialog.lineEdit_Position.setEnabled(False)
    myDialog.tabWidget.setTabText(0, "Описание")
    myDialog.tabWidget.setTabText(1, "Функционал")
    # todo Сделать хабы интерактивным динамическим набором виджетов с подписанными "Наименованиями аэропортов" из базы аэропортов на вкладке "Хабы"
    #  + Кнопка "Добавить аэропорт" внизу справа вкладки.
    #  По каждой кнопке открывается модальный диалог с этим аэропортом (без кнопок и параметров подключения).
    #  Поиск в базе аэропортов по кодам IATA и ICAO.
    #  Соответственно оба поля ввода IATA и ICAO неактивные.
    #  Набрать 3 XML-ных файла-образца хабов авиакомпаний (пара IATA и ICAO) и сделать с них схему dbo.SchemaHubs. Привязать схему к базе.
    #  Добавить в таблице базы поле "Hubs" типа XML (CONTENT dbo.SchemaHubs).
    #  Преимущество - не надо править таблицу в базе, можно править XML-ный файл-образец и перепривязывать схему.
    #  На диалоге аэропорта сделать:
    #  - две гиперссылки на сайт википедии ии на сайт аэропорта
    #  + Кнопка "Изменить" -> Модальный диалог с 2-мя полями ввода
    #  - кнопку, которая выводит модальный диалог с таблицей авиакомпаний, в которых он числится хабом
    myDialog.tabWidget.setTabText(2, "Хабы")
    myDialog.tabWidget.setTabText(3, "Структура")
    myDialog.tabWidget.setTabText(4, "Дополнительно")
    myDialog.tabWidget.setTabText(5, "Примечания")
    myDialog.textEdit_AirLineDescription.setEnabled(False)
    myDialog.graphicsView_Logo.setEnabled(False)
    #myDialog.tab_1.setToolTip("Общее описание авиакомпании")
    myDialog.tab_2_tableWidget_1.setEnabled(False)
    #myDialog.tab_3.setToolTip("Хабы авиакомпании")
    myDialog.tab_3_treeWidget_Hubs.setEnabled(False)
    myDialog.tab_4_listWidget_1.setEnabled(False)
    lb = QtWidgets.QLabel()
    myDialog.tab_5_toolBox_1.addItem(lb, "Указатель 01")
    lb = QtWidgets.QLabel()
    myDialog.tab_5_toolBox_1.addItem(lb, "Указатель 02")
    myDialog.tab_5_toolBox_1.setEnabled(False)
    myDialog.tab_5_treeView_1.setEnabled(False)
    myDialog.tab_6_tableView_1.setEnabled(False)
    myDialog.pushButton_Begin.setToolTip("После нажатия использовать Поиск")
    myDialog.pushButton_Begin.setEnabled(False)
    myDialog.pushButton_Previous.setToolTip("Возможны разрывы в нумерации записей в базе данных, нумерация не по порядку. Использовать Поиск")
    myDialog.pushButton_Previous.setEnabled(False)
    myDialog.pushButton_Next.setToolTip("Возможны разрывы в нумерации записей в базе данных, нумерация не по порядку. Использовать Поиск")
    myDialog.pushButton_Next.setEnabled(False)
    myDialog.pushButton_Update.setToolTip("Запись внесенных изменений\n Перед нажатием правильно заполнить и проверить введенные данные")
    myDialog.pushButton_Update.setEnabled(False)
    myDialogInputIATAandICAO.lineEdit_CodeIATA.setToolTip("Введите код IATA или поставьте галочку, если его нет")
    myDialogInputIATAandICAO.lineEdit_CodeICAO.setToolTip("Введите код ICAO или поставьте галочку, если его нет")
    myDialogInputIATAandICAO.checkBox_Status_IATA.setToolTip("Пустая ячейка в БД (не считается, как пустая строка)")
    myDialogInputIATAandICAO.checkBox_Status_ICAO.setToolTip("Пустая ячейка в БД (не считается, как пустая строка)")
    myDialog.lineEdit_AirLineID.setToolTip("Номер по старой базе данных авиакомпаний")
    myDialog.lineEdit_AirLineAlias.setToolTip("Псевдоним по старой базе данных авиакомпаний")
    myDialogInputIATAandICAO.pushButton_SearchInsert.setToolTip("Внимательно проверить введенные данные. Исправления после вставки не предусматриваются")
    # Добавляем атрибут ввода
    myDialog.lineEditCodeIATA = QtWidgets.QLineEdit()
    myDialog.lineEditCodeICAO = QtWidgets.QLineEdit()
    # Добавляем базы данных в выпадающий список
    listdbs = sorted(config_from_cfg.get(section='DataBases', option='AirLines').split(','))
    if listdbs:
        for point in listdbs:
            #point = point.lstrip(' ')
            stripped_point = point.strip()  # todo см. статью https://stackoverflow.com/questions/959215/how-do-i-remove-leading-whitespace-in-python
            myDialog.comboBox_DB.addItem(stripped_point)
    # Получаем список драйверов баз данных
    # Добавляем атрибут DriversODBC по ходу действия
    DriversODBC = sorted(acfn.getSQLDrivers())
    if DriversODBC:
        for DriverODBC in DriversODBC:
            myDialog.comboBox_Driver.addItem(str(DriverODBC))
    # Привязки обработчиков
    myDialog.pushButton_SelectDB.clicked.connect(lambda: PushButtonConnectDB())
    myDialog.pushButton_Disconnect.clicked.connect(lambda: PushButtonDisconnect())
    myDialog.pushButton_SearchByIATA.clicked.connect(lambda: PushButtonSearchByIATA())
    myDialog.pushButton_SearchByICAO.clicked.connect(lambda: PushButtonSearchByICAO())
    myDialog.pushButton_Insert.clicked.connect(lambda: PushButtonSearchByIATAandICAO())
    myDialog.pushButton_Begin.clicked.connect(lambda: PushButtonBegin())
    myDialog.pushButton_Previous.clicked.connect(lambda: PushButtonPrevious())
    myDialog.pushButton_Next.clicked.connect(lambda: PushButtonNext())
    myDialog.pushButton_Update.clicked.connect(lambda: PushButtonUpdate())
    myDialogInputIATAandICAO.pushButton_SearchInsert.clicked.connect(lambda: PushButtonInput())
    myDialogInputIATAandICAO.checkBox_Status_IATA.clicked.connect(lambda: Check_IATA())
    myDialogInputIATAandICAO.checkBox_Status_ICAO.clicked.connect(lambda: Check_ICAO())

    def PushButtonConnectDB():
        if not St.Connected_AL:
            # Переводим в неактивное состояние
            myDialog.pushButton_SelectDB.setEnabled(False)
            # Подключаемся к базе данных по выбранному источнику
            ChoiceDB = myDialog.comboBox_DB.currentText()
            ChoiceDriver = myDialog.comboBox_Driver.currentText()
            # Добавляем атрибуты DataBase, DriverODBC
            DataBase = str(ChoiceDB)
            DriverODBC = str(ChoiceDriver)
            if acfn.connect_DB_AL_odbc(servername=config_from_cfg.get(section='Servers', option='ServerNameRemote'), driver=DriverODBC, database=DataBase):
                print("  База данных ", DataBase, " подключена")
                Data = acfn.getSQLData_odbc()
                print(" Data = " + str(Data))
                St.Connected_AL = True
                # Переводим в рабочее состояние (продолжение)
                myDialog.comboBox_DB.setEnabled(False)
                myDialog.comboBox_Driver.setEnabled(False)
                myDialog.pushButton_Disconnect.setEnabled(True)
                myDialog.pushButton_Begin.setEnabled(True)  # кнопка "Начало"
                # SQL Server
                myDialog.lineEdit_Server.setText(str(Data[0]))
                myDialog.lineEdit_Server.setEnabled(True)
                myDialog.lineEdit_Server.setReadOnly(True)
                # Драйвер
                myDialog.lineEdit_Driver.setText(str(Data[1]))
                myDialog.lineEdit_Driver.setEnabled(True)
                myDialog.lineEdit_Driver.setReadOnly(True)
                # версия ODBC
                myDialog.lineEdit_ODBCversion.setText(str(Data[2]))
                myDialog.lineEdit_ODBCversion.setEnabled(True)
                myDialog.lineEdit_ODBCversion.setReadOnly(True)
                # Источник данных todo не используется, можно убрать
                #myDialog.lineEdit_DSN.setText(str(Data[3]))
                #myDialog.lineEdit_DSN.setEnabled(True)
                #myDialog.lineEdit_DSN.setReadOnly(True)
                # Схема (если из-под другой учетки, то выводит имя учетки)
                # todo Схема по умолчанию - dbo
                myDialog.lineEdit_Schema.setText(str(Data[4]))
                myDialog.lineEdit_Schema.setEnabled(True)
                myDialog.lineEdit_Schema.setReadOnly(True)
            else:
                # Переводим в рабочее состояние
                myDialog.pushButton_SelectDB.setEnabled(True)
                message = QtWidgets.QMessageBox()
                message.setText("Нет подключения к базе данных авиакомпаний")
                message.setIcon(QtWidgets.QMessageBox.Warning)
                message.exec_()

    def PushButtonDisconnect():
        # кнопка "Отключиться от базы данных"
        if St.Connected_AL:
            acfn.disconnect_AL_odbc()
            # Снимаем флаги
            St.Connected_AL = False
            # Переключаем в исходное состояние
            myDialog.comboBox_DB.setEnabled(True)
            myDialog.comboBox_Driver.setEnabled(True)
            myDialog.pushButton_SelectDB.setEnabled(True)
            myDialog.pushButton_Disconnect.setEnabled(False)
            # Параметры соединения с сервером
            myDialog.lineEdit_Server.setEnabled(False)
            myDialog.lineEdit_Driver.setEnabled(False)
            myDialog.lineEdit_ODBCversion.setEnabled(False)
            myDialog.lineEdit_Schema.setEnabled(False)
            myDialog.lineEdit_AirLineCodeIATA.setEnabled(False)
            myDialog.lineEdit_AirLineCodeICAO.setEnabled(False)
            myDialog.lineEdit_CallSign.setEnabled(False)
            myDialog.pushButton_SearchByIATA.setEnabled(False)
            myDialog.pushButton_SearchByICAO.setEnabled(False)
            myDialog.pushButton_Insert.setEnabled(False)
            myDialog.checkBox_Status.setEnabled(False)
            myDialog.textEdit_AirLineName.setEnabled(False)
            myDialog.textEdit_AirLineCity.setEnabled(False)
            myDialog.dateEdit_CreateDate.setEnabled(False)
            myDialog.textEdit_AirLineCountry.setEnabled(False)
            myDialog.comboBox_Alliance.setEnabled(False)
            myDialog.lineEdit_AirLineID.setEnabled(False)
            myDialog.lineEdit_AirLineAlias.setEnabled(False)
            myDialog.lineEdit_Position.setEnabled(False)
            myDialog.textEdit_AirLineDescription.setEnabled(False)
            myDialog.graphicsView_Logo.setEnabled(False)
            myDialog.tab_2_tableWidget_1.setEnabled(False)
            myDialog.tab_3_treeWidget_Hubs.setEnabled(False)
            myDialog.tab_4_listWidget_1.setEnabled(False)
            myDialog.tab_5_toolBox_1.setEnabled(False)
            myDialog.tab_5_treeView_1.setEnabled(False)
            myDialog.tab_6_tableView_1.setEnabled(False)
            myDialog.pushButton_Begin.setEnabled(False)
            myDialog.pushButton_Previous.setEnabled(False)
            myDialog.pushButton_Next.setEnabled(False)
            myDialog.pushButton_Update.setEnabled(False)

    def SetFields():
        # Выводим запись
        if acfn.AirLineCodeIATA is None:
            myDialog.lineEdit_AirLineCodeIATA.clear()
            myDialog.lineEdit_AirLineCodeIATA.setEnabled(False)
        else:
            myDialog.lineEdit_AirLineCodeIATA.setEnabled(True)
            myDialog.lineEdit_AirLineCodeIATA.setText(str(acfn.AirLineCodeIATA))
        if acfn.AirLineCodeICAO is None:
            myDialog.lineEdit_AirLineCodeICAO.clear()
            myDialog.lineEdit_AirLineCodeICAO.setEnabled(False)
        else:
            myDialog.lineEdit_AirLineCodeICAO.setEnabled(True)
            myDialog.lineEdit_AirLineCodeICAO.setText(str(acfn.AirLineCodeICAO))
        myDialog.lineEdit_CallSign.setText(acfn.AirLineCallSighn)
        myDialog.checkBox_Status.setChecked(acfn.AirLineStatus)
        myDialog.textEdit_AirLineName.clear()
        myDialog.textEdit_AirLineName.append(str(acfn.AirLineName))
        myDialog.textEdit_AirLineCity.clear()
        myDialog.textEdit_AirLineCity.append(str(acfn.AirLineCity))
        #myDialog.dateEdit_CreateDate.dateTimeFromText(A.CreationDate)
        # fixme Замечены случаи, что не читает дату из базы и оставляет предыдущую - ПРОВЕРЯЕМ ДАТУ ПЕРЕД ЗАПИСЬЮ
        if acfn.CreationDate:
            myDialog.dateEdit_CreateDate.setDate(QtCore.QDate.fromString(str(acfn.CreationDate), "yyyy-MM-dd"))
        else:
            myDialog.dateEdit_CreateDate.clear()
        myDialog.textEdit_AirLineCountry.clear()
        myDialog.textEdit_AirLineCountry.append(str(acfn.AirLineCountry))
        # Перезапрашиваем список алиансов и заполняем combobox каждый раз
        Alliances = acfn.QueryAlliances()
        print("Alliances = " + str(Alliances))
        myDialog.comboBox_Alliance.clear()
        if Alliances:
            for Alliance in Alliances:
                myDialog.comboBox_Alliance.addItem(str(Alliance[1]))
            # fixme Первичный ключ имеет разрывы в нумерации, индекс combobox-а - нет. Надо привести в соответствие
            # fixme Нужно вывести номер позиции "A.Alliance" в списке "PKs" (нумеруется с 0) и подставить его в "index" - СДЕЛАЛ
            PKs = []
            for PK in Alliances:
                PKs.append(PK[0])
            print("PKs = " + str(PKs))
            quantity = myDialog.comboBox_Alliance.count()
            index = PKs.index(acfn.Alliance)  # нумеруется с 0
            print("index = " + str(index))
            # todo - Адаптированное решение по подсказке с https://stackoverflow.com/questions/75496493/search-position-in-two-dimensional-list?noredirect=1#comment133202629_75496493 - РАБОТАЕТ
            index_improved = next((i for i, x in enumerate(Alliances) if x[0] == acfn.Alliance), None)
            if index_improved is None:
                index_improved = 3  # Unknown Alliance
                print("Альянс не найден в списке")
            else:
                print("Альянс = " + str(index_improved))
            myDialog.comboBox_Alliance.setCurrentIndex(index_improved)
        myDialog.lineEdit_AirLineID.setText(str(acfn.AirLine_ID))
        myDialog.lineEdit_AirLineAlias.setText(str(acfn.AirLineAlias))
        # Выводим позицию
        myDialog.lineEdit_Position.setText(str(acfn.Position))
        myDialog.lineEdit_Position.setReadOnly(True)
        myDialog.textEdit_AirLineDescription.clear()
        myDialog.textEdit_AirLineDescription.append(str(acfn.AirLineDescription))
        print("Поля ввода заполнены\n")

    def PushButtonSearchByIATA():
        # Кнопка "Поиск"
        LineCodeIATA, ok = QtWidgets.QInputDialog.getText(myDialog, "Код IATA", "Введите код IATA")
        if ok:
            myDialog.lineEditCodeIATA.setText(str(LineCodeIATA))
            Code = myDialog.lineEditCodeIATA.text()
            DBAirLine = acfn.QueryAirLineByIATA(Code)
            # fixme Решение 3 - не перезаписывать код IATA (Недостаток - можно сделать дубликат по коду ICAO, их много, возможно это НОРМА, исправлять только вручную)
            # fixme Решение 4 - код IATA всегда неактивный, он вводится только при вставке
            if DBAirLine is not None:
                acfn.Position = DBAirLine.AirLineUniqueNumber
                acfn.AirLine_ID = DBAirLine.AirLine_ID
                acfn.AirLineName = DBAirLine.AirLineName
                acfn.AirLineAlias = DBAirLine.AirLineAlias
                acfn.AirLineCodeIATA = DBAirLine.AirLineCodeIATA
                acfn.AirLineCodeICAO = DBAirLine.AirLineCodeICAO
                acfn.AirLineCallSighn = DBAirLine.AirLineCallSighn
                acfn.AirLineCity = DBAirLine.AirLineCity
                acfn.AirLineCountry = DBAirLine.AirLineCountry
                if DBAirLine.AirLineStatus is not None:
                    acfn.AirLineStatus = DBAirLine.AirLineStatus
                else:
                    acfn.AirLineStatus = False
                if DBAirLine.CreationDate:
                    acfn.CreationDate = DBAirLine.CreationDate
                acfn.AirLineDescription = DBAirLine.AirLineDescription
                acfn.Alliance = DBAirLine.Alliance
            elif DBAirLine is None:
                message = QtWidgets.QMessageBox()
                message.setText("Запись не найдена")
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.exec_()
            else:
                pass
            if acfn.Position == 1:
                myDialog.pushButton_Begin.setEnabled(False)
                myDialog.pushButton_Previous.setEnabled(False)
            if acfn.Position >= 2:
                myDialog.pushButton_Begin.setEnabled(True)
                myDialog.pushButton_Previous.setEnabled(True)
            SetFields()

    def PushButtonSearchByICAO():
        # Кнопка "Поиск"
        LineCodeICAO, ok = QtWidgets.QInputDialog.getText(myDialog, "Код ICAO", "Введите код ICAO")
        if ok:
            myDialog.lineEditCodeICAO.setText(str(LineCodeICAO))
            Code = myDialog.lineEditCodeICAO.text()
            DBAirLine = acfn.QueryAirLineByICAO(Code)
            if DBAirLine is not None:
                acfn.Position = DBAirLine.AirLineUniqueNumber
                acfn.AirLine_ID = DBAirLine.AirLine_ID
                acfn.AirLineName = DBAirLine.AirLineName
                acfn.AirLineAlias = DBAirLine.AirLineAlias
                acfn.AirLineCodeIATA = DBAirLine.AirLineCodeIATA
                acfn.AirLineCodeICAO = DBAirLine.AirLineCodeICAO
                acfn.AirLineCallSighn = DBAirLine.AirLineCallSighn
                acfn.AirLineCity = DBAirLine.AirLineCity
                acfn.AirLineCountry = DBAirLine.AirLineCountry
                if DBAirLine.AirLineStatus is not None:
                    acfn.AirLineStatus = DBAirLine.AirLineStatus
                else:
                    acfn.AirLineStatus = False
                if DBAirLine.CreationDate:
                    acfn.CreationDate = DBAirLine.CreationDate
                acfn.AirLineDescription = DBAirLine.AirLineDescription
                acfn.Alliance = DBAirLine.Alliance
            elif DBAirLine is None:
                message = QtWidgets.QMessageBox()
                message.setText("Запись не найдена")
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.exec_()
            else:
                pass
            if acfn.Position == 1:
                myDialog.pushButton_Begin.setEnabled(False)
                myDialog.pushButton_Previous.setEnabled(False)
            if acfn.Position >= 2:
                myDialog.pushButton_Begin.setEnabled(True)
                myDialog.pushButton_Previous.setEnabled(True)
            SetFields()

    def PushButtonSearchByIATAandICAO():
        # кнопка "Поиск и Вставка"
        # Отрисовка диалога ввода
        myDialogInputIATAandICAO.setWindowTitle("Диалог ввода")
        myDialogInputIATAandICAO.setWindowModality(QtCore.Qt.ApplicationModal)
        myDialogInputIATAandICAO.show()

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
        DBAirLine = acfn.QueryAirLineByIATAandICAO(iata=Code_IATA, icao=Code_ICAO)
        myDialogInputIATAandICAO.close()

        def Transfer():
            acfn.Position = DBAirLine.AirLineUniqueNumber
            acfn.AirLine_ID = DBAirLine.AirLine_ID
            acfn.AirLineName = DBAirLine.AirLineName
            acfn.AirLineAlias = DBAirLine.AirLineAlias
            acfn.AirLineCodeIATA = DBAirLine.AirLineCodeIATA
            acfn.AirLineCodeICAO = DBAirLine.AirLineCodeICAO
            acfn.AirLineCallSighn = DBAirLine.AirLineCallSighn
            acfn.AirLineCity = DBAirLine.AirLineCity
            acfn.AirLineCountry = DBAirLine.AirLineCountry
            if DBAirLine.AirLineStatus is not None:
                acfn.AirLineStatus = DBAirLine.AirLineStatus
            else:
                acfn.AirLineStatus = False
            if DBAirLine.CreationDate:
                acfn.CreationDate = DBAirLine.CreationDate
            acfn.AirLineDescription = DBAirLine.AirLineDescription
            if DBAirLine.Alliance:
                acfn.Alliance = DBAirLine.Alliance
            else:
                acfn.Alliance = 4
            if acfn.Position == 1:
                myDialog.pushButton_Begin.setEnabled(False)
                myDialog.pushButton_Previous.setEnabled(False)
            if acfn.Position >= 2:
                myDialog.pushButton_Begin.setEnabled(True)
                myDialog.pushButton_Previous.setEnabled(True)
            SetFields()

        if DBAirLine is not None:
            # Переходим на найденную запись
            Transfer()
            message = QtWidgets.QMessageBox()
            message.setText("Такая запись есть")
            message.setIcon(QtWidgets.QMessageBox.Information)
            message.exec_()
        elif DBAirLine is None:
            # Вставка новой строки
            ResultInsert = acfn.InsertAirLineByIATAandICAO(iata=Code_IATA, icao=Code_ICAO)
            if ResultInsert:
                DBAirLine = acfn.QueryAirLineByIATAandICAO(Code_IATA, Code_ICAO)
                if DBAirLine is not None:
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
        DBAirLine = acfn.QueryAirLineByPK(acfn.Position)
        if DBAirLine is not None:
            acfn.AirLine_ID = DBAirLine.AirLine_ID
            acfn.AirLineName = DBAirLine.AirLineName
            acfn.AirLineAlias = DBAirLine.AirLineAlias
            acfn.AirLineCodeIATA = DBAirLine.AirLineCodeIATA
            acfn.AirLineCodeICAO = DBAirLine.AirLineCodeICAO
            acfn.AirLineCallSighn = DBAirLine.AirLineCallSighn
            acfn.AirLineCity = DBAirLine.AirLineCity
            acfn.AirLineCountry = DBAirLine.AirLineCountry
            if DBAirLine.AirLineStatus is not None:
                acfn.AirLineStatus = DBAirLine.AirLineStatus
            else:
                acfn.AirLineStatus = False
            if DBAirLine.CreationDate:
                acfn.CreationDate = DBAirLine.CreationDate
            acfn.AirLineDescription = DBAirLine.AirLineDescription
            if DBAirLine.Alliance:
                acfn.Alliance = DBAirLine.Alliance
            else:
                acfn.Alliance = 4
            SetFields()
            return True
        elif DBAirLine is None:
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

    def PushButtonBegin():
        # кнопка "Начало"
        #A.Position = 10
        myDialog.pushButton_Previous.setEnabled(False)
        #Result = CommonPart()
        Result = True
        if Result:
            # переводим в рабочее состояние (окончание)
            myDialog.lineEdit_AirLineCodeIATA.setEnabled(True)
            myDialog.lineEdit_AirLineCodeICAO.setEnabled(True)
            myDialog.lineEdit_CallSign.setEnabled(True)
            myDialog.pushButton_SearchByIATA.setEnabled(True)
            myDialog.pushButton_SearchByICAO.setEnabled(True)
            myDialog.pushButton_Insert.setEnabled(True)
            myDialog.checkBox_Status.setEnabled(True)
            myDialog.textEdit_AirLineName.setEnabled(True)
            myDialog.textEdit_AirLineCity.setEnabled(True)
            myDialog.dateEdit_CreateDate.setEnabled(True)
            myDialog.dateEdit_CreateDate.setCalendarPopup(True)
            #myDialog.dateEdit_CreateDate.setDisplayFormat("yyyy-mm-dd")
            myDialog.textEdit_AirLineCountry.setEnabled(True)
            myDialog.comboBox_Alliance.setEnabled(True)
            myDialog.lineEdit_AirLineID.setEnabled(True)
            myDialog.lineEdit_AirLineAlias.setEnabled(True)
            myDialog.lineEdit_Position.setEnabled(False)
            myDialog.textEdit_AirLineDescription.setEnabled(True)
            myDialog.graphicsView_Logo.setEnabled(True)
            myDialog.tab_2_tableWidget_1.setEnabled(True)
            myDialog.tab_3_treeWidget_Hubs.setEnabled(True)
            myDialog.tab_4_listWidget_1.setEnabled(True)
            myDialog.tab_5_toolBox_1.setEnabled(True)
            myDialog.tab_5_treeView_1.setEnabled(True)
            myDialog.tab_6_tableView_1.setEnabled(True)
            myDialog.pushButton_Begin.setEnabled(True)
            myDialog.pushButton_Previous.setEnabled(False)
            myDialog.pushButton_Next.setEnabled(True)
            myDialog.pushButton_Update.setEnabled(True)
            # Таблица на второй вкладке Свойств
            table1_CountCol = 4
            table1_RowCount = 24
            myDialog.tab_2_tableWidget_1.setColumnCount(table1_CountCol)
            myDialog.tab_2_tableWidget_1.setRowCount(table1_RowCount)
            namesC = []
            cbs = []
            cals = []
            pbs = []
            for i in range(table1_RowCount):
                namesC.append("C" + str(i+1))
                twi_a = QtWidgets.QTableWidgetItem("String " + str(i + 1))
                myDialog.tab_2_tableWidget_1.setItem(i, 1, twi_a)
                cb1 = QtWidgets.QComboBox()
                for j in range(25):
                    cb1.addItem("Item " + str(j + 1))
                cbs.append(cb1)
                myDialog.tab_2_tableWidget_1.setCellWidget(i, 0, cbs[i])
                cal1 = QtWidgets.QDateEdit()
                cal1.setCalendarPopup(True)
                cals.append(cal1)
                myDialog.tab_2_tableWidget_1.setCellWidget(i, table1_CountCol - 2, cals[i])
                pb1 = QtWidgets.QPushButton()
                pb1.setText("pb1")
                pbs.append(pb1)
                myDialog.tab_2_tableWidget_1.setCellWidget(i, table1_CountCol - 1, pbs[i])
            myDialog.tab_2_tableWidget_1.setHorizontalHeaderLabels(namesC)
            tree_CountCol = 5
            myDialog.tab_3_treeWidget_Hubs.setColumnCount(tree_CountCol)
            labels = []
            for i in range(tree_CountCol):
                labels.append("L" + str(i + 1))
            myDialog.tab_3_treeWidget_Hubs.setHeaderLabels(labels)
            #l1 = QtWidgets.QTreeWidgetItem(["String A", "String B", "String C", "String D", "String E"])
            #l2 = QtWidgets.QTreeWidgetItem(["String AA", "String BB", "String CC", "String DD", "String EE"])
            #myDialog.treeWidget_Hubs.addTopLevelItems(l1)
            #myDialog.treeWidget_Hubs.addTopLevelItems(l2)
            # Таблица с данными на шестой вкладке Свойств

    def PushButtonPrevious():
        # кнопка "Предыдущий"
        acfn.Position -= 1
        CommonPart()
        if acfn.Position == 1:
            myDialog.pushButton_Begin.setEnabled(False)
            myDialog.pushButton_Previous.setEnabled(False)

    def PushButtonNext():
        # кнопка "Следующий"
        acfn.Position += 1
        CommonPart()
        myDialog.pushButton_Begin.setEnabled(True)
        myDialog.pushButton_Previous.setEnabled(True)

    def PushButtonUpdate():
        # Кнопка "Записать"
        # todo Вставить диалог выбора и проверки сертификата (ЭЦП) и условный переход с проверкой
        acfn.AirLine_ID = myDialog.lineEdit_AirLineID.text()
        acfn.AirLineName = myDialog.textEdit_AirLineName.toPlainText()
        acfn.AirLineAlias = myDialog.lineEdit_AirLineAlias.text()
        acfn.AirLineCallSighn = myDialog.lineEdit_CallSign.text()
        acfn.AirLineCity = myDialog.textEdit_AirLineCity.toPlainText()
        acfn.AirLineCountry = myDialog.textEdit_AirLineCountry.toPlainText()
        if myDialog.checkBox_Status.isChecked():
            acfn.AirLineStatus = 1  # True в Python-е -> 1 в SQL(bit)
        else:
            acfn.AirLineStatus = 0  # False в Python-е -> 0 в SQL(bit)
        acfn.CreationDate = myDialog.dateEdit_CreateDate.date().toString('yyyy-MM-dd')
        acfn.AirLineDescription = myDialog.textEdit_AirLineDescription.toPlainText()
        index = myDialog.comboBox_Alliance.currentIndex()
        acfn.Alliance = index + 1  # первичный ключ альянса
        print("old AlliancePK for update =" + str(acfn.Alliance))
        acfn.Alliance = acfn.QueryAlliancePKByName(myDialog.comboBox_Alliance.currentText())
        print("AlliancePK for update =" + str(acfn.Alliance))
        # Вносим изменение
        ResultUpdate = acfn.UpdateAirLineByIATAandICAO(acfn.AirLine_ID,
                                                  acfn.AirLineName,
                                                  acfn.AirLineAlias,
                                                  acfn.AirLineCodeIATA,
                                                  acfn.AirLineCodeICAO,
                                                  acfn.AirLineCallSighn,
                                                  acfn.AirLineCity,
                                                  acfn.AirLineCountry,
                                                  acfn.AirLineStatus,
                                                  acfn.CreationDate,
                                                  acfn.AirLineDescription,
                                                  acfn.Alliance)
        if not ResultUpdate:
            message = QtWidgets.QMessageBox()
            message.setText("Запись не переписалась")
            message.setIcon(QtWidgets.QMessageBox.Warning)
            message.exec_()
    # Отрисовка диалога
    myDialog.show()
    # Правильное закрытие окна
    sys.exit(myApp.exec_())


# Точка входа
# __name__ — это специальная переменная, которая будет равна __main__, только если файл запускается как основная программа, в остальных случаях - имени модуля при импорте в качестве модуля
if __name__ == "__main__":
    myApplication()
