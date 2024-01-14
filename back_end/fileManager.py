# -*- coding: utf-8 -*-
# @Time    : 2023.12.2
# @Author  : Xuan
# @Email   : 2022134346@qq.com
# @File    : fileManager.py
# @Software: Vscode

import os

from md2csv import md_file_to_csv
from DBmanager import DBManager

import globalSetting
    
def singleton(cls):
	instances = {}
	def wrapper(*args, **kwargs):
		if cls not in instances:
			instances[cls] = cls(*args, **kwargs)
		return instances[cls]
	return wrapper

@singleton   
class FileManager:
    def __init__(self):
        # 初始化文件路径
        if not os.path.exists(globalSetting.INPUT_FOLDER):
            os.makedirs(globalSetting.INPUT_FOLDER)
        if not os.path.exists(globalSetting.OUTPUT_FOLDER):
            os.makedirs(globalSetting.OUTPUT_FOLDER)
        if not os.path.exists(globalSetting.STORE_FOLDER):
            os.makedirs(globalSetting.STORE_FOLDER)
    
    def uploadFile(self, file):
        """处理上传的文件
        Args:
            file: 上传的文件对象
        Returns:
            上传结果信息
        """
        file_name = str(file.filename)
        
        # 往数据库中插入文件信息
        db_manager = DBManager()
        db_manager.connect()
        # 默认启用知识库
        id = db_manager.insertInfo(file_name, globalSetting.FileState.ENABLE.value)
        db_manager.disconnect()
        
        # 往本地存入知识库
        file_path = globalSetting.INPUT_FOLDER + str(id) + '.' + file_name.split('.')[-1]
        
        # 多格式文件格式转化和过滤
        if file_name.endswith('.md'):
            file.save(file_path)
            md_file_to_csv(file_path, id)
        elif file_name.endswith('.csv'):
            file.save(file_path)
            self.saveFile(id, file_path)
        else:
            # [TODO] 处理其他文件格式
            return "File Type Error!"
        
    def dropFile(self, id):
        """从数据库和本地删除对应id的文件
        Args:
            id: 文件id
        Returns:
            上传结果信息
        """
        file_types = ['.md', '.csv']
        for file_type in file_types:
            file_path = globalSetting.INPUT_FOLDER + str(id) + file_type
            if os.path.exists(file_path):                
                os.remove(file_path)
                break
        file_path = globalSetting.OUTPUT_FOLDER + str(id) + '.csv'
        if os.path.exists(file_path):
            os.remove(file_path)
            
        # 从数据库中删除
        db_manager = DBManager()
        db_manager.connect()
        db_manager.deleteInfo(id)
        db_manager.disconnect()
        
    def getFileList(self):
        """
            
        """
        db_manager = DBManager()
        db_manager.connect()
        result = db_manager.selectInfo()
        db_manager.disconnect()
        return result
        
    def changeFileState(self, id, state):
        """改变文件状态
        
        Args:
            id (int): 文件id
            state (int): 文件状态
        Returns:
            None
        """
        db_manager = DBManager()
        db_manager.connect()
        db_manager.updateInfo(id, state)
        db_manager.disconnect()
        
    def getEnableFileList(self):
        """获取已启用的数据库列表
        
        Args:
            None
        Returns:
            数据库列表信息
        """
        db_manager = DBManager()
        db_manager.connect()
        result = db_manager.selectEnableInfo()
        db_manager.disconnect()
        return result
    
    def saveFile(self, id, input_file_path):
        """
            保存csv文件到本地存储位置
            Args:
                id: 文件id
                input_file_path: 文件路径
            Returns:
                None
        """
        # [TODO] 本模块应该尽快废弃
        output_file_path = globalSetting.OUTPUT_FOLDER + str(id) + '.csv'
        with open(input_file_path, 'rb') as input_file, open(output_file_path, 'wb') as output_file:
            output_file.write(input_file.read())