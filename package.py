#!/usr/bin/env python3
# package the project

import os, shutil, subprocess

import mcd

files = [
    'mcdsupport.py',
    'mcd/__init__.py',
    'mcd/addmcds.py',
    'mcd/cloze.py',
    'mcd/menus.py',
    'mcd/models.py',
    'mcd/dlgAddMcds.py',
]

def makeDirectories(pkg_dir):
    os.mkdir( pkg_dir )
    os.mkdir( pkg_dir + '/mcd' )
    return

def copyFiles(pkg_dir):    
    for file in files:
        dst = pkg_dir + '/' + file
        shutil.copy( file, dst )
    return
    
def main():
    # build the directory/package name
    pkg_dir = 'mcdsupport-v' + mcd.version
    # create the directories and copy the files
    makeDirectories(pkg_dir)
    copyFiles(pkg_dir)
    # zip everything up
    cmd = 'cd '+pkg_dir+' ; zip -9r ../'+pkg_dir+'.zip .'
    print(cmd)
    subprocess.call( cmd, shell=True )
    # clean up
    shutil.rmtree( pkg_dir )
    
    return

if __name__ == '__main__':
    main()
