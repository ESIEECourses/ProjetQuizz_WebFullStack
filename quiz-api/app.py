# import flask module
from flask import Flask
from flask_cors import CORS
from flask import Flask, request

# import utils functions
from src.jwt_utils import build_token
from src.jwt_utils import isLoggedIn

# import module to hash pwd
import hashlib

# import others modules
import src.question as question
import src.player as player

app = Flask(__name__)
CORS(app)

#########################################
# handle /quiz-info get request
#########################################
@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
    return question.getQuizInfo()


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
        return 'arg \'position\' is missing', 400
    
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
