#!/usr/bin/python
# -*- coding: utf8 -*-

import os, sys
#from PyQt4 import Qt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from gui import MainWindow
import glob, time, config, lib

class urtdscMain(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)

        if os.path.exists(os.path.expanduser('~/.q3a/q3ut4/demos')):
            pass
        else:
            nodemos = '1'

        try:
            path = os.path.expanduser('~/.q3a/q3ut4/demos')
            self.date_file_list = []
            for file in glob.glob(path + "/*.dm_68"):
                stats = os.stat(file)
                lastmod_date = time.localtime(stats[8])
                date_file_tuple = lastmod_date, file
                self.date_file_list.append(date_file_tuple)
                self.date_file_list.sort()
                self.date_file_list.reverse()
            for file in self.date_file_list:
                file_date = time.strftime('%d-%m-%Y @ %H:%M', file[0])
                self.ui.demosList.addItem(file_date)
                nodemos = '0'
        except:
            #self.nodemosfound()
            nodemos = '1'

        self.ui.label.setText("")
        self.ui.screen.setText("")

        self.ui.demosList.itemClicked.connect(self.showDemoInfo)
        QMetaObject.connectSlotsByName(self)

    def showDemoInfo(self):
        maplist = []
        demotime = self.ui.demosList.currentItem().text()
        demoname = lib.demoname(demotime)
        nickname = lib.demonick(demoname)
        screens = lib.demoscreens(lib.demoname(demotime))
        try:
            screenaddr = screens[0]
            self.screenimg = QImage(screenaddr)
            screenshot = QPixmap().fromImage(self.screenimg).scaled(self.ui.screen.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            for scr in screens:
                scrs = scr.split("_")
                if scrs[1] in ('TOHUNGA', 'ORBITAL'):
                    maplist.append(scrs[1] + "_" + scrs[2])
                else:
                    maplist.append(scrs[1])

            maps = ", ".join(maplist).lower()
        except:
            self.screenimg = QImage('gui/noscreenshot.png')
            screenshot = QPixmap().fromImage(self.screenimg).scaled(self.ui.screen.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            maps = "No maps"

        self.ui.label.setText("<b>Demoname:</b> " + demoname + "<br><b>Nickname:</b> " + nickname + "<br><b>Maps:</b> " + maps)
        self.ui.screen.setPixmap(screenshot)

    def resizeEvent(self, event):
        size = event.size()
        screenimg = QPixmap().fromImage(self.screenimg).scaled(self.ui.screen.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ui.screen.setPixmap(screenimg)

if __name__ == "__main__":

    try:
        if config.DEBUG:
            DEBUG = config.DEBUG
    except:
        DEBUG = '0'

    app = QApplication(sys.argv)
    urtdsc = urtdscMain()
    urtdsc.show()
    sys.exit(app.exec_())