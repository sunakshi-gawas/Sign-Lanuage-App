#!/bin/bash
# Activate the virtual environment and run the server
source venv_infer/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
