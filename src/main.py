from flask import Flask
from flask_cors import CORS
from routers.auth import auth
from routers.trains import trains
# from models.core import create_tables, drop_tables

app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(trains)
cors = CORS(app, origins="*")
# app.config['CORS_HEADERS'] = 'Content-Type'


if __name__ == '__main__':
    # drop_tables()
    # create_tables()
    print(app.url_map)
    app.run(debug=True, port=3000)
