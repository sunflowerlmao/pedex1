from flask import Flask, render_template, request, redirect, url_for
import os
import time
import zipfile

app = Flask(__name__)
app.config['grafem'] = 'Графемы'
app.config['ieroglif'] = 'Иероглифы'
app.config['UPLOAD_FOLDER'] = 'uploads'


@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')


@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'POST' and request.files:
        graf = request.files["graf"]
        if graf.filename:
            graf.save(os.path.join(app.config['grafem'], graf.filename))
            with zipfile.ZipFile('Графемы/Графемы.zip', 'r') as zip_ref:
                zip_ref.extractall('Графемы/')
        ier = request.files["ier"]
        if ier.filename:
            ier.save(os.path.join(app.config['ieroglif'], ier.filename))
            with zipfile.ZipFile('Иероглифы/Иероглифы.zip', 'r') as zip_ref:
                zip_ref.extractall('Иероглифы/')
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
