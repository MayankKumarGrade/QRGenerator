from flask import Flask, render_template, request
from waitress import serve
import qrcode
from PIL import Image
from io import BytesIO
from base64 import b64encode

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def generate():
    text = request.form.get('text')
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    
    qr.add_data(text)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="#000000", back_color="#CBDCCB")  # Create QR code with white background
    
    img = img.convert("RGBA")  # Convert the image to RGBA format
    datas = img.getdata()  # Get image data

    new_data = []
    for item in datas:
        # change all white (also shades of whites)
        # pixels to transparent
        if item[0] in list(range(200, 256)):
            new_data.append((255, 255, 255, 128))  # adding transparency
        else:
            new_data.append(item)
            
    img.putdata(new_data)  # Update image data
    
    byte_io = BytesIO()
    img.save(byte_io, 'PNG')
    byte_io.seek(0)
    
    img_b64 = b64encode(byte_io.getvalue()).decode('utf-8')
    
    return render_template('index.html', img_b64=img_b64)

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8000)