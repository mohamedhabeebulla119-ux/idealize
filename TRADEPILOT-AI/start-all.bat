@echo off
REM TradePilot AI - Start All Services (Windows)

echo.
echo ========================================
echo   TradePilot AI - Full Stack Startup
echo ========================================
echo.

REM Check if .venv exists
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install backend requirements
echo.
echo Installing backend dependencies...
pip install -r requirements.txt -q
pip install python-multipart -q

REM Start backend in a new window
echo.
echo Starting backend server on port 8000...
start cmd /k "cd backend && python -m uvicorn main:app --reload --port 8000"

REM Wait a moment for backend to start
timeout /t 3 /nobreak

REM Start frontend in a new window
echo Starting frontend server on port 5173...
cd frontend
start cmd /k "npm install --silent && npm run dev"

echo.
echo ========================================
echo   Services Started!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C in each window to stop services
echo.

pause
