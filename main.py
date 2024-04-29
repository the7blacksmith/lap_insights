from flask import Flask
from views.web.routes import web

UPLOAD_FOLDER = 'csv_files'

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.register_blueprint(web, UPLOAD_FOLDER = UPLOAD_FOLDER)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)