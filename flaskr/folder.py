from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,session,
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('folder', __name__)

@login_required
@bp.before_request
def load_folder():
    folder_id = session.get('folder_id')
    if folder_id :
        g.folders = get_db().execute('SELECT * FROM folders where parent_id  = ?',(folder_id,)).fetchall()
    else:
        g.folders = []


@bp.route('/folder/<int:folderId>')
def folder(folderId):
    db = get_db()
    folders = db.execute(
        "SELECT * FROM folders WHERE  parent_id = ?",
        (folderId,)).fetchall()
    return render_template('homepage/subfolder.html' ,folders=folders)
