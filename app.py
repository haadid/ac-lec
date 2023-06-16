import cv2
import numpy as np
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/detect', methods=['POST'])
def detect():
    if 'image' in request.files:
        image = request.files['image']
        img = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_COLOR)
        resized_img = cv2.resize(img, (224, 224))
        preprocessed_img = np.expand_dims(resized_img, axis=0)
        
        url = 'http://localhost:8601/v1/models/acne:predict'
        headers = {'Content-Type': 'application/json'}
        data = {'instances': preprocessed_img.tolist()}
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            predictions = response.json()['predictions']
            num_acne = len(predictions)
            acne_level = determine_acne_level(num_acne)
            return jsonify({'num_acne': num_acne, 'acne_level': acne_level})

    return jsonify({'error': 'Invalid request'})

def determine_acne_level(num_acne):
    if num_acne == 0:
        return 'Clean'
    elif num_acne <= 4:
        return 'Mild'
    elif num_acne <= 7:
        return 'Severe'
    else:
        return 'Very Severe'

if __name__ == '__main__':
    app.run()
