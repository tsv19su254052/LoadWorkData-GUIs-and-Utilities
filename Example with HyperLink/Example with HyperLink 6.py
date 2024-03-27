from tabwidget import Ui_MainWindow
import sys
from PyQt4 import QtGui, QtCore


class MyApp(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        QtCore.QObject.connect(self.ui.pushButton, QtCore.SIGNAL('clicked()'), self._show)

    def _show(self):
        self.ui.tabWidget.setCurrentWidget(self.ui.tab_2)
        self.ui.textBrowser.setSource(QtCore.QUrl('text.html#anchor'))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mw = MyApp()
    mw.show()
    app.exec_()
