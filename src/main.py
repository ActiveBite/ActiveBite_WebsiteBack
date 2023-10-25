from flask import Flask
from routers.auth import auth
# from models.core import create_tables, drop_tables

app = Flask(__name__)

app.register_blueprint(auth)

if __name__ == '__main__':
    # drop_tables()
    # create_tables()
    app.run(debug=True)
