import streamlit as st
import requests
import json
import os
import tempfile
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
from groq import Groq
import time
from typing import List, Dict, Tuple, Any
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="MedReel Analyzer 💊🎥",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for beautiful mobile-responsive design
st.markdown("""
<style>
    /* Hide sidebar completely */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Main container */
    .main {
        padding: 1rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Title styling - responsive */
    .title-container {
        text-align: center;
        padding: 1.5rem 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .title-text {
        color: white;
        font-size: clamp(1.8rem, 5vw, 3.5rem);
        font-weight: bold;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        line-height: 1.2;
    }
    
    .subtitle-text {
        color: #f0f0f0;
        font-size: clamp(0.9rem, 2.5vw, 1.2rem);
        margin-top: 0.5rem;
    }
    
    /* Debug section */
    .debug-section {
        background: #fff3cd;
        border: 2px solid #ffc107;
        padding: 0.8rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        font-family: monospace;
        font-size: 0.8rem;
        overflow-x: auto;
    }
    
    /* Input container - responsive */
    .input-container {
        background: var(--background-color);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #667eea;
        margin-bottom: 1.5rem;
    }
    
    /* Results container - responsive */
    .result-section {
        background: var(--background-color);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        border-left: 5px solid #667eea;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .result-title {
        color: #667eea;
        font-size: clamp(1.3rem, 3vw, 1.8rem);
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .result-content {
        font-size: clamp(0.9rem, 2vw, 1rem);
        line-height: 1.6;
    }
    
    /* Chat container - mobile friendly */
    .chat-container {
        background: var(--background-color);
        padding: 1rem;
        border-radius: 15px;
        max-height: 500px;
        overflow-y: auto;
        margin-bottom: 1rem;
    }
    
    .user-message {
        background: #667eea;
        color: white;
        padding: 0.8rem 1rem;
        border-radius: 15px 15px 5px 15px;
        margin-bottom: 1rem;
        margin-left: 10%;
        box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3);
        font-size: clamp(0.85rem, 2vw, 1rem);
        word-wrap: break-word;
    }
    
    .assistant-message {
        background: #f0f0f0;
        color: #333;
        padding: 0.8rem 1rem;
        border-radius: 15px 15px 15px 5px;
        margin-bottom: 1rem;
        margin-right: 10%;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        font-size: clamp(0.85rem, 2vw, 1rem);
        word-wrap: break-word;
    }
    
    [data-theme="dark"] .assistant-message {
        background: #2d2d2d;
        color: #e0e0e0;
    }
    
    /* Mobile: full width messages */
    @media (max-width: 768px) {
        .user-message {
            margin-left: 5%;
        }
        .assistant-message {
            margin-right: 5%;
        }
        .main {
            padding: 0.5rem;
        }
        .title-container {
            padding: 1rem 0.5rem;
            margin-bottom: 1rem;
        }
        .result-section {
            padding: 1rem;
        }
    }
    
    /* Buttons - responsive */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 1.5rem;
        font-size: clamp(0.9rem, 2vw, 1.1rem);
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Text visibility for both modes */
    .stMarkdown, p, span, div {
        color: var(--text-color);
    }
    
    [data-theme="light"] {
        --text-color: #333333;
        --background-color: white;
    }
    
    [data-theme="dark"] {
        --text-color: #e0e0e0;
        --background-color: #1e1e1e;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Download buttons - responsive */
    .stDownloadButton>button {
        background: #28a745;
        color: white;
        border-radius: 20px;
        padding: 0.5rem 1rem;
        margin: 0.3rem;
        font-size: clamp(0.8rem, 2vw, 1rem);
    }
    
    /* Emoji styling */
    .emoji {
        font-size: clamp(1.2rem, 3vw, 1.5rem);
        margin-right: 0.5rem;
    }
    
    /* Citation links */
    .citation-link {
        color: #667eea;
        text-decoration: none;
        font-weight: 600;
        border-bottom: 2px solid #667eea;
        padding-bottom: 2px;
        transition: all 0.3s;
    }
    
    .citation-link:hover {
        color: #764ba2;
        border-bottom-color: #764ba2;
    }
    
    .citations-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
        border-left: 4px solid #28a745;
    }
    
    [data-theme="dark"] .citations-section {
        background: #2d2d2d;
    }
    
    /* Input fields - responsive */
    .stTextInput input, .stSelectbox select {
        font-size: clamp(0.9rem, 2vw, 1rem);
        padding: 0.6rem;
    }
    
    /* Form containers */
    .stForm {
        background: var(--background-color);
        padding: 1rem;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'context' not in st.session_state:
    st.session_state.context = {}
if 'debug_mode' not in st.session_state:
    st.session_state.debug_mode = False
if 'api_response' not in st.session_state:
    st.session_state.api_response = None
if 'citations' not in st.session_state:
    st.session_state.citations = []

# Configuration
RAPIDAPI_CONFIG = {
    "url": "https://social-download-all-in-one.p.rapidapi.com/v1/social/autolink",
    "headers": {
        "x-rapidapi-key": "083f33c460msh03094104d3fd8fbp1abb5fjsnbefdd3f236d7",
        "x-rapidapi-host": "social-download-all-in-one.p.rapidapi.com",
        "Content-Type": "application/json"
    }
}

# Groq API Keys with fallback
GROQ_API_KEYS = [
    os.getenv("GROQ_API_KEY_1", ""),
    os.getenv("GROQ_API_KEY_2", ""),
    os.getenv("GROQ_API_KEY_3", "")
]

# Semantic Scholar API Key
SEMANTIC_SCHOLAR_API_KEY = os.getenv("Semantic_Scholar_API_Key", "")

def debug_log(message: str, data: Any = None):
    """Log debug information if debug mode is enabled"""
    if st.session_state.debug_mode:
        st.markdown(f"""
        <div class="debug-section">
            <strong>🐛 DEBUG:</strong> {message}
            {f'<pre>{json.dumps(data, indent=2) if isinstance(data, (dict, list)) else str(data)}</pre>' if data else ''}
        </div>
        """, unsafe_allow_html=True)

def get_groq_client() -> Tuple[Groq, int]:
    """Get Groq client with fallback mechanism"""
    for idx, api_key in enumerate(GROQ_API_KEYS):
        if api_key:
            try:
                client = Groq(api_key=api_key)
                # Test the client
                client.models.list()
                debug_log(f"✅ Successfully connected with API Key #{idx + 1}")
                return client, idx
            except Exception as e:
                debug_log(f"❌ API Key {idx + 1} failed", {"error": str(e)})
                st.warning(f"⚠️ API Key {idx + 1} failed, trying next...")
                continue
    raise Exception("All Groq API keys failed!")

def transcribe_audio(audio_path: str, language: str) -> str:
    """Transcribe audio to text in chunks"""
    import gc
    
    try:
        debug_log(f"Starting transcription for: {audio_path}", {"language": language})
        
        sound = AudioSegment.from_file(audio_path)
        chunks = make_chunks(sound, 10000)  # 10 second chunks
        r = sr.Recognizer()
        full_transcript = []
        
        lang_code = 'hi-IN' if language == 'Hindi' else 'en-US'
        debug_log(f"Total chunks to process: {len(chunks)}", {"lang_code": lang_code})
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, chunk in enumerate(chunks):
            chunk_name = None
            try:
                # Create temp file with unique name
                chunk_name = f"temp_chunk_{i}_{int(time.time() * 1000)}.wav"
                chunk.export(chunk_name, format="wav")
                
                # Small delay to ensure file is written
                time.sleep(0.1)
                
                # Transcribe
                with sr.AudioFile(chunk_name) as source:
                    r.adjust_for_ambient_noise(source, duration=1)
                    audio_data = r.record(source)
                
                # Explicitly close and cleanup
                del source
                gc.collect()
                
                # Recognize speech
                text = r.recognize_google(audio_data, language=lang_code)  # type: ignore
                full_transcript.append(text)
                debug_log(f"Chunk {i+1} transcribed successfully", {"text": text[:50] + "..." if len(text) > 50 else text})
                
                progress = (i + 1) / len(chunks)
                progress_bar.progress(progress)
                status_text.text(f"🎙️ Transcribing... {int(progress * 100)}%")
                
            except sr.UnknownValueError:
                debug_log(f"Chunk {i+1}: Speech not recognized")
                pass
            except sr.RequestError as e:
                debug_log(f"Chunk {i+1}: API error", {"error": str(e)})
                st.warning(f"⚠️ API error: {str(e)}")
            except Exception as e:
                debug_log(f"Chunk {i+1}: Unexpected error", {"error": str(e)})
                pass
            finally:
                # Cleanup temp file with retry
                if chunk_name and os.path.exists(chunk_name):
                    for attempt in range(5):
                        try:
                            time.sleep(0.2)
                            os.remove(chunk_name)
                            break
                        except PermissionError:
                            if attempt < 4:
                                time.sleep(0.3)
                            else:
                                debug_log(f"Failed to delete {chunk_name} after 5 attempts")
                                pass
        
        progress_bar.empty()
        status_text.empty()
        
        final_transcript = " ".join(full_transcript)
        debug_log("Transcription completed", {"length": len(final_transcript), "preview": final_transcript[:100] + "..." if len(final_transcript) > 100 else final_transcript})
        
        return final_transcript
    except Exception as e:
        debug_log("Transcription failed", {"error": str(e)})
        st.error(f"Transcription error: {str(e)}")
        return ""

def fetch_semantic_scholar_papers(query: str) -> List[Dict[str, Any]]:
    """Fetch papers from Semantic Scholar API"""
    try:
        debug_log("Fetching papers from Semantic Scholar", {"query": query})
        
        headers = {}
        if SEMANTIC_SCHOLAR_API_KEY:
            headers["x-api-key"] = SEMANTIC_SCHOLAR_API_KEY
        
        # Search for papers
        search_url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            "query": query,
            "limit": 5,
            "fields": "title,abstract,url,year,authors,citationCount,publicationTypes"
        }
        
        response = requests.get(search_url, params=params, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            papers = data.get('data', [])
            debug_log(f"Found {len(papers)} papers from Semantic Scholar")
            return papers
        else:
            debug_log("Semantic Scholar API error", {"status": response.status_code})
            return []
            
    except Exception as e:
        debug_log("Semantic Scholar search error", {"error": str(e)})
        return []

def fetch_medical_info(query: str) -> Tuple[str, List[Dict[str, str]]]:
    """Fetch medical information from PubMed and Semantic Scholar"""
    citations = []
    
    try:
        debug_log("Fetching medical info", {"query": query})
        
        # PubMed search
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": 3,
            "retmode": "json"
        }
        
        response = requests.get(base_url, params=params)
        pubmed_results = []
        
        if response.status_code == 200:
            data = response.json()
            pmids = data.get('esearchresult', {}).get('idlist', [])
            debug_log("PubMed search results", {"pmids": pmids})
            
            if pmids:
                # Fetch summaries
                summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
                summary_params = {
                    "db": "pubmed",
                    "id": ",".join(pmids),
                    "retmode": "json"
                }
                summary_response = requests.get(summary_url, params=summary_params)
                if summary_response.status_code == 200:
                    summaries = summary_response.json()
                    for pmid in pmids:
                        article = summaries.get('result', {}).get(pmid, {})
                        title = article.get('title', '')
                        if title:
                            pubmed_url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                            pubmed_results.append(f"• {title}")
                            citations.append({
                                "title": title,
                                "url": pubmed_url,
                                "source": "PubMed"
                            })
        
        # Semantic Scholar search
        semantic_papers = fetch_semantic_scholar_papers(query)
        semantic_results = []
        
        for paper in semantic_papers:
            title = paper.get('title', '')
            url = paper.get('url', '')
            year = paper.get('year', 'N/A')
            if title and url:
                semantic_results.append(f"• {title} ({year})")
                citations.append({
                    "title": title,
                    "url": url,
                    "source": "Semantic Scholar",
                    "year": year
                })
        
        # Combine results
        all_results = []
        if pubmed_results:
            all_results.extend(pubmed_results[:2])
        if semantic_results:
            all_results.extend(semantic_results[:3])
        
        debug_log("Medical references found", {"count": len(citations)})
        
        result_text = "\n".join(all_results) if all_results else "No medical references found"
        return result_text, citations
        
    except Exception as e:
        debug_log("Medical search error", {"error": str(e)})
        return f"Medical search error: {str(e)}", citations

def format_analysis_with_proper_markdown(text: str) -> str:
    """Fix markdown formatting - replace ** with actual bold HTML"""
    # Replace **text** with <strong>text</strong>
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    
    # Replace * for bullet points with proper HTML
    lines = text.split('\n')
    formatted_lines = []
    in_list = False
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('* '):
            if not in_list:
                formatted_lines.append('<ul>')
                in_list = True
            formatted_lines.append(f'<li>{stripped[2:]}</li>')
        else:
            if in_list:
                formatted_lines.append('</ul>')
                in_list = False
            if stripped:
                formatted_lines.append(f'<p>{stripped}</p>')
    
    if in_list:
        formatted_lines.append('</ul>')
    
    return '\n'.join(formatted_lines)

def analyze_with_llm(caption: str, transcript: str) -> Tuple[str, List[Dict[str, str]]]:
    """Analyze content with Groq LLM and return formatted analysis with citations"""
    try:
        client, key_idx = get_groq_client()
        st.info(f"🤖 Using API Key #{key_idx + 1}")
        
        # Fetch medical context from both sources
        medical_context, citations = fetch_medical_info(transcript[:200])
        
        # Save citations to session state
        st.session_state.citations = citations
        
        prompt = f"""You are a Gen-Z medical fact-checker with a sense of humor. Analyze this Instagram Reel content:

**Caption:** {caption}

**Transcript:** {transcript}

**Medical References:**
{medical_context}

Your task:
1. **What's the claim?** - Summarize what they're saying (max 2 lines)
2. **Is it legit?** ✅❌ - Rate accuracy (Accurate/Partially True/Misleading/False)
3. **The tea ☕** - Explain what's actually true with scientific backing
4. **Red flags 🚩** - Point out anything sus or incorrect
5. **Bottom line** - Your verdict in one spicy sentence

Keep it:
- In bullet points
- Easy to read
- Funny but factual
- Gen-Z friendly (use emojis!)
- Backed by science

IMPORTANT: Do NOT use ** for bold text. Instead, write naturally without markdown formatting. The system will handle formatting automatically.

Be brutally honest but helpful. If something's wrong, say it. If it's right, give credit."""

        debug_log("Sending request to Groq LLM", {"prompt_length": len(prompt)})
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a medical fact-checker who speaks like a Gen-Z doctor. Be accurate, funny, and use emojis. Write without markdown formatting - use natural language."},
                {"role": "user", "content": prompt}
            ],  # type: ignore
            temperature=0.7,
            max_tokens=2048
        )
        
        result = response.choices[0].message.content or "Analysis not available"
        debug_log("LLM analysis completed", {"length": len(result)})
        
        # Format the result with proper HTML
        formatted_result = format_analysis_with_proper_markdown(result)
        
        return formatted_result, citations
        
    except Exception as e:
        debug_log("LLM analysis failed", {"error": str(e)})
        st.error(f"LLM Analysis failed: {str(e)}")
        return "Analysis failed. Please try again.", []

def display_citations(citations: List[Dict[str, str]]):
    """Display citations in a nice format"""
    if not citations:
        return
    
    citations_html = '<div class="citations-section"><h3>📚 Scientific References & Citations</h3><p><em>Click to verify the sources:</em></p><ul>'
    
    for i, citation in enumerate(citations, 1):
        title = citation.get('title', 'Untitled')
        url = citation.get('url', '#')
        source = citation.get('source', 'Unknown')
        year = citation.get('year', '')
        
        year_text = f" ({year})" if year else ""
        citations_html += f'<li><a href="{url}" target="_blank" class="citation-link">[{i}] {title}</a> - <em>{source}{year_text}</em></li>'
    
    citations_html += '</ul></div>'
    
    st.markdown(citations_html, unsafe_allow_html=True)

def chat_with_context(user_question: str) -> str:
    """Chat with context of the analyzed reel"""
    try:
        client, _ = get_groq_client()
        
        context_info = f"""
        Reel Caption: {st.session_state.context.get('caption', 'N/A')}
        Transcript: {st.session_state.context.get('transcript', 'N/A')}
        Analysis: {st.session_state.context.get('analysis', 'N/A')}
        """
        
        debug_log("Chat request", {"question": user_question})
        
        messages = [
            {"role": "system", "content": f"You are a helpful medical assistant. You have context about an Instagram Reel:\n{context_info}\n\nAnswer questions based on this context. Be friendly, accurate, and use emojis."}
        ]
        
        # Add chat history
        for msg in st.session_state.chat_history[-10:]:
            messages.append({"role": msg["role"], "content": msg["content"]})  # type: ignore
        
        messages.append({"role": "user", "content": user_question})
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,  # type: ignore
            temperature=0.7,
            max_tokens=1024
        )
        
        result = response.choices[0].message.content or ""
        debug_log("Chat response received", {"length": len(result)})
        
        return result
        
    except Exception as e:
        debug_log("Chat error", {"error": str(e)})
        return f"Chat error: {str(e)}"

def extract_audio_url(data: Dict[str, Any]) -> str:
    """Extract audio URL from API response with multiple fallback strategies"""
    debug_log("Extracting audio URL from response", data)
    
    # Strategy 1: Check medias array
    if 'medias' in data and isinstance(data['medias'], list):
        debug_log(f"Found 'medias' array with {len(data['medias'])} items")
        
        # Try to find audio in medias
        for idx, media in enumerate(data['medias']):
            debug_log(f"Media {idx}", media)
            
            # Check if it's audio type
            if isinstance(media, dict):
                if media.get('type') == 'audio' or 'audio' in media.get('url', '').lower():
                    debug_log(f"Found audio at index {idx}")
                    return media['url']
        
        # If not found by type, try index 1 (original approach)
        if len(data['medias']) > 1:
            debug_log("Using medias[1] as fallback")
            return data['medias'][1]['url']
    
    # Strategy 2: Check for direct audio_url field
    if 'audio_url' in data:
        debug_log("Found 'audio_url' field")
        return data['audio_url']
    
    # Strategy 3: Check medias dict (not array)
    if 'medias' in data and isinstance(data['medias'], dict):
        if 'audio' in data['medias']:
            debug_log("Found 'medias.audio' field")
            return data['medias']['audio']
    
    # Strategy 4: Look for any field containing 'audio'
    for key, value in data.items():
        if 'audio' in key.lower() and isinstance(value, str) and value.startswith('http'):
            debug_log(f"Found audio URL in field: {key}")
            return value
    
    raise KeyError(f"Could not find audio URL in response. Available keys: {list(data.keys())}")

# Main App
st.markdown("""
<div class="title-container">
    <h1 class="title-text">💊 MedReel Analyzer 🎥</h1>
    <p class="subtitle-text">Drop that health influencer link, we'll drop the facts ✨</p>
</div>
""", unsafe_allow_html=True)

# Debug toggle - better mobile layout
col_debug1, col_debug2 = st.columns([3, 1])
with col_debug2:
    if st.button("🐛 " + ("ON" if st.session_state.debug_mode else "Debug"), use_container_width=True):
        st.session_state.debug_mode = not st.session_state.debug_mode
        st.rerun()

if st.session_state.debug_mode:
    st.warning("🐛 **Debug Mode Active** - Detailed logs will be shown below")

# Input Section - responsive columns
col1, col2 = st.columns([2, 1])

with col1:
    reel_url = st.text_input(
        "📱 Paste Instagram Reel URL",
        placeholder="https://www.instagram.com/reel/...",
        label_visibility="collapsed"
    )

with col2:
    language = st.selectbox(
        "🌐 Language",
        ["Hindi", "English"],
        label_visibility="collapsed"
    )

analyze_button = st.button("🔍 Analyze This Reel!", use_container_width=True)

# Analysis Section
if analyze_button and reel_url:
    with st.spinner("🔮 Fetching reel data..."):
        try:
            debug_log("Fetching reel data", {"url": reel_url})
            
            # Fetch reel data
            payload = {"url": reel_url}
            response = requests.post(
                RAPIDAPI_CONFIG["url"],
                json=payload,
                headers=RAPIDAPI_CONFIG["headers"]
            )
            
            debug_log("API Response Status", {"status_code": response.status_code})
            
            data = response.json()
            st.session_state.api_response = data  # Save for debugging
            
            debug_log("Full API Response", data)
            
            # Extract caption
            caption = data.get('title', '') or data.get('caption', '') or data.get('description', '') or 'No Caption Found'
            debug_log("Extracted caption", {"caption": caption})
            
            # Extract audio URL with fallback strategies
            try:
                audio_url = extract_audio_url(data)
                debug_log("Audio URL extracted", {"url": audio_url})
            except Exception as e:
                st.error(f"❌ Could not find audio URL in response")
                debug_log("Audio extraction failed", {"error": str(e)})
                
                # Show raw response for debugging
                with st.expander("🔍 View Raw API Response"):
                    st.json(data)
                
                st.info("💡 **Tip:** Enable Debug Mode and check the logs above to see the full API response structure.")
                st.stop()
            
            # Download audio
            debug_log("Downloading audio", {"url": audio_url})
            audio_response = requests.get(audio_url)
            
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_audio:
                temp_audio.write(audio_response.content)
                audio_path = temp_audio.name
            
            debug_log("Audio downloaded", {"path": audio_path, "size": len(audio_response.content)})
            
            st.success("✅ Reel data fetched successfully!")
            
            # Display caption
            st.markdown(f"""
            <div class="result-section">
                <h2 class="result-title">📝 Caption</h2>
                <div class="result-content">{caption}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Transcribe
            with st.spinner("🎙️ Transcribing audio..."):
                transcript = transcribe_audio(audio_path, str(language))
            
            if transcript:
                st.markdown(f"""
                <div class="result-section">
                    <h2 class="result-title">📜 Transcript ({language})</h2>
                    <div class="result-content">{transcript}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Analyze
                with st.spinner("🧠 Analyzing with AI..."):
                    analysis, citations = analyze_with_llm(caption, transcript)
                
                st.markdown(f"""
                <div class="result-section">
                    <h2 class="result-title">🔬 Medical Analysis</h2>
                    <div class="result-content">{analysis}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Display citations
                display_citations(citations)
                
                # Save to session state
                st.session_state.context = {
                    'caption': caption,
                    'transcript': transcript,
                    'analysis': analysis,
                    'audio_path': audio_path,
                    'citations': citations
                }
                
                # Download buttons - responsive grid
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.download_button(
                        "📥 Caption",
                        caption,
                        file_name="caption.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                with col2:
                    st.download_button(
                        "📥 Transcript",
                        transcript,
                        file_name="transcript.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                with col3:
                    # Prepare analysis text without HTML for download
                    analysis_text = re.sub(r'<[^>]+>', '', analysis)
                    st.download_button(
                        "📥 Analysis",
                        analysis_text,
                        file_name="analysis.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
            else:
                st.error("❌ Transcription failed. Please try again.")
            
            # Cleanup
            if os.path.exists(audio_path):
                try:
                    os.remove(audio_path)
                    debug_log("Audio file cleaned up", {"path": audio_path})
                except Exception as e:
                    debug_log("Failed to cleanup audio file", {"error": str(e)})
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            debug_log("Fatal error", {"error": str(e), "type": type(e).__name__})
            
            # Show raw response if available
            if st.session_state.api_response:
                with st.expander("🔍 View Raw API Response"):
                    st.json(st.session_state.api_response)

# Show raw API response in debug mode
if st.session_state.debug_mode and st.session_state.api_response:
    with st.expander("📋 Last API Response (Debug)"):
        st.json(st.session_state.api_response)

# Chat Section
if st.session_state.context:
    st.markdown("""
    <div class="result-section">
        <h2 class="result-title">💬 Ask Questions About This Reel</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f'<div class="user-message">👤 {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-message">🤖 {msg["content"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    with st.form(key='chat_form', clear_on_submit=True):
        user_input = st.text_input(
            "Type your question...",
            placeholder="e.g., Is this claim scientifically proven?",
            label_visibility="collapsed"
        )
        submit = st.form_submit_button("Send 📤", use_container_width=True)
        
        if submit and user_input:
            # Add user message
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Get response
            with st.spinner("🤔 Thinking..."):
                response = chat_with_context(user_input)
            
            # Add assistant message
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            
            st.rerun()

# Footer
st.markdown("""
---
<p style='text-align: center; color: #666; font-size: clamp(0.8rem, 2vw, 0.9rem);'>
Made with 💜 by MedReel Analyzer | Not medical advice, just facts ✨<br>
<em style="font-size: 0.85em;">Powered by Groq, PubMed & Semantic Scholar</em>
</p>
""", unsafe_allow_html=True)