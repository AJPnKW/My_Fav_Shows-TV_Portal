@echo off
setlocal EnableDelayedExpansion

:: Set variables
set LOG_FILE=logs\app_start_%date:~10,4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log
set APP_DIR=%~dp0
set PYTHON_EXE=C:\Users\Lenovo\scoop\apps\inkscape\1.3.2_2023-11-25_091e20e\bin\python.exe
set APP_FILE=%APP_DIR%app.py

:: Create logs directory if it doesn't exist
if not exist "%APP_DIR%logs" mkdir "%APP_DIR%logs"

:: Log start time
echo Starting MY_Fav_Shows-TV_Portal at %date% %time% > "%LOG_FILE%"
echo Launching from: %APP_DIR% >> "%LOG_FILE%"
echo Using Python: %PYTHON_EXE% >> "%LOG_FILE%"

:: Launch Streamlit app
cd /d "%APP_DIR%"
"%PYTHON_EXE%" -m streamlit run "%APP_FILE%" >> "%LOG_FILE%" 2>&1

:: Wait for user input to close
echo.
echo Press Enter to close the console...
set /p input=
