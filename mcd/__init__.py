# -*- coding: utf-8 -*-
#
# Portions of this code are derived from the copyrighted works of:
#    Damien Elmes <anki@ichi2.net>
#   
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# This free project is hosted by GitHub: https://github.com/tarix/mcdsupport

version = "1.2-7"

generic_modes = [
    'space',
    'semicolon'
]

japanese_modes = generic_modes + [
    'kanji',
    'mecab'
]

generic_modeNames = [
    u'Manual: Space',
    u'Manual: Semicolon'
]

japanese_modeNames = generic_modeNames + [
    u'Auto: 漢字',
    u'Auto: Mecab'
]
