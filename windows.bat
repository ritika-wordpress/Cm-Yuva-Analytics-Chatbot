@echo off
title AI Analytics Project Starter

echo Starting Backend...
start cmd /k "cd /d %~dp0backend && pip install -r requirements.txt && uvicorn main:app --reload"

timeout /t 5 > nul

echo Starting Frontend...
start cmd /k "cd /d %~dp0frontend && streamlit run app.py"

echo Application started successfully.
pause