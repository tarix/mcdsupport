# -*- coding: utf-8 -*-
#
# Portions of this code are derived from the copyrighted works of:
#    Damien Elmes <anki@ichi2.net>
#    Adam Mesha <adam@mesha.org>
#   
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# This free project is hosted by GitHub: https://github.com/tarix/mcdsupport

from PyQt4 import QtGui,QtCore
from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import *
from anki import utils
from ankiqt import mw, ui
from anki.errors import FactInvalidError

import mcd, dlgAddMcd, dlgConfigure, mcdCloze, mcdOptions

SHORTCUTKEY = "F9" # seems this does not conflict at all with the builtin cloze shortcut

helpAddMcd = '''
<p><big><center><b>MCD Support for Anki v1.0.1</b></center></big></p>

<p><b>Generating MCD cards</b></p>

<p>First, paste the text that contains the information that you want to learn in the "Phrase / Passage" box.</p>

<p>Next put any notes, definitions, source or other useful information about the passage in the "Notes" box.</p>

<p>Finally add the words or characters that you want clozed and seperate each entry with a space.</p>

<p>If you want tags added to your cards be sure and add that in the tags field.</p>

<p>To generate the cards press the Add button.  When the cards are done being added a small status line will display the results.</p>

<p><b>Development</b></p>

<p>This project is hosted on GitHub at <a href="https://github.com/tarix/mcdsupport">https://github.com/tarix/mcdsupport</a></p>
'''

helpConfigure = '''
<p><big><center><b>MCD Support Configuration</b></center></big></p>

<p><b>Auto Clear</b></p>

<p>Passage Text: If this is checked the passage text will be automatically cleared after new MCD cards are added.</p>
<p>Notes Text: If this is checked the notes text will be automatically cleared after new MCD cards are added.</p>
<p>Clozes: If this is checked the clozes will be automatically cleared after new MCD cards are added.</p>

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
        self.tagslineedit.setDeck(mw.deck)
        self.configbutton.setIcon(QtGui.QIcon(':/icons/configure.png'))
        # add the MCD modes we support
        self.cmbMode.addItems( mcd.modeNames )
        # disable the model combo until we support changing it
        self.modelcombobox.setEnabled(False)
        # disable the mode combo until we support changing it
        #self.cmbMode.setEnabled(False)
		# connect the button signals to their functions
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('helpRequested()'), self.help)
        QtCore.QObject.connect(self.addButton, QtCore.SIGNAL('clicked()'), self.addMcd)
        QtCore.QObject.connect(self.configbutton, QtCore.SIGNAL('clicked()'), self.configure)
    def help(self):
        # show help text
        ui.utils.showText(helpAddMcd, None, type='html')	
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
        mode = mcd.modes[ self.cmbMode.currentIndex() ]
		# create cards
        status = mcdCloze.createCards(model, selectionText, clozesText, notesText, tagsText, mode)
        # update the results
        self.statusLabel.setText(status)
		# see if we should clear any of the text boxes
        if mcdOptions.autoClearPassage == True:
            self.selectionEdit.setPlainText('')
        if mcdOptions.autoClearNotes == True:
            self.notesEdit.setPlainText('')
        if mcdOptions.autoClearClozes == True:
            self.clozesEdit.setText("")
		# end busy cursor
        self.addButton.setEnabled(True)
        mw.app.restoreOverrideCursor()
    def configure(self):
        d = QtGui.QDialog(mw)
        form = Configure()
        form.setupUi(d)
        ret = d.exec_()
        if not ret:
            return

class Configure(dlgConfigure.Ui_Dialog):
    def setupUi(self, Dialog):
        dlgConfigure.Ui_Dialog.setupUi(self, Dialog)
		# set the AutoClear options
        self.chkAutoClearPassage.setChecked( mcdOptions.autoClearPassage )
        self.chkAutoClearNotes.setChecked( mcdOptions.autoClearNotes )
        self.chkAutoClearClozes.setChecked( mcdOptions.autoClearClozes )
        # setup the signals
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('accepted()'), self.okay)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('helpRequested()'), self.help)
    def okay(self):
        # begin busy cursor
        mw.app.setOverrideCursor(QCursor(Qt.WaitCursor))
        mw.app.processEvents()
        # set the options
        mcdOptions.autoClearPassage = self.chkAutoClearPassage.isChecked()
        mcdOptions.autoClearNotes = self.chkAutoClearNotes.isChecked()
        mcdOptions.autoClearClozes = self.chkAutoClearClozes.isChecked()
        # save the options
        mcdOptions.save()
        # end busy cursor
        mw.app.restoreOverrideCursor()
    def help(self):
        # show help text
        ui.utils.showText(helpConfigure, None, type='html')	

def createMenu():
	mw.mainWin.addMcd = QtGui.QAction('Add MCD Cards', mw)
	mw.mainWin.addMcd.setStatusTip('Add MCD Cards')
	mw.mainWin.addMcd.setEnabled(True)
	mw.mainWin.addMcd.setShortcut(SHORTCUTKEY)
	#mw.mainWin.addMcd.setIcon(QtGui.QIcon(ICONPATH))
	mw.connect(mw.mainWin.addMcd, QtCore.SIGNAL('triggered()'), menuAddMcd)
	mw.mainWin.menuTools.addAction(mw.mainWin.addMcd)

createMenu()