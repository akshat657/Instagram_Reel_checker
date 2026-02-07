# MedReel Analyzer - Improved Version 💊🎥

An AI-powered Instagram Reel fact-checker that analyzes health and medical claims with scientific backing.

## 🆕 What's New in This Version

### 1. **Fixed Markdown Formatting** ✅
- **Problem**: Bold text was showing as `**text**` instead of being rendered properly
- **Solution**: Implemented HTML conversion that replaces `**text**` with `<strong>text</strong>`
- Now all bold text, bullet points, and formatting render correctly in the UI

### 2. **Semantic Scholar Integration** 📚
- Added Semantic Scholar API for academic paper search
- Combines PubMed and Semantic Scholar for comprehensive research
- Fetches up to 5 relevant academic papers per analysis
- Provides more diverse and recent research sources

### 3. **Citation Links** 🔗
- Every analysis now includes clickable citation links
- Users can verify all sources directly
- Shows source type (PubMed or Semantic Scholar)
- Includes publication year for Semantic Scholar papers
- Beautiful, styled citation section with hover effects

### 4. **Mobile-Responsive Design** 📱
- Completely redesigned CSS for perfect mobile experience
- Uses `clamp()` for responsive font sizes
- Optimized button sizes and padding for touch screens
- Chat messages adapt width based on screen size
- Tested on phones (portrait/landscape) and laptops

### 5. **Better Error Handling** 🛡️
- More informative error messages
- Better fallback strategies for API failures
- Debug mode shows detailed logs

## 🚀 Installation

### Prerequisites
```bash
Python 3.8+
pip
```

### Install Dependencies
```bash
pip install streamlit requests pydub SpeechRecognition groq python-dotenv
```

### Set Up Environment Variables

1. Copy the example env file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API keys:
```env
# Required: At least one Groq API key
GROQ_API_KEY_1=your_groq_key_here

# Optional but highly recommended for better research
Semantic_Scholar_API_Key=your_semantic_scholar_key_here
```

### Get API Keys

**Groq API** (Required):
- Go to https://console.groq.com
- Sign up and get your free API key
- Add to `.env` file

**Semantic Scholar API** (Optional but Recommended):
- Go to https://www.semanticscholar.org/product/api
- Request free API key (increases rate limits)
- Without key: 100 requests/5 minutes
- With key: 5000 requests/5 minutes

## 🎯 Usage

1. Run the app:
```bash
streamlit run medreel_analyzer_improved.py
```

2. Paste an Instagram Reel URL
3. Select language (Hindi/English)
4. Click "Analyze This Reel!"
5. View the analysis with citations
6. Click citation links to verify sources
7. Ask follow-up questions in the chat

## 📊 Key Features

### Medical Analysis Includes:
1. **Claim Summary** - What's being said
2. **Accuracy Rating** - Accurate/Partially True/Misleading/False
3. **Scientific Backing** - What's actually true
4. **Red Flags** - What's problematic
5. **Bottom Line** - Final verdict

### Citations Include:
- Direct links to PubMed articles
- Semantic Scholar papers with year
- Source attribution
- Easy verification

### Mobile Features:
- Touch-friendly buttons
- Responsive text sizing
- Optimized chat bubbles
- Efficient space usage
- Works in portrait and landscape

## 🔧 Technical Improvements

### HTML Formatting Function
```python
def format_analysis_with_proper_markdown(text: str) -> str:
    """Converts markdown to HTML for proper rendering"""
    # Replaces **text** with <strong>text</strong>
    # Converts bullet lists to <ul><li>
    # Wraps paragraphs in <p> tags
```

### Dual API Integration
```python
def fetch_medical_info(query: str) -> Tuple[str, List[Dict[str, str]]]:
    """Fetches from both PubMed and Semantic Scholar"""
    # Returns formatted references + citation list
```

### Responsive CSS
```css
/* Example of responsive sizing */
font-size: clamp(0.9rem, 2vw, 1rem);
/* min: 0.9rem, preferred: 2vw, max: 1rem */
```

## 🐛 Debug Mode

Enable debug mode to see:
- API response structures
- Transcription progress
- LLM prompts and responses
- Error details
- Citation fetching logs

Toggle with the "🐛 Debug" button in the top-right.

## 📝 Example Output

**Before (Broken)**:
```
**What's the claim?** **text here**
```

**After (Fixed)**:
```
What's the claim? text here
```

**Citations Section**:
```
📚 Scientific References & Citations
Click to verify the sources:

[1] Aspergillus niger mycotoxin production - PubMed
[2] Ochratoxin A health effects study (2023) - Semantic Scholar
[3] Food storage and fungal contamination - Semantic Scholar
```

## 🎨 Design Features

- **Gradient headers** with purple theme
- **Shadow effects** for depth
- **Smooth transitions** on hover
- **Responsive columns** that stack on mobile
- **Clean typography** with proper hierarchy
- **Touch-friendly** 44px minimum tap targets

## 🔐 Privacy & Security

- No data stored permanently
- API keys in `.env` (not committed)
- Session-based chat history
- Temp files cleaned automatically

## 📱 Tested Devices

- ✅ iPhone (Safari, Chrome)
- ✅ Android (Chrome)
- ✅ iPad (Safari)
- ✅ Desktop (Chrome, Firefox, Safari)
- ✅ Various screen sizes (320px - 1920px)

## 🚨 Troubleshooting

**Problem**: Bold text shows as `**text**`
- **Solution**: Updated! This version uses HTML rendering

**Problem**: Citations not showing
- **Solution**: Check Semantic Scholar API key in `.env`

**Problem**: Mobile layout looks cramped
- **Solution**: Updated! This version is fully responsive

**Problem**: No audio URL found
- **Solution**: Enable debug mode to see API response structure

## 🤝 Contributing

Found a bug? Have a suggestion?
1. Enable debug mode
2. Check the console logs
3. Report issue with debug output

## 📄 License

MIT License - feel free to use and modify!

## 🙏 Credits

- **Groq** - LLM API
- **PubMed** - Medical research database
- **Semantic Scholar** - Academic paper database
- **Streamlit** - Web framework
- **RapidAPI** - Instagram data fetching

## 💡 Tips for Best Results

1. **Use Both API Keys**: Semantic Scholar adds valuable academic sources
2. **Enable Debug Mode**: Helps troubleshoot issues
3. **Check Citations**: Always verify sources before trusting claims
4. **Test on Mobile**: Works great on phones now!
5. **Use WiFi**: Transcription works better with stable connection

## 🔮 Future Enhancements

- [ ] Support for YouTube videos
- [ ] Multi-language analysis output
- [ ] PDF report generation
- [ ] Bookmark favorite analyses
- [ ] Share analysis links
- [ ] More citation databases

---

**Made with 💜 by MedReel Analyzer Team**

*Not medical advice - always consult healthcare professionals for medical decisions!*