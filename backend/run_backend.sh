#!/bin/bash
# Activate the virtual environment and run the server from the backend directory
cd "$(dirname "$0")"
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
