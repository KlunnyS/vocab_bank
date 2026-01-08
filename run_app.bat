@echo off
echo =====================
echo Running flask program
echo =====================

:: .venv check
if not exist ".venv" (
    echo Making virtual enviroment
    py -3 -m venv .venv
)

:: run .venv
echo Running virtual enviroment
call .venv\Scripts\activate

:: flask check

python -m pip show flask >null 2>&1 || pip install flask
python -m pip show flask-wtf >null 2>&1 || pip install flask-wtf
python -m pip show flask-sqlalchemy >null 2>&1 || pip install flask-sqlalchemy


:: run app
echo Running flask app
flask --app main run --host=0.0.0.0 --port=5000 --debug


:: exiting
echo Closing server
deactivate

echo.
echo ---------------
echo Server closed

pause