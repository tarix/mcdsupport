# -*- coding: utf-8 -*-
# Copyright: 
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from anki import utils
from ankiqt import mw
from anki.errors import FactInvalidError

CLOZETEXT = u'<span style="font-weight:600; color:#0000ff;">[...]</span>'

def createCards(model, selection, clozes, notes, tags):
    # convert the clozes from a string to a list
    clozes = unicode.replace( unicode(clozes), u'\u3000', u' ' ) # replace wide spaces
    listClozes = clozes.split(u' ')
	# convert tags string to anki tags
    tags = utils.canonifyTags(unicode(tags))	
    # counters for added/failed cards    
    added = 0
    failed = 0
	# pre-convert unicode strings
    uniSelection = unicode(selection)
	# process all of the closes
    for clz in listClozes:
        # formulate the new card
        question = unicode.replace( uniSelection, unicode(clz), CLOZETEXT )
        answer = unicode(clz)
        expression = uniSelection
		# check for cloze that did nothing
        if question == expression:
            continue
        # create a new fact
        fact = mw.deck.newFact(model)
		# add the raw expression for the reading generation
        fact.fields[2].value = expression
        fact.focusLost(fact.fields[2])
		# add the rest of the fields
        fact.fields[0].value = unicode.replace( question, u'\n', u'<br>' )
        fact.fields[1].value = unicode.replace( answer, u'\n', u'<br>' )
        fact.fields[2].value = unicode.replace( expression, u'\n', u'<br>' )
        fact.fields[4].value = unicode.replace( unicode(notes), u'\n', u'<br>' )
        fact.tags = tags
        # add the fact to the deck
        try:
            mw.deck.addFact(fact)
            added += 1
        except FactInvalidError:
            failed += 1
    # flush and rebuild the deck so we can use the new facts
    mw.deck.s.flush()
    mw.deck.rebuildCSS()
    mw.deck.save()
    mw.reset()
	# grab part of the card for the status update
    excerpt = uniSelection[:10]
    if len(uniSelection) > 10: 
        excerpt += u'...'
    # build the results string
    status = u'Processed \'{0}\'  Added {1} new {2}.'.format(excerpt, added, 'card' if added == 1 else 'cards')
    if failed > 0:
	    status += u'  Skipped {0} {1}.'.format(failed, 'card' if failed == 1 else 'cards')
	
    return status