@echo off
title Push script to Gimp plugins folder, start Gimp

set pluginpath=C:\Users\VadShaytReth\.gimp-2.8\plug-ins
set pluginfile=scaleto.py
set gimpexe=gimp-2.8.exe

rem We should pause at this point, if Gimp is still open
rem http://stackoverflow.com/a/1329790/2014893
tasklist /FI "IMAGENAME eq %gimpexe%" 2>NUL | find /I /N "%gimpexe%">NUL
rem echo ERRORLEVEL: %ERRORLEVEL%
if %ERRORLEVEL%==1 goto notRunning
	echo .
	echo You should close Gimp so this works properly...
	echo (Press a button to ignore and continue...)
	pause

:notRunning

rem Catch any syntax problems (GIMP won't inform us)
echo Checking for syntax errors...
python -m py_compile %pluginfile%
rem echo ERRORLEVEL: %ERRORLEVEL%
if %ERRORLEVEL%==0 goto syntaxok
	echo Caught syntax errors; aborting
	pause
	exit
	
:syntaxok

echo Pushing script...
copy .\%pluginfile% %pluginpath%

rem Why did we need to set the 'workdir'?
rem echo Changing workdir...
rem cd C:\Users\RKB\

echo Starting Gimp...
start "" "C:\Program Files\GIMP 2\bin\gimp-2.8.exe"

rem cd "C:\Program Files\GIMP 2\bin\"
rem gimp-2.8.exe --verbose

pause
rem Would like to be able to pause if not running from 
rem the command line...

