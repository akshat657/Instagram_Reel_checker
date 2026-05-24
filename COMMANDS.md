# 🖥️ Useful Commands Reference

Quick reference for all commands you might need.

## 📦 Initial Setup

### Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/medreel-analyzer.git
cd medreel-analyzer
```

### Create Virtual Environment
```bash
# Windows
python -m venv venv

# Mac/Linux
python3 -m venv venv
```

### Activate Virtual Environment
```bash
# Windows (Command Prompt)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Mac/Linux
source venv/bin/activate
```

### Deactivate Virtual Environment
```bash
deactivate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Upgrade Pip
```bash
python -m pip install --upgrade pip
```

## 🚀 Running the App

### Start App (Manual)
```bash
streamlit run app.py
```

### Start App (Script)
```bash
# Windows
run.bat

# Mac/Linux
bash run.sh
```

### Start on Different Port
```bash
streamlit run app.py --server.port 8502
```

### Start in Browser
```bash
streamlit run app.py --browser.gatherUsageStats false
```

## 🔧 Development Commands

### Check Python Version
```bash
python --version
```

### Check Pip Version
```bash
pip --version
```

### Check FFmpeg
```bash
ffmpeg -version
```

### List Installed Packages
```bash
pip list
```

### Check for Outdated Packages
```bash
pip list --outdated
```

### Update a Package
```bash
pip install --upgrade package_name
```

### Freeze Requirements
```bash
pip freeze > requirements.txt
```

## 🐛 Debugging

### Check Streamlit Version
```bash
streamlit --version
```

### Clear Streamlit Cache
```bash
streamlit cache clear
```

### Run with Verbose Logging
```bash
streamlit run app.py --logger.level=debug
```

### Check for Python Errors
```bash
python app.py
# (This won't run the app but will show syntax errors)
```

## 📁 File Operations

### View Current Directory
```bash
# Windows
dir

# Mac/Linux
ls -la
```

### Navigate Directories
```bash
cd folder_name
cd ..  # Go up one level
cd ~   # Go to home directory
```

### Create Directory
```bash
mkdir folder_name
```

### Delete File
```bash
# Windows
del filename

# Mac/Linux
rm filename
```

### Copy File
```bash
# Windows
copy source destination

# Mac/Linux
cp source destination
```

### View File Contents
```bash
# Windows
type filename

# Mac/Linux
cat filename
```

## 🔍 Git Commands

### Check Git Status
```bash
git status
```

### Add Files
```bash
git add .                # Add all files
git add filename         # Add specific file
```

### Commit Changes
```bash
git commit -m "Your commit message"
```

### Push to GitHub
```bash
git push origin main
```

### Pull Latest Changes
```bash
git pull origin main
```

### Create New Branch
```bash
git checkout -b feature-name
```

### Switch Branch
```bash
git checkout main
```

### View Commit History
```bash
git log
git log --oneline  # Compact view
```

### Undo Last Commit (Keep Changes)
```bash
git reset --soft HEAD~1
```

### Undo All Changes
```bash
git reset --hard HEAD
```

### View Remote URL
```bash
git remote -v
```

## 🔐 Environment Variables

### Create .env File
```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

### View .env File
```bash
# Windows
type .env

# Mac/Linux
cat .env
```

### Edit .env File
```bash
# Windows
notepad .env

# Mac/Linux
nano .env
# or
vim .env
```

## 🧪 Testing

### Run App Locally
```bash
streamlit run app.py
```

### Test Specific Port
```bash
streamlit run app.py --server.port 8080
```

### Run in Headless Mode
```bash
streamlit run app.py --server.headless true
```

## 🌐 Network & Port

### Check Port Usage (Windows)
```bash
netstat -ano | findstr :8501
```

### Check Port Usage (Mac/Linux)
```bash
lsof -i :8501
```

### Kill Process on Port (Windows)
```bash
# Find PID first with netstat
taskkill /PID <PID> /F
```

### Kill Process on Port (Mac/Linux)
```bash
kill -9 $(lsof -t -i:8501)
```

## 📦 Package Management

### Install Specific Version
```bash
pip install package_name==1.2.3
```

### Uninstall Package
```bash
pip uninstall package_name
```

### Install from requirements.txt
```bash
pip install -r requirements.txt
```

### Create requirements.txt
```bash
pip freeze > requirements.txt
```

## 🔄 Streamlit Specific

### Config File Location
```bash
streamlit config show
```

### Open Streamlit Docs
```bash
streamlit docs
```

### Create New Streamlit App
```bash
streamlit hello
```

## 💾 Data Management

### Create Data Directories
```bash
mkdir -p data/captions data/transcripts data/analyses data/audio
```

### Remove All Temp Files
```bash
# Windows
del /q temp_chunk_*.wav

# Mac/Linux
rm -f temp_chunk_*.wav
```

### Clear All Data
```bash
# Windows
rmdir /s /q data

# Mac/Linux
rm -rf data
```

## 🐳 Docker (Optional)

### Build Docker Image
```bash
docker build -t medreel-analyzer .
```

### Run Docker Container
```bash
docker run -p 8501:8501 medreel-analyzer
```

### Stop Container
```bash
docker stop <container_id>
```

## 📊 Monitoring

### View Streamlit Logs
```bash
# Logs are in terminal where you ran streamlit
```

### Monitor File Changes
```bash
# Windows
dir /o:d

# Mac/Linux
ls -lt
```

### Check Disk Space
```bash
# Windows
dir

# Mac/Linux
df -h
```

## 🔧 Troubleshooting

### Reinstall Everything
```bash
# Delete venv
rm -rf venv  # or rmdir /s /q venv on Windows

# Recreate
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt
```

### Clear Python Cache
```bash
# Mac/Linux
find . -type d -name __pycache__ -exec rm -rf {} +

# Windows
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"
```

### Reset Git Repository
```bash
# CAREFUL: This deletes all local changes
git reset --hard origin/main
```

## 🚀 Deployment

### Push to GitHub
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Create GitHub Release
```bash
git tag -a v1.0.0 -m "First release"
git push origin v1.0.0
```

## 💡 Productivity

### One Command Setup
```bash
# Windows
setup.bat

# Mac/Linux
bash setup.sh
```

### One Command Run
```bash
# Windows
run.bat

# Mac/Linux
bash run.sh
```

### Update and Run
```bash
git pull && pip install -r requirements.txt && streamlit run app.py
```

## 🆘 Emergency Commands

### Kill All Python Processes
```bash
# Windows
taskkill /F /IM python.exe

# Mac/Linux
pkill -9 python
```

### Force Delete Directory
```bash
# Windows
rmdir /s /q folder_name

# Mac/Linux
rm -rf folder_name
```

### Reset Everything
```bash
# Delete venv, cache, temp files
# Then run setup again
```

## 📚 Learning Commands

### Python Interactive Shell
```bash
python
>>> import streamlit as st
>>> st.__version__
```

### Check Module Installation
```bash
python -c "import streamlit; print(streamlit.__version__)"
```

### Test Groq Connection
```bash
python -c "from groq import Groq; print('Groq imported successfully')"
```

## 🔍 Search Commands

### Find Files
```bash
# Windows
dir /s filename

# Mac/Linux
find . -name "filename"
```

### Search in Files
```bash
# Mac/Linux
grep -r "search_term" .

# Windows
findstr /s /i "search_term" *.*
```

## 📝 Quick Edits

### Edit File Quickly
```bash
# Windows
notepad app.py

# Mac
open -a TextEdit app.py

# Linux
nano app.py
```

## 🎯 Shortcuts

### Streamlit Keyboard Shortcuts
- `R` - Rerun the app
- `C` - Clear cache
- `⌘/Ctrl + /` - Command palette

### Terminal Shortcuts
- `Ctrl + C` - Stop running process
- `Ctrl + D` - Exit terminal
- `↑ / ↓` - Navigate command history
- `Tab` - Autocomplete

## 📖 Documentation Commands

### Open Browser to Docs
```bash
# Streamlit
open https://docs.streamlit.io

# Groq
open https://console.groq.com/docs
```

## 🎉 Celebration Commands

### After Successful Deployment
```bash
echo "🎉 Deployment successful!"
# or
figlet "Success!"
```

---

## 💾 Save This File

Bookmark this page or save these commands for quick reference!

## 🆘 Need Help?

- Check [FAQ.md](FAQ.md)
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Open GitHub Issue

---

Made with 💜 - Happy coding!
