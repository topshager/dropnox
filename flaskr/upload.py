import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.utils import secure_filename
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('upload', __name__)


ALLOWED_EXTENSIONS = {'png','jpeg','gif','pdf','txt'}

def allowed_files(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload',methods=['POST'])
def uploade():


    if 'file' not in request.files:
        flash('no file part')
        return redirect('home.html')
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect('home.html')
    if file and allowed_files(file.filename):
        filename = secure_filename(file.filename)
        filetype = filename.rsplit('.',1)[1].lower()
        db = get_db()
        file = db.execute(
            "INSERT INTO files(id,name,typ ) VALUES(?,?,?)",(g.user['id'],filename,filetype)
            ##MIGRATE DBD AGAIN 
        )
        db.commit()
        flash('File uploaded successfully!')
    else:
        flash('Invalid file type')
    return redirect('homepage/home.html')
