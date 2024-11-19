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

load_dotenv()

uri = os.getenv("MONGODB_URI")


if uri is None:
    raise ValueError("MONGODB_URI not found in environment variables")

client = MongoClient(uri)

db = client['dropnox-file']  # Replace with your database name
collection = db['file']  # Replace with your collection name


@bp.route('/create')
def createfolder():
    return render_template('homepage/createfolder.html')
