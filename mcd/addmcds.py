# -*- coding: utf-8 -*-
#
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
#
# This project is hosted on GitHub: https://github.com/tarix/mcdsupport

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import QDialog

from aqt import mw

import dlgAddMcds

class AddMcds(QDialog):

    def __init__(self, mw):
        print "AddMcds::__init___"
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.form = dlgAddMcds.Ui_Dialog()
        self.form.setupUi(self)
        #self.setupChooser()
        #self.setupEditor()
        #self.setupButtons()
        #self.onReset()
        #self.history = []
        #self.forceClose = False
        #restoreGeom(self, "addMcd")
        #addHook('reset', self.onReset)
        #addHook('currentModelChanged', self.onReset)
        self.mw.requireReset(modal=True)
        self.show()
        #self.setupNewNote()

#class AddDialog(dlgAddMcd.Ui_Dialog):
#    def setupUi(self, Dialog, models, modelidx=None, tags=''):
#        dlgAddMcd.Ui_Dialog.setupUi(self, Dialog)
#        self.modelcombobox.addItems(models)
#        if modelidx is not None:
#            self.modelcombobox.setCurrentIndex(modelidx)
#        self.tagslineedit.setDeck(mw.deck)
#        self.configbutton.setIcon(QtGui.QIcon(':/icons/configure.png'))
#        # add the MCD modes we support
#        modes = ["Manual (Space)", "Manual (Semicolon)"]
#        self.cmbMode.addItems(modes)
#        # disable the model combo until we support changing it
#        self.modelcombobox.setEnabled(False)
#        # disable the mode combo until we support changing it
#        #self.cmbMode.setEnabled(False)
#		# connect the button signals to their functions
#        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('helpRequested()'), self.help)
#        QtCore.QObject.connect(self.addButton, QtCore.SIGNAL('clicked()'), self.addMcd)
#        QtCore.QObject.connect(self.configbutton, QtCore.SIGNAL('clicked()'), self.configure)
#    def help(self):
#        # show help text
#        ui.utils.showText(helpAddMcd, None, type='html')	
#    def addMcd(self):
#        # begin busy cursor
#        mw.app.setOverrideCursor(QCursor(Qt.WaitCursor))
#        self.addButton.setEnabled(False)
#        mw.app.processEvents()
#        # get all user input
#        model = mw.deck.models[self.modelcombobox.currentIndex()]
#        selectionText = self.selectionEdit.toPlainText()
#        notesText = self.notesEdit.toPlainText()
#        clozesText =  self.clozesEdit.text()
#        tagsText = self.tagslineedit.text()
#        mode = self.cmbMode.currentIndex()
#		# create cards
#        status = mcdCloze.createCards(model, selectionText, clozesText, notesText, tagsText, mode)
#        # update the results
#        self.statusLabel.setText(status)
#		# see if we should clear any of the text boxes
#       if mcdOptions.autoClearPassage == True:
#            self.selectionEdit.setPlainText('')
#        if mcdOptions.autoClearNotes == True:
#            self.notesEdit.setPlainText('')
#        if mcdOptions.autoClearClozes == True:
#            self.clozesEdit.setText("")
#		# end busy cursor
#        self.addButton.setEnabled(True)
#        mw.app.restoreOverrideCursor()
#    def configure(self):
#        d = QtGui.QDialog(mw)
#        form = Configure()
#        form.setupUi(d)
#        ret = d.exec_()
#        if not ret:
#            return

#def menuAddMcd():
    #if mw.deck is None:
    #    ui.utils.showInfo('No deck open.')
    #    return
    #models = [m.name for m in mw.deck.models]
	# TODO: make this search more generic
    #try:
    #    modelidx = models.index('Japanese MCD')
    #except ValueError:
    #    modelidx = None
    #if modelidx == None:
    #    ui.utils.showInfo('The current deck does not have the Japanese MCD model.')
    #    return
    #tags = ''
#    d = QtGui.QDialog(mw)
#    form = AddDialog()
#    form.setupUi(d, models, modelidx, tags)
#    ret = d.exec_()
#    if not ret:
#        return
