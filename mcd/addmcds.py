# -*- coding: utf-8 -*-
#
# Portions of this code are derived from the copyrighted works of:
#    Damien Elmes <anki@ichi2.net>
#
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
#
# This project is hosted on GitHub: https://github.com/tarix/mcdsupport

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import QDialog, QCursor

from aqt import mw
from aqt.utils import showInfo, saveGeom, restoreGeom, askUser, openLink
import aqt.modelchooser
import aqt.tagedit

import mcd
from cloze import Cloze
import dlgAddMcds

def removeTabsAndNewlines(str):
    str = str.replace('\t', '')
    str = str.replace('\r', '')
    str = str.replace('\n', '')
    return str
    
class AddMcds(QDialog):

    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.setWindowIcon(QtGui.QIcon(':/icons/list-add.png'))
        self.form = dlgAddMcds.Ui_Dialog()
        self.form.setupUi(self)
        self.setupCombos()
        self.setupTagsAndDeck()
        self.setupButtons()
        self.updateTagsAndDeck()
        self.restoreState()
        self.mw.requireReset(modal=True)
        self.show()

    def setupCombos(self):
		# add MCD modes
        self.form.cmbMode.addItems(mcd.modeNames)
		# add the Model Chooser
        self.modelChooser = aqt.modelchooser.ModelChooser(self.mw, self.form.modelArea)
        
    def setupButtons(self):
        # set the configure icon
        self.form.pbtConfigure.setIcon(QtGui.QIcon(':/icons/configure.png'))
        self.form.pbtConfigure.hide()
        # connect the button signals to their functions
        QtCore.QObject.connect(self.form.pbtTextToNotes, QtCore.SIGNAL('clicked()'), self.copyTextToNotes)
        QtCore.QObject.connect(self.form.pbtTextToClozes, QtCore.SIGNAL('clicked()'), self.copyTextToClozes)
        QtCore.QObject.connect(self.form.pbtNotesToText, QtCore.SIGNAL('clicked()'), self.copyNotesToText)
        QtCore.QObject.connect(self.form.pbtConfigure, QtCore.SIGNAL('clicked()'), self.configure)
        QtCore.QObject.connect(self.form.pbtAdd, QtCore.SIGNAL('clicked()'), self.addMcd)
        QtCore.QObject.connect(self.form.buttonBox, QtCore.SIGNAL('helpRequested()'), self.helpRequested)

    # Tag & deck handling
    ######################################################################

    def setupTagsAndDeck(self):
        # hide and remove the elements from the layout
        self.form.lneDeck.hide()
        self.form.layTags.removeWidget(self.form.lneDeck)
        self.form.lneTags.hide()
        self.form.layTags.removeWidget(self.form.lneTags)
        # create our size policy
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
		# set the deck
        self.deck = aqt.tagedit.TagEdit(self, type=1)
        self.deck.setSizePolicy(sizePolicy)
        self.form.layTags.insertWidget(1, self.deck) # put it just past the label
        # set the tags
        self.tags = aqt.tagedit.TagEdit(self)
        self.tags.setSizePolicy(sizePolicy)
        self.form.layTags.insertWidget(3, self.tags) # put it just past the label

    def updateTagsAndDeck(self):
        if self.tags.col != self.mw.col:
            if self.deck:
                self.deck.setCol(self.mw.col)
            self.tags.setCol(self.mw.col)
        current_deck = self.mw.col.decks.name(self.mw.col.decks.selected())
        self.deck.setText(current_deck)

    # Save/Restore Dialog State
    ######################################################################

    def saveState(self):
        self.mw.pm.profile['mcd.mode'] = self.form.cmbMode.currentIndex()
        #self.mw.pm.profile['mcd.deck'] = self.deck.text()
        self.mw.pm.profile['mcd.tags'] = self.tags.text()
        saveGeom(self, 'mcd.addMcds')
    
    def restoreState(self):
        self.form.cmbMode.setCurrentIndex( self.mw.pm.profile.get('mcd.mode', 0) )
        #self.deck.setText( self.mw.pm.profile.get('mcd.deck') )
        self.tags.setText( self.mw.pm.profile.get('mcd.tags') )
        restoreGeom(self, 'mcd.addMcds')
            
    # Button Events
    ######################################################################

    def copyTextToNotes(self):
        text = self.form.pteText.toPlainText()
        self.form.pteNotes.insertPlainText( text )
    
    def copyTextToClozes(self):
        text = self.form.pteText.toPlainText()
        text = removeTabsAndNewlines(text)
        self.form.lneClozes.setText(text)
    
    def copyNotesToText(self):
        notes = self.form.pteNotes.toPlainText()
        self.form.pteText.insertPlainText( notes )
    
    def configure(self):
        return showInfo("not yet implemented")

    def addMcd(self):
        # begin busy cursor
        mw.app.setOverrideCursor(QCursor(Qt.WaitCursor))
        self.form.lblStatus.setText(u'')
        self.form.pbtAdd.setEnabled(False)
        mw.app.processEvents()
        # get all user input
        cloze = Cloze();
        cloze.mode = mcd.modes[ self.form.cmbMode.currentIndex() ]
        cloze.text = self.form.pteText.toPlainText()
        cloze.notes = self.form.pteNotes.toPlainText()
        cloze.source = self.form.lneSource.text()
        cloze.clozes = self.form.lneClozes.text()
        cloze.deck = self.deck.text()
        cloze.tags = self.tags.text()
		# create the note
        status = cloze.createNote()
        # update the results
        self.form.lblStatus.setText(status)
        # clear the form
        self.form.pteText.clear()
        self.form.pteNotes.clear()
        self.form.lneClozes.clear()
		# end busy cursor
        self.form.pbtAdd.setEnabled(True)
        mw.app.restoreOverrideCursor()
        
    def helpRequested(self):
        openLink('http://code.google.com/p/mcdsupport/wiki/Help')

    # Dialog Close
    ######################################################################

    def reject(self):
        if not self.canClose():
            return
        self.saveState()
        self.modelChooser.cleanup()
        self.mw.maybeReset()
        QDialog.reject(self)

    def canClose(self):
        has_data = self.form.pteText.toPlainText() or self.form.pteNotes.toPlainText()
        if (not has_data or askUser(_("Close and lose current input?"))):
            return True
        return False
