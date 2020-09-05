from pymongo import MongoClient
from pymongo import errors as mongoError
from dotenv import load_dotenv
import os,json

load_dotenv()

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_DATABASE = os.getenv("MONGO_DATABASE")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

def connMongoDB():
    connString = f'mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/{MONGO_DATABASE}?retryWrites=true&w=majority'
    conn = MongoClient(connString)
    db = conn[f"{MONGO_DATABASE}"]
    return db

def getUsers():
    db = connMongoDB()
    collection = db[f"{MONGO_COLLECTION}"]
    result = collection.find()
    return result

def insertUser(params):
    username = params["username"]
    password = params["password"]
    email = params["email"]
    message = {
        "username": username,
        "password": password,
        "email": email
    }

    try:
        db = connMongoDB()
        collection = db[f"{MONGO_COLLECTION}"] 
        collection.insert_one(message).inserted_id
        result = json.loads(message)
        response = {
            "User inserted": result
        }
        return response

    except mongoError.PyMongoError as py_mongo_error:
        error = str(py_mongo_error)
        indexini = error.find("{")
        indexfin = error.find("}")
        extractError = error[indexini:(indexfin+1)].replace("'",'"')
        jsonError = json.loads(extractError)
        messageError = jsonError['errmsg']   
        code = jsonError['code']
        codeName = jsonError['codeName']
        message = {
            "code": code,
            "message": f"{messageError} With codeName: {codeName}"
        }
        return message
