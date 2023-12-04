import sqlite3
import globalSetting

def singleton(cls):
	instances = {}
	def wrapper(*args, **kwargs):
		if cls not in instances:
			instances[cls] = cls(*args, **kwargs)
		return instances[cls]
	return wrapper

@singleton
class DBManager:
	def __init__(self):
		self.db_file = globalSetting.DB_FOLDER + 'fileInfo.db'
		self.conn = None
	
	def createTable(self):
		self.conn.execute('''CREATE TABLE IF NOT EXISTS fileInfo
					(id INTEGER PRIMARY KEY AUTOINCREMENT,
					name TEXT NOT NULL,
					state INTEGER NOT NULL)''')

	def connect(self):
		if not self.conn:
			self.conn = sqlite3.connect(self.db_file)

	def disconnect(self):
		if self.conn:
			self.conn.close()
			self.conn = None

	def executeQuery(self, query):
		if not self.conn:
			self.connect()
		cursor = self.conn.cursor()
		cursor.execute(query)
		result = cursor.fetchall()
		cursor.close()
		return result
		
	def queryNameList(self):
		cursor = self.conn.cursor()
		cursor.execute("SELECT name FROM fileInfo")
		rows = cursor.fetchall()
		nameList = []
		for row in rows:
			nameList.append(row[0])
		return nameList

	def insertInfo(self, name: str, state: int) -> int:
		cursor = self.conn.cursor()
		cursor.execute("INSERT INTO fileInfo (name, state) VALUES (?, ?)", (name, state))
		self.conn.commit()
		return cursor.lastrowid
		
	def deleteInfo(self, id: int):
		cursor = self.conn.cursor()
		cursor.execute("DELETE FROM fileInfo WHERE id = ?", (id,))
		self.conn.commit()
		return cursor.rowcount	
 	
	def updateInfo(self, id: int, state: int):
		cursor = self.conn.cursor()
		cursor.execute("UPDATE fileInfo SET state = ? WHERE id = ?", (state, id))
		self.conn.commit()
  
	def selectInfo(self):
		cursor = self.conn.cursor()
		cursor.execute("SELECT * FROM fileInfo")
		rows = cursor.fetchall()
		return rows

	def selectEnableInfo(self):
		cursor = self.conn.cursor()
		cursor.execute("SELECT * FROM fileInfo WHERE state = 1")
		rows = cursor.fetchall()
		return rows
  
if __name__ == '__main__':
    db_manager = DBManager()
    db_manager.connect()
    db_manager.createTable()
    print(db_manager.selectInfo())    
    db_manager.disconnect()