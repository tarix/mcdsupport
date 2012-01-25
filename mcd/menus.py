# -*- coding: utf-8 -*-
#
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
#
# This project is hosted on GitHub: https://github.com/tarix/mcdsupport

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import QAction

from aqt import mw

import mcd.addmcds

dlgAddMcds = None

def menuAddMcds():
    # TODO: handle existing instance
    dlgAddMcds = mcd.addmcds.AddMcds(mw)

def init():
	mw.form.actionAddMcd = QtGui.QAction('Add MCD Cards', mw)
	mw.form.actionAddMcd.setStatusTip('Add MCD Cards')
	mw.form.actionAddMcd.setEnabled(True)
	#mw.form.actionAddMcd.setShortcut(SHORTCUTKEY)
	mw.connect(mw.form.actionAddMcd, QtCore.SIGNAL('triggered()'), menuAddMcds)
	mw.form.menuTools.addAction(mw.form.actionAddMcd)

init()
