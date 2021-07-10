import os, redis
from flask import Flask
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy

redis_client = FlaskRedis()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nftmash:nftmash@localhost/nftmash'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['REDIS_URL'] = "redis://:nftmash@localhost:6379/0"

    with app.app_context():
        from .models import ranking
        db.init_app(app)
        db.create_all()

        from NFTmash.blueprints import coolcats, cryptopunks, ranking, main

        app.register_blueprint(main.bp)
        app.register_blueprint(ranking.bp)
        app.register_blueprint(coolcats.bp)
        app.register_blueprint(cryptopunks.bp)

        redis_client.init_app(app)

    return app
