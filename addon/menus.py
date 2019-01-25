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

# ----------------------------------------------------------------------------
#
# This was a simple hack to fill out the Expression field for older MCD cards
# in order to provide compatibility with MorphMan. I saved it in case its
# useful for other upgrade functions in the future.
#
# import re
#
# clozeReg = r"\{\{c[0-9]*?::(.*?)(::(.*?))?\}\}"
#
# def stripCloze( s ):
#     def repl(m):
#         if m.group(3):
#             return m.group(3)
#         return m.group(1)
#     s = re.sub(clozeReg, repl, s)
#     return s
#
# def menuFixExpression():
#     mid = mw.col.models.byName('Japanese MCD')
#     text_id = mw.col.models.fieldMap(mid).get('Text', None)[0] 
#     expression_id = mw.col.models.fieldMap(mid).get('Expression', None)[0] 
#     ids = mw.col.findNotes('"note:Japanese MCD"')
#     for id in ids:
#         note = mw.col.getNote(id)
#         expression = note.fields[expression_id]
#         if expression == '':
#             text = note.fields[text_id]
#             note.fields[expression_id] = stripCloze(text)
#             note.flush()
#     mw.col.save()
#     mw.reset()
#
# def initFixExpression():
#     # add the menu option to randomize the deck
#     mw.form.actionAddMcd = QAction('Fix Expression', mw)
#     mw.form.actionAddMcd.setStatusTip('Fix Expression')
#     mw.form.actionAddMcd.setEnabled(True)
#     mw.form.actionAddMcd.triggered.connect(menuFixExpression)
#     mw.form.menuTools.addAction(mw.form.actionAddMcd)
#
# -----------------------------------------------------------------------------

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
