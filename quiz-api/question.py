from model import Answer
from model import Question
import answer as AnswerManager
import sqlite3
from flask import jsonify
from pathlib import Path

def getConnection():
	conn = sqlite3.connect(Path(__file__).parent.resolve() / "QuizDB.db")
	conn.isolation_level = None
	return conn

#########################################
# Quiz data
#########################################
def getQuizInfo():
	conn = getConnection()
	
	# get nb questions
	size = conn.execute("SELECT COUNT(*) FROM question").fetchall()[0][0]
	conn.commit() 
	
	# get scores
	players = conn.execute("SELECT * from player order by score DESC").fetchall()
	conn.commit()

	playersJSON = []
	for player in players:
		playersJSON.append({"playerName": player[1], "score": player[2]})
	
	return {'size': size, 'scores': playersJSON}, 200
	

#########################################
# Setter area
#########################################
def addQuestion(req):
	# handle data
	dataInJSON = req.get_json()
	questionData = Question(
		None,
		title = dataInJSON['title'],
		text = dataInJSON['text'],
		img = dataInJSON['image'],
		pos = dataInJSON['position']
	)

	# add the question
	conn = getConnection()

	try:
		# change pos of next questions 
		conn.execute("UPDATE question SET pos = pos + 1 WHERE pos >= ?", [questionData.getPosition()])
		conn.commit()
		cursor = conn.cursor()
		cursor.execute('INSERT INTO question(title, text, img, pos) VALUES (?, ?, ?, ?)',
					(questionData.getTitle(), questionData.getText(), questionData.getIMG(), questionData.getPosition()))
		id = cursor.lastrowid
		
		pos = 1
		for answer in dataInJSON['possibleAnswers']:
			answerData = Answer(None, answer['text'], answer['isCorrect'], id, pos)
			AnswerManager.addAnswer(answerData)
			pos = pos + 1

		return {'id': id}, 200
	except Exception as err:
		print(err)
		return 'Unauthorized', 401

#########################################
# Getter area
#########################################
def getQuestionByID(id): 
	conn = getConnection()
	
	try:
		result = conn.execute('SELECT * FROM question where id = ?', id).fetchall()[0]
		conn.commit()
		# get question
		question = []
		question.append({'id': result[0], 'title': result[1], 'text': result[2], 'image': result[3], 'position': result[4]})
		
		# get answers
		answers = AnswerManager.getAnswersByQuestionID(id);
		
		# merge both
		merged = { 
				'id': question[0]['id'],
				'title': question[0]['title'],
				'text': question[0]['text'],
				'image': question[0]['image'],
				'position': question[0]['position'],
				'possibleAnswers': answers['possibleAnswers']
				}
		
		return jsonify(merged), 200
	except Exception as err:
		print(err)
		return 'Bad request', 404
	
def getQuestionByPosition(pos):
	conn = getConnection()

	try:
		id = conn.execute('SELECT id FROM question where pos = ?', [pos]).fetchall()[0]
		conn.commit()

		return getQuestionByID(id)
	except Exception as err:
		print(err)
		return 'Bad request', 404

def getQuestionIDwithPosition(pos):
	conn = getConnection()

	try:
		id = conn.execute('SELECT id FROM question where pos = ?', [pos]).fetchall()[0]
		conn.commit()

		return id
	except Exception as err:
		print(err)
		return 'Bad request', 404

#########################################
# Delete area
#########################################
def deleteAll():
	conn = getConnection()

	try: 
		# remove linked answers
		conn.execute("DELETE FROM answer")
		conn.commit()

		# remove questions
		conn.execute("DELETE FROM question")
		conn.commit()

		return 'ok deleted', 204
	except Exception as err:
		print(err)
		return 'Bad request', 400

def deleteByID(id):
	conn = getConnection()
	
	try:
		# get position for later update
		oldQuestionPosition = conn.execute("SELECT * FROM question where id = ?", [id]).fetchall();
		if (len(oldQuestionPosition) == 0):
			return "Bad request", 404

		oldQuestionPosition = oldQuestionPosition[0][4]
		conn.commit()
		
		# remove linked answers
		conn.execute("DELETE FROM answer where questionID = ?", [id])
		conn.commit()

		# remove question
		conn.execute("DELETE FROM question where id = ?", [id])
		conn.commit()

		# update others questions position
		conn.execute("UPDATE question SET pos = pos - 1 WHERE pos > ?", [oldQuestionPosition])
		conn.commit()

		return "Succeed", 204
	except Exception as err:
		print(err)
		return "Bad request", 404

#########################################
# Update area
#########################################
def updateQuestion(req, id):
	try: 
		if (deleteByID(id)[0] == 'Bad request'): 
	  		raise Exception
			
		addQuestion(req)

		return 'Ok', 204
	except Exception as err:
		print(err)
		return 'Bad request', 404
