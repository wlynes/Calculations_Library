%echo off
set folder="C:\Users\wlynes\Desktop\temp prints"
cd /d %folder%
for /F "delims=" %%i in ('dir /b') do (rmdir "%%i" /s/q || del "%%i" /s/q)
