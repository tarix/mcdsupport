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

from .japanese_reading import mecab

# http://www.peterbe.com/plog/uniqifiers-benchmark
def removeDups(seq): # Dave Kirby (f8)
    # Order preserving
    seen = set()
    return [x for x in seq if x not in seen and not seen.add(x)]

def listManualSpace(clozes):
    clozes = str.replace( str(clozes), '\u3000', ' ' ) # replace wide spaces
    return clozes.split(' ')

def listManualSemicolon(clozes):
    return clozes.split(';')

def listKanjiHanzi(clozes):
    return list(clozes)

def formatReplacement(cloze, reading):
    if cloze == reading:
        return cloze
    else:
        return ' %s::%s' % (reading, cloze)

class Cloze():
    def __init__(self):
        # grab reference to anki globals
        self.mw = mw
        # cloze vars
        self.mode = 0
        self.text = ''
        self.notes = ''
        self.source = ''
        self.clozes = ''
        self.whole_words_only = False
        # anki vars
        self.model = ''
        self.deck = ''
        self.tags = ''
        # status
        self.status = ''

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
        # Japanese Learning mode uses manually spaced words
        if self.mode == 'jp_learning':
            listClozes = listManualSpace(self.clozes)
        # remove any empty (whitespace only) entries
        listClozes = [ clz for clz in listClozes if clz.strip() ]
        # remove duplicates
        listClozes = removeDups(listClozes)
        return listClozes

    def _generateReplacementList(self, clozes):
        # learning mode adds the reading
        if self.mode == 'jp_learning':
            # generate the readings from mecab
            try:
                readings = [ mecab.reading(clz) for clz in clozes ]
            except:
                self.status = 'Error: Unable to generate cloze readings. Please install the Japanese Support Plugin.'
                return None
            replacements = [ formatReplacement( clozes[i], reading ) for i, reading in enumerate(readings) ]
        else:
            replacements = clozes
        return replacements

    def _clozeReplace(self, text, cloze, cloze_text):
        # process the replacement based on user options
        if self.whole_words_only:
            return re.sub(r'\b{}\b'.format(cloze), cloze_text, text, flags=re.UNICODE)
        else:
            return str.replace( text, cloze, cloze_text )

    def _clozePrepare(self, text, cloze, num):
        # replace the text with a cloze stub
        cloze_stub = '{{c%d::}}' % num
        return self._clozeReplace( text, cloze, cloze_stub )

    def _clozeFinalize(self, text, cloze, num):
        # replace the subs with the final cloze
        cloze_stub = '{{c%d::}}' % num
        cloze_text = '{{c%d::%s}}' % (num, cloze)
        return str.replace( text, cloze_stub, cloze_text )

    def createNote(self):
        # create the new note
        note = self.mw.col.newNote()
        # set the deck
        if not self.deck.strip():
            note.model()['did'] = 1
        else:
            note.model()['did'] = self.mw.col.decks.id(self.deck)
        # verify this is an Anki 2 cloze model
        if not note.model()['type'] == MODEL_CLOZE:
            self.status = 'Error: '+note.model()['name']+' is not a Cloze note type.' 
            return False
        # create a list of cloze candidates and their replacements
        listClozes = self._generateClozeList()
        replacements = self._generateReplacementList(listClozes)
        if not replacements:
            return False
        # grab part of the card for the status update
        excerpt = self.text[:10]
        excerpt = excerpt.replace('\n', ' ')
        if len(self.text) > 10:
            excerpt += '...'
        # convert the newlines to html
        self.text = str.replace( self.text, '\n', '<br>' )
        self.notes = str.replace( self.notes, '\n', '<br>' )
        self.source = str.replace( self.source, '\n', '<br>' )            
        # save the expression for the reading generation
        expression = self.text
        # pre-process all of the closes
        for i, clz in enumerate(listClozes):
            self.text = self._clozePrepare( self.text, clz, i+1 )
        # finalize the clozes, this two stage process prevents errors with embedded clozes
        for i, clz in enumerate(replacements):
            self.text = self._clozeFinalize( self.text, clz, i+1 )
        # set the tags
        note.tags = self.mw.col.tags.split(self.tags)
        # deal with the source field
        if len(self.source):
            source_id = self.mw.col.models.fieldMap( note.model() ).get('Source', None)
            if source_id:
                note.fields[ source_id[0] ] = self.source
            else:
                self.notes = self.notes + '<br><br>' + self.source
        # check for a reading field
        reading_id = self.mw.col.models.fieldMap( note.model() ).get('Reading', None)
        if reading_id:
            try:
                note.fields[ reading_id[0] ] = mecab.reading(expression)
            except:
                self.status = 'Error: Unable to generate the reading. Please install the Japanese Support Plugin.'
                return False
        # if we have an expression field, save the original text
        expression_id = self.mw.col.models.fieldMap( note.model() ).get('Expression', None)
        if expression_id:
            note.fields[ expression_id[0] ] = expression
        # fill in the note fields
        note.fields[0] = self.text
        note.fields[1] = self.notes
        # check for errors
        if note.dupeOrEmpty():
            self.status = 'Error: Note is empty or a duplicate.'
            return False
        # add the new note
        cards = self.mw.col.addNote(note)
        if not cards:
            self.status = 'Error: This note was not able to generate any cards.'
            return False
        # flag the queue for reset
        self.mw.requireReset()
        # save the collection
        self.mw.col.autosave()
        # set the status
        self.status = 'Added a new note \'{0}\' with {1} {2}.'.format(excerpt, len(listClozes), 'cloze' if len(listClozes) == 1 else 'clozes')
        # return success
        return True
