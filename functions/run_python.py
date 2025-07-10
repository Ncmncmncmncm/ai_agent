import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_new_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_new_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_new_path):
        return f'Error: File "{file_path}" not found.'
    if not os.path.splitext(abs_new_path)[1] == ".py":
        return f'Error: "{file_path}" is not a Python file.'
    try:
        result = subprocess.run(["python3", abs_new_path], timeout=30, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=abs_working_dir)

        stdout_text = result.stdout.decode()
        stderr_text = result.stderr.decode()
        status_code = result.returncode

        if stdout_text == "" and stderr_text == "":
            return "No output produced"
        if status_code != 0:
            return f"Process exited with code {status_code}"
        output = f"STDOUT:{stdout_text}\nSTDERR:{stderr_text}"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute specific python file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the specific Python file to execute.",
            ),
        },
    ),
)