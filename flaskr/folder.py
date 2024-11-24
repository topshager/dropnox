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
    folderId = session.get('folder_id')
    if folderId :
        g.folders = get_db().execute('SELECT * FROM folders where parent_id  = ?',(folderId,)).fetchall()
    else:
        g.folders =  None


@bp.route('/folder')
def folder():
    return render_template('homepage/folder.html')
