import threading

from PyQt5 import QtCore, QtGui, QtWidgets

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(875, 648)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.searchforpoi = QtWidgets.QPushButton(self.centralwidget)
        self.searchforpoi.setGeometry(QtCore.QRect(730, 20, 111, 34))
        self.searchforpoi.setObjectName("searchforpoi")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 20, 691, 31))
        self.lineEdit.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.lineEdit.setObjectName("lineEdit")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(25, 71, 821, 551))
        self.textBrowser.setObjectName("textBrowser")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "POI Updation app"))
        self.searchforpoi.setText(_translate("MainWindow", "Search for POI"))


class DriverWorker(QtCore.QObject):
    urlsSignals = QtCore.pyqtSignal(list)

    def get_urls(self, text):
        threading.Thread(target=self._task, args=(text,), daemon=True).start()

    def _task(self, text):
        options = webdriver.ChromeOptions()
        options.headless = True
        browser = webdriver.Chrome()
        browser.implicitly_wait(30)
        browser.maximize_window()

        browser.get("http://www.duckduckgo.com")
        elem = browser.find_element_by_name("q")
        elem.clear()

        elem.send_keys(text)
        elem.submit()

        lists = browser.find_elements_by_class_name("result__url__domain")

        urls = []
        for a in browser.find_elements_by_xpath(".//a"):
            ab = a.get_attribute("href")
            urls.append(ab)
        self.urlsSignals.emit(urls)
        browser.quit()


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.searchforpoi.clicked.connect(self.input_value)
        self.worker = DriverWorker()
        self.worker.urlsSignals.connect(self.on_urls)
        self.textBrowser.anchorClicked.connect(QtGui.QDesktopServices.openUrl)
        self.textBrowser.setOpenLinks(False)

    @QtCore.pyqtSlot()
    def input_value(self):
        textboxValue = self.lineEdit.text()
        self.worker.get_urls(textboxValue)

    @QtCore.pyqtSlot(list)
    def on_urls(self, urls):
        self.textBrowser.clear()
        for url in urls:
            html = """<a href="{url}">{url}</a>""".format(url=url)
            self.textBrowser.append(html)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
