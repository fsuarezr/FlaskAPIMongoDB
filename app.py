from flask import Flask, request
from response import templateError,templateSuccess
import mongoDB as db
import json


app = Flask(__name__)

#definig routes
@app.route('/users', methods = ['GET'])
def listUsers():
    response = db.getUsers()
    #print(json.loads(response))
    return f'{response}'

@app.route('/users', methods = ['POST'])
def createUser():
    response = []
    array = request.json
    number = len(array)

    if(number > 0):
        for element in array:
            try:
                username = element["username"]
                password = element["password"]
                email = element["email"]

                if username and email and password:
                    params = {
                        "username" : username,
                        "password": password,
                        "email": email
                    }
                    result = db.insertUser(params)
                    response.append(result)
                else:
                    return templateError({"code": 400, "message": "The parameters cannot be empty"})

            except:
                return templateError({"code": 400, "message": "There's one or more missing parameters: username, password or email"})

    else:
        return templateError({"code": 204, "message": "The request does not contain elements"})
    
    return templateSuccess(response)


if __name__ == "__main__":
    app.run(debug=True)