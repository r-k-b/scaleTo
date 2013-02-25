@echo off
title Push script to Gimp plugins folder, start Gimp

rem We should pause at this point, if Gimp is still open
tasklist | find "gimp"
if "%ERRORLEVEL%"=="0" goto notRunning
	echo "You should close Gimp so this works properly..."
	pause

:notRunning

echo Pushing script...
copy .\scaleto.py C:\Users\RKB\.gimp-2.8\plug-ins\

echo Changing workdir...
cd C:\Users\RKB\

echo Starting Gimp...
start "C:\Program Files\GIMP 2\bin\gimp-2.8.exe"

echo Did it work?
pause