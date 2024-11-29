from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('create', __name__)


@bp.before_app_request
def load_user_and_folders():
    """Load the current user and their folders before each request."""
    user_id = session.get('id')

    if user_id:
        g.user = get_db().execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    else:
        g.user = None

@bp.route('/create_top', methods=('GET', 'POST'))
@login_required
def create_folder():
    """Create a new top-level folder."""
    db = get_db()
    error = None

    if request.method == 'POST':
        foldername = request.form.get('folder-name')
        if not foldername:
            error = 'Folder name cannot be blank'
        else:
            try:
                Type = "folder"
                db.execute(
                    "INSERT INTO folders (name, id,typ) VALUES (?,?,?)",
            (foldername, g.user['id'],Type)
)
                db.commit()
            except db.IntegrityError:
                error = f"Folder '{foldername}' already exists"

        if error:
            flash(error)
        else:
            return redirect(url_for('home'))

    return render_template('homepage/folder.html')

@bp.route('/create_child/<int:folder_id>', methods=('GET', 'POST'))
@login_required
def create_child_folder(folder_id):
    db = get_db()
    error = None

    subfolders = db.execute(
                "SELECT * FROM folders WHERE id = ? AND parent_id = ?",(g.user['id'],folder_id)).fetchall()


    if request.method == 'POST':
        foldername = request.form.get('folder-name')
        if not foldername:
            error = 'Folder name cannot be blank'
        else:
            try:
                Type = "file"

                db.execute(
                    "INSERT INTO folders (name,id, parent_id,typ) VALUES (?, ?, ?, ?)",
                    (foldername, g.user['id'], folder_id, Type )
)
                db.commit()
            except db.IntegrityError:
                error = f"Folder '{foldername}' already exists"

        if error:
            flash(error)
        else:
            return redirect(url_for('home.subfolder', folder_id=folder_id))

    return render_template('homepage/create_child.html',folder_id=folder_id, subfolders= subfolders )
