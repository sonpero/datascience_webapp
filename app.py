import pandas as pd
import time
from flask import Flask, render_template, request, send_file, Response

# a predict function
def predict(dataset, name):
    dataset.to_csv(name + '_predict.csv', sep=',')
    return

app = Flask(__name__)

x = 0
go = False
file_name = ''


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_file():
    global file_name
    global go

    uploaded_file = request.files['file']
    file_name = uploaded_file.filename

    if file_name != '':
        go = True
        uploaded_file.save(file_name)
    return ('', 204)


@app.route('/progress')
def progress():
    def generate():
        global x
        global go
        global file_name

        if go:
            x = 10
            yield "data:" + str(x) + "\n\n"
            time.sleep(2)
            ds = pd.read_csv(file_name, sep=';')
            x = 20
            yield "data:" + str(x) + "\n\n"
            time.sleep(2)
            predict(ds, file_name[:-4])
            x = 100
            yield "data:" + str(x) + "\n\n"
            go = False

        yield "data:" + str(x) + "\n\n"
    return Response(generate(), mimetype='text/event-stream')


@app.route('/download')
def download():
    return send_file(file_name[:-4] + '_predict.csv', as_attachment=True)
