import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if len(sys.argv) < 2:
        print("Please provide a prompt as a command line argument.")
        exit(1)
        return
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=sys.argv[1])])
    ]
    
    response = client.models.generate_content(
        model = "gemini-2.0-flash-001",
        contents = messages
    )

    metadata = response.usage_metadata
    response_tokens = metadata.candidates_token_count
    prompt_tokens = metadata.prompt_token_count


    print(response.text)

    if len(sys.argv) > 2:
        if sys.argv[2] == "--verbose":
            print(f"User prompt: {sys.argv[1]}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")

    return

main()

