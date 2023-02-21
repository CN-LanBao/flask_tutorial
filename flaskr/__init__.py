# @Time     : 2023/2/13 21:39
# @Author   : CN-LanBao
from pathlib import Path

from flask import Flask

from . import db, auth, blog


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY="dev", DATABASE=app.instance_path / Path("flaskr.sqlite"))

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    # A simple page that says hello
    @app.route("/hello")
    def hello():
        return "Hello"

    db.init_app(app)

    app.register_blueprint(auth.bp)

    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
