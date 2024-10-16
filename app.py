import os
from flask import Flask, request, jsonify, send_file
from gemini_util import ai_overlay_number, ai_generate_caption, ai_pick_overlay_image, ai_choose_warm_tone_parameter, ai_generate_caption_with_audio
from image_util import convert_to_warm_tone

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

@app.route('/save_audio', methods=['POST'])
def save_audio():
  if 'audio' not in request.files:
    return jsonify({'error': 'No file part'}), 400

  uploaded_file = request.files['audio']
  if uploaded_file.filename == '':
    return jsonify({'error': 'No selected file'}), 400

  if uploaded_file:
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
    uploaded_file.save(file_path)  # Save the audio file to the server
    return jsonify({'message': 'Audio saved successfully', 'file_path': file_path}), 200
  
# will no longer use it? maybe?
@app.route('/get_overlay_number', methods=['POST'])
def get_overlay_number():
  data = request.get_json()
  file_path = data.get('file_path')
  if not file_path or not os.path.exists(file_path):
    return jsonify({'error': 'Invalid file path'}), 400

  number = ai_overlay_number(file_path)  # Get the overlay number from Gemini

  return jsonify({'message': 'Get overlay number successfully', 'number': number}), 200

@app.route('/get_overlay_image', methods=['POST'])
def get_overlay_image():
  data = request.get_json()
  file_path = data.get('file_path')
  category = data.get('category')
  # for testing purpose, file_path is actually the image url
  if not file_path or not os.path.exists(file_path):
    return jsonify({'error': 'Invalid file path'}), 400

  overlay_image_file_paths = ai_pick_overlay_image(file_path, category)  # Pick an overlay image from Gemini
  # there are three files
  
  return jsonify({'message': 'Overlay image picked successfully', 'overlay_image_file_paths': overlay_image_file_paths}), 200

@app.route('/get_processed_image', methods=['POST'])
def get_processed_image():
  data = request.get_json()
  file_path = data.get('file_path') # for testing purpose, file_path is actually the image url
  if not file_path or not os.path.exists(file_path):
    return jsonify({'error': 'Invalid file path'}), 400

  # Convert it to warm tone, and be saved and returned the processed file path
  # processed_file_path = convert_to_warm_tone(file_path)
  warm_tone_parameters = ai_choose_warm_tone_parameter(file_path)
  print(warm_tone_parameters)
  processed_file_path = convert_to_warm_tone(file_path, warm_tone_parameters['brightness'], warm_tone_parameters['contrast'])

  return send_file(processed_file_path, mimetype='image/jpeg')

@app.route('/get_caption', methods=['POST'])
def get_caption():
  data = request.get_json()
  store_name = data.get('storeName')
  items = data.get('items')
  review = data.get('review')

  if not store_name or not items or not review:
    return jsonify({'error': 'Invalid input'}), 400

  caption = ai_generate_caption(store_name, items, review)  # Get the caption from Gemini
  return jsonify({'message': 'Caption generated successfully', 'caption': caption}), 200

@app.route('/get_caption_from_audio', methods=['POST'])
def get_caption_from_audio():
  data = request.get_json()
  audio_file_path = data.get('file_path')  # Get the audio file path from the request

  if not audio_file_path:
    return jsonify({'error': 'Invalid input, file_path missing'}), 400

  # Process the audio file here (e.g., use an audio processing or transcription service)
  caption = ai_generate_caption_with_audio(audio_file_path)  # Your custom function to get caption

  return jsonify({'message': 'Caption generated successfully', 'caption': caption}), 200

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=False)  # Set host to '0.0.0.0'

