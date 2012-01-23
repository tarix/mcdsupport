@ECHO OFF
SET ANKI_ADDON_DIR=%USERPROFILE%\Documents\Anki\addons
ECHO Installing MCD Support Addon to %ANKI_ADDON_DIR%
MKDIR %ANKI_ADDON_DIR%\mcd 2> NUL
COPY /V /Y mcdsupport.py %ANKI_ADDON_DIR%\ > NUL
COPY /V /Y mcd %ANKI_ADDON_DIR%\mcd\ > NUL
