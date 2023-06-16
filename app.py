from flask import Flask, request, jsonify, render_template
import numpy as np
import cv2
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def preprocess_image(image):
    resized_image = cv2.resize(image, (224, 224))
    normalized_image = resized_image / 255.0
    preprocessed_image = np.expand_dims(normalized_image, axis=0)
    return preprocessed_image

def determine_acne_level(num_acne):
    if num_acne == 0:
        return 'Clean'
    elif num_acne <= 4:
        return 'Mild'
    elif num_acne <= 7:
        return 'Severe'
    else:
        return 'Very Severe'

@app.route('/detect', methods=['POST'])
def detect():
    image = request.files['image']
    image_data = image.read()
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    preprocessed_image = preprocess_image(img)

    url = 'http://localhost:8601/v1/models/acne:predict'
    headers = {'Content-Type': 'application/json'}
    data = {'instances': preprocessed_image.tolist()}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        predictions = response.json()['predictions']
        num_acne = len(predictions)
        acne_level = determine_acne_level(num_acne)
        return jsonify({'num_acne': num_acne, 'acne_level': acne_level})

    return jsonify({'error': 'Invalid request'})

if __name__ == '__main__':
    app.run()