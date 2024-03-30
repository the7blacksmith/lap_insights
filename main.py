from flask import Flask
from views.web.routes import web

def create_app():
    app = Flask(__name__)
    app.register_blueprint(web)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)