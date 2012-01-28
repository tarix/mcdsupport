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
        cmd = exe+' mcd\\'+form+'.ui 1> mcd\\'+form+'.py'
        subprocess.call( cmd )
    return

if __name__ == '__main__':
    main()
