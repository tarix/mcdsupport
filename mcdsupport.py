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

def init():
	import mcd.modelJP
	import mcd.modelGEN
	import mcd.mcdUI

from ankiqt import mw
mw.registerPlugin("MCD Support", 0)

from anki.hooks import addHook
addHook('init', init)
