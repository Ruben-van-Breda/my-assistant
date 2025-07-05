#!/bin/bash
export FLASK_APP=service.py
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=5001
flask run