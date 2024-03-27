#--------------------------------- < gui.py > -----------------------------------
#!/usr/bin/env python


import sys, time, subprocess, os
from PyQt5 import QtGui, QtCore, QtWidgets


class Cmd:
    def sensor_start(self):
        print('Sensor Start button click')
        subprocess.Popen("exec " + "python remotedata.py", shell=True)

    def sensor_end(self):
        print('Sensor End button click')
        subprocess.Popen("pkill -f remotedata.py", shell=True)

    def mission_start(self):
        print('Mission Start button click')
        subprocess.Popen("rosrun mavros mavsafety arm", shell=True)
        time.sleep(1)
        subprocess.Popen("rosrun mavros mavsys mode -c OFFBOARD", shell=True)

    def mission_end(self):
        print('Mission End button click')
        subprocess.Popen("rosrun mavros mavsys mode -c AUTO.RTL", shell=True)

    def mission_hold(self):
        print('Mission Hold button click')
        subprocess.Popen("rosrun mavros mavsys mode -c AUTO.LOITER", shell=True)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setMinimumSize(QtCore.QSize(1280, 800))
        self.setWindowTitle("Ocean Exploration UAV")
        self.statusBar().showMessage('Copyright 2020 www.uaslaboratory.com. All rights reserved.')

        # SENSOR
        self.nameLabel0 = QtWidgets.QLabel(self)
        self.nameLabel0.setText('Sensor:')
        self.nameLabel0.move(20, 20)

        # MISSION
        self.nameLabel1 = QtWidgets.QLabel(self)
        self.nameLabel1.setText('Mission:')
        self.nameLabel1.move(20, 50)

        # SENSOR: Start Data Logging
        self.button = QtWidgets.QPushButton('Start', self)
        self.button.setToolTip('Start data logging')
        self.button.move(90, 20)
        self.button.clicked.connect(lambda: Cmd.sensor_start)

        # SENSOR: Start Data Logging
        self.button = QtWidgets.QPushButton('End', self)
        self.button.setToolTip('End data logging')
        self.button.move(190, 20)
        self.button.clicked.connect(lambda: Cmd.sensor_end)

        # MISSION: Start Mission
        self.button = QtWidgets.QPushButton('Start', self)
        self.button.setToolTip('Start UAV mission')
        self.button.move(90, 50)
        self.button.clicked.connect(lambda: Cmd.mission_start)

        # MISSION: End Mission
        self.button = QtWidgets.QPushButton('End', self)
        self.button.setToolTip('End UAV mission')
        self.button.move(190, 50)
        self.button.clicked.connect(lambda: Cmd.mission_end)

        # MISSION: Hold Mission
        self.button = QtWidgets.QPushButton('Hold', self)
        self.button.setToolTip('Hold UAV mission')
        self.button.move(290, 50)
        self.button.clicked.connect(lambda: Cmd.mission_hold)

        self.show()


if __name__ == "__main__":
    #cmd = Cmd()
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
    #time.sleep(5)
