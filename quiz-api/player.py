import sqlite3
from flask import jsonify
from pathlib import Path

def getConnection():
	conn = sqlite3.connect(Path(__file__).parent.resolve() / "QuizDB.db")
	conn.isolation_level = None
	return conn

def getAllPlayers():
	conn = getConnection();
	
	try:
		players = conn.execute("SELECT * from player order by score DESC").fetchall()
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
		conn.execute("INSERT INTO player (name, score) VALUES (?, ?)", (dataJSON["playerName"], dataJSON["score"]))
		conn.commit()

		return dataJSON, 200
	except Exception as err:
		print(err)
		return 'Bad request', 400