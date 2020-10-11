from pymongo import MongoClient
from django.db import IntegrityError

from .models import Therapist, Practice, Symptom, Office

client = MongoClient()
db = client.terrapeute

airtable_registry = {}
id_registry = {}


def import_practices():
    Practice.objects.all().delete()
    for therapy in db.therapies.find():
        if not therapy["name"]:
            continue
        try:
            practice = Practice.objects.create(
                name=therapy["name"], slug=therapy["slug"]
            )
        except IntegrityError:
            continue
        airtable_registry[therapy.get("airtableId") or str(therapy["_id"])] = practice
        id_registry[str(therapy["_id"])] = practice

    print("practices imported")


symptoms = {}


def import_symptoms():
    Symptom.objects.all().delete()
    for symptom in db.symptoms.find():
        if len(symptom["synonyms"]) == 1:
            symptom["synonyms"] = " ".split(symptom["synonyms"][0])
        try:
            instance = Symptom.objects.create(
                name=symptom["name"],
                synonyms=[x.strip() for x in symptom["synonyms"]],
                keywords=symptom["keywords"],
            )
        except IntegrityError:
            continue
        id_registry[str(symptom["_id"])] = instance
        airtable_registry[symptom["airtableId"]] = instance
    for symptom in db.symptoms.find():
        if symptom.get("airtableParentId"):
            instance = airtable_registry[symptom["airtableId"]]
            instance.parent = airtable_registry[symptom["airtableParentId"]]
            instance.save()
    print("symptoms imported")


def import_therapists():
    Therapist.objects.all().delete()
    for t in db.therapists.find():
        therapist = Therapist(
            slug=t["slug"],
            firstname=t["firstname"],
            lastname=t["lastname"],
            email=t.get("email"),
            phone=t["phone"].replace(" ", ""),
            is_certified=bool(t["isCertified"]),
            description=t.get("description"),
            price=t.get("price"),
            timetable=t.get("timetable"),
            languages=t["languages"],
            photo=t.get("photo"),
            socials=t.get("socials"),
            # practices=[id_registry[k] for k in t["therapies"] if k in id_registry],
            agreements=t["agreements"],
            payment_types=t["paymentTypes"],
            # symptoms=[id_registry[s] for s in t["symptoms"] if s in id_registry],
            creation_date=t["creationDate"],
        )
        [
            therapist.practices.add(id_registry[k])
            for k in t["therapies"]
            if k in id_registry
        ]
        [
            therapist.symptoms.add(id_registry[k])
            for k in t["symptoms"]
            if k in id_registry
        ]
        therapist.save()

        for o in t["offices"]:
            office = Office.objects.create(
                street=o.get("street"),
                zipcode=o.get("zipCode"),
                city=o.get("city"),
                country=o.get("country"),
                pictures=o.get("pictures"),
                latlng=o.get("location")["coordinates"],
                therapist=therapist,
            )
        # try:
        #     therapist.save()
        # except Exception as e:
        #     import ipdb; ipdb.set_trace()
        #     print(e, t)


def import_all():
    import_practices()
    import_symptoms()
    import_therapists()
