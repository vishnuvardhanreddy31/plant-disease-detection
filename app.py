import os
import requests
import json
import base64
from flask import Flask, render_template, request
import colorama

app = Flask(__name__)

# Get API key from Plant.id
api_key = 'Qer6421Qea0VPLoKBHQVzpeWGGPVJcqX8Lf7bgCjxP8BZMXIUv'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    # Read image file uploaded by the user
    file = request.files['file']
    image_data = file.read()

    # Encode image data in base64
    encoded_image_data = base64.b64encode(image_data).decode('utf-8')

    # Create JSON payload for API request
    payload = {
        'api_key': api_key,
        'images': [encoded_image_data],
        'modifiers': ['crops_fast', 'similar_images'],
        'language': 'en',
        'disease_details': ['cause', 'common_names', 'classification', 'description', 'treatment', 'url']
    }

    # Send request to Plant.id API
    url = 'https://api.plant.id/v2/health_assessment'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Display API response
    if response.ok:
        response_data = json.loads(response.content)
        name = response_data['health_assessment']['diseases'][0]['name']
        description = response_data['health_assessment']['diseases'][0]['disease_details']['description']
        chemical_treatments = response_data['health_assessment']['diseases'][0]['disease_details']['treatment']['chemical']
        biological_treatments = response_data['health_assessment']['diseases'][0]['disease_details']['treatment']['biological']
        preventive_measures = response_data['health_assessment']['diseases'][0]['disease_details']['treatment']['prevention']

        return render_template('result.html', name=name, description=description, chemical_treatments=chemical_treatments, biological_treatments=biological_treatments, preventive_measures=preventive_measures)

    else:
        return f"Error {response.status_code}: {response.reason}"

if __name__ == '__main__':
    app.run(debug=True)
