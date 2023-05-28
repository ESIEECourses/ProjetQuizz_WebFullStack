
class Question():
	def __init__(self,
			 id: str,
			 title: str,
			 text: str,
			 pos: int,
			 img: str):
		self._id = id
		self._title = title
		self._text = text
		self._img = img
		self._pos = pos

	def getID(self):
		return self._id

	def getTitle(self):
		return self._title

	def getText(self):
		return self._text

	def getIMG(self):
		return self._img

	def getPosition(self):
		return self._pos

