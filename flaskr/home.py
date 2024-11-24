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
        "SELECT * FROM folders WHERE id = ?",
        (g.user['id'],)).fetchall()

    return render_template('homepage/home.html',folders=folders)
