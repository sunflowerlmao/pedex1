import random

from flask import Flask, render_template, request, redirect, url_for, current_app, send_from_directory
import os
from flask import jsonify
import time
import zipfile

app = Flask(__name__)
app.config['grafem'] = 'Графемы'
app.config['ieroglif'] = 'Иероглифы'
app.config['UPLOAD_FOLDER'] = 'uploads'

selected_images = []


@app.route('/', methods=['GET', 'POST'])
def index():
    images = os.listdir(app.config['grafem'])
    return render_template('index.html')

@app.route('/update_selected_images', methods=['POST'])
def update_selected_images():
    selected_images = request.get_json()['selectedImages']
    # Do something with the selected_images array, e.g., store it in a database or session
    return jsonify({'message': 'Selected images updated successfully'})
@app.route('/images', methods=['GET', 'POST'])
def images():
    # Get the list of filenames from the folder
    filenames = os.listdir("static/graf/")

    # Randomly select a subset of filenames


    # Render the HTML template with the filenames
    return render_template('images.html', filenames=filenames)
@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'POST' and request.files:
        graf = request.files["graf"]
        if graf.filename:
            graf.save(os.path.join(app.config['grafem'], graf.filename))
            with zipfile.ZipFile('Графемы/Графемы.zip', 'r') as zip_ref:
                zip_ref.extractall('static/graf/')
        ier = request.files["ier"]
        if ier.filename:
            ier.save(os.path.join(app.config['ieroglif'], ier.filename))
            with zipfile.ZipFile('Иероглифы/Иероглифы.zip', 'r') as zip_ref:
                zip_ref.extractall('static/ierog/')
        baza = request.files["baza"]
        if baza.filename:
            baza.save(os.path.join(app.config['UPLOAD_FOLDER'], baza.filename))
        shablon = request.files["shablon"]
        if shablon.filename:
            shablon.save(os.path.join(app.config['UPLOAD_FOLDER'], shablon.filename))
        return redirect(url_for('success'))

    return render_template('download.html')


@app.route('/success', methods=['GET', 'POST'])
def success():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True)
