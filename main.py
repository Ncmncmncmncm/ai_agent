import os
from dotenv import load_dotenv
import sys
from google import genai
from google.genai import types


from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file_content import schema_write_file
from functions.run_python import schema_run_python_file


load_dotenv()
api_key = os.environ.get('GEMINI_API_KEY')
from google import genai

client = genai.Client(api_key=api_key)

if len(sys.argv) < 2:
    print("Error: No prompt provided.")
    sys.exit(1)

prompt = sys.argv[1]

is_verbose = "--verbose" in sys.argv

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
model_name = "gemini-1.5-flash"
messages = [{"role": "user", "parts": [{"text": prompt}]}]

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)

config=types.GenerateContentConfig(
    tools=[available_functions], 
    system_instruction=system_prompt
)

response = client.models.generate_content(
    model = model_name,
    contents = messages,
    config=config,
)

if is_verbose == True:
    print("User prompt:", prompt)
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

# Check if the response contains function calls
if response.function_calls:
    # Loop through each function call (there might be multiple)
    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
else:
    # If no function calls, print the text response as normal
    print(response.text)

