import os
import google.generativeai as genai
from flask import Flask, jsonify
import random

GOOGLE_API_KEY = os.environ.get('GEMINI_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

# model = genai.GenerativeModel('gemini-1.5-flash')

# response = model.generate_content("What is the meaning of life?")

# print(response.text)

app = Flask(__name__)

@app.route('/random-number', methods=['GET'])
def get_random_number():
    number = random.choice([0, 1, 2])
    return jsonify({"random_number": number})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Set host to '0.0.0.0'

