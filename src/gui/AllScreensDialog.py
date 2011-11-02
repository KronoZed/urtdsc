# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'allscreensdialog.ui'
#
# Created: Wed Nov  2 19:13:26 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(700, 536)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(70)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(700, 500))
        Dialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.screenshotsList = QtGui.QListWidget(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.screenshotsList.sizePolicy().hasHeightForWidth())
        self.screenshotsList.setSizePolicy(sizePolicy)
        self.screenshotsList.setMinimumSize(QtCore.QSize(150, 0))
        self.screenshotsList.setMaximumSize(QtCore.QSize(150, 16777215))
        self.screenshotsList.setObjectName(_fromUtf8("screenshotsList"))
        self.verticalLayout_3.addWidget(self.screenshotsList)
        self.copyToDesktop = QtGui.QPushButton(Dialog)
        self.copyToDesktop.setMinimumSize(QtCore.QSize(150, 0))
        self.copyToDesktop.setMaximumSize(QtCore.QSize(150, 16777215))
        self.copyToDesktop.setObjectName(_fromUtf8("copyToDesktop"))
        self.verticalLayout_3.addWidget(self.copyToDesktop)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.label = QtGui.QLabel(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "View all related screenshots - UrTDSC", None, QtGui.QApplication.UnicodeUTF8))
        self.copyToDesktop.setText(QtGui.QApplication.translate("Dialog", "Copy screenshots\n"
" to desktop", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))

