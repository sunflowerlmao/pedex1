import random
from flask import Flask, render_template, request, redirect, url_for, current_app, send_from_directory, session
import os
from flask import jsonify
import zipfile

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'

selected_filenames = []
bd = []
zadach = ['','']

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/images', methods=['GET', 'POST'])
def images():
    bdload()
    filenames = os.listdir("static/graf/")
    if len(selected_filenames) != 0:
        fn = sortir(selected_filenames)
    else:
        fn = filenames
    filenamesier = os.listdir('static/ierog')
    random_index = random.randint(0, len(filenamesier) - 1)
    random_ier = filenamesier[random_index]
    foundindex(random_ier)
    print(bd)
    print(zadach)
    print(selected_filenames)
    print(sortir(selected_filenames))
    return render_template('images.html', filenames=fn, random_image=random_ier)


def foundindex(a):
    for i in range(len(bd)):
        if bd[i][0] == a[:-4]:
            zadach[0] = bd[i][0]
            zadach[1] = bd[i][1]
def selfile(a):
    cor = []
    for i in range(len(a)):
        cor.append(a[i][:-4])
    return cor


def sortir(a):
    b = selfile(a)
    dostup = []
    for i in range(0,len(bd)-1):
        if all(elem in bd[i][1] for elem in b):
            for elem in bd[i][1]:
                if (elem+'.png') not in dostup:
                    dostup.append(elem+".png")

    return dostup



@app.route('/get_filenames', methods=['GET'])
def get_filenames():
    filenames = []
    for f in os.listdir("static/graf/"):
        if f not in selected_filenames:
            filenames.append(f)
    return jsonify({'filenames': filenames})


@app.route('/add_to_array', methods=['POST'])
def add_to_array():
    data = request.get_json()
    filename = data['filename']
    is_checked = data['is_checked']
    if is_checked:
        print(selected_filenames)
        if filename in selected_filenames:
            selected_filenames.remove(filename)
            print('r ',selected_filenames)
            return jsonify({'status': 'success'})
        elif filename not in selected_filenames:
            selected_filenames.append(filename)
            print('a ',selected_filenames)
            return jsonify({'status': 'success'})
    return jsonify({'status': 'error'})

@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'POST' and request.files:
        graf = request.files["graf"]
        if graf.filename:
            graf.save(os.path.join(app.config['UPLOAD_FOLDER'], graf.filename))
            with zipfile.ZipFile('uploads/Графемы.zip', 'r') as zip_ref:
                zip_ref.extractall('static/graf/')
        ier = request.files["ier"]
        if ier.filename:
            ier.save(os.path.join(app.config['UPLOAD_FOLDER'], ier.filename))
            with zipfile.ZipFile('uploads/Иероглифы.zip', 'r') as zip_ref:
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
    bdload()
    return render_template('success.html')


def bdload():
    database = open('uploads/database.txt', 'r')
    db = [x.split(':') for x in database]
    for i in range(len(db)):
        db[i][1] = db[i][1][:-1]
        db[i][1] = db[i][1].split(',')
        bd.append(db[i])

    database.close()


@app.route('/add_to_array_server', methods=['POST'])
def add_to_array_server():
    data = request.get_json()
    filename = data['filename']
    if filename not in selected_filenames:
        selected_filenames.append(filename)
        print('a ',selected_filenames)
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'})



@app.route('/remove_from_array_server', methods=['POST'])
def remove_from_array_server():
    data = request.get_json()
    filename = data['filename']
    if filename in selected_filenames:
        selected_filenames.remove(filename)
        print('r ',selected_filenames)
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'})


@app.route('/clear', methods=['GET', 'POST'])
def clear():
    q = 'static/graf'
    w = 'static/ierog'
    e = 'uploads/'
    files_to_remove = [os.path.join(q, f) for f in os.listdir(q)]
    for f in files_to_remove:
        os.remove(f)
    files_to_remove = [os.path.join(w, f) for f in os.listdir(w)]
    for f in files_to_remove:
        os.remove(f)
    files_to_remove = [os.path.join(e, f) for f in os.listdir(e)]
    for f in files_to_remove:
        os.remove(f)
    return render_template('clear.html')


if __name__ == '__main__':
    app.run(debug=True)
