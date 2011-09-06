# -*- coding: utf-8 -*-
# Copyright: 
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# MCD Japanese Model
#

from anki.models import Model, CardModel, FieldModel
import anki.stdmodels

def mcdJapaneseModel():
    m = Model(_("Japanese MCD"))
    # question
    f = FieldModel(u'Question', True, True)
    font = u"Arial"
    f.quizFontSize = 22
    f.quizFontFamily = font
    f.editFontSize = 20
    f.editFontFamily = font
    m.addFieldModel(f)
    # answer
    f = FieldModel(u'Answer', True, False)
    font = u"Arial"
    f.quizFontSize = 24
    f.quizFontFamily = font
    f.editFontSize = 20
    f.editFontFamily = font
    m.addFieldModel(f)
    # expression
    f = FieldModel(u'Expression', True, False)
    font = u"Arial"
    f.quizFontSize = 20
    f.quizFontFamily = font
    f.editFontSize = 20
    f.editFontFamily = font
    m.addFieldModel(f)
    # reading
    f = FieldModel(u'Reading', False, False)
    font = u"Arial"
    f.quizFontSize = 18
    f.quizFontFamily = font
    f.editFontSize = 20
    f.editFontFamily = font
    m.addFieldModel(f)
    # notes
    f = FieldModel(u'Notes', False, False)
    font = u"Arial"
    f.quizFontSize = 20
    f.quizFontFamily = font
    f.editFontSize = 20
    f.editFontFamily = font
    m.addFieldModel(f)
    m.addCardModel(CardModel(u"Review",
                   u"%(Question)s",
                   u"%(Answer)s<br>%(^Reading)s<br><br>%(Expression)s<br>%(/Reading)s<br><br>%(Reading)s<br><br>%(Notes)s"))
    m.tags = u"Japanese"
    return m

anki.stdmodels.models['Japanese MCD'] = mcdJapaneseModel
