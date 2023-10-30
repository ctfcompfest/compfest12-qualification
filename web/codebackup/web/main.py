import hashlib
import os
import random
import string
import time

from flask import Flask, request, render_template, render_template_string, session, redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.utils import secure_filename

from lib.config import CONFIG
from lib.myrandom import MyRandom
from lib.security import EncryptDecrypt, sanitize_content, check_path
from lib.utils import generate_user_id, init_user_dir, get_dir_info

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["30000 per hour"],
)

app.secret_key = bytes(CONFIG['FLASK_SECRET'], encoding = 'utf-8')
app.config['UPLOAD_DIR'] = os.path.join(CONFIG['FLASK_PATH'], 'uploads/{userId}/')
app.config['MAX_CONTENT_LENGTH'] = 1024

ED = EncryptDecrypt(CONFIG['FLASK_RSAKEY'])
SECRET_NUMBER = int(app.secret_key.hex()[:16], 16)

def generate_filename(last):
    rnd = MyRandom(8)
    x = rnd.next(last)
    session['enc_last'] = ED.encrypt(str(x))
    return hashlib.md5(str(x).encode()).hexdigest()


@app.route('/')
def index():
    if 'id' not in session:
        seed = int(time.time()) + SECRET_NUMBER
        rnd = MyRandom(8, seed)
        user_id = generate_user_id(16)
         
        session['id'] = user_id
        session['enc_last'] = ED.encrypt(str(rnd.state))
        init_user_dir(app.config['UPLOAD_DIR'].format(userId = session['id']))
    
    user_dir = app.config['UPLOAD_DIR'].format(userId = session['id'])
    try:
        dir_info = get_dir_info(user_dir)
    except StopIteration:
        session.clear()
        return redirect('/')
        
    return render_template('index.html', id = session['id'], dir = dir_info)


@app.route('/upload', methods=['POST'])
def upload_files():
    if 'id' in session and 'file' in request.files:
        user_dir = app.config['UPLOAD_DIR'].format(userId = session['id'])
        file_upload = request.files['file']
        
        try:
            dir_info = get_dir_info(user_dir)
        except StopIteration:
            session.clear()
            return redirect('/')

        if dir_info['num_file'] >= 110: 
            return render_template('upload.html', msg = 'You already reached the maximum number of files.')
        if dir_info['size'] >= 1024:
            return render_template('upload.html', msg = 'You already reached the maximum storage.')
        
        if file_upload.filename != '' and file_upload:
            last = int(ED.decrypt(session['enc_last']))
            file_path = os.path.join(user_dir, generate_filename(last))
            file_upload.save(file_path)
            return render_template('upload.html', msg = 'File uploaded successfully!')
        else:
            return render_template('upload.html', msg = 'Failed to upload your file!')
    return redirect('/')


@app.route('/viewer')
@limiter.limit("250 per hour")
def viewer():
    if 'id' not in session: return redirect('/')

    user_dir = app.config['UPLOAD_DIR'].format(userId = session['id'])

    if request.args.get("file") != None:
        file_path = user_dir + request.args.get("file")
        check_path(file_path)
        file_content = open(file_path).read()
    else:
        file_content = ""
    
    file_content = sanitize_content(file_content)
    template = render_template('viewer.html', file_content = file_content)
    return render_template_string(template)


if __name__ == "__main__":
    app.run(port = CONFIG['FLASK_PORT'], host = CONFIG['FLASK_HOST'])