import sys
# todo Вывести иерархию классов pyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextBrowser


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(True)
        #self.text_browser.setReadOnly(True)
        self.text_browser.append("<a href='https://google.com/'>Google</a>")
        self.text_browser.append("<a href='https://github.com/'>Github</a>")

        layout = QVBoxLayout()
        layout.addWidget(self.text_browser)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
