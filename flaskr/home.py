from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

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

    return render_template('homepage/home.html',folders=folders)



@bp.route('/subfolder/<int:folder_id>')
def subfolder(folder_id):
    db = get_db()

    subfolders = db.execute(
            "SELECT * FROM folders Where parent_id = ? AND id = ?",
        (folder_id,g.user['id'])).fetchall()
    parent_folder = db.execute(
        "SELECT * FROM folders WHERE id =?",
        (folder_id,)
    ).fetchone()
    return render_template('homepage/subfolder.html',folder_id=folder_id,subfolders=subfolders, parent_folder=parent_folder)
