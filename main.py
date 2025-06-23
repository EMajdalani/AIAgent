import os
from dotenv import load_dotenv
from google import genai

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model = "gemini-2.0-flash-001",
        contents = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    )

    metadata = response.usage_metadata
    response_tokens = metadata.candidates_token_count
    prompt_tokens = metadata.prompt_token_count


    print(response.text)
    print(f"Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")

    return

main()

