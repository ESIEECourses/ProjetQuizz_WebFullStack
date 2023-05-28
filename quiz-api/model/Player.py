
class Player():
	def __init__(self, id: int, name: str):
		self._id = id
		self._name = name
		self._score = 0

	def getID(self):
		return self._id
