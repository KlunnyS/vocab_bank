#!/usr/bin/env bash

echo "====================="
echo "Running flask program"
echo "====================="

# .venv check
if [ ! -d ".venv" ]; then
    echo "Making virtual environment"
    python3 -m venv .venv
fi

# run .venv
echo "Running virtual environment"
source .venv/bin/activate

# flask check
python -m pip show flask >/dev/null 2>&1 || pip install flask
python -m pip show flask-wtf >/dev/null 2>&1 || pip install flask-wtf
python -m pip show flask-sqlalchemy >/dev/null 2>&1 || pip install flask-sqlalchemy

# run app
echo "Running flask app"
flask --app main run --debug

# exiting
echo "Closing server"
deactivate

echo
echo "---------------"
echo "Server closed"

read -p "Press Enter to continue..."
