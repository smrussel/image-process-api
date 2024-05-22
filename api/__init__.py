from flask import Flask
import os

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__)
    app.config['upload'] = os.path.join(basedir, 'upload')
    app.config['images'] = os.path.join(basedir, 'images')
    app.config['SECRET_KEY'] = 'your-secret-key'

    from api.bg_remove.routes import bg_bp
    app.register_blueprint(bg_bp, url_prefix="/")
    from api.dominant_colors.routes import dominant_bp
    app.register_blueprint(dominant_bp, url_prefix="/")
    from api.img_recog.routes import rg_bp
    app.register_blueprint(rg_bp, url_prefix="/")

    @app.route('/')
    def home_view():
        return {"Success": "Api is live"}

    return app
