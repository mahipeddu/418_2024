from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import os
import time
from preprocessing import main_preprocessing
from algos import solve_maze_and_draw_path

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER


def solve(input_path, output_folder):
    start = time.time()
    main_preprocessing(input_path, 100)
    output_path = os.path.join(output_folder, 'final.png')
    trav, dist = solve_maze_and_draw_path("processed.png", output_path)
    end = time.time()
    return trav, end - start, dist


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        output_folder = app.config['PROCESSED_FOLDER']
        file.save(input_path)
        t1, t2,t3 = solve(input_path, output_folder)
        return redirect(url_for('processed_file', filename='final.png', t1=t1, t2=t2,t3=t3))
    else:
        return "Invalid file format"


@app.route('/processed/<filename>')
def processed_file(filename):
    t1 = request.args.get('t1')
    t2 = request.args.get('t2')
    t3 = request.args.get('t3')
    return render_template('processed.html', filename=filename, t1=t1, t2=t2,t3=t3)


if __name__ == '__main__':
    app.run(debug=True)
