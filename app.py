# app.py
from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # セッションの秘密鍵
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['DATA_FILE'] = 'data.txt'  # テキスト情報を保存するファイル

# サンプルのユーザーデータ (実際にはデータベースを使用することが一般的)
users = {'admin': 'password'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif'}

# データをテキストファイルに保存
def save_to_file(data):
    with open(app.config['DATA_FILE'], 'a') as file:
        file.write(f"Name: {data['name']}\n")
        file.write(f"Email: {data['email']}\n")
        file.write(f"Message: {data['message']}\n")
        file.write(f"Image: {data['image']}\n\n")

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    image = request.files['image']

    if image and allowed_file(image.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(filename)
        data = {'name': name, 'email': email, 'message': message, 'image': image.filename}
        save_to_file(data)  # データをファイルに保存

    return "<h2>ありがとうございました。</h2>"

@app.route('/display')
def display():
    if 'user' in session:
        data_list = []  # ファイルからデータを読み取るリスト

    with open(app.config['DATA_FILE'], 'r') as file:
        data = {}
        for line in file:
            if line.strip():  # 空行を無視
                key, value = line.strip().split(": ", 1)
                data[key] = value
            elif data:
                data_list.append(data)
                data = {}

    return render_template('display.html', data=data_list)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['user'] = username
            return redirect('/display')
        else:
            return "Invalid username or password"

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
