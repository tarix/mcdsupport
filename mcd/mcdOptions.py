# -*- coding: utf-8 -*-
#
# This is free and unencumbered software released into the public domain.
#
# All rights of the original authors are reserved pursuiant to the following license:
#    GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# This free project is hosted by GitHub: https://github.com/tarix/mcdsupport

from ankiqt import mw, ui

helpFirst = '''
<p><big><center><b>MCD Support for Anki</b></center></big></p>

<p>If you wish to use this MCD cards with this deck be sure and add the "Japanese MCD" model:
<ol>
<li>Click Settings and then Deck Properties ...
<li>Click on the Add button under Model.
<li>Click on "Add: Japanse MCD"
<li>Click OK
</ol>
</p>
'''

autoClearPassage = False
autoClearNotes = False
autoClearClozes = False

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
	# check for message of the day
    motd = mw.deck.getVar('plugin.mcdsupport.motd')
    if (motd is None):
        # this means its a new deck
        ui.utils.showText(helpFirst, None, type='html')	
        motd = 0
    # use this in the future to display upgrade messages
    if (motd is not 1):
        # save the fact we've seen it
        motd = 1
        mw.deck.setVar('plugin.mcdsupport.motd', motd)

from anki.hooks import addHook
addHook("loadDeck", onLoadDeck)
