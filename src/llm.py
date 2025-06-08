
from google import genai
import requests 

def get_gemini_response(api_key: str, prompt: str) -> str:
    """Fetches a response from Google Gemini AI."""
    client = genai.Client(api_key=api_key)
    
    response = client.models.generate_content(contents=prompt, model="gemini-2.0-flash")
    
    if response and response.text:
        return response.text
    else:
        return "No response from Gemini AI."
