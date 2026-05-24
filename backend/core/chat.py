"""
Chat functionality for follow-up questions about analyzed content
"""
from typing import List, Dict
from groq import Groq
from backend.core.transcription import get_groq_client


def chat_with_context(
    user_question: str,
    context: Dict[str, str],
    citations: List[Dict[str, str]],
    chat_history: List[Dict[str, str]] = None
) -> str:
    """
    Answer follow-up questions using context from analyzed reel

    This allows users to ask questions like:
    - "What are the side effects?"
    - "Is this safe during pregnancy?"
    - "What's the recommended dosage?"

    Args:
        user_question: The user's question
        context: Dictionary containing:
            - caption: Instagram Reel caption
            - transcript: Original transcript
            - corrected_transcript: Grammar-corrected transcript
            - analysis: LLM analysis result
        citations: List of research papers with title, url, source
        chat_history: Optional list of previous messages [{"role": "user"|"assistant", "content": "..."}]

    Returns:
        Assistant's response as string

    Example:
        response = chat_with_context(
            user_question="What are the side effects?",
            context={
                "caption": "...",
                "transcript": "...",
                "analysis": "..."
            },
            citations=[...],
            chat_history=[]
        )
    """
    try:
        print(f"💬 Processing chat question: {user_question}")
        client, _ = get_groq_client()

        # Build citations text for context
        citations_text = ""
        if citations:
            citations_text = "\n\nAvailable Scientific Sources:\n"
            for i, cite in enumerate(citations, 1):
                title = cite.get('title', 'Untitled')
                source = cite.get('source', 'Unknown')
                url = cite.get('url', '#')
                citations_text += f"[{i}] {title} - {source} - {url}\n"

        # Build context information
        context_info = f"""
Reel Caption: {context.get('caption', 'N/A')}
Transcript: {context.get('corrected_transcript', context.get('transcript', 'N/A'))}
Analysis: {context.get('analysis', 'N/A')}
{citations_text}
"""

        # Build messages array
        messages = [
            {
                "role": "system",
                "content": f"""You are a helpful medical assistant. You have context about an Instagram Reel:

{context_info}

Answer questions based on this context. Be friendly, accurate, and use emojis. When answering about sources or citations, ALWAYS provide the specific URLs from the citations above.

If the user asks about information not in the context, say so politely and suggest they consult a healthcare professional."""
            }
        ]

        # Add chat history (last 10 messages to keep context manageable)
        if chat_history:
            for msg in chat_history[-10:]:
                messages.append({"role": msg["role"], "content": msg["content"]})

        # Add current user question
        messages.append({"role": "user", "content": user_question})

        print(f"📤 Sending chat request to Groq with {len(messages)} messages")

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,  # Balanced temperature for helpful but factual responses
            max_tokens=1024
        )

        result = response.choices[0].message.content or "Sorry, I couldn't generate a response."
        print(f"✅ Chat response received (length: {len(result)} chars)")

        return result

    except Exception as e:
        print(f"❌ Chat error: {str(e)}")
        raise Exception(f"Chat failed: {str(e)}")
