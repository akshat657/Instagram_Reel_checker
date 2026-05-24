"""
FastAPI routes for MedReel Analyzer API
"""
import os
import asyncio
from fastapi import APIRouter, HTTPException
from backend.models.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    ChatRequest,
    ChatResponse,
    HealthCheckResponse,
    Citation
)
from backend.core.instagram import download_instagram_reel
from backend.core.transcription import transcribe_audio
from backend.core.analysis import (
    correct_transcript_grammar,
    extract_keywords_with_groq,
    analyze_with_llm
)
from backend.core.chat import chat_with_context
from backend.core.research import fetch_all_papers_parallel


# Create router
router = APIRouter(prefix="/api", tags=["api"])


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_reel(request: AnalyzeRequest):
    """
    Analyze Instagram Reel end-to-end

    This endpoint orchestrates the complete analysis pipeline:
    1. Download reel audio via RapidAPI
    2. Transcribe with Groq Whisper (automatic language detection)
    3. Correct transcript grammar using Groq LLM
    4. Extract medical keywords (translate to English if needed)
    5. Fetch research papers from PubMed, PMC, Europe PMC in parallel
    6. Generate medical analysis with inline citations using Groq LLM
    7. Return results with HTML-formatted analysis

    Args:
        request: AnalyzeRequest with Instagram URL and language preference

    Returns:
        AnalyzeResponse with caption, transcripts, analysis, and citations

    Raises:
        HTTPException 400: Invalid URL or request parameters
        HTTPException 500: Internal processing error
    """
    try:
        print(f"🎬 Starting analysis for: {request.url}")

        # Step 1: Download Instagram Reel
        print("📥 Step 1/7: Downloading reel...")
        try:
            caption, audio_path, audio_url = download_instagram_reel(str(request.url))
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to download Instagram reel: {str(e)}"
            )

        # Step 2: Transcribe audio with Google Speech Recognition
        print(f"🎤 Step 2/7: Transcribing audio ({request.language})...")
        try:
            # Run blocking transcription in thread pool to avoid blocking event loop
            transcription_result = await asyncio.to_thread(transcribe_audio, audio_path, request.language)
            transcript = transcription_result["text"]
            detected_language_code = transcription_result["language"]
            detected_language = transcription_result["language_name"]
        except Exception as e:
            # Cleanup audio file on error
            if os.path.exists(audio_path):
                os.remove(audio_path)
            raise HTTPException(
                status_code=500,
                detail=f"Transcription failed: {str(e)}"
            )

        # Step 3: Correct transcript grammar
        print(f"✍️ Step 3/7: Correcting {detected_language} transcript grammar...")
        try:
            corrected_transcript = await asyncio.to_thread(correct_transcript_grammar, transcript, detected_language)
        except Exception as e:
            print(f"⚠️ Grammar correction failed, using original transcript: {str(e)}")
            corrected_transcript = transcript

        # Step 4: Extract medical keywords
        print("🔍 Step 4/7: Extracting medical keywords...")
        try:
            keywords = await asyncio.to_thread(extract_keywords_with_groq, corrected_transcript, detected_language)
            print(f"   Keywords: {keywords}")
        except Exception as e:
            print(f"⚠️ Keyword extraction failed, using fallback: {str(e)}")
            keywords = "medical health nutrition"

        # Step 5: Fetch research papers
        print("📚 Step 5/7: Fetching research papers (PubMed, PMC, Europe PMC)...")
        try:
            papers = await asyncio.to_thread(fetch_all_papers_parallel, keywords)
            print(f"   Found {len(papers)} papers")
        except Exception as e:
            print(f"⚠️ Research fetch failed: {str(e)}")
            papers = []

        # Step 6: Analyze with LLM
        print("🤖 Step 6/7: Analyzing with Groq LLM...")
        try:
            analysis = await asyncio.to_thread(
                analyze_with_llm,
                caption=caption,
                transcript=transcript,
                corrected_transcript=corrected_transcript,
                papers=papers,
                language=detected_language
            )
        except Exception as e:
            # Cleanup audio file on error
            if os.path.exists(audio_path):
                os.remove(audio_path)
            raise HTTPException(
                status_code=500,
                detail=f"Analysis failed: {str(e)}"
            )

        # Step 7: Build response
        print("✅ Step 7/7: Building response...")

        # Convert papers to Citation objects
        citations = [
            Citation(
                title=paper.get("title", "Untitled"),
                url=paper.get("url", "#"),
                source=paper.get("source", "Unknown"),
                year=paper.get("year", "N/A"),
                abstract=paper.get("abstract", "Abstract not available"),
                pmid=paper.get("pmid"),
                doi=paper.get("doi"),
                authors=paper.get("authors"),
                journal=paper.get("journal")
            )
            for paper in papers
        ]

        # Cleanup temp audio file
        if os.path.exists(audio_path):
            os.remove(audio_path)

        print(f"✅ Analysis complete!")

        return AnalyzeResponse(
            caption=caption,
            transcript=transcript,
            corrected_transcript=corrected_transcript,
            detected_language=detected_language,
            analysis=analysis,
            citations=citations,
            audio_url=audio_url
        )

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with context from analyzed reel

    Allows users to ask follow-up questions about the analyzed content.
    The LLM has access to the reel caption, transcript, analysis, and
    research citations to provide informed answers.

    Args:
        request: ChatRequest with message, context, citations, and history

    Returns:
        ChatResponse with assistant's response

    Raises:
        HTTPException 400: Invalid request parameters
        HTTPException 500: Chat processing error
    """
    try:
        print(f"💬 Processing chat: {request.message[:100]}...")

        # Convert Citation objects to dicts
        citations_dict = [
            {
                "title": c.title,
                "url": c.url,
                "source": c.source,
                "year": c.year,
                "abstract": c.abstract,
                "pmid": c.pmid,
                "doi": c.doi,
                "authors": c.authors,
                "journal": c.journal
            }
            for c in request.citations
        ]

        # Convert context to dict
        context_dict = {
            "caption": request.context.caption,
            "transcript": request.context.transcript,
            "corrected_transcript": request.context.corrected_transcript or request.context.transcript,
            "analysis": request.context.analysis
        }

        # Convert history to list of dicts
        history_list = [
            {"role": msg.role, "content": msg.content}
            for msg in request.history
        ]

        # Call chat function
        response_text = chat_with_context(
            user_question=request.message,
            context=context_dict,
            citations=citations_dict,
            chat_history=history_list
        )

        return ChatResponse(response=response_text)

    except Exception as e:
        print(f"❌ Chat error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Chat failed: {str(e)}"
        )


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint for monitoring

    Returns simple status to verify the API is running.
    Used by load balancers, monitoring tools, and deployment checks.

    Returns:
        HealthCheckResponse with status and version
    """
    return HealthCheckResponse(
        status="healthy",
        version="2.0.0"
    )
