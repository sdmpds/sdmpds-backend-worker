import os
import secrets
from datetime import datetime, timedelta
from sqlalchemy import Date, func
from flask import request, jsonify
from werkzeug.utils import secure_filename
from SDMPDS import app, db
from SDMPDS.models import Users, Images


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def auth(login, token):
    user = Users.query.filter_by(login=str(login)).first()
    if not user:
        return 404
    if user.token == token:
        return 200

@app.route("/login", methods=['GET', 'POST'])
def login_user():
    """Logowanie użytkownika do serwera"""
    login = request.values.get("login")
    if not login:
        return jsonify({"blad": "Nie podano loginu"})
    print(login)
    user = Users.query.filter_by(login=str(login)).first()
    print(user)
    if not user:
        nazwa = request.values.get("nazwa")
        if not nazwa:
            nazwa = "Anonim"
        nowyUser = Users(login=login, nazwa=nazwa, token=secrets.token_hex(8), data_utworzenia_tokenu=str(datetime.now()))
        db.session.add(nowyUser)
        db.session.commit()
        print(nowyUser)
        user = nowyUser
    else:
        user.token = secrets.token_hex(8)
        user.data_utworzenia_tokenu = str(datetime.now())
        db.session.commit()
        
    return jsonify({"id": str(user.id), "nazwa": str(user.nazwa), "token": str(user.token),
                    "dataUtworzeniaTokenu": str(user.data_utworzenia_tokenu)})

@app.route('/', methods=['GET', 'POST'])
def hello():
    """Wyświetlenie komunikatu powitalnego na serwerze"""
    time = datetime.now() - timedelta(minutes=15)
    aktywni_uzytkownicy = Users.query.filter(func.strftime('%s', Users.data_utworzenia_tokenu) > func.strftime('%s', str(time))).all()
    response = {"text": "Hello!", "status": 200, "activeUsers": [user.nazwa for user in aktywni_uzytkownicy]}
    return jsonify(response)

@app.route('/images/send', methods=["POST"])
def image_send():
    # to do autoryzacji uzytkownikow w dzialajacej juz aplikacji
    #kod = auth(request.values.get("login"), request.values.get("token"))
    #if kod == 404:
    #    return jsonify({"blad": "Blad autoryzacji uzytkownika"})


    if 'file' not in request.files:
        return jsonify({"blad": "Brak pliku"})
    file = request.files["file"]
    if file.filename == '':
        return jsonify({"blad": "Nie wybrano plikow"})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        czas = datetime.now()
        new_image = Images(name=file.filename, img_src=filename, data_modyfikacji=czas)
        db.session.add(new_image)
        db.session.commit()
        return jsonify({"status": "Zdjecie przeslane",
                        "miejsce zapisu": os.path.join(app.config['UPLOAD_FOLDER'], filename),
                        "data zapisu": czas})
    return jsonify({"status": "Blad przesylu",
                    "opis": "Zdjecie w nieobslugiwanym formacie"})
