# -*- coding: utf-8 -*-
#
# Portions of this code are derived from the copyrighted works of:
#    Damien Elmes <anki@ichi2.net>
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

models.append(("Basic MCD", addBasicMcdModel))

# Japanese MCD
##########################################################################

def addJapaneseMcdModel(col):
    mm = col.models
    m = mm.new("Japanese MCD")
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
    fm = mm.newField("Reading")
    mm.addField(m, fm)
    t = mm.newTemplate("Japanese MCD")
    fmt = "{{cloze:Text}}%s"
    t['qfmt'] = fmt % ""
    t['afmt'] = fmt % "<br>\n{{Reading}}<br>\n{{Notes}}<br>\n{{Source}}"
    mm.addTemplate(m, t)
    mm.add(m)
    return m

models.append(("Japanese MCD", addJapaneseMcdModel))
