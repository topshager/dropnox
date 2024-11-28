import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.utils import secure_filename
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('upload', __name__)


UPLOAD_FOLDER = 'uplaods'
ALLOWED_EXTENSIONS = {'png','jpeg','gif','pdf','txt'}

os.makedirs(UPLOAD_FOLDER,exist_ok=True)

def allowed_files(filenaem):
    return '.' in filenaem and filenaem.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload',methods=['POST'])
def uploade():

        return render_template('homepage/upload.html')




#   if 'file' not in request.files:
#        flash('no file part')
#        return redirect('home.html')
#    file = request.files['file']
#    if file.filename == '':
#        flash('No selected file')
#        return redirect('home.html')
#    if file and allowed_files(file.filename):
#        filename = secure_filename(file.filename)
#        file.save(os.path.join(bp.config['UPLOAD_FOLDER'], filename))
#        flash('File uploaded succcessfully!')
#    flash('Invalid file type')
#    return redirect('hompage/home.html')
#
