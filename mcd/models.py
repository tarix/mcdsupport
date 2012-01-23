# -*- coding: utf-8 -*-
#
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
#
# This project is hosted on GitHub: https://github.com/tarix/mcdsupport

from anki.stdmodels import models

# Basic MCD
##########################################################################

def addBasicMcdModel(col):
    mm = col.models
    m = mm.new("Basic MCD")
    fm = mm.newField("Text")
    mm.addField(m, fm)
    fm = mm.newField("Notes")
    mm.addField(m, fm)
    for i in range(99):
        n = i+1
        t = mm.newTemplate("MCD" + " %d" % n)
        fmt = "{{cloze:%d:Text}}%%s" % n
        t['css'] += """
.cloze {
 font-weight: bold;
 color: blue;
}"""
        t['qfmt'] = fmt % ""
        t['afmt'] = fmt % "<br>\n{{Notes}}"
        mm.addTemplate(m, t)
    mm.add(m)
    return m

models.append(("Basic MCD", addBasicMcdModel))

# Japanese MCD
##########################################################################

def addJapaneseMcdModel(col):
    mm = col.models
    m = mm.new("Japanese MCD")
    fm = mm.newField("Text")
    mm.addField(m, fm)
    fm = mm.newField("Reading")
    mm.addField(m, fm)
    fm = mm.newField("Notes")
    mm.addField(m, fm)
    for i in range(99):
        n = i+1
        t = mm.newTemplate("MCD" + " %d" % n)
        fmt = "{{cloze:%d:Text}}%%s" % n
        t['css'] += """
.cloze {
 font-weight: bold;
 color: blue;
}"""
        t['qfmt'] = fmt % ""
        t['afmt'] = fmt % "<br>\n{{Reading}}<br>\n{{Notes}}"
        mm.addTemplate(m, t)
    mm.add(m)
    return m

models.append(("Japanese MCD", addJapaneseMcdModel))
