import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,session
)
from werkzeug.utils import secure_filename
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('upload', __name__)

ALLOWED_EXTENSIONS = {'png','jpeg','gif','pdf','txt'}

def allowed_files(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('id')

    if user_id is None:
        g.user = None
    else:
        db = get_db()
        g.user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()


@bp.route('/upload',methods=['POST'])
@login_required
def uploade():


    if 'file' not in request.files:
        flash('no file part')
        return redirect(url_for('home'))
    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('home'))

    if file and allowed_files(file.filename):
        filename = secure_filename(file.filename)
        filetype = filename.rsplit('.',1)[1].lower()

        db = get_db()
        file = db.execute(
            "INSERT INTO files(id,name,typ ) VALUES(?,?,?)",(g.user['id'],filename,filetype)
        )
        db.commit()
        
        flash('File uploaded successfully!')

    else:
        flash('Invalid file type')

    return redirect(url_for('home'))
