#--------------------------------- < map.py > -----------------------------------
#!/usr/bin/env python
# Google Maps JavaScript API:
# https://developers.google.com/maps/documentation/javascript/tutorial


import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebKit import QWebSettings  # не ставится
from PyQt5.QtWebKitWidgets import QWebView  # не ставится


app = QtWidgets.QApplication(sys.argv)

web = QWebView()
web.settings().setAttribute(QWebSettings.JavascriptEnabled, True)
tempPath = "file:///" + os.path.join(os.getcwd(), "map.html").replace('\\','/')

web.load(QtCore.QUrl(tempPath))
web.show()

sys.exit(app.exec_())
