#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════╗"
echo "║   💊 MedReel Analyzer Runner 🎥   ║"
echo "╔════════════════════════════════════╗"
echo -e "${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Virtual environment not found!${NC}"
    echo -e "${BLUE}📌 Please run setup.sh first:${NC}"
    echo "   bash setup.sh"
    exit 1
fi

# Activate virtual environment
echo -e "${GREEN}🔌 Activating virtual environment...${NC}"
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ .env file not found!${NC}"
    echo -e "${BLUE}📌 Please create .env file:${NC}"
    echo "   cp .env.example .env"
    echo "   Then add your Groq API keys"
    exit 1
fi

# Check FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo -e "${RED}⚠️  FFmpeg not found!${NC}"
    echo -e "${BLUE}📌 Install FFmpeg:${NC}"
    echo "   macOS: brew install ffmpeg"
    echo "   Linux: sudo apt install ffmpeg"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Run the app
echo ""
echo -e "${GREEN}🚀 Starting MedReel Analyzer...${NC}"
echo -e "${BLUE}📍 App will open at: http://localhost:8501${NC}"
echo ""
echo -e "${BLUE}Press Ctrl+C to stop the server${NC}"
echo ""

streamlit run app.py
