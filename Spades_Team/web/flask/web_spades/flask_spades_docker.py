# pip install flask
# pip3 install flask-bootstrap
# pip3 install flask-bootstrap4
# pip install flask-wtf Flask-SQLAlchemy

from flask import Flask, render_template, request, jsonify, redirect, url_for,send_from_directory

from flask_bootstrap import Bootstrap

import os




app = Flask(__name__) #建立 Flask 物件
# app.config['UPLOAD_FOLDER'] = upload_dir # user 上傳照片的存檔路徑
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

bootstrap = Bootstrap(app)   #建立 bootstrap 物件


@app.route('/')
def my_index():

    return render_template('index.html')

@app.route('/sign_up')
def sign_up():

    return render_template('sign_up.html')

@app.route('/action_number.php',methods=['GET'])
def action_number():
    name = request.args.get('username')

    return render_template('load_pic.html',username = name)

@app.route('/load_pic',methods=['GET','POST'])
def load_pic():
    return render_template('index.html')


@app.route('/upload',methods=['GET','POST'])
def action_load_pic():
    # user 上傳照片的存檔路徑
    upload_dir = r'/code/flask/web_spades/static'

    if request.method == 'POST':
        uploaded_files = request.files.getlist("file[]")
        global filenames
        filenames = []

        for file in uploaded_files:

            filename = file.filename
            file.save(upload_dir+"/"+filename)
            filenames.append(filename)

    print('filenames',filenames)
    return render_template('confirm.html',filenames=filenames)







if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)