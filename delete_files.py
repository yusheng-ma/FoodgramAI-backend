import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# List all files
for file in genai.list_files():
    print(f"{file.display_name}, URI: {file.uri}")
    # Delete file
    genai.delete_file(file.name)
    print(f'Deleted file {file.uri}')
