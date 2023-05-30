# import flask module
from flask import Flask
from flask_cors import CORS
from flask import Flask, request

# import utils functions
from jwt_utils import build_token
from jwt_utils import isLoggedIn

# import module to hash pwd
import hashlib

# import others modules
import question
import player 
import database 

app = Flask(__name__)
CORS(app)

#########################################
# Login the user - Admin access
#########################################
@app.route('/login', methods=['POST'])
def Login():
    payload = request.get_json()

    triedPassword = payload['password'].encode('UTF-8')
    hashedPassword = hashlib.md5(triedPassword).digest()
    
    if hashedPassword == b'\x91\xf4\x02\xdc\xc4\xb1\xb0\xe9O\xc1\xf9\xa5\x18^\xc3\xd8':
        return { "token": build_token()}, 200
    else:
        return 'Unauthorized', 401

#########################################
# rebuild DB
#########################################
@app.route('/rebuild-db', methods=['POST'])
def rebuildDB():
     if (isLoggedIn()):
          return database.create_database()
     else:
          return 'Unauthorized', 401

#########################################
# delete all players
#########################################
@app.route('/participations/all', methods=['DELETE'])
def deleteAllPlayers():
    if (isLoggedIn()):
        return player.deleteAll()
    else:
        return 'Unauthorized', 401

#########################################
# delete all questions
#########################################
@app.route('/questions/all', methods=['DELETE'])
def deleteAllQuestions():
    if (isLoggedIn()):
        return question.deleteAll()
    else:
        return 'Unauthorized', 401

#########################################
# handle /quiz-info get request
#########################################
@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
    return question.getQuizInfo()

#########################################
# if User is logged
# add question
#########################################
@app.route('/questions', methods=['POST'])
def addQuestion():
    # check if user is logged in
    if (isLoggedIn()):
        return question.addQuestion(request)
    
    return 'Unauthorized', 401

#########################################
# Get question
# by ID or 
# by position
#########################################
@app.route('/questions/<id>', methods=['GET'])
def getQuestionByID(id):
    return question.getQuestionByID(id)

@app.route('/questions', methods=['GET'])
def getQuestionByPosition():   
    if (request.args.get('position') == None):
        return 'error : you need to give a position !', 404
    
    return question.getQuestionByPosition(request.args.get('position'))

#########################################
# Delete question
#########################################
@app.route('/questions/<id>', methods=['DELETE'])
def deleteByID(id):
    if(isLoggedIn()):
        return question.deleteByID(id)
    return 'Unauthorized', 401

#########################################
# Update question
#########################################
@app.route('/questions/<id>', methods=['PUT'])
def updateQuestion(id):
    if (isLoggedIn()):
        return question.updateQuestion(request, id)

    return 'Unauthorized', 401

#########################################
# Get all players
#########################################
@app.route('/players', methods=['GET'])
def getPlayers():
    return player.getAllPlayers()
    
#########################################
# add new player
#########################################
@app.route('/participations', methods=['POST'])
def addPlayer():
    return player.addNewOne(request)

if __name__ == "__main__":
    app.run()
