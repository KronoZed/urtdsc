#!/usr/bin/python
# -*- coding: utf8 -*-

import os, sys
#from PyQt4 import Qt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from gui import MainWindow, AllScreensDialog, AboutWindow
import glob, time, config, lib

class urtdscMain(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)

        # Settings
        self.settings = QSettings('urtdsc', 'settings')
        self.restoreGeometry(self.settings.value('geometry').toByteArray())
        self.restoreState(self.settings.value('state').toByteArray())

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

        QMetaObject.connectSlotsByName(self)
        self.ui.demosList.itemClicked.connect(self.showDemoInfo)
        self.ui.copyDemoToDesktop.clicked.connect(self.copydemos)
        self.ui.viewAllScreenshots.clicked.connect(self.allScreenshotsDialog)
        self.ui.action_About_urtdsc.triggered.connect(self.aboutWindow)
        self.ui.actionAbout_Qt.triggered.connect(self.aboutQt)

    def showDemoInfo(self):
        maplist = []
        global demotime
        demotime = self.ui.demosList.currentItem().text()
        demoname = lib.demoname(demotime)
        nickname = lib.demonick(demoname)
        self.screens = lib.demoscreens(lib.demoname(demotime))
        try:
            screenaddr = self.screens[0]
            self.screenimg = QImage(screenaddr)
            screenshot = QPixmap().fromImage(self.screenimg).scaled(self.ui.screen.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            for scr in self.screens:
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

    def copydemos(self, event):
        lib.copyfile(os.path.expanduser("~/" + config.URT_FOLDER + "/q3ut4/demos/") + lib.demoname(demotime))

    def allScreenshotsDialog(self):
        als = allScreens(self)
        als.show()

    def aboutWindow(self):
        aboutw = QDialog()
        aboutw.ui = AboutWindow.Ui_Dialog()
        aboutw.ui.setupUi(aboutw)

        aboutw.ui.textBrowser.setBackgroundRole(QPalette.AlternateBase)

        aboutw.exec_()

    def aboutQt(self):
        QMessageBox.aboutQt(self)

    def resizeEvent(self, event):
        size = event.size()
        screenimg = QPixmap().fromImage(self.screenimg).scaled(self.ui.screen.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ui.screen.setPixmap(screenimg)

    def closeEvent(self, QCloseEvent):
        self.settings.setValue('state', self.saveState())
        self.settings.setValue('geometry', self.saveGeometry())

class allScreens(QDialog):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.ui = AllScreensDialog.Ui_Dialog()
        self.ui.setupUi(self)

        maplist = []

        self.ui.label.setText("")
        self.ui.screenshotsList.setIconSize(QSize(140, 140))

        try:
            self.scrlist = lib.demoscreens(lib.demoname(demotime))

            for screen in self.scrlist:
                screenimg = QImage(screen)
                screenshotForList = QIcon(QPixmap.fromImage(screenimg).scaled(QSize(140, 140), Qt.KeepAspectRatio, Qt.SmoothTransformation))
                itemForList = QListWidgetItem(screenshotForList, QString.fromUtf8(''), self.ui.screenshotsList)
                self.ui.screenshotsList.addItem(itemForList)
        except:
            self.ui.label.setText("<big><span style='color:red;font-weight:bold;'>You must select demo first!</span></big>")

        QMetaObject.connectSlotsByName(self)
        self.ui.screenshotsList.clicked.connect(self.showScreen)
        self.ui.copyToDesktop.clicked.connect(self.copyToDesktop)
        
    def showScreen(self):
        screenidx = self.ui.screenshotsList.currentRow()
        self.screenimg = QImage(self.scrlist[screenidx])
        screenshot = QPixmap().fromImage(self.screenimg).scaled(self.ui.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ui.label.setPixmap(screenshot)

    def resizeEvent(self, event):
        size = event.size()
        screenimg = QPixmap().fromImage(self.screenimg).scaled(self.ui.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ui.label.setPixmap(screenimg)

    def copyToDesktop(self, event):
        for screen in self.scrlist:
            lib.copyfile(screen)

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