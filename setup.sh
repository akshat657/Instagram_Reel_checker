#!/bin/bash

echo "🚀 MedReel Analyzer Setup Script"
echo "================================="
echo ""

# Check Python version
echo "📌 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python $python_version found"
echo ""

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv venv
echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip
echo "✅ Pip upgraded"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Check FFmpeg
echo "🎵 Checking FFmpeg installation..."
if command -v ffmpeg &> /dev/null
then
    echo "✅ FFmpeg is installed: $(ffmpeg -version | head -n1)"
else
    echo "⚠️ FFmpeg is NOT installed!"
    echo "Please install FFmpeg:"
    echo "  - macOS: brew install ffmpeg"
    echo "  - Linux: sudo apt install ffmpeg"
    echo "  - Windows: choco install ffmpeg"
fi
echo ""

# Create .env file
echo "📝 Setting up environment variables..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ .env file created from template"
    echo "⚠️ Please edit .env and add your Groq API keys!"
else
    echo "✅ .env file already exists"
fi
echo ""

# Create data directories
echo "📁 Creating data directories..."
mkdir -p data/captions
mkdir -p data/transcripts
mkdir -p data/analyses
mkdir -p data/audio
echo "✅ Data directories created"
echo ""

echo "================================="
echo "✨ Setup Complete! ✨"
echo "================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your Groq API keys"
echo "   Get free keys from: https://console.groq.com/"
echo ""
echo "2. Run the app:"
echo "   source venv/bin/activate  # Activate virtual environment"
echo "   streamlit run app.py       # Start the app"
echo ""
echo "3. Open http://localhost:8501 in your browser"
echo ""
echo "Happy analyzing! 💊🎥"
