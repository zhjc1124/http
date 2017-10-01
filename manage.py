from flask import Flask, request, url_for, redirect
from werkzeug.utils import secure_filename
import os
import opc
UPLOAD_FOLDER = '/home/ubuntu/http/static/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/get')
def get():
    return 'test for get!'


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request.form)
        file = request.files['file']
        file.save('test.jpg')
        opc.split()
        return '''
        <!doctype html>
        <img src="./1.jpg" />
        <img src="./2.jgp" />
        <img src="./3.jgp" />
        <img src="./4.jgp" />
        <img src="./5.jgp" />
        <img src="./6.jgp" />
        <img src="./7.jgp" />
        <img src="./8.jgp" />
        '''
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(port=8000)
