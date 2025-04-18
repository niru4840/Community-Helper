from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max image size

donations = []

@app.route('/')
def index():
    return render_template('index.html', donations=donations)

@app.route('/donate', methods=['POST'])
def donate():
    name = request.form['name']
    contact = request.form['contact']
    address = request.form['address']
    item_name = request.form['item_name']
    description = request.form['description']
    image = request.files['image']

    # Validate contact number (10 digits)
    if not contact.isdigit() or len(contact) != 10:
        return "❌ Contact number must be exactly 10 digits.", 400

    # Save image securely
    image_filename = ""
    if image:
        image_filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
        image.save(image_path)

    # Add to donations
    donation = {
        'name': name,
        'contact': contact,
        'address': address,
        'item_name': item_name,
        'description': description,
        'image': image_filename,
        'status': 'Available'
    }
    donations.append(donation)

    return redirect(url_for('index'))

@app.route('/request_item/<int:item_index>')
def request_item(item_index):
    if 0 <= item_index < len(donations) and donations[item_index]['status'] == 'Available':
        donations[item_index]['status'] = 'Donated'
    return redirect(url_for('index'))

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
