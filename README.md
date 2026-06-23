# 💊 MedReel Analyzer 🎥

**Stop the Cap. Fact-check the Reel.**

MedReel Analyzer is an AI-powered web application that downloads, transcribes, and fact-checks Instagram Reels containing health advice. Paste a Reel link → get transcript → AI verifies claims using medical research → receive evidence-backed analysis with citations.

**Live Demo:** [https://medreel-nine.vercel.app/](https://medreel-nine.vercel.app/)

---

## 🧠 Tech Stack

**Frontend:** React + Vite + Tailwind CSS  
**Backend:** FastAPI + Python  
**AI:** Groq (Llama 3.3 70B) for analysis, Google Speech Recognition for transcription  
**APIs:** RapidAPI (Instagram), PubMed + PMC + Europe PMC (research papers)  
**Deployment:** Vercel (frontend) + Render (backend)  
**Tools:** FFmpeg, ThreadPoolExecutor (parallel API calls)  
**Languages:** Hindi + English transcription (manual selection)

---

## ✨ Key Features

- 🎨 **Beautiful dual-theme UI** (Cyber-Medical dark + Clinical Luminance light)
- 📱 **Single Page Application** with smooth transitions
- 🎤 **Audio transcription** with manual language selection (English/Hindi)
- 🔬 **AI medical fact-checking** with 8-10 scientific citations
- 📚 **Inline citations [1][2]** from PubMed, PMC, and Europe PMC
- 🔗 **Clickable research paper links** with abstract previews
- 💬 **Interactive chat** for follow-up questions
- 📥 **Download** transcripts and analysis as text files
- 🌓 **Dark/Light theme** toggle with glassmorphism effects
- 🔄 **Auto API-key fallback** for reliability (3 Groq keys)
- ⏰ **Auto-deploy** with GitHub Actions cron job (keeps backend awake)

---

## 📚 Research Citations

MedReel Analyzer backs every analysis with real scientific research:

- Fetches **8-10 papers** from trusted medical databases
- Sources: **PubMed**, **PubMed Central (PMC)**, **Europe PMC**
- AI cites papers inline using **[1][2]** format
- Every citation is **clickable** with full paper details
- Completely **free** APIs with generous limits

**Example:** "Studies show curcumin reduces inflammation [1][2], but absorption is poor without piperine [3]."

---

## 🚀 Run Locally

### Prerequisites

- Python 3.10+
- Node.js 18+
- FFmpeg

### Backend Setup

```bash
# Clone repository
git clone https://github.com/akshat657/Instagram_Reel_checker.git
cd Instagram_Reel_checker

# Create virtual environment
python -m venv venv3
source venv3/bin/activate   # Mac/Linux
venv3\Scripts\activate      # Windows

# Install Python dependencies
pip install -r backend/requirements.txt

# Create .env file with API keys
echo "GROQ_API_KEY_1=your_first_key" >> .env
echo "GROQ_API_KEY_2=your_second_key" >> .env
echo "GROQ_API_KEY_3=your_third_key" >> .env
echo "RAPIDAPI_KEY=your_rapidapi_key" >> .env

# Run backend server
python run_backend.py
```

Backend will start at: **http://localhost:8000**

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will start at: **http://localhost:5173**

---

## 🌐 Deployment

### Architecture

- **Frontend**: Deployed on Vercel (https://medreel-nine.vercel.app/)
- **Backend**: Deployed on Render (https://medreel-backend.onrender.com)
- **Cron Job**: GitHub Actions pings backend every 10 minutes (prevents Render free tier sleep)

### Deploy Your Own

#### Backend (Render)

1. Push code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Create new **Blueprint** → Connect GitHub repo
4. Add environment variables:
   - `GROQ_API_KEY_1`, `GROQ_API_KEY_2`, `GROQ_API_KEY_3`
   - `RAPIDAPI_KEY`
5. Deploy!

#### Frontend (Vercel)

1. Go to [Vercel](https://vercel.com/new)
2. Import GitHub repo
3. Set **Root Directory**: `frontend`
4. Set **Framework**: Vite
5. Add environment variable:
   - `VITE_API_URL=https://your-backend.onrender.com`
6. Deploy!

#### Enable Cron Job

1. GitHub repo → **Actions** tab
2. Enable workflows
3. "Keep Backend Awake" will run every 10 minutes

**Full deployment guide:** See [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 🎨 Design

Built with Google Stitch-inspired design systems:

- **Cyber-Medical Interface** (Dark Theme)
  - Futuristic, Gen-Z aesthetic
  - Cyan/purple accent colors
  - Glassmorphism effects
  
- **Clinical Luminance** (Light Theme)
  - Professional, sterile aesthetic
  - Blue accent colors
  - Medical-grade clarity

---

## 🔒 Privacy

- No permanent storage
- Temporary audio files auto-deleted after analysis
- No user tracking or analytics
- API keys stored securely in environment variables

---

## ⚠️ Disclaimer

**Educational tool only. Not medical advice.**  
Always consult qualified healthcare professionals for medical decisions.

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

---

## 👨‍💻 Developer

**Developed by Akshat Khandelwal**

- 🔗 [LinkedIn](https://www.linkedin.com/in/akshat-khandelwal-79647a245/)
- 💻 [GitHub](https://github.com/akshat657)

---

## 🙏 Acknowledgments

- **Groq** for fast LLM inference
- **PubMed, PMC, Europe PMC** for free research APIs
- **Google Stitch** for design inspiration
- **Vercel** and **Render** for free hosting

---

**Made with 💜 using GenAI + LLM pipelines**

Medical misinformation spreads 6x faster than truth. Let's change that. 🚀
