# ❓ Frequently Asked Questions (FAQ)

## 📱 General Questions

### What is MedReel Analyzer?
MedReel Analyzer is an AI-powered tool that analyzes health-related Instagram Reels for medical accuracy. It downloads the reel, transcribes it, and uses advanced AI to fact-check the claims made in the video.

### Is it free to use?
Yes! The app is completely free. However, you'll need:
- Free Groq API keys (get from console.groq.com)
- The RapidAPI key in the code (or get your own)

### What languages are supported?
Currently:
- **Hindi** (हिंदी in Devanagari script)
- **English**

More languages coming soon!

### Is this medical advice?
**No!** This tool is for educational purposes only. Always consult qualified healthcare professionals for medical advice.

## 🔧 Setup & Installation

### How do I get Groq API keys?
1. Go to [console.groq.com](https://console.groq.com/)
2. Sign up (it's free!)
3. Go to "API Keys"
4. Create 3 keys (for fallback)
5. Add them to your `.env` file

### Why do I need 3 API keys?
For reliability! If one key hits rate limits, the app automatically switches to the next one. This ensures uninterrupted service.

### How do I install FFmpeg?

**Windows:**
```bash
choco install ffmpeg
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

### I get "FFmpeg not found" error
Make sure FFmpeg is installed and in your system PATH. Verify with:
```bash
ffmpeg -version
```

### Setup fails on Windows
Common issues:
1. **Python not in PATH**: Reinstall Python and check "Add to PATH"
2. **Permission issues**: Run terminal as Administrator
3. **Long path names**: Move project to C:\medreel

## 🎯 Using the App

### How do I analyze a reel?
1. Copy Instagram Reel URL
2. Paste in the text box
3. Select language (Hindi/English)
4. Click "Analyze This Reel!"
5. Wait for results

### What Instagram URLs are supported?
Any Instagram Reel URL like:
- `https://www.instagram.com/reel/ABC123/`
- `https://instagram.com/reel/ABC123/?igsh=...`

### Transcription is empty or wrong
Try:
- Check if reel has clear audio
- Try different language setting
- Check internet connection
- Reel might have background music only (no speech)

### Analysis seems off
The AI analyzes based on:
- Transcript accuracy
- Available medical literature
- Prompt engineering

If analysis is incorrect:
- Report via GitHub Issues
- Include the Reel URL
- Describe what's wrong

### Can I download the results?
Yes! Click the download buttons for:
- Caption (text)
- Transcript (text)
- Analysis (text)

## 💬 Chat Feature

### How does chat work?
After analyzing a reel, you can ask questions. The AI has full context of:
- Caption
- Transcript
- Analysis

### Chat doesn't remember old conversations
By design! Each analysis starts fresh. But within one analysis session, chat remembers the last 10 messages.

### Can I ask unrelated questions?
The chat is focused on the analyzed reel. For general questions, use regular Claude or ChatGPT.

## 🚀 Deployment

### How do I deploy to Streamlit Cloud?
See [DEPLOYMENT.md](DEPLOYMENT.md) for complete guide.

Quick steps:
1. Push code to GitHub
2. Go to share.streamlit.io
3. Connect your repository
4. Add API keys in secrets
5. Deploy!

### My app keeps sleeping
Free tier apps sleep after inactivity. They wake up when someone visits (takes ~30 seconds).

### Can I use a custom domain?
Not on free tier. Options:
- Upgrade to Streamlit Teams
- Use URL shortener (bit.ly)
- Self-host on your domain

### Deployment failed
Check:
- `packages.txt` includes `ffmpeg`
- All secrets are added correctly
- Repository is public
- Check deployment logs

## 🔒 Privacy & Security

### Where is my data stored?
**Nowhere!** All processing is temporary:
- Files are created in temp directories
- Deleted after analysis
- No database
- Nothing saved

### Are my API keys safe?
Yes, if you:
- Keep them in `.env` (never commit to GitHub)
- Use Streamlit secrets for deployment
- Don't share them publicly

### Can others see my analyzed reels?
No. Each session is private. The app doesn't store any user data.

### Is the RapidAPI key exposed?
The key in the code is mine and has limited usage. For production:
1. Get your own key from RapidAPI
2. Add to `.env` file
3. Update code to use it

## ⚡ Performance

### Why is transcription slow?
- Audio is processed in 10-second chunks
- Google Speech API has latency
- Longer reels take more time

Average times:
- 30s reel: ~30 seconds
- 60s reel: ~60 seconds

### Can I make it faster?
Options:
- Use paid transcription API (Groq Whisper, AssemblyAI)
- Increase chunk size (less accurate)
- Use better hardware

### App crashes on long reels
Streamlit Cloud has memory limits (800MB). Solutions:
- Test with shorter reels
- Upgrade to paid tier
- Self-host with more resources

## 🐛 Troubleshooting

### "All Groq API keys failed"
- Check all 3 keys are valid
- Verify no typos in `.env`
- Check if keys are rate-limited
- Wait 60 seconds and retry

### "Module not found" error
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Streamlit won't start
```bash
# Check if already running
# Kill the process and restart

# Or use different port
streamlit run app.py --server.port 8502
```

### "Permission denied" errors
**Windows:** Run as Administrator
**Mac/Linux:** Check file permissions
```bash
chmod +x setup.sh run.sh
```

### Chat shows old messages
Clear session:
- Refresh the page (F5)
- Or click "Rerun" in Streamlit

## 💰 Costs

### Is everything free?
**Free tiers:**
- ✅ Groq API (generous free tier)
- ✅ Streamlit Cloud (1GB storage)
- ✅ PubMed API (completely free)
- ✅ Google Speech Recognition (free)

**Paid (optional):**
- RapidAPI Instagram API (mine is limited, get your own)
- Streamlit Teams ($250/month for more resources)

### What are the rate limits?
- **Groq:** 14,400 requests/day (free tier)
- **Speech Recognition:** ~50 requests/minute
- **RapidAPI:** Depends on your plan

## 🤝 Contributing

### Can I contribute?
Absolutely! See [CONTRIBUTING.md](CONTRIBUTING.md)

### I found a bug
Open an issue on GitHub with:
- Clear description
- Steps to reproduce
- Screenshots
- Your environment

### I have a feature idea
Open a feature request on GitHub! We'd love to hear it.

## 📞 Support

### Where do I get help?

1. **Documentation:**
   - README.md
   - DEPLOYMENT.md
   - TESTING.md

2. **Issues:**
   - Search existing issues
   - Open new issue

3. **Community:**
   - GitHub Discussions
   - Streamlit Forum

### How do I report a bug?
1. Go to GitHub Issues
2. Click "New Issue"
3. Choose "Bug Report"
4. Fill in the template

### Can I hire you for custom development?
Open an issue or email. We can discuss!

## 🎓 Learning Resources

### I want to learn more about:

**Streamlit:**
- [Streamlit Docs](https://docs.streamlit.io)
- [Streamlit Gallery](https://streamlit.io/gallery)

**Groq API:**
- [Groq Docs](https://console.groq.com/docs)
- [Groq Cookbook](https://github.com/groq/groq-cookbook)

**Instagram APIs:**
- [RapidAPI Hub](https://rapidapi.com/hub)

**Medical APIs:**
- [PubMed API](https://www.ncbi.nlm.nih.gov/home/develop/api/)

## 🎉 Success Stories

### Can I share my deployment?
Yes! We'd love to feature it. Share on:
- GitHub Discussions
- Twitter (tag us!)
- LinkedIn

### Can I use this commercially?
Yes! MIT License allows commercial use. But:
- Credit the original project
- Don't claim you made it
- Share improvements back

## 📊 Analytics

### Can I track usage?
Streamlit Cloud provides:
- Viewer count
- Session stats
- No detailed analytics on free tier

For detailed analytics:
- Use Google Analytics
- Add custom tracking
- Upgrade to Teams tier

## 🔮 Future Plans

### What's coming next?
- More languages (Spanish, French, etc.)
- Video download option
- PDF export
- Batch processing
- Mobile app

### Can I suggest features?
Yes! Open a feature request on GitHub.

## 📚 Additional Resources

- [Streamlit Cheat Sheet](https://cheat-sheet.streamlit.app)
- [Python for Medical AI](https://github.com/topics/medical-ai)
- [Gen-Z Design Trends](https://uxdesign.cc)

---

**Still have questions?** 

Open an issue on GitHub or check the documentation!

Made with 💜 by MedReel Analyzer Team
