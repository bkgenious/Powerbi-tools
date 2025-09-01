@echo off
setlocal

echo Creating virtual environment if it doesn't exist...
if not exist venv (
    python -m venv venv
)

echo Activating virtual environment...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment activation script not found!
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

echo Upgrading pip and installing dependencies...
python -m pip install --upgrade pip setuptools wheel
pip install waitress flask torch transformers pandas numpy scikit-learn python-dotenv flask-sqlalchemy flask-login flask-cors PyJWT plotly
pip install -r requirements.txt --no-warn-script-location

echo Starting the application...
python run.py

if errorlevel 1 (
    echo Error starting the application. Check the error message above.
    pause
    exit /b 1
)

pause
