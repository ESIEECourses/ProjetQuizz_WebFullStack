import sqlite3
from flask import jsonify
from flask import json
from pathlib import Path
import question
import answer

def getConnection():
	conn = sqlite3.connect(Path(__file__).parent.resolve() / "QuizDB.db")
	conn.isolation_level = None
	return conn

def getAllPlayers():
	conn = getConnection();
	
	try:
		players = conn.execute("SELECT * from player order by score").fetchall()
		conn.commit()
		
		playersJSON = []
		for player in players:
			playersJSON.append({"name": player[1], "score": player[2]})
			
		return jsonify(playersJSON), 200
	except Exception as err:
		print(err)

def addNewOne(data):
	dataJSON = data.get_json()
	conn = getConnection();

	try:
		if "score" in dataJSON:
			conn.execute("INSERT INTO player (name, score) VALUES (?, ?)", (dataJSON["playerName"], dataJSON["score"]))
			conn.commit()
		elif len(dataJSON["answers"]) == question.getQuizInfo()[0]["size"]:
			score = getScore(dataJSON["answers"])
			conn.execute("INSERT INTO player (name, score) VALUES (?, ?)", (dataJSON["playerName"], score))
			conn.commit()
			return {"playerName": dataJSON["playerName"], "score": score}, 200
		else:
			return 'Bad request', 400

		return dataJSON, 200
	except Exception as err:
		print(err)
		return 'Bad request', 400

def getScore(answers):
	score = 0
	idxQuestion = 1

	for a in answers:
		if (answer.isCorrect(a, question.getQuestionIDwithPosition(idxQuestion)[0])):
			score += 1
   
		idxQuestion += 1

	return score
	
 
def deleteAll():
	conn = getConnection()

	try: 
		conn.execute("DELETE FROM player")
		conn.commit()

		return 'ok deleted', 204
	except Exception as err:
		print(err)
		return 'Bad request', 400