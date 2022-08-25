from flask import Flask
from routes import api_code
from flask_cors import CORS

UPLOAD_FOLDER = 'data'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.register_blueprint(api_code)
CORS(app)


@app.route('/test')
def test():
    return 'Servidor escuchando...'


if __name__ == '__main__':
    app.run(debug=True)
