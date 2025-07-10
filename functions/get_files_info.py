import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    path = os.path.join(working_directory, directory)
    abs_path = os.path.abspath(path)
    abs_dir = os.path.abspath(working_directory)
    if not abs_path.startswith(abs_dir):
          return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_path):
          return f'Error: "{directory}" is not a directory'
    try:
        list_path = os.listdir(abs_path)
        results = []
        for item in list_path:
            new_path = os.path.join(abs_path, item)
            size = os.path.getsize(new_path)
            dir = os.path.isdir(new_path)
            formatted_item = f"- {item}: file_size={size} bytes, is_dir={dir}"
            results.append(formatted_item)
        return "\n".join(results)
    except Exception as e:
        return f"Error: {str(e)}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


