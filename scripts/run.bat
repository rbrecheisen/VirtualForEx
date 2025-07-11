@echo off

setlocal

set /p VERSION=<virtualforex\src\virtualforex\resources\VERSION

set START_DIR=%CD%

if /I "%~1"=="" (

    cd virtualforex
    call briefcase dev

) else if /I "%~1"=="--test" (

    cd virtualforex
    call briefcase dev --test

) else if /I "%~1"=="--exe" (

    cd virtualforex
    call briefcase run

) else if /I "%~1"=="--build" (

    rmdir /s /q virtualforex\build
    call python scripts\python\updatetomlversion.py %VERSION%
    call python scripts\python\updatetomlrequirements.py
    cd virtualforex
    call briefcase create
    call briefcase build

) else if /I "%~1"=="--package" (

    cd virtualforex
    call briefcase package --adhoc-sign
    
)

cd %START_DIR%


endlocal