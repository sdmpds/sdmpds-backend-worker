import asyncio
import base64
import os
import random
import uuid
from datetime import datetime, timedelta

import aioredis
import simplejson as json
from quart import request, jsonify

from SDMPDS import app, db
from SDMPDS.models.marker_model import Marker
from SDMPDS.models.question_model import Question
from SDMPDS.opencv_haarcascade import find_people


async def process_image(image_id, image_src):
    # wysyłanie zdjęcia (jego adresu na serwerze) do funkcji
    # count = find_people(image_src)
    print("funkcja przetwarzająca obraz o id = {}".format(image_id))
    print("przetwarzanie...")
    # await asyncio.sleep(20)
    # random_recognized = random.randint(0, 30)
    recognized = find_people(image_src)
    print("przetworzono, znaleziono {} osób".format(recognized))
    marker = Marker.query.filter_by(
        id=image_id).first()  # wpisanie do bazy ilości znalezionych osób i zmiana status na ukończony
    marker.status = "completed"
    marker.recognized = recognized
    db.session.commit()


@app.route('/markers', methods=["POST"])
async def create_marker():
    # to do autoryzacji uzytkownikow w dzialajacej juz aplikacji
    # kod = auth(request.values.get("login"), request.values.get("token"))
    # if kod == 404:
    #    return jsonify({"blad": "Blad autoryzacji uzytkownika"})

    data = await request.get_json(force=True)
    file_name = str(uuid.uuid4())
    with open(os.path.dirname(__file__) + '/../../images/' + file_name + ".jpg", "wb") as file:
        file.write(base64.b64decode(data['photo']))
        new_image = Marker(
            device_id=str(data['id']),
            name=data['name'],
            date=datetime.now(),  # this eliminate difference between time zones
            recognized=None,
            status="pending",
            coordinates=str(data['coordinates']),
            img_src="./images/" + file_name + ".jpg"
        )
        db.session.add(new_image)
        db.session.commit()
    loop = asyncio.get_event_loop()  # transfer to counting function
    await aioredis.create_redis('redis://localhost', loop=loop)
    loop.create_task(process_image(new_image.id, new_image.img_src))
    return jsonify({
        "code": 201,
        "status": "pending"
    })


@app.route("/markers")
async def get_marker():
    markers = Marker.query.filter(Marker.date > str(datetime.now() - timedelta(minutes=5)))
    quest = Question.query.filter(Question.date > str(datetime.now() - timedelta(minutes=3)))
    questions = []
    pending = []
    completed = []
    for question in quest:
        double_quotes = question.coordinates.replace("\'", "\"")
        coordinates = json.loads(double_quotes)
        questions.append({
            "id": question.id,
            "name": question.name,
            "date": question.date,
            "deviceId": question.device_id,
            "coordinates": coordinates,
            "question": question.question
        })

    for image in markers:
        double_quotes = image.coordinates.replace("\'", "\"")
        coordinates = json.loads(double_quotes)
        if image.status == "pending":
            pending.append({
                "id": image.id,
                "name": image.name,
                "date": image.date,
                "deviceId": image.device_id,
                "coordinates": coordinates
            })
        elif image.status == "completed":
            completed.append({
                "id": image.id,
                "date": image.date,
                "name": image.name,
                "deviceId": image.device_id,
                "recognized": image.recognized,
                "coordinates": coordinates
            })
    return jsonify({
        "pending": pending,
        "completed": completed,
        "question": questions
    })


@app.route("/questions", methods=["POST"])
async def create_question():
    data = await request.get_json(force=True)
    new_question = Question(
        device_id=str(data['id']),
        name=data['name'],
        date=datetime.now(),
        coordinates=str(data['coordinates']),
        question=data['question']
    )
    db.session.add(new_question)
    db.session.commit()
    return jsonify({
        "status": "complete"
    })
