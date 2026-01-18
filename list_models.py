import google.generativeai as genai
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent / 'backend' / '.env'
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("API Key not found!")
else:
    genai.configure(api_key=api_key)
    print("Available models:")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)
    except Exception as e:
        print(f"Error listing models: {e}")
