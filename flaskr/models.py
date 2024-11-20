from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(77), unique=True, nullable=False)
    password = db.Column(db.String(55), nullable=False)

class Folder(db.Model):
    __tablename__ = 'folders'
    folder_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('folders.folder_id', ondelete='CASCADE'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class File(db.Model):
    __tablename__ = 'files'
    file_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    folder_id = db.Column(db.Integer, db.ForeignKey('folders.folder_id', ondelete='CASCADE'))
    size = db.Column(db.BigInteger, nullable=False)
    typ = db.Column(db.Text, nullable=False)
    content = db.Column(db.LargeBinary)  # BYTEA equivalent in SQLAlchemy
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
