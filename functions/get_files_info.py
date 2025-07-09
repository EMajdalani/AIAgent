import os


def get_files_info(working_directory, directory=None):
    if directory is None:
        directory = "."

    resolved_path = os.path.abspath(os.path.join(working_directory, directory))

    if not resolved_path.startswith(os.path.abspath(working_directory)):
        return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"
    
    if not os.path.isdir(resolved_path):
        return f"Error: \"{directory}\" is not a directory" 

    try:
        file_list = os.listdir(resolved_path)
    except Exception as e:
        return f"Error: Cannot list contents of directory \"{directory}\": {e}"
    
    dir_contents = ""
    for file in file_list:
        file_name = file
        file_path = os.path.join(resolved_path, file)
        try:
            file_size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
        except Exception as e:
            continue
        dir_contents += f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}\n"
    refined_dir_contents = dir_contents.rstrip("\n")

    return refined_dir_contents