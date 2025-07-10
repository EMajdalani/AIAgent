import os

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
    
    
    