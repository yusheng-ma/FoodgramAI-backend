import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Get a list of uploaded files
uploaded_files = dict()
for file in genai.list_files():
  uploaded_files[file.display_name] = file

# Uploader function
def upload_to_gemini(path, mime_type=None):
  display_name = os.path.basename(path)

  if display_name in uploaded_files:
    print(f"File '{display_name}' already exists in Gemini.")
    return uploaded_files[display_name]
  
  file = genai.upload_file(path, mime_type=mime_type, display_name=display_name)
  print(f"Uploaded file '{file.name}'({file.display_name}) as: {file.uri}")
  return file

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # system_instruction=''
)

files = [
  upload_to_gemini("./assets/milk/1.png", mime_type="image/png"),
  upload_to_gemini("./assets/milk/2.png", mime_type="image/png"),
  upload_to_gemini("./assets/milk/3.png", mime_type="image/png"),
  upload_to_gemini("./assets/milk/4.png", mime_type="image/png"),
  upload_to_gemini("./assets/milk/5.png", mime_type="image/png"),
  upload_to_gemini("./assets/milk/6.png", mime_type="image/png"),
  upload_to_gemini("./assets/milk/7.png", mime_type="image/png"),
]

def ai_overlay_number(file_path):
  chat_session = model.start_chat(
    history=[
      {
        "role": "user",
        "parts": [
          files[0],
          files[1],
          files[2],
          files[3],
          files[4],
          files[5],
          files[6],
          "Here's posing 7 images, they are used to be overlapped on an user's camera to help them posing when taking photos. They are indexed with Image 1 to Image 7. In each image, there are white lines that show an example posing, and the rest of the picture are leaved blank/transparent. I want you to remember these 7 posing images, analyze and response me with their posing features (for example, Image 1: two people sitting side by side, drink close to their head).",
        ],
      },
      {
        "role": "model",
        "parts": [
          "Image 1: two people sitting side by side, drink close to their head\nImage 2: one person with one arm raised, holding a drink\nImage 3: one person sitting, holding a drink \nImage 4: one person standing, holding a drink in one hand, the other hand is on their hip\nImage 5: two people sitting side by side, drink close to their head\nImage 6: one person sitting, holding a drink \nImage 7: one person sitting, holding a drink",
        ],
      },
      {
        "role": "user",
        "parts": [
          "Later, on the following prompts, I would give you one current camera view photo on each one prompt. You have to response me with the most suitable posing image number you choose according to the current camera view photo. Your response should contain only one integer to indicate the pose image number (for example, if your answer is Image 1, you would simply response me with 1). You shall not explain the choice for me. If you understand, tell me again what I just mentioned to you.",
        ],
      },
      {
        "role": "model",
        "parts": [
          "You will give me a camera view photo for each prompt, and I will respond with the most suitable posing image number (from 1 to 7) based on the photo. I will not explain my choice. \n",
        ],
      },
    ]
  )

  gemini_file = upload_to_gemini(file_path, mime_type="image/jpeg")
  message_parts = [
    gemini_file,
    "Here is one current camera view photo. Respond me with the most suitable pose image number."
  ]
  response = chat_session.send_message(message_parts)
  return response.text