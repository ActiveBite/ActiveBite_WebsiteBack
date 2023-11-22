from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routers.auth import auth
from routers.trainings import trainings

from models.core import create_tables, drop_tables
from routers.exercises import exercises

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'active-bite-superpupersukasecret'
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 86400  # seconds / 24 hours
jwt = JWTManager(app)
app.register_blueprint(auth)
app.register_blueprint(trainings)
app.register_blueprint(exercises)
cors = CORS(app, origins="*")
# app.config['CORS_HEADERS'] = 'Content-Type'


if __name__ == '__main__':
    drop_tables()
    create_tables()
    app.run(debug=True, port=3030)
