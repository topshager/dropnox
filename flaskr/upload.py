import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,session,jsonify,current_app
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
        file_content = file.read()

        db = get_db()
        file = db.execute(
            "INSERT INTO files(content,id,name,typ) VALUES(?,?,?,?)",(file_content,g.user['id'],filename,filetype)
        )
        db.commit()

        flash('File uploaded successfully!')

    else:
        flash('Invalid file type')

    return redirect(url_for('home'))

@login_required
@bp.route('/upload-folder',methods=['POST'])
def upload_folder():
    if 'files' not in request.files:
        return jsonify({'message':'No files in the request'}),400

    files = request.files.getlist('files')
    i =0
    while i == 0:
        for file in files:
            path= (file.filename).split('/')
            folder_name = path[0]
        i+=1
        print(folder_name)

    db = get_db()
    user_id = session.get('id')
    Type = "folder"
    db.execute(
            "INSERT INTO folders (name,typ,id) VALUES(?,?,?)",
            (folder_name,Type,user_id)
        )
    db.commit()

    folder_id = db.execute(
        "select * from folders  where name = ? ORDER BY created_at DESC  LIMIT 1",
        (folder_name,)
    ).fetchone()

    if not folder_id:
        return jsonify({'message': 'Failed to retrieve folder ID'}), 500

    folder_id = folder_id['folder_id']
    print(folder_id)

    for file in files:
        print(file)
        if file and allowed_files(file.filename):
            filename = secure_filename(file.filename.split('/')[-1])
            file_content = file.read()
            file_type = filename.rsplit('.', 1)[1].lower()
            db.execute(
                "INSERT INTO files (content, folder_id, name, typ) VALUES (?, ?, ?, ?)",
                (file_content, folder_id, filename, file_type)
            )
            db.commit()
        else:
            print("could not ")
            pass




    return jsonify({'message': f'{len(files)} files uploaded successfully'})
