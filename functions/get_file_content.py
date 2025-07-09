import os
from functions.config import *


def get_file_content(working_directory, file_path):
    if file_path is None:
        return f"Error: Input valid file path"
    
    resolved_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not resolved_file_path.startswith(os.path.abspath(working_directory)):
        return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"
    
    if not os.path.isfile(resolved_file_path):
        return f"Error: File not found or is not a regular file: \"{file_path}\""
    
    try:
        with open(resolved_file_path, "r") as f:
            file_content_string = f.read()
            if len(file_content_string) > MAX_CHARS:
                trunc_content_string = file_content_string[0:MAX_CHARS]
                return f"{trunc_content_string}[... File \"{file_path}\" truncated at 10000 characters]"
            else:
                return file_content_string
    except Exception as e:
        return f"Error: \"{file_path}\" cannot be opened {e}"  
