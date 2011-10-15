# -*- coding: utf-8 -*-
#
# This is free and unencumbered software released into the public domain.
#
# All rights of the original authors are reserved pursuiant to the following license:
#    GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# This free project is hosted by GitHub: https://github.com/tarix/mcdsupport

from ankiqt import mw

autoClearPassage = False
autoClearNotes = False
autoClearNotes = False

def save():
    # autoClearPassage
    global autoClearPassage
    mw.deck.setVar('plugin.mcdsupport.autoClearPassage', autoClearPassage)
    # autoClearNotes
    global autoClearNotes
    mw.deck.setVar('plugin.mcdsupport.autoClearNotes', autoClearNotes)
    # autoClearClozes
    global autoClearClozes
    mw.deck.setVar('plugin.mcdsupport.autoClearClozes', autoClearClozes)   

def onLoadDeck():
    # autoClearPassage
    global autoClearPassage
    autoClearPassage = mw.deck.getBool('plugin.mcdsupport.autoClearPassage')
    if (autoClearPassage is None):
        autoClearPassage = False
    # autoClearNotes
    global autoClearNotes
    autoClearNotes = mw.deck.getBool('plugin.mcdsupport.autoClearNotes')
    if (autoClearNotes is None):
        autoClearNotes = False
    # autoClearClozes
    global autoClearClozes
    autoClearClozes = mw.deck.getBool('plugin.mcdsupport.autoClearClozes')
    if (autoClearClozes is None):
        autoClearClozes = False

from anki.hooks import addHook
addHook("loadDeck", onLoadDeck)
