from flask import Flask, request, send_file, render_template_string
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def index():
    with open('remove_bg.html', 'r', encoding='utf-8') as f:
        return render_template_string(f.read())

@app.route('/remove-bg', methods=['POST'])
def remove_bg_route():
    try:
        if 'image' not in request.files:
            return 'No image uploaded', 400
        file = request.files['image']
        input_data = file.read()
        output_data = remove(input_data)
        output_image = Image.open(io.BytesIO(output_data))
        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    except Exception as e:
        print("Error processing image:", e)
        return f"Error processing image: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)