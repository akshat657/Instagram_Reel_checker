"""
Audio transcription using Google Speech Recognition (from original app.py)
"""
import os
import time
from typing import Dict, Tuple
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
from groq import Groq
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from backend.config import get_groq_api_keys


def get_groq_client() -> Tuple[Groq, int]:
    """
    Get Groq client with automatic fallback across multiple API keys
    (Used for LLM operations: grammar correction, keyword extraction, analysis)

    Returns:
        Tuple of (Groq client instance, key index used)

    Raises:
        Exception: If all API keys fail
    """
    api_keys = get_groq_api_keys()

    for idx, api_key in enumerate(api_keys):
        if api_key:
            try:
                client = Groq(api_key=api_key)
                # Simple test - just create client, don't call API yet
                print(f"✅ Connected with Groq API Key #{idx + 1}")
                return client, idx
            except Exception as e:
                print(f"❌ Groq API Key #{idx + 1} failed: {str(e)}")
                continue

    raise Exception("All Groq API keys failed! Please check your .env file.")


def transcribe_audio_google(audio_path: str, language: str = "English") -> Dict[str, any]:
    """
    Transcribe audio using Google Speech Recognition (original app.py method)

    Args:
        audio_path: Path to audio file
        language: "English" or "Hindi" (default: "English")

    Returns:
        Dictionary with:
        - text: Transcribed text
        - language: Language code
        - language_name: Full language name
    """
    print(f"🎤 Starting Google Speech Recognition for: {audio_path}")
    print(f"   Language: {language}")

    try:
        # Load audio
        sound = AudioSegment.from_file(audio_path)
        chunks = make_chunks(sound, 10000)  # 10-second chunks
        r = sr.Recognizer()
        full_transcript = []

        # Language code mapping
        lang_code = 'hi-IN' if language == 'Hindi' else 'en-US'

        print(f"   Processing {len(chunks)} chunks...")

        for i, chunk in enumerate(chunks):
            chunk_name = None
            try:
                # Export chunk to temporary WAV file
                chunk_name = f"temp_chunk_{i}_{int(time.time() * 1000)}.wav"
                chunk.export(chunk_name, format="wav")
                time.sleep(0.1)  # Ensure file is written

                # Transcribe chunk
                with sr.AudioFile(chunk_name) as source:
                    r.adjust_for_ambient_noise(source, duration=1)
                    audio_data = r.record(source)

                text = r.recognize_google(audio_data, language=lang_code)
                full_transcript.append(text)
                print(f"   Chunk {i+1}/{len(chunks)}: {text[:50]}...")

            except sr.UnknownValueError:
                print(f"   Chunk {i+1}: Speech not recognized")
                pass
            except sr.RequestError as e:
                print(f"   Chunk {i+1}: API error: {str(e)}")
                pass
            except Exception as e:
                print(f"   Chunk {i+1}: Error: {str(e)}")
                pass
            finally:
                # Cleanup temp file
                if chunk_name and os.path.exists(chunk_name):
                    for attempt in range(5):
                        try:
                            time.sleep(0.2)
                            os.remove(chunk_name)
                            break
                        except PermissionError:
                            if attempt < 4:
                                time.sleep(0.3)

        final_transcript = " ".join(full_transcript)
        print(f"✅ Transcription complete!")
        print(f"   Total length: {len(final_transcript)} characters")
        print(f"   Preview: {final_transcript[:100]}...")

        return {
            "text": final_transcript,
            "language": "hi" if language == "Hindi" else "en",
            "language_name": language,
        }

    except Exception as e:
        print(f"❌ Transcription failed: {str(e)}")
        raise Exception(f"Transcription failed: {str(e)}")


# Main function used by routes
def transcribe_audio(audio_path: str, language: str) -> Dict[str, any]:
    """
    Transcribe audio - uses Google Speech Recognition

    Args:
        audio_path: Path to audio file
        language: "English" or "Hindi" (required)

    Returns:
        Dict with text, language, language_name
    """
    # Validate language
    if language not in ["English", "Hindi"]:
        raise ValueError(f"Language must be 'English' or 'Hindi', got: {language}")

    return transcribe_audio_google(audio_path, language)
