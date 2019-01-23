#!/usr/bin/python
#
# install plugin to anki addons folder

import os, sys, shutil

# Anki helpers

isMac = sys.platform.startswith("darwin")
isWin = sys.platform.startswith("win32")

# ripped from https://github.com/dae/anki/blob/master/aqt/profiles.py
def ankiBase():
    if isWin:
        return os.path.join(os.getenv('APPDATA'), "Anki2")
    elif isMac:
        return os.path.expanduser("~/Library/Application Support/Anki2")
    else:
        dataDir = os.environ.get(
            "XDG_DATA_HOME", os.path.expanduser("~/.local/share"))
        if not os.path.exists(dataDir):
            os.makedirs(dataDir)
        return os.path.join(dataDir, "Anki2")

# main

def main():
    # get the anki addon dir
    anki_addon_dir = os.path.join(ankiBase(), 'addons21')
    # make our filepaths
    mcdsupport_dir = os.path.join(anki_addon_dir, 'mcdsupport')
    # show status
    print 'Installing MCD Support Addon to', mcdsupport_dir
    # do the uninstall
    if os.path.exists(mcdsupport_dir):
        shutil.rmtree(mcdsupport_dir) 
    # do the install
    shutil.copytree('addon', mcdsupport_dir)
    return

if __name__ == '__main__':
    main()
