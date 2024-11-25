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
    folder_id = session.get('folder_id')

    if user_id:
        g.user = get_db().execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    else:
        g.user = None

    if folder_id:
        g.folders = get_db().execute(
            'SELECT * FROM folders WHERE parent_id = ?', (folder_id,)
        ).fetchall()
    else:
        g.folders = []

@bp.route('/create', methods=('GET', 'POST'))
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
                db.execute(
                    "INSERT INTO folders (name, id) VALUES (?, ?)",
                    (foldername, g.user['id'])
                )
                db.commit()
            except db.IntegrityError:
                error = f"Folder '{foldername}' already exists"

        if error:
            flash(error)
        else:
            return redirect(url_for('home'))

    return render_template('homepage/folder.html')

@bp.route('/create_child', methods=('GET', 'POST'))
@login_required
def create_child_folder():
    """Create a child folder inside the currently selected folder."""
    db = get_db()
    error = None
    folder_id = session.get('folder_id')

    if not folder_id:
        flash("No parent folder selected.")
        return redirect(url_for('home'))

    if request.method == 'POST':
        foldername = request.form.get('folder-name')
        if not foldername:
            error = 'Folder name cannot be blank'
        else:
            try:
                db.execute(
                    "INSERT INTO folders (name, user_id, parent_id) VALUES (?, ?, ?)",
                    (foldername, g.user['id'], folder_id)
                )
                db.commit()
            except db.IntegrityError:
                error = f"Folder '{foldername}' already exists"

        if error:
            flash(error)
        else:
            return redirect(url_for('folder'))  # Adjust as necessary for the redirect

    return render_template('homepage/createchildfolder.html')
