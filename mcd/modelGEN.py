# -*- coding: utf-8 -*-
#
# This is free and unencumbered software released into the public domain.
#
# Portions of this code are derived from the copyrighted works of:
#    Damien Elmes <anki@ichi2.net>
#   
# All rights of the original authors are reserved pursuiant to the following license:
#    GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# This free project is hosted by GitHub: https://github.com/tarix/mcdsupport

from anki.models import Model, CardModel, FieldModel
import anki.stdmodels

def mcdGenericModel():
    m = Model(_("Generic MCD"))
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
                   u"%(Answer)s<br><br>%(Expression)s<br><br>%(Notes)s"))
    m.tags = u"Generic"
    return m

anki.stdmodels.models['Generic MCD'] = mcdGenericModel
