from flask import Flask, request, Response
from response import templateError,templateSuccess
import mongoDB as db
import json

app = Flask(__name__)

#definig routes
@app.route('/users', methods = ['GET'])
def getUsers():
    result = db.getUsers()
    response = {
        "Number of documents" : result[0],
        "Documents recovered" : json.loads(result[1])
    }
    return templateSuccess(response)
    #return Response(response, mimetype='application/json')

@app.route('/users/<id>', methods = ['GET'])
def getUser(id):
    result = db.getUser(id)
    if hasattr(result, 'code'):
        return templateError(result)
    else:
        return templateSuccess(json.loads(result))

@app.route('/users', methods = ['POST'])
def createUser():
    response = []
    array = request.json
    number = len(array)

    if(number > 0):
        for element in array:
            try:
                username = element['username']
                password = element['password']
                email = element['email']
            except:
                return templateError({'code': 400, 'message': 'There is one or more missing parameters: username, password or email'})
            
            if username and email and password:
                params = {
                    'username' : username,
                    'password': password,
                    'email': email
                }
                result = db.insertUser(params)
                if hasattr(result, 'code'):
                    return templateError(result)
                else:
                    response.append(result)

            else:
                return templateError({'code': 400, 'message': 'The parameters cannot be empty'})

    else:
        return templateError({'code': 204, 'message': 'The request does not contain elements'})
    
    return templateSuccess(response)
    #return templateSuccess('Messages received')

@app.route('/users/<id>', methods = ['PUT'])
def updateUser(id):
    try:
        username = request.json['username']
        password = request.json['password']
        email = request.json['email']
    except:
        return templateError({'code': 400, 'message': 'There is one or more missing parameters: username, password or email'})
    
    if username and email and password:
        params = {
            'username' : username,
            'password': password,
            'email': email
        }
        result = db.updateUser(id,params)

        if hasattr(result, 'code'):
            return templateError(result)
        else:
            return templateSuccess(result)
    else:
        return templateError({'code': 400, 'message': 'The parameters cannot be empty'})


@app.route('/users/<id>', methods = ['DELETE'])
def deleteUser(id):
    print(id)
    result = db.deleteUser(id)
    print(result)
    if hasattr(result, 'code'):
        return templateError(result)
    else:
        return templateSuccess(result)

if __name__ == '__main__':
    app.run(debug=True)