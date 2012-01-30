#!/usr/bin/python
#
# install plugin to anki addons folder

import os, sys, shutil

# Anki helpers

isMac = sys.platform.startswith("darwin")
isWin = sys.platform.startswith("windows")

# ripped from ankiqt/aqt/profiles.py
def ankiBase():
	if isWin:
		return os.path.expanduser("~\\Documents\\Anki")
	elif isMac:
		return os.path.expanduser("~/Documents/Anki")
	else:
		return os.path.expanduser("~/Anki")

# main

def main():
    # get the anki addon dir
    anki_addon_dir = os.path.join(ankiBase(), 'addons')
    # make our filepaths
    mcdsupport_py = os.path.join(anki_addon_dir, 'mcdsupport.py')
    mcd_dir = os.path.join(anki_addon_dir, 'mcd')
    # show status
    print 'Installing MCD Support Addon to', anki_addon_dir
    # do the uninstall
    if os.path.exists(mcdsupport_py):
        os.remove(mcdsupport_py)
    if os.path.exists(mcd_dir):
        shutil.rmtree(mcd_dir) 
    # do the install
    shutil.copy('mcdsupport.py', anki_addon_dir)
    shutil.copytree('mcd', mcd_dir)
    return

if __name__ == '__main__':
    main()
