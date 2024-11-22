

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
def createfolder():
    if request.method == 'POST':
        foldername = request.form['folder-name']
        db = get_db()
        error = None

        if not foldername:
            error = 'File name cannot be blank'
        if error  is None:
            try:
                db.execute(
                    " INSERT INTO folders (name) VALUES (?)",
                    (foldername,),
                )
            except db.IntegrityError:
                error = f"file {foldername} is already created"
        flash(error)
    return render_template('homepage/createfolder.html')
