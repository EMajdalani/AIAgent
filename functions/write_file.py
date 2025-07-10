import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites a file in the specified directory, constrained to the working directory. If the file doesn't exist, it's created and written.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to write files from, relative to the working directory. If not provided, writes files in the working directory itself.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to the file"
            )
        },
    ),
)

def write_file(working_directory, file_path, content):
    if content is None:
        return f"Error: No content submitted."
    
    if file_path is None:
        return f"Error: No file path submitted"
    
    resolved_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not resolved_path.startswith(os.path.abspath(working_directory)):
        return f"Error: Cannot write to \"{file_path}\" as it is outside the permitted working directory"
    
    try:
        if not os.path.exists(resolved_path):
            dir_list = resolved_path.split("/")[:-1]
            new_path = "/".join(dir_list)
            os.makedirs(new_path, mode=0o777, exist_ok=True)
    except Exception as e:
        f"Error: \"{file_path}\" could not be created {e}"

    try:
        with open (resolved_path, "w") as f:
            f.write(content)
            return f"Successfully wrote to \"{file_path}\" ({len(content)} characters written)"
    except Exception as e:
        f"Error: Write to \"{file_path}\" Unsuccessful. {e}"
    
    
    