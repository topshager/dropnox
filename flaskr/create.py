
from flask import Flask ,jsonify
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
import os
bp = Blueprint('create', __name__)
@bp.route('/create',methods=('GET','POST'))
@login_required
def createfolder():
    db = get_db
    error = None
    folders = []

    if request.method == 'POST':
        foldername = request.form['folder-name']


        if not foldername:
            error = 'File name cannot be blank'
        else:
            try:
                db.execute(
                    " INSERT INTO folders (name) VALUES (?)",
                    (foldername,),
                )
                db.commit()
            except db.IntegrityError:
                error = f"file {foldername} is already created"


        if error:
            flash(error)
        else:
            return redirect(url_for('home'))
    folders = db.execute(
        "SELECT * FROM folders WHERE username = ?",
        (g.user['username'],)  # Assuming g.user['username'] contains the username
    ).fetchall()

    return render_template('homepage/createfolder.html')
