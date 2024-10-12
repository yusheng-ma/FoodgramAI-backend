from flask import Flask, request, jsonify
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

# Set up the Flask app
app = Flask(__name__)

# Directory to save uploaded images
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
  os.makedirs(UPLOAD_FOLDER)

@app.route('/save_image', methods=['POST'])
def save_image():
  if 'image' not in request.files:
    return jsonify({'error': 'No file part'}), 400

  uploaded_file = request.files['image']
  if uploaded_file.filename == '':
    return jsonify({'error': 'No selected file'}), 400

  if uploaded_file:
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
    uploaded_file.save(file_path)  # Save the image to the server
    return jsonify({'message': 'Image saved successfully', 'file_path': file_path}), 200

@app.route('/get_overlay_number', methods=['POST'])
def get_overlay_number():
  data = request.get_json()
  file_path = data.get('file_path')
  if not file_path or not os.path.exists(file_path):
    return jsonify({'error': 'Invalid file path'}), 400

  # Upload the image to Gemini
  gemini_file = upload_to_gemini(file_path, mime_type="image/jpeg")
  message_parts = [
    gemini_file,
    "Here is one current camera view photo. Respond me with the most suitable pose image number."
  ]
  response = chat_session.send_message(message_parts)

  return jsonify({'message': 'Get overlay number successfully', 'number': response.text}), 200

@app.route('/get_processed_image', methods=['POST'])
def get_processed_image():
  data = request.get_json()
  file_path = data.get('file_path') # for testing purpose, file_path is actually the image url
  # if not file_path or not os.path.exists(file_path):
  #   return jsonify({'error': 'Invalid file path'}), 400

  # Simulate the response from OpenAI API: ?processed=true
  response = file_path + "?processed=true"

  return jsonify({'message': 'Image processed successfully', 'response': response}), 200

@app.route('/get_caption', methods=['POST'])
def get_caption():
  data = request.get_json()
  text = data.get('text')
  if not text:
    return jsonify({'error': 'Invalid text input'}), 400

  # Simulate the response from OpenAI API
  caption = "這是 AI 生成的文案"
  return jsonify({'message': 'Caption generated successfully', 'caption': caption}), 200

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=False)  # Set host to '0.0.0.0'

