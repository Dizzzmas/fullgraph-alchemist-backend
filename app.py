from flask import Flask
from config import DevelopmentConfig


app = Flask(__name__)

app.config.from_object(DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



if __name__ == '__main__':
    app.run()