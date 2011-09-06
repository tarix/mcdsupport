@ECHO OFF
MKDIR %APPDATA%\.anki\plugins\mcd 2> NUL
COPY /V /Y mcdsupport.py %APPDATA%\.anki\plugins\ > NUL
COPY /V /Y mcd %APPDATA%\.anki\plugins\mcd\ > NUL
