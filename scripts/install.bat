@echo off

setlocal

if /I "%~1"=="--upgrade" (
    python -m pip install --upgrade -r requirements-windows.txt
) else (
    python -m pip install -r requirements-windows.txt
)

endlocal