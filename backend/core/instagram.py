"""
Instagram Reel downloader using RapidAPI
"""
import os
import requests
import tempfile
from typing import Dict, Any, Tuple
from backend.config import settings


def extract_audio_url(data: Dict[str, Any]) -> str:
    """
    Extract audio URL from RapidAPI response with multiple fallback strategies

    The API response structure can vary, so we try multiple strategies:
    1. Check medias array for audio type
    2. Check for direct audio_url field
    3. Check medias dict (not array)
    4. Look for any field containing 'audio'

    Args:
        data: JSON response from RapidAPI

    Returns:
        Audio URL string

    Raises:
        KeyError: If no audio URL found in response

    Example:
        data = {
            "medias": [
                {"type": "video", "url": "..."},
                {"type": "audio", "url": "https://...audio.mp3"}
            ]
        }
        url = extract_audio_url(data)
        # Returns: "https://...audio.mp3"
    """
    print(f"Extracting audio URL from response (keys: {list(data.keys())})")

    # Strategy 1: Check medias array
    if 'medias' in data and isinstance(data['medias'], list):
        print(f"Found 'medias' array with {len(data['medias'])} items")

        # Try to find audio in medias
        for idx, media in enumerate(data['medias']):
            # Check if it's audio type
            if isinstance(media, dict):
                if media.get('type') == 'audio' or 'audio' in media.get('url', '').lower():
                    print(f"✅ Found audio at medias[{idx}]")
                    return media['url']

        # If not found by type, try index 1 (common position)
        if len(data['medias']) > 1:
            print("Using medias[1] as fallback")
            return data['medias'][1]['url']

    # Strategy 2: Check for direct audio_url field
    if 'audio_url' in data:
        print("✅ Found 'audio_url' field")
        return data['audio_url']

    # Strategy 3: Check medias dict (not array)
    if 'medias' in data and isinstance(data['medias'], dict):
        if 'audio' in data['medias']:
            print("✅ Found 'medias.audio' field")
            return data['medias']['audio']

    # Strategy 4: Look for any field containing 'audio'
    for key, value in data.items():
        if 'audio' in key.lower() and isinstance(value, str) and value.startswith('http'):
            print(f"✅ Found audio URL in field: {key}")
            return value

    raise KeyError(f"Could not find audio URL in response. Available keys: {list(data.keys())}")


def download_instagram_reel(url: str) -> Tuple[str, str, str]:
    """
    Download Instagram Reel and extract audio

    Uses RapidAPI's Social Download All-in-One API to fetch reel data,
    then downloads the audio file to a temporary location.

    Args:
        url: Instagram Reel URL (e.g., "https://www.instagram.com/reel/...")

    Returns:
        Tuple of (caption, audio_file_path, audio_url)
        - caption: Reel caption/title
        - audio_file_path: Local path to downloaded audio file
        - audio_url: Original audio URL from API

    Raises:
        Exception: If RapidAPI request fails or audio extraction fails

    Example:
        caption, audio_path, audio_url = download_instagram_reel(
            "https://www.instagram.com/reel/ABC123/"
        )
        print(f"Caption: {caption}")
        print(f"Audio saved to: {audio_path}")
    """
    print(f"📥 Downloading Instagram Reel: {url}")

    try:
        # RapidAPI configuration
        rapidapi_config = {
            "url": "https://social-download-all-in-one.p.rapidapi.com/v1/social/autolink",
            "headers": {
                "x-rapidapi-key": settings.rapidapi_key,
                "x-rapidapi-host": "social-download-all-in-one.p.rapidapi.com",
                "Content-Type": "application/json"
            }
        }

        # Make request to RapidAPI
        payload = {"url": url}
        response = requests.post(
            rapidapi_config["url"],
            json=payload,
            headers=rapidapi_config["headers"],
            timeout=30
        )

        print(f"RapidAPI response status: {response.status_code}")

        if response.status_code != 200:
            raise Exception(f"RapidAPI request failed with status {response.status_code}: {response.text}")

        data = response.json()

        # Extract caption
        caption = (
            data.get('title', '') or
            data.get('caption', '') or
            data.get('description', '') or
            'No Caption Found'
        )
        print(f"✅ Caption extracted: {caption[:100]}{'...' if len(caption) > 100 else ''}")

        # Extract audio URL
        audio_url = extract_audio_url(data)
        print(f"✅ Audio URL: {audio_url}")

        # Download audio file
        print("📥 Downloading audio file...")
        audio_response = requests.get(audio_url, timeout=60)

        if audio_response.status_code != 200:
            raise Exception(f"Audio download failed with status {audio_response.status_code}")

        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_audio:
            temp_audio.write(audio_response.content)
            audio_path = temp_audio.name

        file_size_mb = len(audio_response.content) / (1024 * 1024)
        print(f"✅ Audio downloaded successfully: {audio_path}")
        print(f"   File size: {file_size_mb:.1f}MB")

        return caption, audio_path, audio_url

    except requests.exceptions.Timeout:
        raise Exception("Request timed out. The Instagram server might be slow or the reel might be unavailable.")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error while downloading reel: {str(e)}")
    except KeyError as e:
        raise Exception(f"Failed to extract audio from response: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to download Instagram reel: {str(e)}")
