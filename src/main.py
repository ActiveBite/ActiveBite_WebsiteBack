from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routers.auth import auth
from routers.trainings import trainings

from models.core import create_tables, drop_tables
from routers.exercises import exercises

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'active-bite-superpupersukasecret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 86400  # seconds / 24 hours
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
jwt = JWTManager(app)
CORS(app, origins=['https://bug-free-space-disco-q4gxww45xrvc6ww5-3000.app.github.dev',
                   'https://friendly-pancake-qjq9j64xg7w397pq-3000.app.github.dev',
                   'http://localhost:3000', 'http://127.0.0.1:3000'], supports_credentials=True, )
app.register_blueprint(auth)
app.register_blueprint(trainings)
app.register_blueprint(exercises)
# app.config['CORS_HEADERS'] = 'Content-Type'


if __name__ == '__main__':
    drop_tables()
    create_tables()
    app.run(debug=True, port=3030)
