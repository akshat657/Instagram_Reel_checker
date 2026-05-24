"""
Medical claim analysis using Groq LLM
"""
import re
from typing import List, Dict, Tuple
from groq import Groq
from backend.core.transcription import get_groq_client


def correct_transcript_grammar(transcript: str, language: str) -> str:
    """
    Use Groq to correct grammatical errors in transcript while keeping original language.

    Args:
        transcript: Original transcript with potential errors
        language: Language of transcript ("Hindi", "English", etc.)

    Returns:
        Grammatically corrected transcript in same language

    Example:
        corrected = correct_transcript_grammar("मैं बहुत अच्छे है", "Hindi")
        # Returns: "मैं बहुत अच्छा हूं"
    """
    try:
        print(f"📝 Correcting {language} transcript grammar...")
        client, _ = get_groq_client()

        prompt = f"""You are a transcript correction expert.

Your task: Fix grammatical errors and transcription mistakes in this {language} transcript.

Rules:
- Keep the transcript in {language} language
- Fix spelling mistakes and grammar errors
- Improve readability but preserve original meaning
- Keep all medical terms intact

Original transcript:
{transcript}

Provide ONLY the corrected {language} transcript. No explanations."""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,  # Low temperature for deterministic corrections
            max_tokens=1024
        )

        corrected = response.choices[0].message.content or transcript
        print(f"✅ Grammar correction complete")
        print(f"   Original length: {len(transcript)} characters")
        print(f"   Corrected length: {len(corrected)} characters")
        print(f"   Preview: {corrected[:150]}...")
        return corrected

    except Exception as e:
        print(f"⚠️ Grammar correction failed: {str(e)}")
        # Fallback to original transcript if correction fails
        return transcript


def extract_keywords_with_groq(transcript: str, language: str) -> str:
    """
    Use Groq to extract medical keywords from transcript and translate to English.

    This is critical for multi-language support. Even if the transcript is in Hindi,
    the keywords are translated to English so we can search PubMed/PMC/Europe PMC
    which primarily index English papers.

    Args:
        transcript: Transcript in any language
        language: Language of transcript

    Returns:
        Medical keywords in English for research paper search

    Example:
        keywords = extract_keywords_with_groq("मुझे सिरदर्द है", "Hindi")
        # Returns: "headache pain migraine"
    """
    try:
        print(f"🔍 Extracting medical keywords from {language} transcript...")
        client, _ = get_groq_client()

        prompt = f"""You are a medical keyword extraction expert.

Your task: Extract medical keywords from this {language} transcript and provide them in English.

Extract:
- Medical conditions and diseases
- Symptoms
- Treatments and medications
- Body parts and organs
- Chemical compounds
- Vitamins and supplements
- Medical procedures

{language} transcript:
{transcript}

Provide ONLY the medical keywords in English, separated by spaces. Maximum 15 keywords. No explanations."""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Slightly higher for more varied keyword extraction
            max_tokens=256
        )

        keywords = response.choices[0].message.content or ""
        keywords = keywords.strip()

        # Fallback if no keywords extracted
        if not keywords or len(keywords) < 5:
            print("⚠️ No keywords extracted, using fallback")
            return "medical health nutrition"

        print(f"✅ Keywords extracted: {keywords}")
        return keywords

    except Exception as e:
        print(f"⚠️ Keyword extraction failed: {str(e)}")
        return "medical health nutrition"


def make_citations_clickable(text: str) -> str:
    """
    Replace [1], [2], etc. with clickable anchor links.

    Args:
        text: HTML formatted text with [1][2] citations

    Returns:
        Text with clickable citation links

    Example:
        text = "This is true [1]. But that is false [2]."
        result = make_citations_clickable(text)
        # Returns: 'This is true <a href="#citation-1">[1]</a>...'
    """
    def replace_citation(match):
        num = match.group(1)
        return f'<a href="#citation-{num}" style="color: #667eea; text-decoration: none; font-weight: 600;">[{num}]</a>'

    # Pattern: [digit]
    pattern = r'\[(\d+)\]'
    result = re.sub(pattern, replace_citation, text)

    return result


def format_analysis_with_proper_markdown(text: str) -> str:
    """
    Convert plain text analysis to properly formatted HTML

    Converts:
    - **bold** to <strong>bold</strong>
    - * bullet points to <ul><li> lists
    - Line breaks to <p> paragraphs
    - [1][2] citations to clickable links

    Args:
        text: Plain text analysis from LLM

    Returns:
        HTML formatted text with inline styles
    """
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
                formatted_lines.append('<ul style="margin-left: 1.5rem;">')
                in_list = True
            formatted_lines.append(f'<li style="margin-bottom: 0.5rem;">{stripped[2:]}</li>')
        else:
            if in_list:
                formatted_lines.append('</ul>')
                in_list = False
            if stripped:
                formatted_lines.append(f'<p style="margin-bottom: 0.8rem;">{stripped}</p>')

    if in_list:
        formatted_lines.append('</ul>')

    result = '\n'.join(formatted_lines)

    # Make citations clickable
    result = make_citations_clickable(result)

    return result


def analyze_with_llm(
    caption: str,
    transcript: str,
    corrected_transcript: str,
    papers: List[Dict[str, str]],
    language: str = "English"
) -> str:
    """
    Analyze medical claims using Groq LLM with inline citations

    This is the core analysis function that:
    1. Takes caption, transcript, and research papers
    2. Builds a prompt asking LLM to fact-check with citations
    3. Returns HTML-formatted analysis with clickable [1][2][3] links

    Args:
        caption: Instagram Reel caption text
        transcript: Original transcript from audio
        corrected_transcript: Grammar-corrected transcript
        papers: List of research papers from PubMed/PMC/Europe PMC
        language: Language of transcript

    Returns:
        HTML-formatted analysis text with inline citations

    Example:
        analysis = analyze_with_llm(
            caption="Drink turmeric for health!",
            transcript="...",
            corrected_transcript="...",
            papers=[...],
            language="English"
        )
        # Returns: "<p>This claim is partially true [1][2]...</p>"
    """
    try:
        print(f"🧠 Starting LLM analysis with {len(papers)} research papers...")
        client, key_idx = get_groq_client()
        print(f"🤖 Using Groq API Key #{key_idx + 1}")

        # Build numbered paper list for LLM
        papers_text = ""
        if papers:
            papers_text = "\n**Research Papers Available (CITE THESE using [1], [2], etc.):**\n\n"
            for i, paper in enumerate(papers, 1):
                papers_text += f"""[{i}] Title: "{paper['title']}" ({paper['year']})
    Source: {paper['source']}
    Abstract: {paper['abstract']}

"""

        # Build prompt with inline citation instruction
        prompt = f"""You are a Gen-Z medical fact-checker with a sense of humor. Analyze this Instagram Reel content and CITE research papers inline using [1], [2], [3] format.

**Caption:** {caption}

**Transcript:** {corrected_transcript}

{papers_text}

Your task:
1. **What's the claim?** - Summarize what they're saying (max 2 lines)
2. **Is it legit?** ✅❌ - Rate accuracy (Accurate/Partially True/Misleading/False) with CITATIONS
3. **The tea ☕** - Explain what's actually true with scientific backing using citations [1][2]
4. **Red flags 🚩** - Point out anything sus or incorrect with citations
5. **Bottom line** - Your verdict in one spicy sentence

IMPORTANT:
- Use inline citations like: "Studies show X [1][2]. However, Y [3]."
- Cite papers that support or refute specific claims
- Only cite papers you were given above
- If no papers available, mention "based on general medical knowledge"

Keep it:
- In bullet points
- Easy to read
- Funny but factual
- Gen-Z friendly (use emojis!)
- Backed by science

Be brutally honest but helpful. If something's wrong, say it. If it's right, give credit."""

        print(f"📤 Sending request to Groq LLM (prompt length: {len(prompt)} chars)")

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a medical fact-checker who speaks like a Gen-Z doctor. Be accurate, funny, and cite research papers inline using [1][2] format. Write without markdown formatting - the system handles that."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,  # Higher temperature for creative but factual writing
            max_tokens=2048
        )

        result = response.choices[0].message.content or "Analysis not available"
        print(f"✅ LLM analysis completed (length: {len(result)} chars)")

        # Check if LLM used citations
        citation_pattern = r'\[\d+\]'
        citations_found = re.findall(citation_pattern, result)

        if len(citations_found) == 0 and len(papers) > 0:
            print("⚠️ LLM did not use inline citations despite papers being available")
        else:
            print(f"✅ LLM used {len(citations_found)} inline citations")

        # Format the result with proper HTML
        formatted_result = format_analysis_with_proper_markdown(result)

        return formatted_result

    except Exception as e:
        print(f"❌ LLM analysis failed: {str(e)}")
        raise Exception(f"Analysis failed: {str(e)}")
