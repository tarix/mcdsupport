# -*- coding: utf-8 -*-
#
# Portions of this code are derived from the copyrighted works of:
#    Damien Elmes <anki@ichi2.net>
#
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
#
# This project is hosted on GitHub: https://github.com/tarix/mcdsupport

import re

from anki import utils
from anki.consts import *

from aqt import mw

# http://www.peterbe.com/plog/uniqifiers-benchmark
def removeDups(seq): # Dave Kirby (f8)
    # Order preserving
    seen = set()
    return [x for x in seq if x not in seen and not seen.add(x)]

def listManualSpace(clozes):
    clozes = unicode.replace( unicode(clozes), u'\u3000', u' ' ) # replace wide spaces
    return clozes.split(u' ')

def listManualSemicolon(clozes):
    return clozes.split(u';')

def listKanjiHanzi(clozes):
    return list(clozes)

class Cloze():
    def __init__(self):
        # cloze vars
        self.mode = 0
        self.text = u''
        self.notes = u''
        self.source = u''
        self.clozes = u''
        self.whole_words_only = False
        # anki vars
        self.model = u''
        self.deck = u''
        self.tags = u''
        # status
        self.status = u''

    def _generateClozeList(self):
        # Manual (space delimeter)
        if self.mode == 'space':
            listClozes = listManualSpace(self.clozes)
        # Manual (semicolon delimeter)
        elif self.mode == 'semicolon':
            listClozes = listManualSemicolon(self.clozes)
        # Kanji/Hanzi
        elif self.mode == 'kanji':
            listClozes = listKanjiHanzi(self.clozes)
        # remove any empty (whitespace only) entries
        listClozes = [ clz for clz in listClozes if clz.strip() ]
        # remove duplicates
        listClozes = removeDups(listClozes)
        return listClozes

    def _clozeReplace(self, text, cloze, cloze_text):
        # process the replacement based on user options
        if self.whole_words_only:
            return re.sub(ur'\b{}\b'.format(cloze), cloze_text, text, flags=re.UNICODE)
        else:
            return unicode.replace( text, cloze, cloze_text )

    def _clozePrepare(self, text, cloze, num):
        # replace the text with a cloze sub
        cloze_stub = u'{{c%d::' % num + u'}}'
        return self._clozeReplace( text, cloze, cloze_stub )

    def _clozeFinalize(self, text, cloze, num):
        # replace the subs with the final cloze
        cloze_stub = u'{{c%d::' % num + u'}}'
        cloze_text = u'{{c%d::' % num + cloze + u'}}'
        return unicode.replace( text, cloze_stub, cloze_text )

    def createNote(self):
        # create the new note
        note = mw.col.newNote()
        # set the deck
        if not self.deck.strip():
            note.model()['did'] = 1
        else:
            note.model()['did'] = mw.col.decks.id(self.deck)
        # verify this is an Anki 2 cloze model
        if not note.model()['type'] == MODEL_CLOZE:
            self.status = u'Error: '+note.model()['name']+' is not a Cloze model.' 
            return False
        # create a list of cloze candidates
        listClozes = self._generateClozeList()
        # grab part of the card for the status update
        excerpt = self.text[:10]
        excerpt = excerpt.replace(u'\n', u' ')
        if len(self.text) > 10:
            excerpt += u'...'
        # convert the newlines to html
        self.text = unicode.replace( self.text, '\n', '<br>' )
        self.notes = unicode.replace( self.notes, '\n', '<br>' )
        self.source = unicode.replace( self.source, '\n', '<br>' )            
        # save the text for the reading generation
        reading = self.text
        # pre-process all of the closes
        for i, clz in enumerate(listClozes):
            self.text = self._clozePrepare( self.text, clz, i+1 )
        # finalize the clozes, this two stage process prevents errors with embedded clozes
        for i, clz in enumerate(listClozes):
            self.text = self._clozeFinalize( self.text, clz, i+1 )
        # set the tags
        note.tags = mw.col.tags.split(self.tags)
        # deal with the source field
        if len(self.source):
            source_id = mw.col.models.fieldMap( note.model() ).get('Source', None)
            if source_id:
                note.fields[ source_id[0] ] = self.source
            else:
                self.notes = self.notes + u'<br><br>' + self.source
        # check for a reading field
        reading_id = mw.col.models.fieldMap( note.model() ).get('Reading', None)
        if reading_id:
            try:
                from japanese.reading import mecab
                note.fields[ reading_id[0] ] = mecab.reading(reading)
            except:
                self.status = u'Error: Unable to generate the reading. Please install the Japanese Support Plugin.'
                return False
        # fill in the note fields
        note.fields[0] = self.text
        note.fields[1] = self.notes
        # check for errors
        if note.dupeOrEmpty():
            self.status = u'Error: Note is empty or a duplicate'
            return False
        cards = mw.col.addNote(note)
        # save the collection
        mw.col.autosave()
        # set the status
        self.status = u'Added a new note \'{0}\' with {1} {2}.'.format(excerpt, len(listClozes), u'cloze' if len(listClozes) == 1 else u'clozes')
        # return success
        return True
