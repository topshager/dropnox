
from flask import Flask ,jsonify
from flask import (
    Blueprint, flash, g, redirect, render_template, request,session, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
import os
bp = Blueprint('create', __name__)

@bp.before_app_request
def load_user():
    user_id = session.get('id')
    if user_id:
        g.user = get_db().execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    else:
        g.user = None


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def createfolder():
    db = get_db()  # Call the function to get the database connection
    error = None

    if request.method == 'POST':
        foldername = request.form.get('folder-name')  # Safely get the folder name
        if not foldername:
            error = 'Folder name cannot be blank'
        else:
            try:
                # Insert folder name with the username of the logged-in user
                db.execute(
                    "INSERT INTO folders (name,id ) VALUES (?,?)",
                    (foldername,g.user['id'],)
                )
                db.commit()
            except db.IntegrityError:
                error = f"Folder '{foldername}' already exists"


            if error:
                flash(error)
            else:
                return redirect(url_for('home'))  # Stay on the same page after creation

    # Fetch all folders for the current user
    folders = db.execute(
        "SELECT * FROM folders WHERE id = ?",
        (g.user['id'],)
    ).fetchall()
    return render_template('homepage/createfolder.html', folders=folders)
