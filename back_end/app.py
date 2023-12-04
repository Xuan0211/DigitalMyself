from flask import Flask,request
from flask_cors import CORS
import json
import os

import globalSetting

from sendToOpenAI import sendMsgToOpenAI
from fileManager import FileManager
file_manager = FileManager()

app = Flask(__name__)
# 解决跨域问题
CORS(app)

# 基础对话
@app.route('/manager/sendMsg', methods=['GET', 'POST'])
def sendMsg():
    getData = request.get_json()
    res = sendMsgToOpenAI(getData)
    data = {
        "ans": res,
    }
    res_json = json.dumps(data)

    return res_json

@app.route('/upload', methods=['POST'])
def uploadFile():
    # 获取上传的文件
    file = request.files['file'] 
    file_manager.uploadFile(file)
    return 'File uploaded successfully!'

@app.route('/manager/dropFile', methods=['GET'])
def dropFile():
    id = request.args.get('id')
    file_manager.dropFile(id)
    return 'File dropped successfully!'

@app.route('/manager/getList', methods=['GET'])
def getList():
    md_files = Path(globalSetting.OUTPUT_FOLDER).rglob('*.csv')

    data = {
        "fileList": []
    }
    
    for file in md_files:
        filename = os.path.splitext(os.path.basename(str(file)))[0]
        data["fileList"].append({"state": 0,"filename": str(filename)})

    res_json = json.dumps(data)
    
    return res_json

@app.route('/manager/getFileList', methods=['GET'] )
def getFileList():
    fileList = []
    
    # 去掉后缀名
    for file in file_manager.getFileList():
        file = list(file)
        file[1] = os.path.splitext(str(file[1]))[0]
        fileList.append({"id": file[0], "filename": file[1], "state": file[2]})
        
    data = {
        "fileList": fileList
    }
    
    res_json = json.dumps(data)
    
    return res_json

@app.route('/manager/changeFileState', methods=['GET'])
def changeFileState():
    id = request.args.get('id')
    state = request.args.get('state')
    file_manager.changeFileState(id, state)
    return 'File state changed successfully!'