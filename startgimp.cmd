@echo off
title Push script to Gimp plugins folder, start Gimp

set pluginpath=C:\Users\VadShaytReth\.gimp-2.8\plug-ins

rem We should pause at this point, if Gimp is still open
echo tasklist | find "gimp" >NUL 2>&1
rem echo %ERRORLEVEL%
if "%ERRORLEVEL%"=="1" goto notRunning
	echo .
	echo You should close Gimp so this works properly...
	echo (Press a button to ignore and continue...)
	pause

:notRunning

echo Pushing script...
copy .\scaleto.py %pluginpath%

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

