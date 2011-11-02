#!/usr/bin/python
# -*- coding: utf8 -*-

import os, sys
from PyQt4 import Qt
from gui import MainWindow

class urtdscMain(Qt.QMainWindow):
    def __init__(self, parent=None):
        Qt.QWidget.__init__(self, parent)
        self.ui = MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    urtdsc = urtdscMain()
    urtdsc.show()
    sys.exit(app.exec_())