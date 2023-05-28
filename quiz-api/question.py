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
    players = conn.execute("SELECT * from player order by score DESC LIMIT 3").fetchall()
    conn.commit()

    playersJSON = []
    for player in players:
        playersJSON.append({"name": player[1], "score": player[2]})
    
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
        cursor = conn.cursor()
        cursor.execute('INSERT INTO question(title, text, img, pos) VALUES (?, ?, ?, ?)',
                    (questionData.getTitle(), questionData.getText(), questionData.getIMG(), questionData.getPosition()))
        id = cursor.lastrowid
        for answer in dataInJSON['possibleAnswers']:
            answerData = Answer(None, answer['text'], answer['isCorrect'], id)
            AnswerManager.addAnswer(answerData)

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
        merged = []
        merged.append({ 'id': question[0]['id'], 'title': question[0]['title'], 'text': question[0]['text'], 'image': question[0]['image'], 'position': question[0]['position'], 'possibleAnswers': answers['possibleAnswers']})

        return jsonify(merged), 200
    except Exception as err:
        print(err)
    
def getQuestionByPosition(pos):
    conn = getConnection()

    try:
        id = conn.execute('SELECT id FROM question where pos = ?', [pos]).fetchall()[0]
        conn.commit()

        return getQuestionByID(id)
    except Exception as err:
        print(err)

def deleteByID(id):
    conn = getConnection()
    
    # get position for later update
    oldQuestionPosition = conn.execute("SELECT * FROM question where id = ?", [id]).fetchall()[0][4];
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

    return "Succeed", 200

def updateQuestion(req, id):
    question = req.get_json()
    conn = getConnection()
    
    # get previous position 
    oldPosition = conn.execute('SELECT pos FROM question where id = ?', [id]).fetchall()[0][0]
    conn.commit()
    
    # update data
    conn.execute("UPDATE question SET title = ?, text = ?, img = ?, pos = ? WHERE id = ?", (question["title"], question["text"], question["image"], question["position"], id ))
    conn.commit()
    
    # remove old answers
    conn.execute("DELETE FROM answer where questionID = ?", [id])
    conn.commit()
    
    # put new ones
    for answer in question['possibleAnswers']:  
        answerData = Answer(None, answer['text'], answer['isCorrect'], id)
        AnswerManager.addAnswer(answerData)
        
    # rearange order
    if question["position"] < oldPosition:
        conn.execute("UPDATE question SET pos = pos - 1 WHERE pos >= ? AND pos < ?", (question["position"], oldPosition))
        conn.commit()
    else:
        conn.execute("UPDATE question SET pos = pos + 1 WHERE pos <= ? AND pos > ?", (question["position"], oldPosition))
        conn.commit()
        
    return "Success", 200
        

    
