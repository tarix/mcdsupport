#!/usr/bin/python
#
# ui build script

import os
import subprocess

forms = [
    'dlgAddMcds'
]

pyuic = { 
    'posix': 'pyuic4',
    'nt': 'pyuic4.bat'
}

def main():
    exe = pyuic[ os.name ]
    for form in forms:
        print 'Building '+form+' ...'
        form_path = os.path.join('mcd', form)
        cmd = exe+' '+form_path+'.ui 1> '+form_path+'.py'
        subprocess.call( cmd, shell=True )
    return

if __name__ == '__main__':
    main()
