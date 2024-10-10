import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Get a list of uploaded files
uploaded_files = dict()
for file in genai.list_files():
  uploaded_files[file.display_name] = file

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
  system_instruction="Your response should contain only one integer to indicate the pose image number (for example, if your answer is Image 1, you would simply response me with 1). You shall not example the choice for me.",
)

files = [
  upload_to_gemini("./assets/pose/1.png", mime_type="image/png"),
  upload_to_gemini("./assets/pose/2.png", mime_type="image/png"),
  upload_to_gemini("./assets/pose/3.png", mime_type="image/png"),
  upload_to_gemini("./assets/pose/4.png", mime_type="image/png"),
  upload_to_gemini("./assets/pose/5.png", mime_type="image/png"),
  upload_to_gemini("./assets/pose/6.png", mime_type="image/png"),
  upload_to_gemini("./assets/pose/7.png", mime_type="image/png"),
  upload_to_gemini("./assets/pose/8.png", mime_type="image/png"),
  upload_to_gemini("./assets/pose/9.png", mime_type="image/png"),
  upload_to_gemini("./assets/pose/10.png", mime_type="image/png"),
  upload_to_gemini("./assets/pose/11.png", mime_type="image/png"),
  upload_to_gemini("./assets/pose/12.png", mime_type="image/png"),
  upload_to_gemini("./assets/pose/13.png", mime_type="image/png"),
  upload_to_gemini("./assets/pose/14.png", mime_type="image/png"),
  upload_to_gemini("./assets/pose/15.png", mime_type="image/png"),
  upload_to_gemini("./assets/pose/16.png", mime_type="image/png"),
  upload_to_gemini("./assets/pose/17.png", mime_type="image/png"),
  upload_to_gemini("./assets/pose/18.png", mime_type="image/png"),
  upload_to_gemini("./assets/pose/19.png", mime_type="image/png"),
  upload_to_gemini("./assets/pose/20.png", mime_type="image/png"),
  upload_to_gemini("./assets/pose/21.png", mime_type="image/png"),
  upload_to_gemini("./assets/input_screen/input_screen.jpg", mime_type="image/jpeg"),
]

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
        files[7],
        files[8],
        files[9],
        files[10],
        files[11],
        files[12],
        files[13],
        files[14],
        files[15],
        files[16],
        files[17],
        files[18],
        files[19],
        files[20],
        "Here's 21 pose images, they are used to be overlapped on an user's camera to help them posing when taking photos. They are indexed with Image 1 to Image 21. In each pose image, there are white lines that show an example posing, and the rest of the picture are leaved blank/transparent. I want you to remember these 21 pose images, analyze and response me with their posing features (for example, Image 1: standing, man in the middle, left hand behind the head). Later, on the following prompts, I would give you one current camera view photo on each one prompt. You have to response me with the most suitable posing image number you choose according to the current camera view photo. Your response should contain only one integer to indicate the pose image number (for example, if your answer is Image 1, you would simply response me with 1). You shall not example the choice for me.",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Okay, I've seen the 21 pose images and have analyzed their features. I'm ready for the camera view photos. Please provide them one at a time, and I'll respond with the most suitable pose image number. I will only respond with a single integer indicating the image number. \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        files[21],
        "Here is one current camera view photo. Respond me with the most suitable pose image number.",
      ],
    },
    {
      "role": "model",
      "parts": [
        "10\n",
      ],
    },
  ]
)

# =============================================================================

from flask import Flask, request, jsonify
import random

# Set up the Flask app
app = Flask(__name__)

# Directory to save uploaded images
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
  os.makedirs(UPLOAD_FOLDER)

@app.route('/upload-image', methods=['POST'])
def upload_image():
  if 'image' not in request.files:
    return jsonify({'error': 'No file part'}), 400

  file = request.files['image']
  if file.filename == '':
    return jsonify({'error': 'No selected file'}), 400

  if file:
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)  # Save the image to the server

    # Upload the image to Gemini
    file = upload_to_gemini(filepath, mime_type="image/jpeg")
    parts = [
        file,
        "Here is one current camera view photo. Respond me with the most suitable pose image number."
    ]
    response = chat_session.send_message(parts)

    return jsonify({'message': 'Image uploaded successfully', 'file_path': filepath, 'response': response.text}), 200

@app.route('/random-number', methods=['GET'])
def get_random_number():
  number = random.choice([0, 1, 2])
  
  parts = [
    files[21],
    "Here is one current camera view photo. Respond me with the most suitable pose image number."
  ]
  response = chat_session.send_message(parts)

  return jsonify({"random_number": number, "response": response.text})
  return jsonify({"random_number": number})

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=False)  # Set host to '0.0.0.0'

