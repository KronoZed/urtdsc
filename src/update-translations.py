#!/usr/bin/python
# -*- coding: utf8 -*-
import os
from PyQt4.QtCore import QLocale

def update_translations():
    # Get current locale name
    curlocale = str(QLocale.system().name().toUtf8())

    # Update translations of current locale or create new
    exitcode = os.system("pylupdate4 AboutWindow.py AllScreensDialog.py urtdsc.py -ts translations/urtdsc-" + curlocale + ".ts")

if __name__ == "__main__":
    update_translations()