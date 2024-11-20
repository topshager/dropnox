from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
import os
from dotenv import load_dotenv
from pymongo import MongoClient

bp = Blueprint('create', __name__)

@bp.route('/create')
def createfolder():
    return render_template('homepage/createfolder.html')
