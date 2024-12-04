from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from base64 import b64encode
from werkzeug.exceptions import abort
from PIL import Image
import io
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('home', __name__)

@bp.route('/')
@login_required
def home():
    db = get_db()
    folders = db.execute(
        "SELECT * FROM folders WHERE id = ? AND parent_id IS NULL",
        (g.user['id'],)).fetchall()
    files = db.execute(
        "SELECT * FROM files WHERE  id = ? AND folder_id  IS NULL",
        (g.user['id'],)).fetchall()

    file_preview = []
    for file in files:
            try:
                if file['typ'] == 'txt':
                    content = file['content']
                    lines =content.decode('utf-8').splitlines()[:5]
                    file_preview.append({'name':file['name'],'preview':lines})
                    print(file['typ'])

                elif file['typ'] in ('png' ,'jpeg','gif'):
                    content = file['content']
                    image_data = io.BytesIO(content)
                    with Image.open(image_data ) as img:
                        img.thumbnail((150,150))
                        preview_data = io.BytesIO()
                        img.save(preview_data,format='PNG')
                        preview_data.seek(0)
                        preview_base64 = b64encode(preview_data.read()).decode('utf-8')
                        file_preview.append({'name':file['name'],'preview':f"data:image/png;base64,{preview_base64}"})

            except Exception as e:
                file_preview.append({'name': file['name'], 'preview': ["Error generating preview"]})

    return render_template('homepage/home.html',folders=folders,files=files,file_preview=file_preview)



@bp.route('/subfolder/<int:folder_id>')
def subfolder(folder_id):
    db = get_db()

    if subfolder:
        subfolders = db.execute(
            "SELECT * FROM folders Where parent_id = ? AND id = ?",
            (folder_id,g.user['id'])).fetchall()
        parent_folder = db.execute(
            "SELECT * FROM folders WHERE id =?",
            (folder_id,)
        ).fetchone()
    else:
        flash("No subfolders found.")
        return redirect(url_for('home.home'))

    return render_template('homepage/subfolder.html',folder_id=folder_id,subfolders=subfolders, parent_folder=parent_folder)
