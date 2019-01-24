#!/usr/bin/python
#
# ui build script

import os
import subprocess

forms = [
    'dlgAddMcds'
]

pyuic = { 
    'posix': 'pyuic5',
    'nt': 'pyuic5.bat'
}

def main():
    exe = pyuic[ os.name ]
    for form in forms:
        print 'Building '+form+' ...'
        iform_path = os.path.join('ui',    form+'.ui')
        oform_path = os.path.join('addon', form+'.py')
        cmd = exe+' '+iform_path+' 1> '+oform_path
        subprocess.call( cmd, shell=True )
    return

if __name__ == '__main__':
    main()
