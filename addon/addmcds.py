# -*- coding: utf-8 -*-
#
# Portions of this code are derived from the copyrighted works of:
#    Damien Elmes <anki@ichi2.net>
#
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
#
# This project is hosted on GitHub: https://github.com/tarix/mcdsupport

from aqt import mw
from aqt.utils import showInfo, saveGeom, restoreGeom, askUser, openLink
from aqt.qt import *

import aqt.modelchooser
import aqt.tagedit

from . import _globals
from .cloze import Cloze
from . import dlgAddMcds

def removeTabsAndNewlines(str):
    str = str.replace('\t', '')
    str = str.replace('\r', '')
    str = str.replace('\n', '')
    return str
    
class AddMcds(QDialog):

    def __init__(self, mw):
        super(AddMcds, self).__init__(mw)
        #QDialog.__init__(self, parent=mw, Qt.Window)
        self.mw = mw
        self.setWindowIcon(QIcon(':/icons/list-add.png'))
        self.form = dlgAddMcds.Ui_Dialog()
        self.form.setupUi(self)
        self.setupCombos()
        self.setupTagsAndDeck()
        self.setupButtons()
        self.updateTagsAndDeck()
        self.restoreState()
        self.mw.requireReset(modal=True)
        self.setWindowTitle( self.windowTitle()+' ('+_globals.appname+')' )
        self.show()

    def setupCombos(self):
        # add MCD modes
        self.form.cmbMode.addItems(_globals.modeNames)
        # add the Model Chooser
        self.modelChooser = aqt.modelchooser.ModelChooser(self.mw, self.form.modelArea)
        
    def setupButtons(self):
        # set the configure icon
        self.form.pbtConfigure.setIcon(QIcon(':/icons/configure.png'))
        self.form.pbtConfigure.hide()
        # connect the button signals to their functions
        self.form.pbtTextToNotes.clicked.connect(self.copyTextToNotes)
        self.form.pbtTextToClozes.clicked.connect(self.copyTextToClozes)
        self.form.pbtNotesToText.clicked.connect(self.copyNotesToText)
        self.form.pbtConfigure.clicked.connect(self.configure)
        self.form.pbtAdd.clicked.connect(self.addMcd)
        self.form.buttonBox.helpRequested.connect(self.helpRequested)

    # Tag & deck handling
    ######################################################################

    def setupTagsAndDeck(self):
        # hide and remove the elements from the layout
        self.form.lneDeck.hide()
        self.form.layTags.removeWidget(self.form.lneDeck)
        self.form.lneTags.hide()
        self.form.layTags.removeWidget(self.form.lneTags)
        # set the deck
        self.deck = aqt.tagedit.TagEdit(self, type=1)
        self.form.layTags.insertWidget(1, self.deck) # put it just past the label
        # set the tags
        self.tags = aqt.tagedit.TagEdit(self)
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
        self.mw.pm.profile['mcd.whole_words'] = self.form.tbtWholeWords.isChecked()
        saveGeom(self, 'mcd.addMcds')
    
    def restoreState(self):
        self.form.cmbMode.setCurrentIndex( self.mw.pm.profile.get('mcd.mode', 0) )
        #self.deck.setText( self.mw.pm.profile.get('mcd.deck') )
        self.tags.setText( self.mw.pm.profile.get('mcd.tags') )
        self.form.tbtWholeWords.setChecked( self.mw.pm.profile.get('mcd.whole_words', False) )
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
        self.mw.app.setOverrideCursor(QCursor(Qt.WaitCursor))
        self.form.lblStatus.setText('')
        self.form.pbtAdd.setEnabled(False)
        self.mw.app.processEvents()
        # get all user input
        cloze = Cloze();
        cloze.mode = _globals.modes[ self.form.cmbMode.currentIndex() ]
        cloze.text = self.form.pteText.toPlainText()
        cloze.notes = self.form.pteNotes.toPlainText()
        cloze.source = self.form.lneSource.text()
        cloze.clozes = self.form.lneClozes.text()
        cloze.whole_words_only = self.form.tbtWholeWords.isChecked()
        cloze.deck = self.deck.text()
        cloze.tags = self.tags.text()
        # create the note
        okay = cloze.createNote()
        # update the results
        self.form.lblStatus.setText(cloze.status)
        # clear the form
        if okay:
            self.form.pteText.clear()
            self.form.pteNotes.clear()
            self.form.lneClozes.clear()
        # end busy cursor
        self.form.pbtAdd.setEnabled(True)
        self.mw.app.restoreOverrideCursor()
        
    def helpRequested(self):
        openLink('https://github.com/tarix/mcdsupport')

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
