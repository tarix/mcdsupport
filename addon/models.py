# -*- coding: utf-8 -*-
#
# Portions of this code are derived from the copyrighted works of:
#    Damien Elmes <anki@ichi2.net>
#
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
#
# This project is hosted on GitHub: https://github.com/tarix/mcdsupport

from anki.consts import MODEL_CLOZE
from anki.stdmodels import models

# Basic MCD
##########################################################################

def addBasicMcdModel(col):
    mm = col.models
    m = mm.new("Basic MCD")
    m['type'] = MODEL_CLOZE    
    m['css'] += """
.cloze {
 font-weight: bold;
 color: blue;
}"""
    fm = mm.newField("Text")
    mm.addField(m, fm)
    fm = mm.newField("Notes")
    mm.addField(m, fm)
    fm = mm.newField("Source")
    mm.addField(m, fm)
    t = mm.newTemplate("Basic MCD")
    fmt = "{{cloze:Text}}%s"
    t['qfmt'] = fmt % ""
    t['afmt'] = fmt % "<br>\n{{Notes}}<br>\n{{Source}}"
    mm.addTemplate(m, t)
    mm.add(m)
    return m

models.append((lambda: _("Basic MCD"), addBasicMcdModel))

# Japanese MCD
##########################################################################

def addJapaneseMcdModel(col):
    mm = col.models
    m = mm.new("Japanese MCD")
    m['type'] = MODEL_CLOZE    
    m['css'] += """
.cloze {
 font-weight: bold;
 color: blue;
}"""
    fm = mm.newField("Text")
    mm.addField(m, fm)
    fm = mm.newField("Notes")
    mm.addField(m, fm)
    fm = mm.newField("Source")
    mm.addField(m, fm)
    fm = mm.newField("Expression")
    mm.addField(m, fm)
    fm = mm.newField("Reading")
    mm.addField(m, fm)
    t = mm.newTemplate("Japanese MCD")
    t['qfmt'] = "<span lang=\"jp\"><div class=front>{{kanji:cloze:Text}}</div></span>"
    t['afmt'] = "<span lang=\"jp\">\n<div class=front>{{furigana:cloze:Text}}</div>\n\n<hr>\n\n{{#Notes}}{{furigana:Notes}}<br><br>{{/Notes}}\n{{#Reading}}{{furigana:Reading}}<br><br>{{/Reading}}\n{{Source}}\n</span>"
    mm.addTemplate(m, t)
    mm.add(m)
    return m

models.append((lambda: _("Japanese MCD"), addJapaneseMcdModel))
