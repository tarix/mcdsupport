# -*- coding: utf-8 -*-
# Copyright: 
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# MCD plugin

from PyQt4 import QtGui,QtCore
from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import *
from anki import utils
from ankiqt import mw, ui
from anki.errors import FactInvalidError

import dlgAddMcd, mcdCloze

SHORTCUTKEY = "F9" # seems this does not conflict at all with the builtin cloze shortcut

def menuAddMcd():
    if mw.deck is None:
        ui.utils.showInfo('No deck open.')
        return
    models = [m.name for m in mw.deck.models]
	# TODO: make this search more generic
    try:
        modelidx = models.index('Japanese MCD')
    except ValueError:
        modelidx = None
    if modelidx == None:
        ui.utils.showInfo('The current deck does not have the Japanese MCD model.')
        return
    tags = ''
    d = QtGui.QDialog(mw)
    form = AddDialog()
    form.setupUi(d, models, modelidx, tags)
    ret = d.exec_()
    if not ret:
        return

class AddDialog(dlgAddMcd.Ui_Dialog):
    def setupUi(self, Dialog, models, modelidx=None, tags=''):
        dlgAddMcd.Ui_Dialog.setupUi(self, Dialog)
        self.modelcombobox.addItems(models)
        if modelidx is not None:
            self.modelcombobox.setCurrentIndex(modelidx)
#        self.tagslineedit.setDeck(mw.deck)
#        self.tagslineedit.setText(tags)
#        self.configbutton.setIcon(QtGui.QIcon(':/icons/configure.png'))
#
#        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("helpRequested()"), gethelp)
        QtCore.QObject.connect(self.addButton, QtCore.SIGNAL('clicked()'), self.addMcd)
    def addMcd(self):
        # begin busy cursor
        mw.app.setOverrideCursor(QCursor(Qt.WaitCursor))
        self.addButton.setEnabled(False)
        mw.app.processEvents()
        # get all user input
        model = mw.deck.models[self.modelcombobox.currentIndex()]
        selectionText = self.selectionEdit.toPlainText()
        notesText = self.notesEdit.toPlainText()
        clozesText =  self.clozesEdit.text()
        tagsText = self.tagslineedit.text()
		# create cards
        status = mcdCloze.createCards(model, selectionText, clozesText, notesText, tagsText)
        # update the results
        self.statusLabel.setText(status)
		# end busy cursor
        self.addButton.setEnabled(True)
        mw.app.restoreOverrideCursor()

def createMenu():
	mw.mainWin.addMcd = QtGui.QAction('Add MCD Cards', mw)
	mw.mainWin.addMcd.setStatusTip('Add MCD Cards')
	mw.mainWin.addMcd.setEnabled(True)
	mw.mainWin.addMcd.setShortcut(SHORTCUTKEY)
	#mw.mainWin.addMcd.setIcon(QtGui.QIcon(ICONPATH))
	mw.connect(mw.mainWin.addMcd, QtCore.SIGNAL('triggered()'), menuAddMcd)
	mw.mainWin.menuTools.addAction(mw.mainWin.addMcd)

createMenu()