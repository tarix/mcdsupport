# -*- coding: utf-8 -*-
#
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
#
# This project is hosted on GitHub: https://github.com/tarix/mcdsupport

from aqt import mw
from anki.hooks import addHook

def init():
    import mcd.models
#	import mcd.mcdUI

#mw.addonManager.registerAddon("MCD Support", 20000);
init()  #addHook('init', init)
