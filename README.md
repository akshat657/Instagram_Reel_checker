
# 💊 MedReel Analyzer 🎥

MedReel Analyzer is an AI web app that downloads, transcribes, and fact-checks Instagram Reels containing health advice.  
Paste a Reel link → get transcript → AI verifies claims using medical research → receive a simple, Gen-Z friendly verdict.

---

## 🧠 Tech Stack
**Frontend:** Streamlit  
**Backend:** Python  
**AI:** Groq (Llama 3.3 70B),SpeechRecognition  
**APIs:** RapidAPI (Instagram), PubMed (medical papers)  
**Tools:** FFmpeg, LangChain utilities  
**Languages:** Hindi + English transcription

---

## ✨ Key Features
- Paste Instagram Reel URL and analyze instantly
- Automatic audio extraction + transcription
- AI medical fact-checking with scientific references
- Interactive chat for follow-up questions
- Download transcripts and analysis
- Dark/Light responsive UI
- Auto API-key fallback for reliability

---

## 🚀 Run Locally

```bash
git clone https://github.com/yourusername/medreel-analyzer.git
cd medreel-analyzer

python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

pip install -r requirements.txt
````

Install FFmpeg:

* Windows → `choco install ffmpeg`
* Mac → `brew install ffmpeg`
* Linux → `sudo apt install ffmpeg`

Create `.env` and add Groq API key:

```
GROQ_API_KEY=your_key_here
```

Run app:

```bash
streamlit run app.py
```

Open → [http://localhost:8501](http://localhost:8501)

---

## 🌐 Deploy (Streamlit Cloud)

1. Push repo to GitHub
2. Go to [https://share.streamlit.io](https://share.streamlit.io)
3. Select repo → `app.py`
4. Add secrets (API keys)
5. Add `packages.txt` containing:

```
ffmpeg
```

---

## 🔒 Privacy

No permanent storage. Temporary files auto-deleted. No tracking.

---

## ⚠️ Disclaimer

Educational tool only. Not medical advice.

---

Made with 💜 using GenAI + LLM pipelines

```
```
