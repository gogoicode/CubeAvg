from flask import Flask, request, jsonify
from PIL import Image
import Text_extract  # This is your custom logic file

app = Flask(__name__)

@app.route('/process-image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    image = Image.open(image_file.stream)
    print("Image received!")


    # Call your processing function from your_processing_script.py
    result = Text_extract.process(image)

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
