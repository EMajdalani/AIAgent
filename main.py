import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    function_content = None
    MAX_STEPS = 20
    steps = 0
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

    When you have finished all requested tasks, respond with the phrase \"Task Complete\".
    """

    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
    )


    if len(sys.argv) < 2:
        print("Please provide a prompt as a command line argument.")
        exit(1)
        return
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=sys.argv[1])])
    ]
    try:
        while steps < MAX_STEPS:
            response = client.models.generate_content(
                model = "gemini-2.0-flash-001",
                contents = messages,
                config = types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
            )

            metadata = response.usage_metadata
            response_tokens = metadata.candidates_token_count
            prompt_tokens = metadata.prompt_token_count
            function_info = response.function_calls
            message_text = None

            if hasattr(response, "text") and response.text:
                message_text = response.text
            else:
                try:
                    message_text = response.candidates[0].content.parts[0].text
                except Exception:
                    pass
                

            if len(sys.argv) > 2:
                if sys.argv[2] == "--verbose":

                    for candidate in response.candidates:
                        messages.append(candidate.content)
                        if function_info is not None:
                            for function in function_info:
                                function_result = call_function(function, verbose=True)
                                messages.append(function_result)
                                try:
                                    function_content = function_result.parts[0].function_response.response
                                except Exception as e:
                                    return f"Error: No function output found {e}"
                        
                    if message_text:
                        print(message_text)

                    if function_info is not None:
                        print(f"-> {function_content}")

                    print(f"User prompt: {sys.argv[1]}")
                    print(f"Prompt tokens: {prompt_tokens}")
                    print(f"Response tokens: {response_tokens}")
            else:

                for candidate in response.candidates:
                    messages.append(candidate.content)
                    if function_info is not None:
                        for function in function_info:
                            function_result = call_function(function, verbose=False)
                            messages.append(function_result)
                            try:
                                function_content = function_result.parts[0].function_response.response
                            except Exception as e:
                                return f"Error: No function output found {e}"
                
                if message_text:
                    print(message_text)

                if function_info is not None:
                    print(f"-> {function_content}")
            
            if "task complete" in response.candidates[0].content.parts[0].text.lower():
                break
            
            steps += 1
    except Exception as e:
        return f"Error: Could not generate result {e}"
    
    return

main()

