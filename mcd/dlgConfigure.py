# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mcd\dlgConfigure.ui'
#
# Created: Wed Jan 11 16:56:08 2012
#      by: PyQt4 UI code generator 4.8.5
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
        Dialog.resize(255, 204)
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Configure MCD Support", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Auto Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.chkAutoClearPassage = QtGui.QCheckBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkAutoClearPassage.sizePolicy().hasHeightForWidth())
        self.chkAutoClearPassage.setSizePolicy(sizePolicy)
        self.chkAutoClearPassage.setText(QtGui.QApplication.translate("Dialog", "Passage Text", None, QtGui.QApplication.UnicodeUTF8))
        self.chkAutoClearPassage.setObjectName(_fromUtf8("chkAutoClearPassage"))
        self.verticalLayout_2.addWidget(self.chkAutoClearPassage)
        self.chkAutoClearNotes = QtGui.QCheckBox(self.groupBox)
        self.chkAutoClearNotes.setText(QtGui.QApplication.translate("Dialog", "Notes Text", None, QtGui.QApplication.UnicodeUTF8))
        self.chkAutoClearNotes.setObjectName(_fromUtf8("chkAutoClearNotes"))
        self.verticalLayout_2.addWidget(self.chkAutoClearNotes)
        self.chkAutoClearClozes = QtGui.QCheckBox(self.groupBox)
        self.chkAutoClearClozes.setText(QtGui.QApplication.translate("Dialog", "Clozes", None, QtGui.QApplication.UnicodeUTF8))
        self.chkAutoClearClozes.setObjectName(_fromUtf8("chkAutoClearClozes"))
        self.verticalLayout_2.addWidget(self.chkAutoClearClozes)
        self.verticalLayout.addWidget(self.groupBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Help|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        pass

