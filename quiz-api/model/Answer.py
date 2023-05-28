
class Answer():
	def __init__(self, id: int, value: str, is_correct: bool, question_id: int):
		self._id = id
		self._value = value
		self._correct = is_correct
		self._question_id = question_id

	def getID(self):
		return self._id

	def getValue(self):
		return self._value
	
	def isCorrect(self):
		return self._correct
		
	def getQuestionID(self):
		return self._question_id
