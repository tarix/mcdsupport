# -*- coding: utf-8 -*-
#
# This is free and unencumbered software released into the public domain.
#
# Portions of this code are derived from the copyrighted works of:
#    Damien Elmes <anki@ichi2.net>
#    Adam Mesha <adam@mesha.org>
#   
# All rights of the original authors are reserved pursuiant to the following license:
#    GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# This free project is hosted by GitHub: https://github.com/tarix/mcdsupport

from PyQt4 import QtGui,QtCore
from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import *
from anki import utils
from ankiqt import mw, ui
from anki.errors import FactInvalidError

import dlgAddMcd, mcdCloze

SHORTCUTKEY = "F9" # seems this does not conflict at all with the builtin cloze shortcut

helptext = '''
<p>MCD Support for Anki v0.1.3</p>

<p><big><b>Generating MCD cards</b></big></p>

<p>First, past the text that contains the information that you want to learn in the "Phrase / Passage" box.</p>

<p>Next put any notes, definitions, source or other useful information about the passage in the "Notes" box.</p>

<p>Finally add the words or characters that you want clozed and seperate each entry with a space.</p>

<p>If you want tags added to your cards be sure and add that in the tags field.</p>

<p>To generate the cards press the Add button.  When the cards are done being added a small status line will display the results.</p>
'''

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
        # disable the model combo until we have better support
        self.modelcombobox.setEnabled(False)
        self.tagslineedit.setDeck(mw.deck)
        self.configbutton.setIcon(QtGui.QIcon(':/icons/configure.png'))

        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("helpRequested()"), self.help)
        QtCore.QObject.connect(self.addButton, QtCore.SIGNAL('clicked()'), self.addMcd)
    def help(self):
        # show help text
        ui.utils.showText(helptext, None, type='html')	
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