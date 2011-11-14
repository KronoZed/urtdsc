#!/usr/bin/python
# -*- coding: utf8 -*-

import os, sys
#from PyQt4 import Qt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import MainWindow, AllScreensDialog, AboutWindow
import glob, time, config, lib, commands

class urtdscMain(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)

        # Translations
        try:
            dirr = '/usr/share/urtdsc/'
            translator = QTranslator(app)
            translator.load("urtdsc-" + QLocale.system().name() + ".qm", dirr)
            app.installTranslator(translator)
            lib.log('1', "Loaded translation for: " + QLocale.system().name() + " from " + dirr)
        except:
            lib.log('1', "Cant load translations!")

        # Settings
        self.settings = QSettings('urtdsc', 'settings')
        self.restoreGeometry(self.settings.value('geometry').toByteArray())
        self.restoreState(self.settings.value('state').toByteArray())

        try:
            self.revision = "-" + commands.getoutput('git rev-parse --short HEAD')
        except:
            self.revision = ""

        if os.path.exists(os.path.expanduser('~/.q3a/q3ut4/demos')):
            pass
        else:
            nodemos = '1'

        self.fillDemosList(1)

        self.ui.label.setText("")

        # We need this for translations >.<
        self.ui.copyDemoToDesktop.setText(self.tr("Copy demo to desktop"))
        self.ui.viewAllScreenshots.setText(self.tr("View all screenshots"))
        self.ui.createArchive.setText(self.tr("Create archive..."))
        self.ui.menu_File.setTitle(self.tr("&File"))
        self.ui.action_Options.setText(self.tr("&Options"))
        self.ui.action_Exit.setText(self.tr("&Exit"))
        self.ui.menu_Demos.setTitle(self.tr("&Demos"))
        self.ui.action_Update_list.setText(self.tr("&Update list"))
        self.ui.menu_Help.setTitle(self.tr("&Help"))
        self.ui.action_About_urtdsc.setText(self.tr("About &UrTDSC..."))
        self.ui.actionAbout_Qt.setText(self.tr("About &Qt..."))

        QMetaObject.connectSlotsByName(self)
        self.ui.demosList.itemClicked.connect(self.showDemoInfo)
        self.ui.demosList.itemSelectionChanged.connect(self.showDemoInfo)
        self.ui.demosList.itemActivated.connect(self.showDemoInfo)
        self.ui.demosList.customContextMenuRequested.connect(self.demoContextMenu)
        self.ui.copyDemoToDesktop.clicked.connect(self.copydemos)
        self.ui.viewAllScreenshots.clicked.connect(self.allScreenshotsDialog)
        self.ui.action_Update_list.triggered.connect(self.fillDemosList)
        self.ui.action_About_urtdsc.triggered.connect(self.aboutWindow)
        self.ui.actionAbout_Qt.triggered.connect(self.aboutQt)
        self.ui.action_Exit.triggered.connect(self.close)

    def fillDemosList(self, type):
        self.ui.demosList.clear()
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
            if type == 1:
                self.ui.statusbar.showMessage(self.tr("Demo list loaded. Total: ") + str(self.ui.demosList.count()) + " " + self.tr("demos") + ".")
            else:
                self.ui.statusbar.showMessage(self.tr("Demo list reloaded. Total: ") + str(self.ui.demosList.count()) + " " + self.tr("demos") + ".")
        except:
            self.nodemosfound()
            nodemos = '1'

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
            self.screenimg = QImage('/usr/share/urtdsc/noscreenshot.png')
            screenshot = QPixmap().fromImage(self.screenimg).scaled(self.ui.screen.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            maps = "No maps"

        self.ui.label.setText("<b>" + self.tr("Demoname") + ":</b> " + demoname + "<br><b>" + self.tr("Nickname") + ":</b> " + nickname + "<br><b>" + self.tr("Maps") + ":</b> " + maps)
        self.ui.screen.setPixmap(screenshot)
        self.ui.statusbar.showMessage(self.tr("Demo ") + demoname + self.tr(" have ") + str(len(self.screens)) + self.tr(" screenshot(s)."))

    def copydemos(self):
        lib.copyfile(os.path.expanduser("~/" + config.URT_FOLDER + "/q3ut4/demos/") + lib.demoname(demotime))

    def copyallstuff(self):
        lib.copyfile(os.path.expanduser("~/" + config.URT_FOLDER + "/q3ut4/demos/") + lib.demoname(demotime))
        for screen in self.screens:
            lib.copyfile(screen)

    def removeallstuff(self):
        lib.removefile(os.path.expanduser("~/" + config.URT_FOLDER + "/q3ut4/demos/") + lib.demoname(demotime))
        for screen in self.screens:
            lib.removefile(screen)

        self.fillDemosList(2)

    def allScreenshotsDialog(self):
        als = allScreens(self)
        als.show()

    def nodemosfound(self):
        QMessageBox.critical(self, "UrTDSC - FAIL!", self.tr("No demos found."))

    def nosshotsfound(self):
        QMessageBox.critical(self, "UrTDSC - FAIL!", self.tr("No screenshots found."))

    def demoContextMenu(self, pos):
        demomenu = QMenu("Demos menu")
        demomenu.addAction(self.tr("Copy all stuff to desktop"), self.copyallstuff)
        demomenu.addSeparator()
        demomenu.addAction(self.tr("Remove demo and related stuff from disk"), self.removeallstuff)
        demomenu.exec_(self.ui.demosList.mapToGlobal(pos))

    def aboutWindow(self):
        aboutw = QDialog()
        aboutw.ui = AboutWindow.Ui_Dialog()
        aboutw.ui.setupUi(aboutw)
        aboutw.ui.label_2.setText('<p><span style=" font-size:11pt; font-weight:600;">Version 0.3-beta' + self.revision +'</span></p></body></html>')
        aboutw.exec_()

    def aboutQt(self):
        QMessageBox.aboutQt(self)

    def resizeEvent(self, event):
        size = event.size()
        try:
            screenimg = QPixmap().fromImage(self.screenimg).scaled(self.ui.screen.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.ui.screen.setPixmap(screenimg)
        except:
            self.ui.screen.setText("<big><b>" + self.tr("Select demo from the left list") + "</b></big>")

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
            pass

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
        try:
            screenimg = QPixmap().fromImage(self.screenimg).scaled(self.ui.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.ui.label.setPixmap(screenimg)
        except:
            if self.ui.screenshotsList.count() > 0:
                self.ui.label.setText("<big><b>" + self.tr("Select screenshot") + "</b></big>")
            else:
                self.ui.label.setText("<big><span style='color:red;font-weight:bold;'>" + self.tr("You must select demo first!") + "</span></big>")

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