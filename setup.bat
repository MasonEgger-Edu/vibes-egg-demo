@echo off

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install the package in development mode
pip install -e .

echo Setup complete! To activate the virtual environment, run: venv\Scripts\activate.bat 