from flask import Flask, request, Response
from response import templateError,templateSuccess
import mongoDB as db
import json

app = Flask(__name__) 

#definig routes
@app.route('/users', methods = ['GET'])
def getUsers():
    result = db.getUsers()
    if 'code' in result:
        return templateError(result)

    response = {
        "Number_documents" : result[0],
        "Documents_recovered" : json.loads(result[1])
    }
    return templateSuccess(response)
    #return Response(response, mimetype='application/json')

@app.route('/users/<id>', methods = ['GET'])
def getUser(id):
    result = db.getUser(id)
    if 'code' in result:
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
            if 'username' in element and 'email' in element and 'password' in element:
                username = element['username']
                password = element['password']
                email = element['email']
            
                if username.strip() and email.strip() and password.strip():
                    params = {
                        'username' : username,
                        'password': password,
                        'email': email
                    }
                    result = db.insertUser(params)
                    if 'code' in result:
                        return templateError(result)
                    else:
                        response.append(result)

                else:
                    return templateError({'code': 400, 'message': 'The parameters cannot be empty'})
            else:
                return templateError({'code': 400, 'message': 'There is one or more missing parameters: username, password or email'})

    else:
        return templateError({'code': 204, 'message': 'The request does not contain elements'})
    
    return templateSuccess(response)
    #return templateSuccess('Messages received')

@app.route('/users/<id>', methods = ['PUT'])
def updateUser(id):
    data = request.json
    if 'username' in data and 'email' in data and 'password' in data:
        username = data['username']
        password = data['password']
        email = data['email']
    
        if username.strip() and email.strip() and password.strip():
            params = {
                'username' : username,
                'password': password,
                'email': email
            }
            result = db.updateUser(id,params)

            if 'code' in result:
                return templateError(result)
            else:
                return templateSuccess(result)
        else:
            return templateError({'code': 400, 'message': 'The parameters cannot be empty'})
    else:
        return templateError({'code': 400, 'message': 'There is one or more missing parameters: username, password or email'})


@app.route('/users/<id>', methods = ['DELETE'])
def deleteUser(id):
    print(id)
    result = db.deleteUser(id)
    if 'code' in result:
        return templateError(result)
    else:
        return templateSuccess(result)

if __name__ == '__main__':
    app.run(debug=True)