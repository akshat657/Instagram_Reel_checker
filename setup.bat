@echo off
echo ========================================
echo 🚀 MedReel Analyzer Setup Script
echo ========================================
echo.

:: Check Python version
echo 📌 Checking Python version...
python --version
echo.

:: Create virtual environment
echo 🔧 Creating virtual environment...
python -m venv venv
echo ✅ Virtual environment created
echo.

:: Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat
echo ✅ Virtual environment activated
echo.

:: Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip
echo ✅ Pip upgraded
echo.

:: Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt
echo ✅ Dependencies installed
echo.

:: Check FFmpeg
echo 🎵 Checking FFmpeg installation...
where ffmpeg >nul 2>nul
if %errorlevel% equ 0 (
    echo ✅ FFmpeg is installed
    ffmpeg -version | findstr "version"
) else (
    echo ⚠️ FFmpeg is NOT installed!
    echo Please install FFmpeg:
    echo   - Using Chocolatey: choco install ffmpeg
    echo   - Or download from: https://ffmpeg.org/download.html
)
echo.

:: Create .env file
echo 📝 Setting up environment variables...
if not exist .env (
    copy .env.example .env
    echo ✅ .env file created from template
    echo ⚠️ Please edit .env and add your Groq API keys!
) else (
    echo ✅ .env file already exists
)
echo.

:: Create data directories
echo 📁 Creating data directories...
if not exist data mkdir data
if not exist data\captions mkdir data\captions
if not exist data\transcripts mkdir data\transcripts
if not exist data\analyses mkdir data\analyses
if not exist data\audio mkdir data\audio
echo ✅ Data directories created
echo.

echo ========================================
echo ✨ Setup Complete! ✨
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file and add your Groq API keys
echo    Get free keys from: https://console.groq.com/
echo.
echo 2. Run the app:
echo    venv\Scripts\activate     # Activate virtual environment
echo    streamlit run app.py       # Start the app
echo.
echo 3. Open http://localhost:8501 in your browser
echo.
echo Happy analyzing! 💊🎥
echo.
pause
