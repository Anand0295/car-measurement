from flask import Flask, request, jsonify
from flask_cors import CORS
import tempfile
import base64
import os
from measurement import measure_car

app = Flask(__name__)
CORS(app)

@app.route('/measure', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image'}), 400
    
    file = request.files['image']
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
        file.save(temp_file.name)
        temp_path = temp_file.name
    
    result = measure_car(temp_path)
    
    if result and result['image_path'] and os.path.exists(result['image_path']):
        with open(result['image_path'], 'rb') as img_file:
            img_data = base64.b64encode(img_file.read()).decode('utf-8')
            result['image_base64'] = f'data:image/jpeg;base64,{img_data}'
        
        try:
            os.unlink(result['image_path'])
        except:
            pass
    
    try:
        os.unlink(temp_path)
    except:
        pass
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=False, port=5001)
