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
from PyQt4.QtGui import QAction

from aqt import mw
from aqt.utils import tooltip

import mcd.addmcds

dlgAddMcds = None

def menuAddMcds():
    # TODO: handle existing instance
    dlgAddMcds = mcd.addmcds.AddMcds(mw)

def menuRandomizeDeck():
    # randomize the currently selected deck
    deck = mw.col.decks.current()
    # get this deck configuration
    conf = mw.col.decks.confForDid( deck['id'] )
    # only randomize if the current deck is set to random
    if conf['new']['order'] == 0:
        mw.col.sched.randomizeCards( deck['id'] )
        tip = deck['name']+' randomized.'
    else:
        tip = deck['name']+' is not a random deck.'
    tooltip( tip, period=5000 )

def init():
    mw.form.menuTools.addSeparator()
    # add the menu option for the main dialog
    mw.form.actionAddMcd = QtGui.QAction('Add MCD Cards', mw)
    mw.form.actionAddMcd.setStatusTip('Add MCD Cards')
    mw.form.actionAddMcd.setEnabled(True)
    mw.form.actionAddMcd.setShortcut('Ctrl+M')
    mw.form.actionAddMcd.setIcon(QtGui.QIcon(':/icons/list-add.png'))
    mw.connect(mw.form.actionAddMcd, QtCore.SIGNAL('triggered()'), menuAddMcds)
    mw.form.menuTools.addAction(mw.form.actionAddMcd)
    # add the menu option to randomize the deck
    mw.form.actionAddMcd = QtGui.QAction('Randomize Deck', mw)
    mw.form.actionAddMcd.setStatusTip('Randomize Deck')
    mw.form.actionAddMcd.setEnabled(True)
    mw.form.actionAddMcd.setShortcut('Ctrl+R')
    mw.form.actionAddMcd.setIcon(QtGui.QIcon(':/icons/package_games_card.png'))
    mw.connect(mw.form.actionAddMcd, QtCore.SIGNAL('triggered()'), menuRandomizeDeck)
    mw.form.menuTools.addAction(mw.form.actionAddMcd)

init()
