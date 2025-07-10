import os
import subprocess

def run_python_file(working_directory, file_path):
    if file_path is None:
        return "Error: No file path given."
    
    resolved_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not resolved_path.startswith(os.path.abspath(working_directory)):
        return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"
    
    if not os.path.exists(resolved_path):
        return f"Error: File \"{file_path}\" not found."
    
    if not resolved_path.endswith(".py"):
        return f"Error: \"{file_path}\" is not a Python file."
    
    try:
        result = subprocess.run(["python3", resolved_path], capture_output=True, timeout=30, check=True)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    if result is None:
        output_msg = "No output produced."
    else:
        output_msg = ""
    
    if result.returncode != 0:
        return_code = f"Process exited with code {result.returncode}"
    else:
        return_code = ""

    output = f"STDOUT: {result.stdout.decode()}\nSTDERR: {result.stderr.decode()}\n{return_code}\n{output_msg}"

    final_output = output.rstrip("\n")

    return final_output