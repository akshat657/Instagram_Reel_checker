
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**MedReel Analyzer** is a Streamlit web app that downloads Instagram Reels, transcribes audio, and fact-checks medical claims using AI and scientific research papers.

**Core Flow:**
1. User pastes Instagram Reel URL
2. App downloads audio via RapidAPI
3. Audio is transcribed (supports Hindi + English)
4. Transcript grammar is corrected by Groq LLM
5. Medical keywords are extracted and translated to English
6. Research papers are fetched from PubMed, PMC, and Europe PMC in parallel
7. Groq LLM analyzes claims with inline citations [1][2]
8. User can chat with AI for follow-up questions

## Running the App

```bash
# Development
streamlit run app.py

# Open in browser at http://localhost:8501
```

**Debug Mode:** Click "🐛 Debug" button in top-right to see detailed logs (extraction keywords, API responses, citation counts).

**Test API Keys:**
```bash
python a.py  # Validates all 3 Groq API keys
```

## Architecture

### Core Files

**`app.py` (main application)**
- Streamlit UI and business logic
- ~1300 lines
- Key sections:
  - CSS styling (lines 27-250)
  - Session state management (lines 360-403)
  - Audio transcription (line 498)
  - Transcript processing (lines 719-827)
  - LLM analysis (line 883)
  - Citation display (line 1011)
  - Chat interface (line 1083)

**`research_fetcher.py` (research paper fetching)**
- Parallel API calls to medical databases
- Functions:
  - `fetch_pubmed_papers()` - PubMed abstracts
  - `fetch_pmc_papers()` - PubMed Central open-access
  - `fetch_europe_pmc_papers()` - Europe PMC database
  - `deduplicate_papers()` - Removes duplicates by PMID, DOI, title similarity
  - `fetch_all_papers_parallel()` - Main entry point (ThreadPoolExecutor)

**`a.py` (testing utility)**
- Tests all 3 Groq API keys against the API
- Useful for debugging rate limit issues

### Multi-Language Transcript Handling

**CRITICAL PATTERN:** Transcripts stay in original language, only keywords are translated.

```python
# Flow for Hindi/non-English reels:
1. transcribe_audio(language="Hindi") → Hindi transcript (Devanagari)
2. correct_transcript_grammar(transcript, "Hindi") → Corrected Hindi
3. extract_keywords_with_groq(transcript, "Hindi") → English keywords
4. fetch_all_papers_parallel(english_keywords) → Research papers
5. analyze_with_llm(..., language="Hindi") → Analysis with citations
```

**Why this matters:**
- Old regex-based `extract_medical_keywords()` only worked for English
- Hindi transcripts would fail keyword extraction → 0 citations
- New Groq-based extraction translates keywords to English for proper paper matching
- Display still shows original language transcript

### Research Citation System

**Inline Citations:** Analysis text includes `[1][2][3]` that link to paper details at bottom.

**Technical implementation:**
1. `fetch_all_papers_parallel()` returns 8-10 papers with abstracts
2. Papers are passed to LLM with explicit citation instructions
3. `make_citations_clickable()` converts `[1]` to `<a href="#citation-1">[1]</a>`
4. `display_citations()` renders papers with `id="citation-1"` anchors
5. Clicking citation jumps to paper details

**Paper sources:** PubMed, PMC, Europe PMC (all free APIs)
- Fetched in parallel with 8-second timeout per source
- Deduplication by PMID, DOI, and 90% title similarity
- Abstracts truncated to 250 words

### API Key Management

**Groq API Keys:** 3 keys with automatic fallback
```python
GROQ_API_KEYS = [
    os.getenv("GROQ_API_KEY_1"),
    os.getenv("GROQ_API_KEY_2"),
    os.getenv("GROQ_API_KEY_3")
]
```

**Fallback logic:** If key hits rate limit, `get_groq_client()` tries next key.

**RapidAPI:** Single key for Instagram data
```python
os.getenv("RAPIDAPI_KEY")
```

### Session State

Important state variables:
- `st.session_state.debug_mode` - Debug logging on/off
- `st.session_state.debug_logs` - Log entries for debug panel
- `st.session_state.citations` - Current analysis citations
- `st.session_state.transcript` - Last transcript
- `st.session_state.analysis` - Last analysis result
- `st.session_state.chat_history` - Conversation messages

**Reset:** "🔄 New Analysis" button clears all state

## Environment Variables

Required in `.env` file:
```
GROQ_API_KEY_1=gsk_...
GROQ_API_KEY_2=gsk_...
GROQ_API_KEY_3=gsk_...
RAPIDAPI_KEY=...
```

**Get keys:**
- Groq: https://console.groq.com/keys
- RapidAPI: https://rapidapi.com/ (Instagram API)

## Key Functions

### `correct_transcript_grammar(transcript: str, language: str) -> str`
Uses Groq to fix grammar errors while keeping original language.
- Temperature: 0.2 (more deterministic)
- Model: llama-3.3-70b-versatile

### `extract_keywords_with_groq(transcript: str, language: str) -> str`
Extracts medical keywords from any language and translates to English.
- Looks for: conditions, symptoms, treatments, medications, vitamins, chemicals
- Fallback: "medical health nutrition" if extraction fails
- Max 15 keywords

### `analyze_with_llm(caption: str, transcript: str, language: str) -> Tuple[str, List[Dict]]`
Main analysis function:
1. Corrects transcript grammar (native language)
2. Extracts keywords (translated to English)
3. Fetches research papers
4. Generates analysis with citations
5. Returns formatted HTML + paper list

**Prompt structure:** Gen-Z friendly, emoji-heavy, brutally honest medical fact-checking.

### `fetch_all_papers_parallel(query: str) -> List[Dict[str, Any]]`
Fetches 8-10 papers from 3 sources in parallel.
- Uses ThreadPoolExecutor with 3 workers
- 10-second total timeout
- Deduplicates results
- Returns: title, abstract, url, source, year, pmid, doi

### `transcribe_audio(audio_path: str, language: str) -> str`
Transcribes audio using Google Speech Recognition.
- Chunks audio into 30-second segments
- Processes in parallel with ThreadPoolExecutor
- Supports Hindi (`hi-IN`) and English (`en-US`)
- Requires FFmpeg for audio processing

## Development Patterns

### Adding New Features

1. **Debug Mode First:** Add debug_log() calls for visibility
2. **Session State:** Store results in st.session_state for persistence
3. **Error Handling:** All external API calls should have try/except
4. **UI Updates:** Use st.spinner() for loading states

### Testing Changes

1. Enable debug mode in UI
2. Test with both English and Hindi reels
3. Check debug logs for API responses
4. Verify citations appear and are clickable
5. Test chat follow-ups

### Common Pitfalls

**❌ Don't:** Use regex patterns for non-English text
**✅ Do:** Use Groq LLM for text processing across languages

**❌ Don't:** Assume transcripts are in English
**✅ Do:** Pass language parameter through the pipeline

**❌ Don't:** Fetch papers sequentially
**✅ Do:** Use parallel fetching (research_fetcher.py)

**❌ Don't:** Hardcode citations in prompt
**✅ Do:** Pass paper list to LLM and let it cite dynamically

## FFmpeg Requirement

**Critical dependency:** App requires FFmpeg for audio processing.

**Installation:**
- Windows: `choco install ffmpeg`
- Mac: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`

**Deployment:** Add `ffmpeg` to `packages.txt` for Streamlit Cloud.

## Deployment

**Streamlit Cloud:**
1. Push to GitHub
2. Connect at https://share.streamlit.io
3. Add secrets (GROQ_API_KEY_1, GROQ_API_KEY_2, GROQ_API_KEY_3, RAPIDAPI_KEY)
4. Ensure `packages.txt` contains `ffmpeg`

**Environment:**
- Python 3.8+
- See `requirements.txt` for dependencies

## Debugging

**Enable Debug Mode:** Click "🐛 Debug" button in app UI.

**Debug logs show:**
- Extracted keywords
- Search queries sent to APIs
- Number of papers fetched per source
- Paper titles and metadata
- Citation count
- LLM responses

**Common issues:**
- **Zero citations:** Check debug logs for keyword extraction output
- **Hindi transcripts fail:** Verify Groq-based extraction is being used
- **API errors:** Test keys with `python a.py`
- **Audio errors:** Verify FFmpeg is installed

## Code Style

- **Temperature settings:**
  - 0.2 for grammar correction (deterministic)
  - 0.3 for keyword extraction (focused)
  - 0.7 for analysis (creative but factual)
- **Timeouts:** 8 seconds per API call, 10 seconds total for parallel ops
- **Error messages:** User-friendly in UI, detailed in debug logs
- **HTML/CSS:** Inline in app.py for Streamlit compatibility
