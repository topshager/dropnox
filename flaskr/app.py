from flask import Flask
from flask_migrate import Migrate
from models import db, User, Folder, File

app = Flask(__name__)

# PostgreSQL connection URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/db_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)
