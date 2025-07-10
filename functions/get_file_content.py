import os

def get_file_content(working_directory, file_path):
     abs_new_dir = os.path.abspath(working_directory)
     abs_new_path = os.path.abspath(os.path.join(working_directory, file_path))
     if not abs_new_path.startswith(abs_new_dir):
         return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
     if not os.path.isfile(abs_new_path):
          return f'Error: File not found or is not a regular file: "{file_path}"'
     MAX_CHARS = 10000
     try:
        with open(abs_new_path, "r") as a:
            file_content_string = a.read(MAX_CHARS)
            next_char = a.read(1)
            if next_char:
                return file_content_string + f'[...File "{file_path}" truncated at 10000 characters]'
            else:
                return file_content_string
     except Exception as e:
         return f"Error: {str(e)}"