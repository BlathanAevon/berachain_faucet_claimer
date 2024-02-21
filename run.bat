@echo off
if exist ".\venv" (
    echo Venv is already created, running script...
) else (
    echo Creating virtual environment...
    python -m venv venv
)

if "%OS%"=="Windows_NT" (
    call venv\Scripts\activate
) else (
    call venv/bin/activate
)

echo Installing requirements...
pip install -q -r requirements.txt
echo Requirements installed!

python main.py
