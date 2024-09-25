from flask import Flask
from .views import views  # Ensure this import is correct

app = Flask(__name__)

def user_accounts():
    app = Flask(__name__)

    # Register blueprint
    app.register_blueprint(views, url_prefix="/")

    return app
