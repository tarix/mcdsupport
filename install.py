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
        loc = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
        # the returned value seem to automatically include the app name, but we use Anki2 rather
        # than Anki
        assert loc.endswith("/Anki")
        loc += "2"
        return loc
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
