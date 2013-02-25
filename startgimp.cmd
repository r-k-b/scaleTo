@echo off
title Push script to Gimp plugins folder, start Gimp

rem We should pause at this point, if Gimp is still open
echo tasklist | find "gimp" >NUL 2>&1
rem echo %ERRORLEVEL%
if "%ERRORLEVEL%"=="1" goto notRunning
	echo .
	echo You should close Gimp so this works properly...
	pause

:notRunning

echo Pushing script...
copy .\scaleto.py C:\Users\RKB\.gimp-2.8\plug-ins\

echo Changing workdir...
cd C:\Users\RKB\

echo Starting Gimp...
start "" "C:\Program Files\GIMP 2\bin\gimp-2.8.exe"

rem echo Did it work?
rem pause