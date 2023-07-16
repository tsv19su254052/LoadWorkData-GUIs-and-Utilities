#  Interpreter 3.7 -> 3.10 -> 3.11


# QtSQL медленнее, чем pyodbc
import pyodbc
import sys
from PyQt5 import QtWidgets, QtCore

# Импорт пользовательской библиотеки (файла *.py в этой же папке)
import Classes


# Делаем экземпляры
# fixme При наследовании с композицией непонятно - где и в каких местах участвуют части предков
A = Classes.AirLine()
S = Classes.Servers()
# Добавляем аттрибуты
S.ServerName = "data-server-1.movistar.vrn.skylink.local"
S.Connected_AL = False
S.Connected_AC = False
S.Connected_RT = False
S.Connected_FN = False


# Основная функция
def myApplication():
    # Одно прикладное приложение
    # todo Делаем сопряжение экземпляров классов с SQL-ными базами данных - семантическими противоположностями ООП, примеров мало
    myApp = QtWidgets.QApplication(sys.argv)
    # fixme Правильно делать экземпляр с композицией
    # Делаем экземпляры
    myDialog = Classes.Ui_DialogCorrectAirLine()
    myDialog.setupUi(Dialog=myDialog)  # надо вызывать явно
    myDialog.setFixedSize(862, 830)
    myDialog.setWindowTitle('АвиаКомпании')
    myDialogInput = Classes.Ui_DialogCorrectAirLineInput()
    myDialogInput.setupUi(Dialog=myDialogInput)
    myDialogInput.setFixedSize(240, 245)
    # Переводим в исходное состояние
    #myDialogInput.checkBox_Status_IATA.isChecked(False)
    #myDialogInput.checkBox_Status_ICAO.isChecked(False)
    # Дополняем функционал экземпляра главного диалога
    # Переводим в исходное состояние
    myDialog.comboBox_Driver.setToolTip("предпочтительно - драйвер ODBC для SDK SQL Server-а \n(работает во всех режимах, полностью функционален, расходует больше ресурсов сервера) \nдля просмотра и внесения исправлений компл. драйвер SQL Server-а \n (не отрабатывает вложенные обработки исключений)")
    myDialog.pushButton_SelectDB.setToolTip("После подключения нажмите кнопку Начало, далее - Поиск")
    myDialog.pushButton_Disconnect.setToolTip("Перед закрытием диалога отключиться от базы данных")
    myDialog.pushButton_Disconnect.setEnabled(False)
    # Параметры соединения с сервером
    myDialog.lineEdit_Server.setEnabled(False)
    myDialog.lineEdit_Driver.setEnabled(False)
    myDialog.lineEdit_ODBCversion.setEnabled(False)
    myDialog.lineEdit_DSN.setEnabled(False)
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
    myDialog.comboBox_Alliance.setEditable(True)
    myDialog.comboBox_Alliance.setEnabled(False)
    myDialog.lineEdit_AirLineID.setEnabled(False)
    myDialog.lineEdit_AirLineAlias.setEnabled(False)
    myDialog.lineEdit_Position.setEnabled(False)
    # todo Сделать 2 гиперссылки на:
    #  сайт на википедии,
    #  сайт авиакомпании
    #  + Кнопку диалога их правки (чтобы не выводить длинную краказябру, подставить псевдонимы)
    #  Простенькие примеры с https://stackoverflow.com/questions/29987065/how-can-i-make-link-on-web-page-in-window-using-pyqt4
    """
    Бесхозный многострочный текст в роли комментария
    ------------------------------------------------------------
    from PyQt5.QtGui import QDesktopServices
    from PyQt5.QtCore import QUrl

    class MainWindow(QMainWindow, Ui_MainWindow):
        def link(self, linkStr):
            QDesktopServices.openUrl(QUrl(linkStr))

        def __init__(self):
            super(MainWindow, self).__init__()

            # Set up the user interface from Designer.
            self.setupUi(self)
            self.label.linkActivated.connect(self.link)
            self.label.setText('<a href="http://stackoverflow.com/">Stackoverflow/</a>')  # Адрес + Псевдоним

    -------------------------------------------------------------
    label.setText('<a href="http://stackoverflow.com/">Link</a>')  # Адрес + Псевдоним
    label.setOpenExternalLinks(True)
    -------------------------------------------------------------
    from PyQt5 import QtWidgets

    app = QtWidgets.QApplication([])
    w = QtWidgets.QMainWindow()
    QtWidgets.QLabel(parent=w, text='Hover mouse here', toolTip='<a href="http://google.com">Unclickable link</a>')  # Адрес + Псевдоним
    w.show()
    app.exec_()
    -------------------------------------------------------------
    """

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
    myDialogInput.lineEdit_AirLineCodeIATA.setToolTip("Введите код IATA или поставьте галочку, если его нет")
    myDialogInput.lineEdit_AirLineCodeICAO.setToolTip("Введите код ICAO или поставьте галочку, если его нет")
    myDialogInput.checkBox_Status_IATA.setToolTip("Пустая ячейка в БД (не считается, как пустая строка)")
    myDialogInput.checkBox_Status_ICAO.setToolTip("Пустая ячейка в БД (не считается, как пустая строка)")
    myDialog.lineEdit_AirLineID.setToolTip("Номер по старой базе данных авиакомпаний")
    myDialog.lineEdit_AirLineAlias.setToolTip("Псевдоним по старой базе данных авиакомпаний")
    myDialogInput.pushButton_SearchInsert.setToolTip("Внимательно проверить введенные данные. Исправления после вставки не предусматриваются")
    # Добавляем атрибут ввода
    myDialog.lineEditCodeIATA = QtWidgets.QLineEdit()
    myDialog.lineEditCodeICAO = QtWidgets.QLineEdit()
    # Добавляем базы данных в выпадающий список
    myDialog.comboBox_DB.addItem("AirLinesDBNew62")
    # Получаем список драйверов баз данных
    # Добавляем атрибут DriversODBC по ходу действия
    S.DriversODBC = pyodbc.drivers()
    if S.DriversODBC:
        for DriverODBC in S.DriversODBC:
            if not DriverODBC:
                break
            myDialog.comboBox_Driver.addItem(str(DriverODBC))
    # Привязки обработчиков
    myDialog.pushButton_SelectDB.clicked.connect(lambda: PushButtonSelectDB())
    myDialog.pushButton_Disconnect.clicked.connect(lambda: PushButtonDisconnect())
    myDialog.pushButton_SearchByIATA.clicked.connect(lambda: PushButtonSearchByIATA())
    myDialog.pushButton_SearchByICAO.clicked.connect(lambda: PushButtonSearchByICAO())
    myDialog.pushButton_Insert.clicked.connect(lambda: PushButtonSearchByIATAandICAO())
    myDialog.pushButton_Begin.clicked.connect(lambda: PushButtonBegin())
    myDialog.pushButton_Previous.clicked.connect(lambda: PushButtonPrevious())
    myDialog.pushButton_Next.clicked.connect(lambda: PushButtonNext())
    myDialog.pushButton_Update.clicked.connect(lambda: PushButtonUpdate())
    myDialogInput.pushButton_SearchInsert.clicked.connect(lambda: PushButtonInsert())
    myDialogInput.checkBox_Status_IATA.clicked.connect(lambda: Check_IATA())
    myDialogInput.checkBox_Status_ICAO.clicked.connect(lambda: Check_ICAO())

    def PushButtonSelectDB():
        if not S.Connected_AL:
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
                # Переводим в рабочее состояние (продолжение)
                myDialog.comboBox_DB.setEnabled(False)
                myDialog.comboBox_Driver.setEnabled(False)
                myDialog.pushButton_Disconnect.setEnabled(True)
                myDialog.pushButton_Begin.setEnabled(True)  # кнопка "Начало"
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
                # SQL Server
                myDialog.lineEdit_Server.setText(S.cnxnAL.getinfo(pyodbc.SQL_SERVER_NAME))
                myDialog.lineEdit_Server.setEnabled(True)
                # Драйвер
                myDialog.lineEdit_Driver.setText(S.cnxnAL.getinfo(pyodbc.SQL_DRIVER_NAME))
                myDialog.lineEdit_Driver.setEnabled(True)
                # версия ODBC
                myDialog.lineEdit_ODBCversion.setText(S.cnxnAL.getinfo(pyodbc.SQL_ODBC_VER))
                myDialog.lineEdit_ODBCversion.setEnabled(True)
                # Источник данных
                myDialog.lineEdit_DSN.setText(S.cnxnAL.getinfo(pyodbc.SQL_DATA_SOURCE_NAME))
                myDialog.lineEdit_DSN.setEnabled(True)
                # Схема (если из-под другой учетки, то выводит имя учетки)
                # todo Схема по умолчанию - dbo
                myDialog.lineEdit_Schema.setText(S.cnxnAL.getinfo(pyodbc.SQL_USER_NAME))
                myDialog.lineEdit_Schema.setEnabled(True)
                # Переводим в рабочее состояние
                myDialog.pushButton_SelectDB.setEnabled(False)
            except Exception:
                message = QtWidgets.QMessageBox()
                message.setText("Нет подключения к базе данных авиакомпаний")
                message.setIcon(QtWidgets.QMessageBox.Warning)
                message.exec_()
            else:
                pass
            finally:
                pass

    def PushButtonDisconnect():
        # кнопка "Отключиться от базы данных"
        if S.Connected_AL:
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
            myDialog.pushButton_SelectDB.setEnabled(True)
            myDialog.pushButton_Disconnect.setEnabled(False)
            # Параметры соединения с сервером
            myDialog.lineEdit_Server.setEnabled(False)
            myDialog.lineEdit_Driver.setEnabled(False)
            myDialog.lineEdit_ODBCversion.setEnabled(False)
            myDialog.lineEdit_DSN.setEnabled(False)
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
        if A.AirLineCodeIATA is None:
            myDialog.lineEdit_AirLineCodeIATA.clear()
            myDialog.lineEdit_AirLineCodeIATA.setEnabled(False)
        else:
            myDialog.lineEdit_AirLineCodeIATA.setEnabled(True)
            myDialog.lineEdit_AirLineCodeIATA.setText(str(A.AirLineCodeIATA))
        if A.AirLineCodeICAO is None:
            myDialog.lineEdit_AirLineCodeICAO.clear()
            myDialog.lineEdit_AirLineCodeICAO.setEnabled(False)
        else:
            myDialog.lineEdit_AirLineCodeICAO.setEnabled(True)
            myDialog.lineEdit_AirLineCodeICAO.setText(str(A.AirLineCodeICAO))
        myDialog.lineEdit_CallSign.setText(A.AirLineCallSighn)
        myDialog.checkBox_Status.setChecked(A.AirLineStatus)
        myDialog.textEdit_AirLineName.clear()
        myDialog.textEdit_AirLineName.append(str(A.AirLineName))
        myDialog.textEdit_AirLineCity.clear()
        myDialog.textEdit_AirLineCity.append(str(A.AirLineCity))
        #myDialog.dateEdit_CreateDate.dateTimeFromText(A.CreationDate)
        # fixme Замечены случаи, что не читает дату из базы и оставляет предыдущую - ПРОВЕРЯЕМ ДАТУ ПЕРЕД ЗАПИСЬЮ
        if A.CreationDate:
            myDialog.dateEdit_CreateDate.setDate(QtCore.QDate.fromString(str(A.CreationDate), "yyyy-MM-dd"))
        else:
            myDialog.dateEdit_CreateDate.clear()
        myDialog.textEdit_AirLineCountry.clear()
        myDialog.textEdit_AirLineCountry.append(str(A.AirLineCountry))
        # Перезапрашиваем список алиансов и заполняем combobox каждый раз
        Alliances = S.QueryAlliances()
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
            index = PKs.index(A.Alliance)  # нумеруется с 0
            print("index = " + str(index))
            # todo - Адаптированное решение с https://stackoverflow.com/questions/75496493/search-position-in-two-dimensional-list?noredirect=1#comment133202629_75496493 - РАБОТАЕТ
            index_improved = next((i for i, x in enumerate(Alliances) if x[0] == A.Alliance), None)
            if index_improved is None:
                index_improved = 3  # Unknown Alliance
                print("Альянс не найден в списке")
            else:
                print("Альянс = " + str(index_improved))
            myDialog.comboBox_Alliance.setCurrentIndex(index_improved)
        myDialog.lineEdit_AirLineID.setText(str(A.AirLine_ID))
        myDialog.lineEdit_AirLineAlias.setText(str(A.AirLineAlias))
        # Выводим позицию
        myDialog.lineEdit_Position.setText(str(A.Position))
        myDialog.textEdit_AirLineDescription.clear()
        myDialog.textEdit_AirLineDescription.append(str(A.AirLineDescription))
        print("Поля ввода заполнены\n")

    def PushButtonSearchByIATA():
        # Кнопка "Поиск"
        LineCodeIATA, ok = QtWidgets.QInputDialog.getText(myDialog, "Код IATA", "Введите код IATA")
        if ok:
            myDialog.lineEditCodeIATA.setText(str(LineCodeIATA))
            Code = myDialog.lineEditCodeIATA.text()
            DBAirLine = S.QueryAirLineByIATA(Code)
            # fixme Решение 3 - не перезаписывать код IATA (Недостаток - можно сделать дубликат по коду ICAO, их много, возможно это НОРМА, исправлять только вручную)
            # fixme Решение 4 - код IATA всегда неактивный, он вводится только при вставке
            if DBAirLine is not None:
                A.Position = DBAirLine.AirLineUniqueNumber
                A.AirLine_ID = DBAirLine.AirLine_ID
                A.AirLineName = DBAirLine.AirLineName
                A.AirLineAlias = DBAirLine.AirLineAlias
                A.AirLineCodeIATA = DBAirLine.AirLineCodeIATA
                A.AirLineCodeICAO = DBAirLine.AirLineCodeICAO
                A.AirLineCallSighn = DBAirLine.AirLineCallSighn
                A.AirLineCity = DBAirLine.AirLineCity
                A.AirLineCountry = DBAirLine.AirLineCountry
                if DBAirLine.AirLineStatus is not None:
                    A.AirLineStatus = DBAirLine.AirLineStatus
                else:
                    A.AirLineStatus = False
                if DBAirLine.CreationDate:
                    A.CreationDate = DBAirLine.CreationDate
                A.AirLineDescription = DBAirLine.AirLineDescription
                A.Alliance = DBAirLine.Alliance
            elif DBAirLine is None:
                message = QtWidgets.QMessageBox()
                message.setText("Запись не найдена")
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.exec_()
            else:
                pass
            if A.Position == 1:
                myDialog.pushButton_Begin.setEnabled(False)
                myDialog.pushButton_Previous.setEnabled(False)
            if A.Position >= 2:
                myDialog.pushButton_Begin.setEnabled(True)
                myDialog.pushButton_Previous.setEnabled(True)
            SetFields()

    def PushButtonSearchByICAO():
        # Кнопка "Поиск"
        LineCodeICAO, ok = QtWidgets.QInputDialog.getText(myDialog, "Код ICAO", "Введите код ICAO")
        if ok:
            myDialog.lineEditCodeICAO.setText(str(LineCodeICAO))
            Code = myDialog.lineEditCodeICAO.text()
            DBAirLine = S.QueryAirLineByICAO(Code)
            if DBAirLine is not None:
                A.Position = DBAirLine.AirLineUniqueNumber
                A.AirLine_ID = DBAirLine.AirLine_ID
                A.AirLineName = DBAirLine.AirLineName
                A.AirLineAlias = DBAirLine.AirLineAlias
                A.AirLineCodeIATA = DBAirLine.AirLineCodeIATA
                A.AirLineCodeICAO = DBAirLine.AirLineCodeICAO
                A.AirLineCallSighn = DBAirLine.AirLineCallSighn
                A.AirLineCity = DBAirLine.AirLineCity
                A.AirLineCountry = DBAirLine.AirLineCountry
                if DBAirLine.AirLineStatus is not None:
                    A.AirLineStatus = DBAirLine.AirLineStatus
                else:
                    A.AirLineStatus = False
                if DBAirLine.CreationDate:
                    A.CreationDate = DBAirLine.CreationDate
                A.AirLineDescription = DBAirLine.AirLineDescription
                A.Alliance = DBAirLine.Alliance
            elif DBAirLine is None:
                message = QtWidgets.QMessageBox()
                message.setText("Запись не найдена")
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.exec_()
            else:
                pass
            if A.Position == 1:
                myDialog.pushButton_Begin.setEnabled(False)
                myDialog.pushButton_Previous.setEnabled(False)
            if A.Position >= 2:
                myDialog.pushButton_Begin.setEnabled(True)
                myDialog.pushButton_Previous.setEnabled(True)
            SetFields()

    def PushButtonSearchByIATAandICAO():
        # кнопка "Поиск и Вставка"
        # Отрисовка диалога ввода
        myDialogInput.setWindowTitle("Диалог ввода")
        myDialogInput.setWindowModality(QtCore.Qt.ApplicationModal)
        myDialogInput.show()
        # Привязки обработчиков

    def Check_IATA():
        if myDialogInput.checkBox_Status_IATA.isChecked():
            myDialogInput.lineEdit_AirLineCodeIATA.setEnabled(False)
        else:
            myDialogInput.lineEdit_AirLineCodeIATA.setEnabled(True)

    def Check_ICAO():
        if myDialogInput.checkBox_Status_ICAO.isChecked():
            myDialogInput.lineEdit_AirLineCodeICAO.setEnabled(False)
        else:
            myDialogInput.lineEdit_AirLineCodeICAO.setEnabled(True)

    def PushButtonInsert():
        if myDialogInput.checkBox_Status_IATA.isChecked():
            Code_IATA = None
        else:
            Code_IATA = myDialogInput.lineEdit_AirLineCodeIATA.text()
        if myDialogInput.checkBox_Status_ICAO.isChecked():
            Code_ICAO = None
        else:
            Code_ICAO = myDialogInput.lineEdit_AirLineCodeICAO.text()
        DBAirLine = S.QueryAirLineByIATAandICAO(iata=Code_IATA, icao=Code_ICAO)
        myDialogInput.close()

        def Transfer():
            A.Position = DBAirLine.AirLineUniqueNumber
            A.AirLine_ID = DBAirLine.AirLine_ID
            A.AirLineName = DBAirLine.AirLineName
            A.AirLineAlias = DBAirLine.AirLineAlias
            A.AirLineCodeIATA = DBAirLine.AirLineCodeIATA
            A.AirLineCodeICAO = DBAirLine.AirLineCodeICAO
            A.AirLineCallSighn = DBAirLine.AirLineCallSighn
            A.AirLineCity = DBAirLine.AirLineCity
            A.AirLineCountry = DBAirLine.AirLineCountry
            if DBAirLine.AirLineStatus is not None:
                A.AirLineStatus = DBAirLine.AirLineStatus
            else:
                A.AirLineStatus = False
            if DBAirLine.CreationDate:
                A.CreationDate = DBAirLine.CreationDate
            A.AirLineDescription = DBAirLine.AirLineDescription
            if DBAirLine.Alliance:
                A.Alliance = DBAirLine.Alliance
            else:
                A.Alliance = 4
            if A.Position == 1:
                myDialog.pushButton_Begin.setEnabled(False)
                myDialog.pushButton_Previous.setEnabled(False)
            if A.Position >= 2:
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
            ResultInsert = S.InsertAirLineByIATAandICAO(Code_IATA, Code_ICAO)
            if ResultInsert:
                DBAirLine = S.QueryAirLineByIATAandICAO(Code_IATA, Code_ICAO)
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
        DBAirLine = S.QueryAirLineByPK(A.Position)
        if DBAirLine is not None:
            A.AirLine_ID = DBAirLine.AirLine_ID
            A.AirLineName = DBAirLine.AirLineName
            A.AirLineAlias = DBAirLine.AirLineAlias
            A.AirLineCodeIATA = DBAirLine.AirLineCodeIATA
            A.AirLineCodeICAO = DBAirLine.AirLineCodeICAO
            A.AirLineCallSighn = DBAirLine.AirLineCallSighn
            A.AirLineCity = DBAirLine.AirLineCity
            A.AirLineCountry = DBAirLine.AirLineCountry
            if DBAirLine.AirLineStatus is not None:
                A.AirLineStatus = DBAirLine.AirLineStatus
            else:
                A.AirLineStatus = False
            if DBAirLine.CreationDate:
                A.CreationDate = DBAirLine.CreationDate
            A.AirLineDescription = DBAirLine.AirLineDescription
            if DBAirLine.Alliance:
                A.Alliance = DBAirLine.Alliance
            else:
                A.Alliance = 4
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
        A.Position -= 1
        CommonPart()
        if A.Position == 1:
            myDialog.pushButton_Begin.setEnabled(False)
            myDialog.pushButton_Previous.setEnabled(False)

    def PushButtonNext():
        # кнопка "Следующий"
        A.Position += 1
        CommonPart()
        myDialog.pushButton_Begin.setEnabled(True)
        myDialog.pushButton_Previous.setEnabled(True)

    def PushButtonUpdate():
        # Кнопка "Записать"
        # todo Вставить диалог выбора и проверки сертификата (ЭЦП) и условный переход с проверкой
        A.AirLine_ID = myDialog.lineEdit_AirLineID.text()
        A.AirLineName = myDialog.textEdit_AirLineName.toPlainText()
        A.AirLineAlias = myDialog.lineEdit_AirLineAlias.text()
        A.AirLineCallSighn = myDialog.lineEdit_CallSign.text()
        A.AirLineCity = myDialog.textEdit_AirLineCity.toPlainText()
        A.AirLineCountry = myDialog.textEdit_AirLineCountry.toPlainText()
        if myDialog.checkBox_Status.isChecked():
            A.AirLineStatus = 1  # True в Python-е -> 1 в SQL(bit)
        else:
            A.AirLineStatus = 0  # False в Python-е -> 0 в SQL(bit)
        A.CreationDate = myDialog.dateEdit_CreateDate.date().toString('yyyy-MM-dd')
        A.AirLineDescription = myDialog.textEdit_AirLineDescription.toPlainText()
        index = myDialog.comboBox_Alliance.currentIndex()
        A.Alliance = index + 1  # первичный ключ альянса
        print("old AlliancePK for update =" + str(A.Alliance))
        A.Alliance = S.QueryAlliancePKByName(myDialog.comboBox_Alliance.currentText())[0]
        print("AlliancePK for update =" + str(A.Alliance))
        # Вносим изменение
        ResultUpdate = S.UpdateAirLineByIATAandICAO(A.AirLine_ID,
                                                    A.AirLineName,
                                                    A.AirLineAlias,
                                                    A.AirLineCodeIATA,
                                                    A.AirLineCodeICAO,
                                                    A.AirLineCallSighn,
                                                    A.AirLineCity,
                                                    A.AirLineCountry,
                                                    A.AirLineStatus,
                                                    A.CreationDate,
                                                    A.AirLineDescription,
                                                    A.Alliance)
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
