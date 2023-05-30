import sqlite3
from pathlib import Path

def getConnection():
	conn = sqlite3.connect(Path(__file__).parent.resolve() / "QuizDB.db")
	conn.isolation_level = None
	return conn


def addAnswer(data):
	conn = getConnection()

	try:        
		conn.execute('INSERT INTO answer VALUES (?, ?, ?, ?, ?)',
					(data.getID(), data.getValue(), data.isCorrect(), data.getQuestionID(), data.getPos()))
		conn.commit()

		return data.getID()
	except Exception as err:
		print(err)
		return 'Unauthorized', 401
	
def getAnswersByQuestionID(id):
	conn = getConnection()
	
	try:
		# get answers
		answers = conn.execute('SELECT * FROM answer where questionID = ?', id).fetchall()
		conn.commit()
		
		# put it in JSON
		answersJSON = {'possibleAnswers': []}
		for answer in answers:
			answersJSON['possibleAnswers'].append({"text": answer[1], "isCorrect": bool(answer[2])})

		return answersJSON
	except Exception as err:
		print(err)

#########################################
# Check answer isCorrect
#########################################
def isCorrect(answer, id):
	conn = getConnection()

	try:
		correctAnswer = conn.execute("SELECT pos FROM answer WHERE correct = 1 and questionID = ?", [id]).fetchall()[0][0]
		conn.commit()
		return correctAnswer == answer
	except Exception as e:
		print(e)
		return '', 401