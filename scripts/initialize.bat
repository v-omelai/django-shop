@echo off

cd ..
powershell -Command "Start-Process 'python.exe' -ArgumentList '-m pip install --upgrade pip' -Verb runAs -Wait"
powershell -Command "Start-Process 'python.exe' -ArgumentList '-m venv venv' -Verb runAs -Wait"
powershell -NoExit -Command "& {Set-ExecutionPolicy -Scope Process Bypass -Force; .\venv\Scripts\Activate.ps1; pip install -r requirements.txt}"
