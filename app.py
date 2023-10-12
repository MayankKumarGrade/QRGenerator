from flask import Flask, render_template, request
from waitress import serve
import qrcode
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
    
    img = qr.make_image(fill_color="white", back_color="transparent")  # Changed colors here
    
    byte_io = BytesIO()
    img.save(byte_io, 'PNG')
    byte_io.seek(0)
    
    img_b64 = b64encode(byte_io.getvalue()).decode('utf-8')
    
    return render_template('index.html', img_b64=img_b64)

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8000)
