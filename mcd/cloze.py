# -*- coding: utf-8 -*-
#
# Portions of this code are derived from the copyrighted works of:
#    Damien Elmes <anki@ichi2.net>
#
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
#
# This project is hosted on GitHub: https://github.com/tarix/mcdsupport

from anki import utils

from aqt import mw

#from anki.errors import FactInvalidError

def listManualSpace(clozes):
    clozes = unicode.replace( unicode(clozes), u'\u3000', u' ' ) # replace wide spaces
    return clozes.split(u' ')

def listManualSemicolon(clozes):
    return clozes.split(u';')

def listKanjiHanzi(clozes):
    return list(clozes)

def clozeManual(text, cloze, num):
    # simply replace our selection directly
    cloze_text = u'{{c%d::' % num + cloze + u'}}'
    return unicode.replace( text, cloze, cloze_text )

class Cloze():
    def __init__(self):
        # cloze vars
        self.mode = 0
        self.text = u''
        self.notes = u''
        self.source = None
        self.clozes = u''
        # anki vars
        self.model = u''
        self.deck = u''
        self.tags = u''

    def createNote(self):
        # Manual (space delimeter)
        if self.mode == 0:
            listClozes = listManualSpace(self.clozes)
        # Manual (semicolon delimeter)
        elif self.mode == 1:
            listClozes = listManualSemicolon(self.clozes)
        # Kanji/Hanzi
        elif self.mode == 2:
            listClozes = listKanjiHanzi(self.clozes)
        # TODO: remove duplicates
        # grab part of the card for the status update
        excerpt = self.text[:10]
        excerpt = excerpt.replace(u'\n', u' ')
        if len(self.text) > 10: 
            excerpt += u'...'
        # process all of the closes
        added = 0
        num_cloze = 0
        for clz in listClozes:
	        # skip empty clozes (for example double spaces)
            if (clz.strip() == ''):
               continue
            num_cloze = num_cloze + 1
            # process this cloze
            self.text = clozeManual( self.text, clz, num_cloze )
        # TODO: deal with embedded clozes
        # create the new note
        note = mw.col.newNote()
        # set the deck
        if not self.deck.strip():
            note.did = 1
        else:
            note.did = mw.col.decks.id(self.deck)
        # set the tags
        note.tags = mw.col.tags.split(self.tags)
        # see if we have a source field
        source_id = mw.col.models.fieldMap( note.model() ).get('Source', None)
        # deal with the source field
        if self.source:
            if source_id:
                note.fields[ source_id ] = self.source
            else:
                self.notes = self.notes + u'<br><br>' + self.source
        # fill in the note fields
        note.fields[0] = self.text
        note.fields[1] = self.notes
        # check for errors
        if note.dupeOrEmpty():
            return u'Error: Note is empty or a duplicate'
        cards = mw.col.addNote(note)
        # save the collection
        mw.col.autosave()
        # TODO: Japanese reading generation
        # return the results
        status = u'Added \'{0}\' with {1} {2}.'.format(excerpt, num_cloze, u'cloze' if num_cloze == 1 else u'clozes')
        return status
