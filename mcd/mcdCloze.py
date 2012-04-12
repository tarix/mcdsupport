# -*- coding: utf-8 -*-
#
# Portions of this code are derived from the copyrighted works of:
#    Damien Elmes <anki@ichi2.net>
#    Adam Mesha <adam@mesha.org>
#   
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# This free project is hosted by GitHub: https://github.com/tarix/mcdsupport

from anki import utils
from ankiqt import mw
from anki.errors import FactInvalidError
from mcdMecab import listMecab

CLOZETEXT = u'<span style="font-weight:600; color:#0000ff;">[...]</span>'

def listManualSpace(clozes):
    # convert the clozes from a string to a list
    clozes = unicode.replace( unicode(clozes), u'\u3000', u' ' ) # replace wide spaces
    listClozes = clozes.split(u' ')
    # done
    return listClozes

def listManualSemicolon(clozes):
    # convert the clozes from a string to a list
    listClozes = unicode( clozes ).split(u';')
    # done
    return listClozes

def listKanjiHanzi(clozes):
    return list( unicode(clozes) )

def clozeManual(selection, cloze):
    # simply replace our selection directly
    return unicode.replace( selection, cloze, CLOZETEXT )

def createCards(model, selection, clozes, notes, tags, mode):
    # pre-convert unicode strings
    uniSelection = unicode(selection)

    # Manual (space delimeter)
    if mode == 'space':
        listClozes = listManualSpace(clozes)
    # Manual (semicolon delimeter)
    elif mode == 'semicolon':
        listClozes = listManualSemicolon(clozes)
    # Auto: Kanji/Hanzi
    elif mode == 'kanji':
        listClozes = listKanjiHanzi(clozes)
    elif mode == 'mecab':
        listClozes = listMecab(uniSelection, CLOZETEXT)

	# convert tags string to anki tags
    tags = utils.canonifyTags(unicode(tags))
    # counters for added/failed cards
    added = 0
    failed = 0

    # process all of the closes
    for clz in listClozes:

        # create a new fact
        fact = mw.deck.newFact(model)

        def setField(index, value):
          fact.fields[index].value = unicode.replace( value, u'\n', u'<br>' )

        if mode == 'mecab':
          question = clz[0]
          answer = clz[1]
          expression = clz[2]
          setField(3, clz[3])
        else:
              # skip empty clozes (for example double spaces)
          if (clz.strip() == ''):
              continue
          # formulate the new card
          question = clozeManual( uniSelection, unicode(clz) )
          answer = unicode(clz)
          expression = uniSelection

          # check for cloze that did nothing
          if question == expression:
              continue

          # Japanese reading generation (newline hack from the Japanese support plugin)
          if model.name == 'Japanese MCD':
             fact.fields[2].value = expression.replace( "\n", "htmlNewLine" )
             fact.focusLost(fact.fields[2])
             fact.fields[3].value = fact.fields[3].value.replace( "htmlNewLine", "<br>" )
   
        # add the rest of the fields
        setField(0, question)
        setField(1, answer)
        setField(2, expression)
        idx = 4 if model.name == 'Japanese MCD' else 3
        setField(idx, unicode(notes))
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
    excerpt = excerpt.replace('\n', ' ')
    if len(uniSelection) > 10: 
        excerpt += u'...'
    # build the results string
    status = u'Processed \'{0}\'  Added {1} new {2}.'.format(excerpt, added, 'card' if added == 1 else 'cards')
    if failed > 0:
        status += u'  Skipped {0} {1}.'.format(failed, 'card' if failed == 1 else 'cards')
    
    return status
