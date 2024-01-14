# -*- coding: utf-8 -*-
# @Time    : 2023.1.13
# @Author  : Xuan
# @Email   : 2022134346@qq.com
# @File    : DBmanager.py
# @Software: Vscode

"""
    本模块负责管理和数据库有关的操作
"""

import sqlite3
import globalSetting

# 单例
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
		# 生成数据库初始文件
		self.db_file = globalSetting.DB_FOLDER + 'fileInfo.db'
		self.conn = None
	
	def createTable(self):
		# 创建表格
		self.conn.execute('''CREATE TABLE IF NOT EXISTS fileInfo
					(id INTEGER PRIMARY KEY AUTOINCREMENT,
					name TEXT NOT NULL,
					state INTEGER NOT NULL)''')

	def connect(self):
		# 连接数据库
		if not self.conn:
			self.conn = sqlite3.connect(self.db_file)

	def disconnect(self):
		# 断开数据库
		if self.conn:
			self.conn.close()
			self.conn = None

	def executeQuery(self, query):
		"""执行query语句，返回结果集
  
		Args: 
  			sql语句
     
		Returns:
  			结果集
		"""
		if not self.conn:
			self.connect()
		cursor = self.conn.cursor()
		cursor.execute(query)
		result = cursor.fetchall()
		cursor.close()
		return result
		
	def queryNameList(self):
        # 查询文件名列表
		cursor = self.conn.cursor()
		cursor.execute("SELECT name FROM fileInfo")
		rows = cursor.fetchall()
		nameList = []
		for row in rows:
			nameList.append(row[0])
		return nameList

	def insertInfo(self, name: str, state: int) -> int:
		"""插入一条新知识库信息

			Args: 
   				name (string): 文件名
   				state (int): 状态
     
			Returns:
   				int: 插入记录的ID
			Raises:
   				sqlite3.Error: 如果插入失败，抛出异常
			Example:
   				insertInfo("test.txt", 1) 
  		"""
		cursor = self.conn.cursor()
		cursor.execute("INSERT INTO fileInfo (name, state) VALUES (?, ?)", (name, state))
		self.conn.commit()
		return cursor.lastrowid
		
	def deleteInfo(self, id: int):
		"""删除一条知识库信息

			Args:
				id (int): 知识库ID

			Returns:
				int: 删除的记录数
			Raises:
				sqlite3.Error: 如果删除失败，抛出异常
			Example:
				deleteInfo(1) 
  		
  		"""
		cursor = self.conn.cursor()
		cursor.execute("DELETE FROM fileInfo WHERE id = ?", (id,))
		self.conn.commit()
		return cursor.rowcount	
 	
	def updateInfo(self, id: int, state: int):
		"""更新一条数据库信息
			Args:
				id (int): 知识库ID
				state (int): 状态
			Returns:
				None
			Raises:
				sqlite3.Error: 如果更新失败，抛出异常
			Example:
				updateInfo(1, 1) 
  		"""
		cursor = self.conn.cursor()
		cursor.execute("UPDATE fileInfo SET state = ? WHERE id = ?", (state, id))
		self.conn.commit()
  
	def selectInfo(self):
        """获取所有文件信息
			Args:
				None
			Returns:
				list: 文件信息列表
			Raises:
				sqlite3.Error: 如果查询失败，抛出异常
			Example:
				selectInfo() 
        """
		cursor = self.conn.cursor()
		cursor.execute("SELECT * FROM fileInfo")
		rows = cursor.fetchall()
		return rows

	def selectEnableInfo(self):
		"""获取所有已启用的数据库
			Args:
				None
			Returns:
				list: 文件信息列表
			Raises:
				sqlite3.Error: 如果查询失败，抛出异常
			Example:
				selectEnableInfo() 
  		"""
		cursor = self.conn.cursor()
		cursor.execute("SELECT * FROM fileInfo WHERE state = 1")
		rows = cursor.fetchall()
		return rows
  
if __name__ == '__main__':
    # 单元测试
    # 生成数据库单例
    db_manager = DBManager()
    # 连接数据库
    db_manager.connect()
    # 建立表格
    db_manager.createTable()
    # 获得数据
    print(db_manager.selectInfo())   
    # 断开连接 
    db_manager.disconnect()
    
    print("DBmanager Test Success!")