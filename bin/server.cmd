@echo off
call "%~dp0\..\tools\build\build.bat" server --wait-on-error "-p 7777" %*
