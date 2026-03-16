# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Qt_Designer_DialogInputByIATAandICAOhjymSf.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(240, 245)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(130, 30, 31, 16))
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(130, 60, 31, 16))
        self.lineEdit_CodeIATA = QLineEdit(Dialog)
        self.lineEdit_CodeIATA.setObjectName(u"lineEdit_CodeIATA")
        self.lineEdit_CodeIATA.setGeometry(QRect(10, 30, 113, 20))
        self.lineEdit_CodeICAO = QLineEdit(Dialog)
        self.lineEdit_CodeICAO.setObjectName(u"lineEdit_CodeICAO")
        self.lineEdit_CodeICAO.setGeometry(QRect(10, 60, 113, 20))
        self.checkBox_Status_IATA = QCheckBox(Dialog)
        self.checkBox_Status_IATA.setObjectName(u"checkBox_Status_IATA")
        self.checkBox_Status_IATA.setGeometry(QRect(170, 30, 61, 18))
        self.pushButton_SearchInsert = QPushButton(Dialog)
        self.pushButton_SearchInsert.setObjectName(u"pushButton_SearchInsert")
        self.pushButton_SearchInsert.setGeometry(QRect(150, 90, 81, 23))
        self.checkBox_Status_ICAO = QCheckBox(Dialog)
        self.checkBox_Status_ICAO.setObjectName(u"checkBox_Status_ICAO")
        self.checkBox_Status_ICAO.setGeometry(QRect(170, 60, 61, 18))
        self.label_25 = QLabel(Dialog)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setGeometry(QRect(10, 90, 131, 141))
        self.label_25.setPixmap(QPixmap(u"Q:/SoftWare Application/GraphicalIDEs/GraphicalResources/Icons/edit.ico"))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"IATA", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"ICAO", None))
        self.checkBox_Status_IATA.setText(QCoreApplication.translate("Dialog", u"\u041f\u0443\u0441\u0442\u043e", None))
        self.pushButton_SearchInsert.setText(QCoreApplication.translate("Dialog", u"\u0412\u0441\u0442\u0430\u0432\u043a\u0430", None))
        self.checkBox_Status_ICAO.setText(QCoreApplication.translate("Dialog", u"\u041f\u0443\u0441\u0442\u043e", None))
        self.label_25.setText("")
    # retranslateUi

