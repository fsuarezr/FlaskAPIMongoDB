from flask import Flask, request, Response
from response import templateError,templateSuccess
import mongoDB as db
import json

app = Flask(__name__)

#definig routes
@app.route('/users', methods = ['GET'])
def listUsers():
    result = db.getUsers()
    response = {
        "Number of elements" : result[0],
        "Recovered items" : result[1]
    }
    return templateSuccess(response)
    #return Response(response, mimetype='application/json')

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
                response.append(result)

            else:
                return templateError({'code': 400, 'message': 'The parameters cannot be empty'})

    else:
        return templateError({'code': 204, 'message': 'The request does not contain elements'})
    
    return templateSuccess(response)
    #return templateSuccess('Messages received')

if __name__ == '__main__':
    app.run(debug=True)