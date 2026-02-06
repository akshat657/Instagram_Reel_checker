# 💊 MedReel Analyzer 🎥

A Gen-Z friendly Instagram Reel medical fact-checker that downloads, transcribes, and analyzes health content using AI.

## ✨ Features

- 📱 **Paste & Analyze**: Just drop an Instagram Reel URL
- 🎙️ **Multi-language Support**: Hindi & English transcription
- 🤖 **AI-Powered Analysis**: Uses Llama 3.3 70B for medical fact-checking
- 📚 **Medical References**: Pulls data from PubMed for scientific backing
- 💬 **Interactive Chat**: Ask questions about the analyzed reel
- 🎨 **Beautiful UI**: Dark/Light mode support with Gen-Z aesthetics
- 📥 **Download Everything**: Caption, transcript, and analysis
- 🔄 **Fallback System**: 3 Groq API keys for reliability

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- FFmpeg (for audio processing)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/medreel-analyzer.git
cd medreel-analyzer
```

2. **Create virtual environment**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Install FFmpeg**

**Windows:**
```bash
# Using Chocolatey
choco install ffmpeg

# Or download from https://ffmpeg.org/download.html
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

5. **Set up environment variables**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your Groq API keys
# Get free keys from: https://console.groq.com/
```

Your `.env` file should look like:
```env
GROQ_API_KEY_1=gsk_xxxxxxxxxxxxxxxxxxxxx
GROQ_API_KEY_2=gsk_xxxxxxxxxxxxxxxxxxxxx
GROQ_API_KEY_3=gsk_xxxxxxxxxxxxxxxxxxxxx
```

6. **Run the app**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 🌐 Deployment to Streamlit Cloud

### Step 1: Prepare Your Repository

1. Create a new GitHub repository
2. Push your code:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/medreel-analyzer.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository: `yourusername/medreel-analyzer`
5. Set:
   - **Branch**: `main`
   - **Main file path**: `app.py`
6. Click "Advanced settings"
7. Add your secrets (environment variables):
   ```toml
   GROQ_API_KEY_1 = "gsk_xxxxxxxxxxxxxxxxxxxxx"
   GROQ_API_KEY_2 = "gsk_xxxxxxxxxxxxxxxxxxxxx"
   GROQ_API_KEY_3 = "gsk_xxxxxxxxxxxxxxxxxxxxx"
   ```
8. Click "Deploy!"

### Step 3: System Dependencies

Create a `packages.txt` file in your repository root:
```bash
ffmpeg
```

This tells Streamlit Cloud to install FFmpeg automatically.

## 📁 Project Structure

```
medreel-analyzer/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── packages.txt          # System dependencies for Streamlit Cloud
├── README.md             # This file
│
└── data/                 # Auto-created directory
    ├── captions/         # Downloaded captions
    ├── transcripts/      # Generated transcripts
    ├── analyses/         # AI analyses
    └── audio/            # Temporary audio files
```

## 🔧 How It Works

### Data Flow:

1. **User Input**: Pastes Instagram Reel URL
2. **RapidAPI**: Fetches reel metadata and audio
3. **Speech Recognition**: Transcribes audio (Hindi/English)
4. **PubMed API**: Searches medical references
5. **Groq LLM**: Analyzes with Llama 3.3 70B
6. **Results**: Displays analysis in Gen-Z friendly format
7. **Chat**: Enables Q&A about the reel

### Data Storage:

- **During Session**: All files stored in temporary directory
- **After Session**: Files deleted automatically (privacy-first)
- **User Downloads**: Manual download option for all outputs
- **No Database**: Completely stateless (no user data stored)

### API Key Fallback:

```
Key 1 Fails → Try Key 2 → Try Key 3 → Error
```

## 🎨 UI Features

- **No Sidebar**: Clean, focused interface
- **Gradient Titles**: Eye-catching headers
- **Responsive Design**: Works on all devices
- **Dark/Light Mode**: Automatic theme switching
- **Emoji Support**: Gen-Z friendly aesthetics
- **Progress Indicators**: Real-time processing updates
- **Download Buttons**: Easy export of all data

## 🔒 Privacy & Security

- ✅ No data stored on server
- ✅ Temporary files deleted after processing
- ✅ Environment variables for API keys
- ✅ No user tracking
- ✅ Open source

## 🐛 Troubleshooting

### FFmpeg not found
```bash
# Verify installation
ffmpeg -version

# If not found, install as per your OS instructions above
```

### Transcription fails
- Check internet connection
- Ensure audio is clear
- Try different language setting

### API rate limits
- App automatically switches between 3 API keys
- Get more free keys from Groq Console

### Streamlit Cloud deployment fails
- Check `packages.txt` includes `ffmpeg`
- Verify all secrets are added correctly
- Check repository is public or you have access

## 📝 Getting Groq API Keys

1. Go to [console.groq.com](https://console.groq.com/)
2. Sign up/Login (free)
3. Navigate to "API Keys"
4. Click "Create API Key"
5. Copy and paste into `.env` file
6. Repeat 2 more times for fallback keys

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

MIT License - feel free to use this project however you want!

## ⚠️ Disclaimer

This tool is for educational purposes only. Always consult healthcare professionals for medical advice. The AI analysis is not a substitute for professional medical consultation.

## 🙏 Credits

- **Groq**: For amazing LLM API
- **Streamlit**: For the awesome framework
- **RapidAPI**: For Instagram data access
- **PubMed**: For medical references
- **You**: For using this tool! 💜

## 📧 Support

Found a bug? Have a suggestion?
- Open an issue on GitHub
- Star ⭐ the repo if you find it useful!

---

Made with 💜 by the MedReel Analyzer team
