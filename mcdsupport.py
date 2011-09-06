# -*- coding: utf-8 -*-
# Copyright: 
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

def init():
	import mcd.modelJP
	import mcd.mcdUI

from ankiqt import mw
mw.registerPlugin("MCD Support", 9999)

from anki.hooks import addHook
addHook('init', init)

#from ankiqt import ui
#ui.utils.showInfo('registered')
