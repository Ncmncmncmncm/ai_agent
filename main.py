import os
from dotenv import load_dotenv
import sys
from google import genai
from google.genai import types


from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file_content import schema_write_file
from functions.run_python import schema_run_python_file

from functions.call_function import call_function

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

done = False
for _ in range(20):
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=config,
    )

    for candidate in response.candidates:
        # If candidate.text exists, use it:
        if hasattr(candidate, "text") and candidate.text:
            part = {"text": candidate.text}
            messages.append(types.Content(role="model", parts=[part]))
            print(candidate.text)
            done = True
            break
        else:
            # Some candidates might have content as list of Parts or similar
            messages.append(candidate.content)
    if done:
        break

    # Check if the response contains function calls
    if response.function_calls:
        # Loop through each function call (there might be multiple)
        for function_call_part in response.function_calls:
            # Call your function, passing the command-line verbose flag
            function_call_result = call_function(function_call_part, verbose=is_verbose)

            messages.append(types.Content(role="tool", parts=function_call_result.parts))

            # Check the structure of the returned content
            if not (function_call_result and
                    function_call_result.parts and
                    len(function_call_result.parts) > 0 and
                    function_call_result.parts[0].function_response and
                    function_call_result.parts[0].function_response.response is not None):
                raise RuntimeError("Fatal error: function_call_result does not contain a valid function response.")

            # If verbose, print the result of the function call
            if is_verbose: # This is a simpler way to write if is_verbose == True
                print(f"-> {function_call_result.parts[0].function_response.response}")