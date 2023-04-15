@echo off
Start Flask Server
echo Start flask server
CALL venv\Scripts\activate
cd app
python api.py
pause