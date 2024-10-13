import os
from flask import Flask, request, jsonify, send_file
from gemini_util import upload_to_gemini, chat_session

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
  if not file_path or not os.path.exists(file_path):
    return jsonify({'error': 'Invalid file path'}), 400

  # Simulate the response from OpenAI API: ?processed=true
  processed_file_path = file_path

  return send_file(processed_file_path, mimetype='image/jpeg')
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

