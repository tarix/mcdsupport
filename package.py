# package the project

import os
import shutil

import mcd

files = [
    'mcdsupport.py',
    'mcd\\__init__.py',
    'mcd\\dlgAddMcd.py',
    'mcd\\dlgConfigure.py',
    'mcd\\mcdCloze.py',
    'mcd\\mcdMecab.py',
    'mcd\\mcdOptions.py',
    'mcd\\mcdUI.py',
    'mcd\\modelGEN.py',
    'mcd\\modelJP.py',
]

def makeDirectories(pkg_dir):
    os.mkdir( pkg_dir )
    os.mkdir( pkg_dir + '\\mcd' )
    return

def copyFiles(pkg_dir):    
    for file in files:
        dst = pkg_dir + '\\' + file
        shutil.copy( file, dst )
    return
    
def main():
    pkg_dir = 'mcdsupport-v' + mcd.version
    makeDirectories(pkg_dir)
    copyFiles(pkg_dir)
    return

if __name__ == '__main__':
    main()
