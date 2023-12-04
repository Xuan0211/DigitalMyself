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
        if not os.path.exists(globalSetting.INPUT_FOLDER):
            os.makedirs(globalSetting.INPUT_FOLDER)
        if not os.path.exists(globalSetting.OUTPUT_FOLDER):
            os.makedirs(globalSetting.OUTPUT_FOLDER)
        if not os.path.exists(globalSetting.STORE_FOLDER):
            os.makedirs(globalSetting.STORE_FOLDER)
    
    def uploadFile(self, file):
        file_name = str(file.filename)
        db_manager = DBManager()
        db_manager.connect()
        id = db_manager.insertInfo(file_name, globalSetting.FileState.ENABLE.value)
        db_manager.disconnect()
        file_path = globalSetting.INPUT_FOLDER + str(id) + '.' + file_name.split('.')[-1]
        
        if file_name.endswith('.md'):
            file.save(file_path)
            md_file_to_csv(file_path, id)
        elif file_name.endswith('.csv'):
            file.save(file_path)
            self.saveFile(id, file_path)
        else:
            return "File Type Error!"
        
    def dropFile(self, id):
        file_types = ['.md', '.csv']
        for file_type in file_types:
            file_path = globalSetting.INPUT_FOLDER + str(id) + file_type
            if os.path.exists(file_path):                
                os.remove(file_path)
                break
        file_path = globalSetting.OUTPUT_FOLDER + str(id) + '.csv'
        if os.path.exists(file_path):
            os.remove(file_path)
        db_manager = DBManager()
        db_manager.connect()
        db_manager.deleteInfo(id)
        db_manager.disconnect()
        
    def getFileList(self):
        db_manager = DBManager()
        db_manager.connect()
        result = db_manager.selectInfo()
        db_manager.disconnect()
        return result
        
    def changeFileState(self, id, state):
        db_manager = DBManager()
        db_manager.connect()
        db_manager.updateInfo(id, state)
        db_manager.disconnect()
        
    def getEnableFileList(self):
        db_manager = DBManager()
        db_manager.connect()
        result = db_manager.selectEnableInfo()
        db_manager.disconnect()
        return result
    
    def saveFile(self, id, input_file_path):
        output_file_path = globalSetting.OUTPUT_FOLDER + str(id) + '.csv'
        with open(input_file_path, 'rb') as input_file, open(output_file_path, 'wb') as output_file:
            output_file.write(input_file.read())