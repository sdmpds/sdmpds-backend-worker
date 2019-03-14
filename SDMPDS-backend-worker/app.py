from flask import Flask
from flask import redirect
from flask import url_for
from flask import jsonify


app = Flask(__name__)

wsgi_app = app.wsgi_app

ilosc_uzytkownikow = 0

@app.route("/login", methods=['GET', 'POST'])
def login():
    """Logowanie użytkownika do serwera"""
    global ilosc_uzytkownikow
    ilosc_uzytkownikow += 1
    return redirect(url_for('.hello'))

@app.route('/', methods=['GET', 'POST'])
def hello():
    """Wyświetlenie komunikatu powitalnego na serwerze"""
    global ilosc_uzytkownikow
    response = { "text": "Hello!", "status": 200, "activeUsers": ilosc_uzytkownikow }
    return jsonify(response)

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
