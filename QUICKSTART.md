# 🚀 Quick Start Guide - For Complete Beginners

Welcome! This guide will help you get MedReel Analyzer running in **less than 15 minutes**, even if you've never coded before.

## 📋 What You'll Need

- [ ] A computer (Windows, Mac, or Linux)
- [ ] Internet connection
- [ ] 15 minutes of your time
- [ ] Coffee ☕ (optional but recommended)

## 🎯 Step-by-Step Setup

### Step 1: Install Python (5 minutes)

#### Windows:
1. Go to [python.org/downloads](https://python.org/downloads)
2. Click "Download Python 3.11" (or latest)
3. **IMPORTANT:** Check ☑️ "Add Python to PATH"
4. Click "Install Now"
5. Wait for installation

#### Mac:
```bash
# Open Terminal and paste:
brew install python@3.11
```
(If you don't have Homebrew, get it from [brew.sh](https://brew.sh))

#### Linux:
```bash
sudo apt update
sudo apt install python3.11 python3-pip
```

**Verify installation:**
```bash
python --version
# Should show: Python 3.11.x
```

### Step 2: Install Git (2 minutes)

#### Windows:
1. Go to [git-scm.com](https://git-scm.com)
2. Download and install
3. Use default settings

#### Mac:
```bash
brew install git
```

#### Linux:
```bash
sudo apt install git
```

**Verify:**
```bash
git --version
# Should show: git version 2.x.x
```

### Step 3: Install FFmpeg (3 minutes)

#### Windows:
```bash
# In PowerShell (as Admin):
choco install ffmpeg

# Don't have Chocolatey? Get it from:
# https://chocolatey.org/install
```

#### Mac:
```bash
brew install ffmpeg
```

#### Linux:
```bash
sudo apt update
sudo apt install ffmpeg
```

**Verify:**
```bash
ffmpeg -version
# Should show FFmpeg version info
```

### Step 4: Get Groq API Keys (5 minutes)

1. **Go to:** [console.groq.com](https://console.groq.com/)
2. **Sign up** with Google/GitHub (it's free!)
3. **Click:** "API Keys" in sidebar
4. **Click:** "Create API Key"
5. **Name it:** "MedReel-Key-1"
6. **Copy** the key (starts with `gsk_`)
7. **Repeat** steps 4-6 two more times for 3 total keys

**Save these keys in a notepad!** You'll need them soon.

### Step 5: Download the Project (2 minutes)

#### Option A: Download ZIP (Easiest)
1. Go to the GitHub repo
2. Click green "Code" button
3. Click "Download ZIP"
4. Extract to a folder (e.g., `C:\medreel` or `~/medreel`)

#### Option B: Clone with Git
```bash
# Open terminal/command prompt
git clone https://github.com/YOUR_USERNAME/medreel-analyzer.git
cd medreel-analyzer
```

### Step 6: Run Setup (1 minute)

Open terminal in the project folder:

#### Windows:
```bash
# Right-click in folder → "Open in Terminal"
# Then run:
setup.bat
```

#### Mac/Linux:
```bash
# Open Terminal in the folder
# Then run:
bash setup.sh
```

This will:
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Create `.env` file

### Step 7: Add API Keys (1 minute)

1. **Find** the `.env` file in your project folder
2. **Open** it with Notepad (Windows) or TextEdit (Mac)
3. **Replace** the placeholder text:

```env
GROQ_API_KEY_1=gsk_paste_your_first_key_here
GROQ_API_KEY_2=gsk_paste_your_second_key_here
GROQ_API_KEY_3=gsk_paste_your_third_key_here
```

4. **Save** the file

### Step 8: Run the App! (1 minute)

#### Windows:
```bash
run.bat
```

#### Mac/Linux:
```bash
bash run.sh
```

**The app will open at:** `http://localhost:8501` 🎉

## 🎨 First Use

### Analyze Your First Reel

1. **Find** an Instagram Reel with health advice
   - Example: `https://www.instagram.com/reel/DUV5eiCieMQ/`

2. **Copy** the URL

3. **Paste** in the app

4. **Select** language (Hindi or English)

5. **Click** "🔍 Analyze This Reel!"

6. **Wait** for magic to happen ✨

### What You'll Get

- 📝 **Caption** - The reel's text
- 📜 **Transcript** - What was said in the video
- 🔬 **Analysis** - AI fact-check with medical references
- 💬 **Chat** - Ask questions about the reel
- 📥 **Downloads** - Save all results

## 🐛 Something Went Wrong?

### "Python not found"
**Fix:** Reinstall Python and check "Add to PATH"

### "FFmpeg not found"
**Fix:** Follow Step 3 again carefully

### "pip not recognized"
**Fix:** 
```bash
python -m pip install --upgrade pip
```

### "Module not found"
**Fix:**
```bash
# In project folder:
pip install -r requirements.txt
```

### App won't start
**Fix:**
```bash
# Close all terminals
# Open new terminal
# Navigate to project folder
# Run: run.bat (Windows) or bash run.sh (Mac/Linux)
```

### "All API keys failed"
**Fix:** Check your `.env` file:
- Keys are correct (no typos)
- Keys start with `gsk_`
- No extra spaces
- File is saved

## 📚 Next Steps

### Want to Deploy Online?

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete guide to put your app on the internet!

### Want to Customize?

- **Colors:** Edit CSS in `app.py`
- **Features:** Add new functionality
- **Languages:** Add more language support

See [CONTRIBUTING.md](CONTRIBUTING.md) for tips.

### Want to Learn More?

- **Python:** [python.org/about/gettingstarted](https://python.org/about/gettingstarted/)
- **Streamlit:** [docs.streamlit.io](https://docs.streamlit.io)
- **Git:** [git-scm.com/doc](https://git-scm.com/doc)

## ✅ Checklist

Before asking for help, verify:

- [ ] Python 3.8+ installed
- [ ] Git installed
- [ ] FFmpeg installed
- [ ] Project downloaded/cloned
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] `.env` file created with valid API keys
- [ ] No typos in API keys

## 🆘 Still Stuck?

1. **Check FAQ:** [FAQ.md](FAQ.md)
2. **Search Issues:** [GitHub Issues](https://github.com/YOUR_USERNAME/medreel-analyzer/issues)
3. **Ask for Help:** Open a new issue with:
   - Your OS (Windows/Mac/Linux)
   - Python version
   - Error message (screenshot)
   - What you tried

## 🎉 Success!

If you see the app running:

1. ⭐ **Star** the GitHub repo
2. 📱 **Try** analyzing a reel
3. 🐦 **Share** on Twitter
4. 💜 **Enjoy** fact-checking health content!

## 🔥 Pro Tips

1. **Save API keys safely** - Don't share them!
2. **Use short reels** - Faster processing
3. **Try both languages** - See the difference
4. **Ask questions in chat** - Learn more about claims
5. **Download results** - Keep for reference

## 📞 Quick Links

- [Full Documentation](README.md)
- [Deployment Guide](DEPLOYMENT.md)
- [FAQ](FAQ.md)
- [Get Help](https://github.com/YOUR_USERNAME/medreel-analyzer/issues)

---

**Congratulations!** You're now running an AI-powered medical fact-checker! 🎊

Made with 💜 - Happy analyzing!
