#  Interpreter 3.7


import pyodbc  # pymssql работает тяжелее, пробуем SQLAlchemy
import pandas
import itertools
import datetime
import time
import os
import json
import sys
import socket
import threading
from PyQt5 import QtWidgets  # QtCore, QtGui, QtNetwork, QtOpenGL, QtScript, QtSQL (медленнее чем pyodbc), QtDesigner - запускаем в командной строке, QtXml
import pathlib
#import stringcolor  # fixme в IDLE и в pyCharm раскраска не работает, в командной строке сразу слетает
import colorama
import termcolor
#import tqdm  # fixme tqdm нужен свой цикл -> сюда не подходит

# Импорт пользовательской библиотеки (файла *.py в этой же папке)
import Classes
# fixme Есть проблемка при импорте пользовательских библиотек из внешних файлов по другим путям из других папок ... -> Пишу пути по-разному.
#  Иногда не срабатывает. Пока не ясно, как писать правильнее
# todo  - Сделать пользовательскую наработку (не библиотеку и не пакет) отдельным репозиторием (как альтернативу виртуальному окружению) -> Использовал существующую, как пример
#       - Импортировать ее внутри репозитория для повторного применения синхронно (mutualy connected) или асинхронно (independent) -> Импортировал асинхронно,
#       обновление только вручную
#       - Посмотреть, чтобы у импортируемой наработки в репозитории на github-е появился значек "Used by ...", что она применяется -> Пока не наблюдается
#       - на github-е папка с подмодулем должна быть написана синим текстом -> Синяя ссылка, по которой никуда не перейдешь
#       - Результат импорта -> на github-е - ссылка, внутри pyCharm - локальный дубликат репозиториев в локальную ветку
# todo Научиться делать это по возможности только внутри pyCharm-а -> pyCharm пока не поддерживают 'git submodules' [@Aleks10](https://qna.habr.com/q/196071) и связанные с ним
#  команды
# todo Было бы удобно, если бы внутри pyCharm-а был функционал для работы с XML-ными файлами, как в MicroSoft XML Notepad


# Название локальной ветки и ее версии обработки с цветным выводом
__myOwnDevelopingVersion__ = 8.15
# todo Версия задается тут. Пакеты на GitHub-е *.tar.gz (под Linux или под BSD) не нужны. Выпуск релизов пока не имеет практической пользы, как указано в ReadME.md

colorama.init(autoreset=False)  # используем Colorama, чтобы сделать работу Termcolor на Windows, оставляем цветовое оформление до следующего явного указания
print(termcolor.colored("Обработка v" + str(__myOwnDevelopingVersion__) + " загрузки рабочих данных в БД SQL Server-а", 'blue', 'on_yellow'))
print("Разработал Тарасов Сергей tsv19su@yandex.ru")
#print("Разработал " + stringcolor.bold("Тарасов Сергей").cs("red", "gold") + " tsv19su@yandex.ru")
print(termcolor.colored("Пользователь = " + str(os.getlogin()), 'green', 'on_yellow'))

# fixme Вывести в файл requirements.txt список пакетов с версиями
# pip freeze > requirements.txt

# fixme Установить пакеты с определенными версиями
# pip install -r requirements.txt

# fixme Установить пакет из папки
# pip install SomePackage-1.0-py2.py3-none-any.whl

# Делаем экземпляр
S = Classes.Server()
# Добавляем еще аттрибуты
S.radioButtonUseDB = True
S.InputFileCSV = ' '
S.LogFileTXT = ' '
S.ErrorFileTXT = 'ErrorLog.txt'
S.SetInputDate = False


def Disconnect_AL():
    # Снимаем курсор
    S.seekAL.close()
    # Отключаемся от базы данных
    S.cnxnAL.close()


def Disconnect_AC():
    # Снимаем курсор
    S.seekAC.close()
    # Отключаемся от базы данных
    S.cnxnAC.close()


def Disconnect_RT():
    # Снимаем курсор
    S.seekRT.close()
    # Отключаемся от базы данных
    S.cnxnRT.close()


def Disconnect_FN():
    # Снимаем курсор
    S.seekFN.close()
    # Отключаемся от базы данных
    S.cnxnFN.close()


def LoadThread(Csv, Log):
    """
    Читаем входной файл и перепаковываем его в DataFrame (кодировка UTF-8, шапка таблицы на столбцы, разделитель - ,)
    Источник BTSgov (убал из файла все косые, запятые и кавычки)
    https://www.transtats.bts.gov/DL_SelectFields.asp - не работает
    https://www.transtats.bts.gov/DL_SelectFields.asp?gnoyr_VQ=FGJ&QO_fu146_anzr=b0-gvzr - работает
    """
    print("  Чтение, перепаковка и проверка входного файла")
    print("  ожидайте ...", end=' ')
    DataFrameFromCSV = pandas.read_csv(Csv, sep=",")
    # В исходном файле *.csv подписаны столбцы -> в DataFrame можно перемещаться по именам столбцов -> Разбираем на столбцы и работаем с ними
    ListAirLineCodeIATA = DataFrameFromCSV['OP_UNIQUE_CARRIER'].tolist()
    ListAirCraft = DataFrameFromCSV['TAIL_NUM'].tolist()
    ListAirPortDeparture = DataFrameFromCSV['ORIGIN'].tolist()
    ListAirPortArrival = DataFrameFromCSV['DEST'].tolist()
    ListFlightNumber = DataFrameFromCSV['OP_CARRIER_FL_NUM'].tolist()
    ListFlightDate = DataFrameFromCSV['FL_DATE'].tolist()
    print("готово")
    # Списки
    ListAirLinesAdded = []
    ListAirLinesFailed = []
    ListAirCraftsAdded = []
    ListAirCraftsUpdated = []
    ListAirCraftsFailed = []
    ListAirPortsNotFounded = []
    # Счетчики
    CountRoutesAdded = 0
    CountRoutesFailed = 0
    CountFlightsAdded = 0
    CountFlightsPadded = 0
    CountFlightsFailed = 0
    CountProgressBarFailed = 0
    # Распределение плотности перезапросов сервера
    DistributionDensityAirLines = []
    DistributionDensityAirCrafts = []
    DistributionDensityAirRoutes = []
    DistributionDensityAirFlights = []
    Density = 10  # раз в секунду
    MaxDelay = 750 * Density  # секунд
    for Index in range(MaxDelay):
        DistributionDensityAirLines.append(0)
        DistributionDensityAirCrafts.append(0)
        DistributionDensityAirRoutes.append(0)
        DistributionDensityAirFlights.append(0)
    # Дата и время сейчас
    Now = time.time()
    DateTime = time.ctime(Now)
    # Отметка времени начала загрузки
    __StartTime__ = datetime.datetime.now()
    print(termcolor.colored("Загрузка начата", "red", "on_yellow"))
    # Сигнал на обновление полоски выполнения
    # _signalUpdateProgressBar = QtCore.pyqtSignal(float)
    completion = 0  # Выполнение загрузки
    #pbar = tqdm.tqdm(len(ListAirLineCodeIATA))
    # Один внешний цикл и три вложенных цикла
    for AL, AC, Dep, Arr, FN, FD in zip(ListAirLineCodeIATA, ListAirCraft, ListAirPortDeparture, ListAirPortArrival, ListFlightNumber, ListFlightDate):
        print(colorama.Fore.BLUE + "Авикомпания", str(AL), end=" ")
        CurrentMax_i = 0  # Текущий максимум, секунд -> Обнуляем
        # Цикл попыток
        for i in range(MaxDelay):
            CurrentMax_i = i
            DBAirLine = S.QueryAirLineByIATA(AL)
            if DBAirLine is None:
                if S.InsertAirLineByIATAandICAO(AL, None):
                    ListAirLinesAdded.append(AL)
                    print(colorama.Fore.GREEN + "добавили ", end=" ")
                    break
                else:
                    print(colorama.Fore.LIGHTYELLOW_EX + "+", end=" ")
                    time.sleep(i / Density)  # пытаемся уйти от взаимоблокировки
            elif DBAirLine is not None:
                break
            else:
                print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                time.sleep(i / Density)  # пытаемся уйти от взаимоблокировки
        else:
            ListAirLinesFailed.append(AL)
        print(" ")
        DistributionDensityAirLines[CurrentMax_i] += 1
        print(colorama.Fore.BLUE + " Самолет", str(AC), end=" ")
        CurrentMax_i = 0  # Текущий максимум, секунд -> Обнуляем
        # Цикл попыток
        for i in range(MaxDelay):
            CurrentMax_i = i
            DBAirCraft = S.QueryAirCraftByRegistration(AC)
            if DBAirCraft is None:
                DBAirLine = S.QueryAirLineByIATA(AL)
                if DBAirLine is None:
                    # Вставляем самолет с пустым внешним ключем
                    if S.InsertAirCraftByRegistration(Registration=AC, ALPK=None):
                        ListAirCraftsAdded.append(AC)
                        print(colorama.Fore.GREEN + "добавили", end=" ")
                        break
                    else:
                        print(colorama.Fore.LIGHTYELLOW_EX + "+", end=" ")
                        time.sleep(i / Density)  # пытаемся уйти от взаимоблокировки
                elif DBAirLine is not None:
                    # Вставляем самолет (на предыдущем цикле вставили авиакомпанию)
                    if S.InsertAirCraftByRegistration(Registration=AC, ALPK=DBAirLine.AirLineUniqueNumber):
                        ListAirCraftsAdded.append(AC)
                        print(colorama.Fore.GREEN + "добавили", end=" ")
                        break
                    else:
                        print(colorama.Fore.LIGHTYELLOW_EX + "+", end=" ")
                        time.sleep(i / Density)  # пытаемся уйти от взаимоблокировки
                else:
                    print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                    time.sleep(i / Density)  # пытаемся уйти от взаимоблокировки
            elif DBAirCraft is not None:
                # todo Когда сделаю базу данных по самолетам, эту часть переделать
                DBAirLinePK = S.QueryAirLineByPK(DBAirCraft.AirCraftAirLine)
                if DBAirLinePK is None or DBAirLinePK.AirLineCodeIATA != AL:
                    # fixme пустая ячейка в таблице SQL-ной БД - NULL <-> в Python-е - (None,) -> в условиях None и (None,) - не False и не True
                    # fixme Просмотрел таблицу самолетов скриптом на SQL -> регистрация UNKNOWN не имеет внешнего ключа авиакомпании
                    # fixme Просмотрел таблицу самолетов скриптом на SQL -> регистрация nan каждый раз переписывается на другую компанию-оператора
                    DBAirLine = S.QueryAirLineByIATA(AL)
                    if DBAirLine is None:
                        break
                    elif DBAirLine is not None:
                        if S.UpdateAirCraft(Registration=AC, ALPK=DBAirLine.AirLineUniqueNumber):
                            ListAirCraftsUpdated.append(AC)
                            print(colorama.Fore.LIGHTCYAN_EX + "переписали на", str(AL), end=" ")
                            break
                        else:
                            print(colorama.Fore.LIGHTYELLOW_EX + "*", end=" ")
                            time.sleep(i / Density)  # пытаемся уйти от взаимоблокировки
                    else:
                        print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                        time.sleep(i / Density)  # пытаемся уйти от взаимоблокировки
                elif DBAirLinePK.AirLineCodeIATA == AL:
                    break
                else:
                    print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                    time.sleep(i / Density)  # пытаемся уйти от взаимоблокировки
            else:
                print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                time.sleep(i / Density)  # пытаемся уйти от взаимоблокировки
        else:
            ListAirCraftsFailed.append(AC)
        print(" ")
        DistributionDensityAirCrafts[CurrentMax_i] += 1
        print(colorama.Fore.BLUE + " Маршрут", str(Dep), "-", str(Arr), end=" ")
        CurrentMax_i = 0  # Текущий максимум, секунд -> Обнуляем
        # Цикл попыток
        for i in range(MaxDelay):
            CurrentMax_i = i
            DBAirPortDep = S.QueryAirPortByIATA(Dep)
            if DBAirPortDep is not None:
                DBAirPortArr = S.QueryAirPortByIATA(Arr)
                if DBAirPortArr is not None:
                    DBAirRoute = S.QueryAirRoute(Dep, Arr)
                    if DBAirRoute is None:
                        # Если есть оба аэропорта и нет маршрута
                        if S.InsertAirRoute(DBAirPortDep.AirPortUniqueNumber, DBAirPortArr.AirPortUniqueNumber):
                            CountRoutesAdded += 1
                            print(colorama.Fore.GREEN + "добавили", end=" ")
                            break
                        else:
                            print(colorama.Fore.LIGHTYELLOW_EX + "+", end=" ")
                            time.sleep(i / Density)  # пытаемся уйти от взаимоблокировки
                    elif DBAirRoute is not None:
                        break
                    else:
                        print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                        time.sleep(i / Density)  # пытаемся уйти от взаимоблокировки
                elif DBAirPortArr is None:
                    ListAirPortsNotFounded.append(Arr)
                    # Вставляем аэропорт только с кодом IATA
                    if S.InsertAirPortByIATA(Arr):
                        print(colorama.Fore.GREEN + "добавили аэропорт", str(Arr), end=" ")
                    else:
                        print(colorama.Fore.LIGHTYELLOW_EX + "+", end=" ")
                        time.sleep(i / Density)  # пытаемся уйти от взаимоблокировки
                else:
                    print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                    time.sleep(i / Density)  # пытаемся уйти от взаимоблокировки
            elif DBAirPortDep is None:
                ListAirPortsNotFounded.append(Dep)
                # Вставляем аэропорт только с кодом IATA
                if S.InsertAirPortByIATA(Dep):
                    print(colorama.Fore.GREEN + "добавили аэропорт", str(Dep), end=" ")
                else:
                    print(colorama.Fore.LIGHTYELLOW_EX + "+", end=" ")
                    time.sleep(i / Density)  # пытаемся уйти от взаимоблокировки
            else:
                print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                time.sleep(i / Density)  # пытаемся уйти от взаимоблокировки
        else:
            CountRoutesFailed += 1
        print(" ")
        DistributionDensityAirRoutes[CurrentMax_i] += 1
        print(colorama.Fore.BLUE + " Авиарейс", str(AL) + str(FN), end=" ")
        CurrentMax_i = 0  # Текущий максимум, секунд -> Обнуляем
        if not S.SetInputDate:
            FD = S.BeginDate
        # Цикл попыток
        for i in range(MaxDelay):
            CurrentMax_i = i
            DBAirLine = S.QueryAirLineByIATA(AL)
            if DBAirLine is not None:
                DBAirCraft = S.QueryAirCraftByRegistration(AC)
                if DBAirCraft is not None:
                    DBAirRoute = S.QueryAirRoute(Dep, Arr)
                    if DBAirRoute is not None:
                        # todo между транзакциями маршрут и самолет еще раз перезапросить внутри вызываемой функции - СДЕЛАЛ
                        ResultModify = S.ModifyAirFlight(AC, AL, FN, Dep, Arr, FD, S.BeginDate)
                        if ResultModify == 0:
                            print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                            time.sleep(i / Density)  # пытаемся уйти от взаимоблокировки
                        if ResultModify == 1:
                            CountFlightsAdded += 1
                            print(colorama.Fore.GREEN + "вставили", end=" ")
                            break
                        if ResultModify == 2:
                            CountFlightsPadded += 1
                            print(colorama.Fore.GREEN + "сплюсовали", end=" ")
                            break
                    elif DBAirRoute is None:
                        CountFlightsFailed += 1
                        break
                    else:
                        print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                        time.sleep(i / Density)
                elif DBAirCraft is None:
                    CountFlightsFailed += 1
                    break
                else:
                    print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                    time.sleep(i / Density)
            elif DBAirLine is None:
                CountFlightsFailed += 1
                break
            else:
                print(colorama.Fore.LIGHTYELLOW_EX + "?", end=" ")
                time.sleep(i / Density)  # пытаемся уйти от взаимоблокировки
        else:
            CountFlightsFailed += 1
        print(" ")
        DistributionDensityAirFlights[CurrentMax_i] += 1
        completion += 1
        Execute = round(100 * completion / len(ListFlightNumber), 2)  # вычисляем и округляем процент выполнения до 2 цифр после запятой
        # todo Сделать полосу выполнения все время внизу со всеми параметрами например с помощью tqdm - Не работает в цикле
        print(colorama.Fore.CYAN + "Выполнение =", str(Execute), "%")
        #pbar.update()
        #myDialog.progressBar_completion.setValue(int(Execute))  # fixme выдает ошибку про рекурсивную отрисовку (см. снимок экрана)
    #pbar.close()
    print(termcolor.colored("Загрузка окончена", "red", "on_yellow"))
    # Отметка времени окончания загрузки
    __EndTime__ = datetime.datetime.now()
    # Убираем с конца столбцы с нулями
    for Index in reversed(range(MaxDelay)):
        if DistributionDensityAirLines[Index] == 0 and DistributionDensityAirCrafts[Index] == 0 and DistributionDensityAirRoutes[Index] == 0 and DistributionDensityAirFlights[Index] == 0:
            DistributionDensityAirLines.pop(Index)
            DistributionDensityAirCrafts.pop(Index)
            DistributionDensityAirRoutes.pop(Index)
            DistributionDensityAirFlights.pop(Index)
        else:
            break
    # Собираем списки в DataFrame
    DataFrameDistributionDensity = pandas.DataFrame([DistributionDensityAirLines,
                                                     DistributionDensityAirCrafts,
                                                     DistributionDensityAirRoutes,
                                                     DistributionDensityAirFlights],
                                                    index=[" - авиакомпании", " - самолеты", " - маршруты", " - авиарейсы"])
    DataFrameDistributionDensity.index.name = "Базы данных:"
    OutputString = " \n \n"
    OutputString += "Загрузка рабочих данных (версия обработки - " + str(__myOwnDevelopingVersion__) + ") начата " + str(DateTime) + " \n"
    OutputString += " Загрузка проведена с " + str(socket.gethostname()) + " \n"
    OutputString += " Источник входных данных = " + str(S.filenameCSV) + " \n"
    OutputString += " Входные данные внесены за " + str(S.BeginDate) + " \n"
    if S.SetInputDate:
        OutputString += " Дата авиарейса проставлена из входного файла\n"
    else:
        OutputString += " Дата авиарейса проставлена как 1-ое число указанного месяца \n"
    OutputString += " Сервер СУБД = " + str(S.cnxnFN.getinfo(pyodbc.SQL_SERVER_NAME)) + " \n"
    OutputString += " Драйвер = " + str(S.cnxnFN.getinfo(pyodbc.SQL_DRIVER_NAME)) + " \n"
    OutputString += " Версия ODBC = " + str(S.cnxnFN.getinfo(pyodbc.SQL_ODBC_VER)) + " \n"
    OutputString += " DSN = " + str(S.cnxnFN.getinfo(pyodbc.SQL_DATA_SOURCE_NAME)) + " \n"
    OutputString += " Схема = " + str(S.cnxnFN.getinfo(pyodbc.SQL_USER_NAME)) + " \n"
    OutputString += " Длительность загрузки = " + str(__EndTime__ - __StartTime__) + " \n"
    OutputString += " Пользователь = " + str(os.getlogin()) + " \n"
    OutputString += " Итоги: \n"
    # Формируем итоги
    # todo Сделать итоги в виде XML и писать его полем XML.Document в базу данных
    if ListAirLinesAdded:
        OutputString += " - добавлены авиакомпании: \n  "
        OutputString += str(set(ListAirLinesAdded))  # fixme с регистрациями NaN надолго зависает, не убирает повторы и не группирует
        OutputString += " \n"
    if ListAirLinesFailed:
        OutputString += " - не добавлены данные по авиакомпаниям: \n  "
        OutputString += str(set(ListAirLinesFailed))
        OutputString += " \n"
    if ListAirCraftsAdded:
        OutputString += " - добавлены самолеты: \n  "
        OutputString += str(set(ListAirCraftsAdded))
        OutputString += " \n"
    if ListAirCraftsUpdated:
        OutputString += " - добавлены данные по самолетам: \n  "
        OutputString += str(set(ListAirCraftsUpdated))
        # Убираем только повторы, идущие подряд, но с сохранением исходного порядка fixme не работает
        OutPutNew = [el for el, _ in itertools.groupby(ListAirCraftsUpdated)]
        OutputString += " \n"
    if ListAirCraftsFailed:
        OutputString += " - не добавлены данные по самолетам: \n  "
        OutputString += str(set(ListAirCraftsFailed))
        OutputString += " \n"
    if CountRoutesAdded:
        OutputString += " - добавлено " + str(CountRoutesAdded) + " маршрутов \n"
    if CountRoutesFailed:
        OutputString += " - не добавлено " + str(CountRoutesFailed) + " маршрутов \n"
        OutputString += " \n"
    if ListAirPortsNotFounded:
        OutputString += " - не найдены аэропорты: \n  "
        OutputString += str(set(ListAirPortsNotFounded))
        OutputString += " \n"
    if CountFlightsAdded:
        OutputString += " - добавлено " + str(CountFlightsAdded) + " авиарейсов \n"
    if CountFlightsFailed:
        OutputString += " - не добавлено " + str(CountFlightsFailed) + " авиарейсов \n"
    if CountFlightsPadded:
        OutputString += " - сплюсовано " + str(CountFlightsPadded) + " авиарейсов \n"
    if CountProgressBarFailed:
        OutputString += " - отказов полосы выполнения =" + str(CountProgressBarFailed) + " \n"
    OutputString += " - перезапросы сервера: \n" + str(DataFrameDistributionDensity) + " \n"
    # Дописываем в журнал (обычным способом)
    # fixme Большая строка не дописывается, скрипт долго висит
    try:
        LogFile = open(Log, 'a')
        LogFile.write(OutputString)
        #LogFile.write('Вывод обычным способом\n')
    except IOError:
        try:
            LogError = open(S.ErrorFileTXT, 'a')
            LogError.write("Ошибка дозаписи результатов по " + str(S.filenameCSV) + " в " + str(S.filenameTXT) + " \n")
        except IOError:
            print("Ошибка дозаписи в файл журнала")
        finally:
            LogError.close()
        print(colorama.Fore.LIGHTYELLOW_EX + "Ошибка дозаписи в " + str(S.filenameTXT))
    finally:
        LogFile.close()
    # Дописываем в журнал (с помощью менеджера контекста)
    # with open(Log, 'a') as LogFile:
    #     LogFile.write(OutputString)
    #     LogFile.write('Вывод с помощью менеджера контекста\n')
    Disconnect_AL()
    Disconnect_AC()
    Disconnect_RT()
    Disconnect_FN()


# Основная функция
def myApplication():
    # Одно прикладное приложение
    myApp = QtWidgets.QApplication(sys.argv)
    # Делаем экземпляры
    myDialog = Classes.Ui_DialogLoadAirFlights()
    myDialog.setupUi(Dialog=myDialog)  # надо вызывать явно
    myDialog.setFixedSize(770, 380)
    myDialog.setWindowTitle('Загрузка рабочих данных')
    # Дополняем функционал экземпляра главного диалога
    # Переводим в исходное состояние
    myDialog.label_Version.setText("Версия обработки " + str(__myOwnDevelopingVersion__))
    myDialog.radioButton_DB.setChecked(True)
    myDialog.radioButton_DB.setToolTip("Использовать имя базы данных и драйвер СУБД")
    myDialog.radioButton_DSN.setChecked(False)
    myDialog.radioButton_DSN.setToolTip("Использовать системный или пользовательский DSN\n(настроено и проверено внутри)")
    myDialog.pushButton_Disconnect_AL.setEnabled(False)
    myDialog.pushButton_Disconnect_RT.setEnabled(False)
    myDialog.pushButton_Disconnect_FN.setEnabled(False)
    myDialog.dateEdit_BeginDate.setEnabled(False)
    myDialog.dateEdit_BeginDate.setToolTip("Дата начала периода загрузки рабочих данных")
    myDialog.checkBox_SetInputDate.setChecked(False)
    myDialog.checkBox_SetInputDate.setEnabled(False)
    myDialog.checkBox_SetInputDate.setToolTip("Перенос даты авиарейса из входных данных")
    myDialog.pushButton_ChooseCSVFile.setEnabled(False)
    myDialog.lineEdit_CSVFile.setEnabled(False)
    myDialog.pushButton_ChooseTXTFile.setEnabled(False)
    myDialog.lineEdit_TXTFile.setEnabled(False)
    myDialog.progressBar_completion.setEnabled(False)
    myDialog.progressBar_completion.setToolTip("Выполнение загрузки рабочих данных, проценты")
    myDialog.pushButton_GetStarted.setEnabled(False)
    myDialog.pushButton_GetStarted.setToolTip("Запуск загрузки входных данных по авиарейсам в базу данных на сервере \nВнимательно проверьте параметры загрузки")
    # параметры соединения с сервером
    myDialog.lineEdit_Server.setEnabled(False)
    myDialog.lineEdit_Driver_AL.setEnabled(False)
    myDialog.lineEdit_Driver_RT.setEnabled(False)
    myDialog.lineEdit_Driver_FN.setEnabled(False)
    myDialog.lineEdit_ODBCversion_AL.setEnabled(False)
    myDialog.lineEdit_ODBCversion_RT.setEnabled(False)
    myDialog.lineEdit_ODBCversion_FN.setEnabled(False)
    myDialog.lineEdit_DSN_FN.setEnabled(False)
    myDialog.lineEdit_Schema_AL.setEnabled(False)
    myDialog.lineEdit_Schema_RT.setEnabled(False)
    myDialog.lineEdit_Schema_FN.setEnabled(False)
    # Получаем список DSN-ов
    # Добавляем атрибут DSNs по ходу действия
    S.DSNs = pyodbc.dataSources()  # добавленные DSN-ы
    if S.DSNs:
        for DSN in S.DSNs:
            if not DSN:
                break
            myDialog.comboBox_DSN_FN.addItem(str(DSN))
    # Получаем список драйверов баз данных
    # Добавляем атрибут DriversODBC по ходу действия
    S.DriversODBC = pyodbc.drivers()
    if S.DriversODBC:
        for DriverODBC in S.DriversODBC:
            if not DriverODBC:
                break
            myDialog.comboBox_Driver_AL.addItem(str(DriverODBC))
            myDialog.comboBox_Driver_RT.addItem(str(DriverODBC))
            myDialog.comboBox_Driver_FN.addItem(str(DriverODBC))
    # Добавляем базы данных в выпадающие списки
    myDialog.comboBox_DB_AL.addItem("AirLinesDBNew62")
    myDialog.comboBox_DB_RT.addItem("AirPortsAndRoutesDBNew62")
    myDialog.comboBox_DB_FN.addItem("AirFlightsDBNew42")
    myDialog.comboBox_DB_FN.addItem("AirFlightsDBNew52")
    myDialog.comboBox_DB_FN.addItem("AirFlightsDBNew62")
    myDialog.comboBox_DB_FN.addItem("AirFlightsDBNew62Test")
    # Привязки обработчиков todo без lambda не работает
    myDialog.pushButton_Connect_AL.clicked.connect(lambda: PushButtonSelectDB_AL())  # Подключиться к базе данных
    myDialog.pushButton_Disconnect_AL.clicked.connect(lambda: PushButtonDisconnect_AL())  # Отключиться от базы данных
    myDialog.pushButton_Connect_RT.clicked.connect(lambda: PushButtonSelectDB_RT())
    myDialog.pushButton_Disconnect_RT.clicked.connect(lambda: PushButtonDisconnect_RT())
    # todo Объединить обе radioButton в одно, как на tkBuilder, и переделать на triggered
    myDialog.radioButton_DB.clicked.connect(lambda: RadioButtonDB())
    myDialog.radioButton_DSN.clicked.connect(lambda: RadioButtonDSN())
    #myDialog.radioButton_DB.toggled.connect(lambda: RadioButtons())
    #myDialog.radioButton_DSN.toggled.connect(lambda: RadioButtons())
    myDialog.pushButton_Connect_FN.clicked.connect(lambda: PushButtonSelectDB_FN())
    myDialog.pushButton_Disconnect_FN.clicked.connect(lambda: PushButtonDisconnect_FN())
    myDialog.pushButton_ChooseCSVFile.clicked.connect(lambda: PushButtonChooseCSVFile())  # Выбрать файл данных
    myDialog.pushButton_ChooseTXTFile.clicked.connect(lambda: PushButtonChooseLOGFile())  # Выбрать файл журнала
    myDialog.pushButton_GetStarted.clicked.connect(lambda: PushButtonGetStarted())  # Начать загрузку

    def PushButtonSelectDB_AL():
        if not S.Connected_AL:
            # Подключаемся к базе данных авиакомпаний
            # todo Схема по умолчанию - dbo, другая схема указывается в явном виде
            # https://docs.microsoft.com/ru-ru/previous-versions/dotnet/framework/data/adonet/sql/ownership-and-user-schema-separation-in-sql-server
            # Добавляем атрибуты DataBase, DriverODBC
            S.DataBase_AL = myDialog.comboBox_DB_AL.currentText()
            S.DriverODBC_AL = myDialog.comboBox_Driver_AL.currentText()
            try:
                # Добавляем атрибут cnxn
                # через драйвер СУБД + клиентский API-курсор
                S.cnxnAL = pyodbc.connect(driver=S.DriverODBC_AL, server=S.ServerName, database=S.DataBase_AL)
                print("  БД = ", S.DataBase_AL, "подключена")
                S.Connected_AL = True
                # Переводим в рабочее состояние (продолжение)
                myDialog.comboBox_DB_AL.setEnabled(False)
                myDialog.comboBox_Driver_AL.setEnabled(False)
                myDialog.pushButton_Disconnect_AL.setEnabled(True)
                if S.Connected_AC and S.Connected_RT and S.Connected_FN:
                    myDialog.pushButton_ChooseCSVFile.setEnabled(True)
                    myDialog.lineEdit_CSVFile.setEnabled(True)
                    myDialog.pushButton_ChooseTXTFile.setEnabled(True)
                    myDialog.lineEdit_TXTFile.setEnabled(True)
                    myDialog.dateEdit_BeginDate.setEnabled(True)
                    myDialog.dateEdit_BeginDate.setCalendarPopup(True)
                    myDialog.checkBox_SetInputDate.setEnabled(True)
                    myDialog.progressBar_completion.setEnabled(True)
                    myDialog.progressBar_completion.reset()
                    myDialog.pushButton_GetStarted.setEnabled(True)
                # Разрешаем транзакции и вызываем функцию commit() при необходимости в явном виде, в СУБД по умолчанию FALSE
                S.cnxnAL.autocommit = False
                print("autocommit is disabled")
                # Делаем свой экземпляр и ставим набор курсоров
                # КУРСОР нужен для перехода функционального языка формул на процедурный или для вставки процедурных кусков в функциональный скрипт.
                #
                # Способы реализации курсоров:
                #  - SQL, Transact-SQL,
                #  - серверные API-курсоры (OLE DB, ADO, ODBC),
                #  - клиентские API-курсоры (выборка кэшируется на клиенте)
                #
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
                print("seeks is on")
                # Драйвер
                myDialog.lineEdit_Driver_AL.setText(S.cnxnAL.getinfo(pyodbc.SQL_DRIVER_NAME))
                myDialog.lineEdit_Driver_AL.setEnabled(True)
                # версия ODBC
                myDialog.lineEdit_ODBCversion_AL.setText(S.cnxnAL.getinfo(pyodbc.SQL_ODBC_VER))
                myDialog.lineEdit_ODBCversion_AL.setEnabled(True)
                # Схема (если из-под другой учетки, то выводит имя учетки)
                myDialog.lineEdit_Schema_AL.setText(S.cnxnAL.getinfo(pyodbc.SQL_USER_NAME))
                myDialog.lineEdit_Schema_AL.setEnabled(True)
                # Переводим в рабочее состояние
                myDialog.pushButton_Connect_AL.setEnabled(False)
            except Exception:
                message = QtWidgets.QMessageBox()
                message.setText("Нет подключения к базе данных авиакомпаний")
                message.setIcon(QtWidgets.QMessageBox.Warning)
                message.exec_()
            else:
                pass
            finally:
                pass

    def PushButtonDisconnect_AL():
        # Обработчик кнопки 'Отключиться от базы данных'
        if S.Connected_AL:
            Disconnect_AL()
            S.Connected_AL = False
            # Переключаем в исходное состояние
            myDialog.comboBox_DB_AL.setEnabled(True)
            myDialog.comboBox_Driver_AL.setEnabled(True)
            myDialog.pushButton_Connect_AL.setEnabled(True)
            myDialog.pushButton_Disconnect_AL.setEnabled(False)
            myDialog.dateEdit_BeginDate.setEnabled(False)
            myDialog.checkBox_SetInputDate.setEnabled(False)
            myDialog.pushButton_ChooseCSVFile.setEnabled(False)
            myDialog.lineEdit_CSVFile.setEnabled(False)
            myDialog.pushButton_ChooseTXTFile.setEnabled(False)
            myDialog.lineEdit_TXTFile.setEnabled(False)
            myDialog.progressBar_completion.setEnabled(True)
            myDialog.progressBar_completion.reset()
            myDialog.pushButton_GetStarted.setEnabled(False)
            # параметры соединения с сервером
            myDialog.lineEdit_Server.setEnabled(False)
            myDialog.lineEdit_Driver_AL.setEnabled(False)
            myDialog.lineEdit_ODBCversion_AL.setEnabled(False)
            myDialog.lineEdit_Schema_AL.setEnabled(False)

    def PushButtonSelectDB_RT():
        if not S.Connected_RT:
            # Подключаемся к базе данных аэропортов и маршрутов
            # todo Схема по умолчанию - dbo, другая схема указывается в явном виде
            # Добавляем атрибуты DataBase, DriverODBC
            S.DataBase_RT = myDialog.comboBox_DB_RT.currentText()
            S.DriverODBC_RT = myDialog.comboBox_Driver_RT.currentText()
            try:
                # Добавляем атрибут cnxn
                # через драйвер СУБД + клиентский API-курсор
                S.cnxnRT = pyodbc.connect(driver=S.DriverODBC_RT, server=S.ServerName, database=S.DataBase_RT)
                print("  БД = ", S.DataBase_RT, "подключена")
                S.Connected_RT = True
                # Переводим в рабочее состояние (продолжение)
                myDialog.comboBox_DB_RT.setEnabled(False)
                myDialog.comboBox_Driver_RT.setEnabled(False)
                myDialog.pushButton_Disconnect_RT.setEnabled(True)
                if S.Connected_AL and S.Connected_AC and S.Connected_FN:
                    myDialog.pushButton_ChooseCSVFile.setEnabled(True)
                    myDialog.lineEdit_CSVFile.setEnabled(True)
                    myDialog.pushButton_ChooseTXTFile.setEnabled(True)
                    myDialog.lineEdit_TXTFile.setEnabled(True)
                    myDialog.dateEdit_BeginDate.setEnabled(True)
                    myDialog.dateEdit_BeginDate.setCalendarPopup(True)
                    myDialog.checkBox_SetInputDate.setEnabled(True)
                    myDialog.progressBar_completion.setEnabled(True)
                    myDialog.progressBar_completion.reset()
                    myDialog.pushButton_GetStarted.setEnabled(True)
                # Разрешаем транзакции и вызываем функцию commit() при необходимости в явном виде, в СУБД по умолчанию FALSE
                S.cnxnRT.autocommit = False
                print("autocommit is disabled")
                # Делаем свой экземпляр и ставим набор курсоров
                # КУРСОР нужен для перехода функционального языка формул на процедурный или для вставки процедурных кусков в функциональный скрипт.
                #
                # Способы реализации курсоров:
                #  - SQL, Transact-SQL,
                #  - серверные API-курсоры (OLE DB, ADO, ODBC),
                #  - клиентские API-курсоры (выборка кэшируется на клиенте)
                #
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
                S.seekRT = S.cnxnRT.cursor()
                print("seeks is on")
                # Драйвер
                myDialog.lineEdit_Driver_RT.setText(S.cnxnRT.getinfo(pyodbc.SQL_DRIVER_NAME))
                myDialog.lineEdit_Driver_RT.setEnabled(True)
                # версия ODBC
                myDialog.lineEdit_ODBCversion_RT.setText(S.cnxnRT.getinfo(pyodbc.SQL_ODBC_VER))
                myDialog.lineEdit_ODBCversion_RT.setEnabled(True)
                # Схема (если из-под другой учетки, то выводит имя учетки)
                myDialog.lineEdit_Schema_RT.setText(S.cnxnRT.getinfo(pyodbc.SQL_USER_NAME))
                myDialog.lineEdit_Schema_RT.setEnabled(True)
                # Переводим в рабочее состояние
                myDialog.pushButton_Connect_RT.setEnabled(False)
            except Exception:
                message = QtWidgets.QMessageBox()
                message.setText("Нет подключения к базе данных аэропортов и маршрутов")
                message.setIcon(QtWidgets.QMessageBox.Warning)
                message.exec_()
            else:
                pass
            finally:
                pass

    def PushButtonDisconnect_RT():
        # Обработчик кнопки 'Отключиться от базы данных'
        if S.Connected_RT:
            Disconnect_RT()
            S.Connected_RT = False
            # Переключаем в исходное состояние
            myDialog.comboBox_DB_RT.setEnabled(True)
            myDialog.comboBox_Driver_RT.setEnabled(True)
            myDialog.pushButton_Connect_RT.setEnabled(True)
            myDialog.pushButton_Disconnect_RT.setEnabled(False)
            myDialog.dateEdit_BeginDate.setEnabled(False)
            myDialog.checkBox_SetInputDate.setEnabled(False)
            myDialog.pushButton_ChooseCSVFile.setEnabled(False)
            myDialog.lineEdit_CSVFile.setEnabled(False)
            myDialog.pushButton_ChooseTXTFile.setEnabled(False)
            myDialog.lineEdit_TXTFile.setEnabled(False)
            myDialog.progressBar_completion.setEnabled(False)
            myDialog.pushButton_GetStarted.setEnabled(False)
            # параметры соединения с сервером
            myDialog.lineEdit_Server.setEnabled(False)
            myDialog.lineEdit_Driver_RT.setEnabled(False)
            myDialog.lineEdit_ODBCversion_RT.setEnabled(False)
            myDialog.lineEdit_Schema_RT.setEnabled(False)

    def RadioButtonDB():
        if not S.Connected_FN:
            myDialog.comboBox_DB_FN.setEnabled(True)
            myDialog.comboBox_Driver_FN.setEnabled(True)
            myDialog.comboBox_DSN_FN.setEnabled(False)
            S.radioButtonUseDB = True
            print("подключаемся без DSN")

    def RadioButtonDSN():
        if not S.Connected_FN:
            myDialog.comboBox_DB_FN.setEnabled(False)
            myDialog.comboBox_Driver_FN.setEnabled(False)
            myDialog.comboBox_DSN_FN.setEnabled(True)
            S.radioButtonUseDB = False
            print("подключаемся через DSN")

    def RadioButtons():
        print("Щелкнули переключатель")  # при привязке через toggled выводит эту надпись по два раза

    def PushButtonSelectDB_FN():
        if not S.Connected_AC:
            # Подключаемся к базе данных самолетов - пока так же, как и авиарейсы
            # todo Схема по умолчанию - dbo, другая схема указывается в явном виде
            ChoiceDB_AC = myDialog.comboBox_DB_FN.currentText()
            ChoiceDriver_AC = myDialog.comboBox_Driver_FN.currentText()
            # Добавляем атрибуты DataBase, DriverODBC
            S.DataBase_AC = str(ChoiceDB_AC)
            S.DriverODBC_AC = str(ChoiceDriver_AC)
            ChoiceDSN_AC = myDialog.comboBox_DSN_FN.currentText()
            # Добавляем атрибут myDSN
            S.myDSN_AC = ChoiceDSN_AC
            try:
                # Добавляем атрибут cnxn
                if S.radioButtonUseDB:
                    # через драйвер СУБД + клиентский API-курсор
                    S.cnxnAC = pyodbc.connect(driver=S.DriverODBC_AC, server=S.ServerName, database=S.DataBase_AC)
                    print("  БД = ", S.DataBase_AC, "подключена")
                else:
                    # через DSN + клиентский API-курсор (все настроено и протестировано в DSN)
                    S.cnxnAC = pyodbc.connect("DSN=" + S.myDSN_AC)
                    print("  DSN = ", S.myDSN_AC, "подключен")
                S.Connected_AC = True
                # Переводим в рабочее состояние (продолжение)
                # Разрешаем транзакции и вызываем функцию commit() при необходимости в явном виде, в СУБД по умолчанию FALSE
                S.cnxnAC.autocommit = False
                print("autocommit is disabled")
                # Делаем свой экземпляр и ставим набор курсоров
                # КУРСОР нужен для перехода функционального языка формул на процедурный или для вставки процедурных кусков в функциональный скрипт.
                #
                # Способы реализации курсоров:
                #  - SQL, Transact-SQL,
                #  - серверные API-курсоры (OLE DB, ADO, ODBC),
                #  - клиентские API-курсоры (выборка кэшируется на клиенте)
                #
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
                S.seekAC = S.cnxnAC.cursor()
                print("seeks is on")
            except Exception:
                message = QtWidgets.QMessageBox()
                message.setText("Нет подключения к базе данных самолетов")
                message.setIcon(QtWidgets.QMessageBox.Warning)
                message.exec_()
            else:
                pass
            finally:
                pass
        if not S.Connected_FN:
            # Подключаемся к базе данных авиарейсов
            # todo Схема по умолчанию - dbo, другая схема указывается в явном виде
            ChoiceDB_FN = myDialog.comboBox_DB_FN.currentText()
            ChoiceDriver_FN = myDialog.comboBox_Driver_FN.currentText()
            # Добавляем атрибуты DataBase, DriverODBC
            S.DataBase_FN = str(ChoiceDB_FN)
            S.DriverODBC_FN = str(ChoiceDriver_FN)
            ChoiceDSN_FN = myDialog.comboBox_DSN_FN.currentText()
            # Добавляем атрибут myDSN
            S.myDSN_FN = ChoiceDSN_FN
            try:
                # Добавляем атрибут cnxn
                if S.radioButtonUseDB:
                    # через драйвер СУБД + клиентский API-курсор
                    S.cnxnFN = pyodbc.connect(driver=S.DriverODBC_FN, server=S.ServerName, database=S.DataBase_FN)
                    print("  БД = ", S.DataBase_FN, "подключена")
                else:
                    # через DSN + клиентский API-курсор (все настроено и протестировано в DSN)
                    S.cnxnFN = pyodbc.connect("DSN=" + S.myDSN_FN)
                    print("  DSN = ", S.myDSN_FN, "подключен")
                S.Connected_FN = True
                # Переводим в рабочее состояние (продолжение)
                myDialog.radioButton_DB.setEnabled(False)
                myDialog.radioButton_DSN.setEnabled(False)
                myDialog.comboBox_DB_FN.setEnabled(False)
                myDialog.comboBox_Driver_FN.setEnabled(False)
                myDialog.comboBox_DSN_FN.setEnabled(False)
                myDialog.pushButton_Disconnect_FN.setEnabled(True)
                if S.Connected_AL and S.Connected_AC and S.Connected_RT:
                    myDialog.pushButton_ChooseCSVFile.setEnabled(True)
                    myDialog.lineEdit_CSVFile.setEnabled(True)
                    myDialog.pushButton_ChooseTXTFile.setEnabled(True)
                    myDialog.lineEdit_TXTFile.setEnabled(True)
                    myDialog.dateEdit_BeginDate.setEnabled(True)
                    myDialog.dateEdit_BeginDate.setCalendarPopup(True)
                    myDialog.checkBox_SetInputDate.setEnabled(True)
                    myDialog.progressBar_completion.setEnabled(True)
                    myDialog.progressBar_completion.reset()
                    myDialog.pushButton_GetStarted.setEnabled(True)
                # Разрешаем транзакции и вызываем функцию commit() при необходимости в явном виде, в СУБД по умолчанию FALSE
                S.cnxnFN.autocommit = False
                print("autocommit is disabled")
                # Делаем свой экземпляр и ставим набор курсоров
                # КУРСОР нужен для перехода функционального языка формул на процедурный или для вставки процедурных кусков в функциональный скрипт.
                #
                # Способы реализации курсоров:
                #  - SQL, Transact-SQL,
                #  - серверные API-курсоры (OLE DB, ADO, ODBC),
                #  - клиентские API-курсоры (выборка кэшируется на клиенте)
                #
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
                S.seekFN = S.cnxnFN.cursor()
                print("seeks is on")
                # SQL Server
                myDialog.lineEdit_Server.setText(S.cnxnFN.getinfo(pyodbc.SQL_SERVER_NAME))
                myDialog.lineEdit_Server.setEnabled(True)
                # Драйвер
                myDialog.lineEdit_Driver_FN.setText(S.cnxnFN.getinfo(pyodbc.SQL_DRIVER_NAME))
                myDialog.lineEdit_Driver_FN.setEnabled(True)
                # версия ODBC
                myDialog.lineEdit_ODBCversion_FN.setText(S.cnxnFN.getinfo(pyodbc.SQL_ODBC_VER))
                myDialog.lineEdit_ODBCversion_FN.setEnabled(True)
                # Источник данных
                myDialog.lineEdit_DSN_FN.setText(S.cnxnFN.getinfo(pyodbc.SQL_DATA_SOURCE_NAME))
                myDialog.lineEdit_DSN_FN.setEnabled(True)
                # Схема (если из-под другой учетки, то выводит имя учетки)
                myDialog.lineEdit_Schema_FN.setText(S.cnxnFN.getinfo(pyodbc.SQL_USER_NAME))
                myDialog.lineEdit_Schema_FN.setEnabled(True)
                # Переводим в рабочее состояние
                myDialog.pushButton_Connect_FN.setEnabled(False)
            except Exception:
                message = QtWidgets.QMessageBox()
                message.setText("Нет подключения к базе данных авиарейсов")
                message.setIcon(QtWidgets.QMessageBox.Warning)
                message.exec_()
            else:
                pass
            finally:
                pass

    def PushButtonDisconnect_FN():
        # Обработчик кнопки 'Отключиться от базы данных'
        if S.Connected_AC:
            Disconnect_AC()
            S.Connected_AC = False
        if S.Connected_FN:
            Disconnect_FN()
            S.Connected_FN = False
            # Переключаем в исходное состояние
            myDialog.radioButton_DB.setEnabled(True)
            myDialog.radioButton_DSN.setEnabled(True)
            myDialog.comboBox_DB_FN.setEnabled(True)
            myDialog.comboBox_Driver_FN.setEnabled(True)
            myDialog.comboBox_DSN_FN.setEnabled(True)
            myDialog.pushButton_Connect_FN.setEnabled(True)
            myDialog.pushButton_Disconnect_FN.setEnabled(False)
            myDialog.dateEdit_BeginDate.setEnabled(False)
            myDialog.checkBox_SetInputDate.setEnabled(False)
            myDialog.pushButton_ChooseCSVFile.setEnabled(False)
            myDialog.lineEdit_CSVFile.setEnabled(False)
            myDialog.pushButton_ChooseTXTFile.setEnabled(False)
            myDialog.lineEdit_TXTFile.setEnabled(False)
            myDialog.progressBar_completion.setEnabled(False)
            myDialog.pushButton_GetStarted.setEnabled(False)
            # параметры соединения с сервером
            myDialog.lineEdit_Server.setEnabled(False)
            myDialog.lineEdit_Driver_FN.setEnabled(False)
            myDialog.lineEdit_ODBCversion_FN.setEnabled(False)
            myDialog.lineEdit_DSN_FN.setEnabled(False)
            myDialog.lineEdit_Schema_FN.setEnabled(False)

    def PushButtonChooseCSVFile():
        filter = "Data files (*.csv)"
        S.InputFileCSV = QtWidgets.QFileDialog.getOpenFileName(None, "Открыть рабочие данные", ' ', filter=filter)[0]
        S.urnCSV = S.InputFileCSV.rstrip(os.sep)  # не сработало
        S.filenameCSV = pathlib.Path(S.InputFileCSV).name  # сработало
        myDialog.lineEdit_CSVFile.setText(S.filenameCSV)

    def PushButtonChooseLOGFile():
        filter = "Log Files (*.txt *.text)"
        S.LogFileTXT = QtWidgets.QFileDialog.getOpenFileName(None, "Открыть журнал", ' ', filter=filter)[0]
        S.filenameTXT = pathlib.Path(S.LogFileTXT).name
        myDialog.lineEdit_TXTFile.setText(S.filenameTXT)

    def PushButtonGetStarted():
        S.BeginDate = myDialog.dateEdit_BeginDate.date().toString('yyyy-MM-dd')
        if myDialog.checkBox_SetInputDate.isChecked():
            S.SetInputDate = True
        else:
            S.SetInputDate = False
        myDialog.pushButton_ChooseCSVFile.setEnabled(False)
        myDialog.pushButton_ChooseTXTFile.setEnabled(False)
        myDialog.dateEdit_BeginDate.setEnabled(False)
        myDialog.checkBox_SetInputDate.setEnabled(False)
        myDialog.pushButton_GetStarted.setEnabled(False)
        # fixme Поток работает со своим файлом данных и журналом - СДЕЛАЛ
        threadLoad = threading.Thread(target=LoadThread, daemon=False, args=(S.InputFileCSV, S.LogFileTXT,))  # поток не сам по себе
        threadLoad.start()
        threadLoad.join(2)  # ждем поток в основном потоке (графическая оболочка зависает) 2 секунды
        myDialog.close()  # закрываем графическую оболочку, текстовая остается
    # Отрисовка диалога
    myDialog.show()
    # Правильное закрытие диалога
    sys.exit(myApp.exec_())


# Точка входа
# __name__ — это специальная переменная, которая будет равна __main__, только если файл запускается как основная программа, в остальных случаях - имени модуля при импорте в качестве модуля
if __name__ == "__main__":
    myApplication()
