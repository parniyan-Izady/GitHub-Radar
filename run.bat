@echo off
title GitHub Relationship Radar
echo Starting GitHub Radar local server...
start "" "http://localhost:8000"
where py >nul 2>nul && (py server.py) || (python server.py)
pause
