import os
import secrets
from datetime import datetime, timedelta
import uuid
from time import sleep
import base64
import asyncio
import aioredis
import redis
from quart import request, jsonify
from sqlalchemy import Date, func
from SDMPDS import app, db
from SDMPDS.models import Users, Images
from SDMPDS.opencv_haarcascade import findPeople



sr = redis.StrictRedis(host='localhost', port=6379)
sr.execute_command('FLUSHDB')



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

async def process_image(id, image_src):
    #wysyłanie zdjęcia (jego adresu na serwerze) do funkcji
    #count = findPeople(image_src)
    print("funkcja przetwarzająca obraz o id = {}".format(id))
    print("przetwarzanie...")
    sleep(5)
    print("przetworzono, znaleziono x osób")
    # wpisanie do bazy ilości znalezionych osób i zmiana status na ukończony
    #img = Images.query.filter_by(id = id).first()
    #img.status = "done"
    #db.session.commit()

@app.route('/marker', methods=["POST"])
async def image_send():
    # to do autoryzacji uzytkownikow w dzialajacej juz aplikacji
    #kod = auth(request.values.get("login"), request.values.get("token"))
    #if kod == 404:
    #    return jsonify({"blad": "Blad autoryzacji uzytkownika"})

    data = await request.get_json(force=True)

    zdjecie = data['photo']
    nazwa_pliku = str(uuid.uuid4())
    with open(os.path.dirname(__file__) + '/../images/' 
              + nazwa_pliku+".jpg", "wb") as file:
        file.write(base64.b64decode(zdjecie))
        new_image = Images(date=data['date'], name=nazwa_pliku, recognized=None,
                           coordinates=str(data['coordinates']),
                         img_src="./images/"+nazwa_pliku+".jpg", status="pending")
        db.session.add(new_image)
        db.session.commit()

    #przesłanie do funkcji zliczającej
    loop = asyncio.get_event_loop()
    await aioredis.create_redis('redis://localhost', loop=loop)
    loop.create_task(process_image(new_image.id, new_image.img_src))
    
    #odesłanie 200 ok

    json = jsonify({
            "id": data['id'],
            "date": data['date'],
            "name": data['name'],
            "coordinates": data['coordinates'],
            "uuid": new_image.name,
            "status": "pending"
        })

    return(json)
