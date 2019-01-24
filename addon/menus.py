# -*- coding: utf-8 -*-
#
# Portions of this code are derived from the copyrighted works of:
#    Damien Elmes <anki@ichi2.net>
#
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
#
# This project is hosted on GitHub: https://github.com/tarix/mcdsupport

from aqt import mw
from aqt.qt import *
from aqt.utils import tooltip

from .addmcds import *

dlgAddMcds = None

def menuAddMcds():
    # TODO: handle existing instance
    dlgAddMcds = AddMcds(mw)

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
    mw.form.actionAddMcd = QAction('Add MCD Cards', mw)
    mw.form.actionAddMcd.setStatusTip('Add MCD Cards')
    mw.form.actionAddMcd.setEnabled(True)
    mw.form.actionAddMcd.setShortcut('Ctrl+M')
    mw.form.actionAddMcd.setIcon(QIcon(':/icons/list-add.png'))
    mw.form.actionAddMcd.triggered.connect(menuAddMcds)
    mw.form.menuTools.addAction(mw.form.actionAddMcd)
    # add the menu option to randomize the deck
    mw.form.actionAddMcd = QAction('Randomize Deck', mw)
    mw.form.actionAddMcd.setStatusTip('Randomize Deck')
    mw.form.actionAddMcd.setEnabled(True)
    mw.form.actionAddMcd.setShortcut('Ctrl+R')
    mw.form.actionAddMcd.setIcon(QIcon(':/icons/package_games_card.png'))
    mw.form.actionAddMcd.triggered.connect(menuRandomizeDeck)
    mw.form.menuTools.addAction(mw.form.actionAddMcd)

init()
