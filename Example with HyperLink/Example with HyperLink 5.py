from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets


class WebEnginePage(QtWebEngineWidgets.QWebEnginePage):
    def createWindow(self, _type):
        page = WebEnginePage(self)
        page.urlChanged.connect(self.on_url_changed)
        return page

    @QtCore.pyqtSlot(QtCore.QUrl)
    def on_url_changed(self, url):
        page = self.sender()
        self.setUrl(url)
        page.deleteLater()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.browser = QtWebEngineWidgets.QWebEngineView()
        page = WebEnginePage(self.browser)
        self.browser.setPage(page)
        self.browser.load(QtCore.QUrl("https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_a_target"))
        self.setCentralWidget(self.browser)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.showMaximized()
    sys.exit(app.exec_())
