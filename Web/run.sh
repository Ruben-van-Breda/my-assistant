#!/bin/zsh
# Run the Flask app in development mode
export FLASK_APP=app/app.py
export FLASK_ENV=development
flask run
