@ECHO OFF
setlocal
set PYTHONPATH=%PYTHONPATH%;lib
python unit/test/manhill/all.py
endlocal
pause