import  functools

from flask import (
    Blueprint,flash,g ,redirect,render_template,request,session,url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('auth',__name__,url_prefix='/auth')

@bp.route('/register',methods=('GET','POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = "Password is required."
        if error is None:
            try:
                db.execute(
                    "INSERT INTO users (username,password) VALUES (?,?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"users{username} is already registered."
            else: return redirect(url_for("auth.login"))
        flash(error)
    return render_template('auth/register.html')


@bp.route('/login',methods=('GET','POST'))
def login():
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * from users where username = ?',(username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect password.'
        elif not check_password_hash(user['password'],password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['id'] = user['id']
            return redirect(url_for('home',))
        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    id = session.get('id')

    if id is None:
        g.user = None

    else:
        g.user = get_db().execute(
            'Select * from users where id =?',(id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
