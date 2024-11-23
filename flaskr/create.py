
from flask import Flask ,jsonify
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
import os
bp = Blueprint('create', __name__)


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
                    "INSERT INTO folders (name ) VALUES (?)",
                    (foldername)
                )
                db.commit()
            except db.IntegrityError:
                error = f"Folder '{foldername}' already exists"

        if error:
            flash(error)
        else:
            return redirect(url_for('create.createfolder'))  # Stay on the same page after creation

    # Fetch all folders for the current user
    folders = db.execute(
        "SELECT * FROM users WHERE username = ?",
        (g.user['username'],)
    ).fetchall()

    return render_template('homepage/createfolder.html', folders=folders)
