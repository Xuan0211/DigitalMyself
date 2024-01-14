# -*- coding: utf-8 -*-
# @Time    : 2023.1.13
# @Author  : Xuan
# @Email   : 2022134346@qq.com
# @File    : app.py
# @Software: Vscode

"""
    本模块负责解析前端请求，调用后端。
"""
# 调用flask框架
from flask import Flask,request
# 调用 CORS 解决跨域问题
from flask_cors import CORS
# json解析器
import json
# 地址解析
import os

# 调用全局设置
import globalSetting

# 调用算法模块和文件模块的两边际类
from sendToOpenAI import sendMsgToOpenAI
from fileManager import FileManager
# 获取单例
file_manager = FileManager()

app = Flask(__name__)
# 解决跨域问题
CORS(app)

# 基础对话
@app.route('/manager/sendMsg', methods=['GET', 'POST'])
    """
        解析前端请求，返回机器人对话
    """
    # 获取问题
    getData = request.get_json()
    # 生成答案
    res = sendMsgToOpenAI(getData)
    # 返回答案
    data = {
        "ans": res,
    }
    res_json = json.dumps(data)

    return res_json

@app.route('/upload', methods=['POST'])
def uploadFile():
    """
        获取并处理前端上传的文件，将其作为知识库存储下来
    """
    # 获取文件
    file = request.files['file']
    # 处理文件
    file_manager.uploadFile(file)
    return 'File uploaded successfully!'

@app.route('/manager/dropFile', methods=['GET'])
def dropFile():
    """
        根据前端发来的id删除对应的知识库
    """
    # 获取文件id
    id = request.args.get('id')
    # 删除文件
    file_manager.dropFile(id)
    return 'File dropped successfully!'

@app.route('/manager/getFileList', methods=['GET'] )
def getFileList():
    """
        获取全部知识库
    """
    fileList = []
    
    # 获取文件列表并去掉后缀名，转化为正确json格式
    for file in file_manager.getFileList():
        file = list(file)
        file[1] = os.path.splitext(str(file[1]))[0]
        """
            id: 文件id
            filename: 文件名 string
            state: 文件状态 0：未启用 1：启用
        """
        fileList.append({"id": file[0], "filename": file[1], "state": file[2]})
        
    data = {
        "fileList": fileList
    }
    
    res_json = json.dumps(data)
    
    return res_json

@app.route('/manager/changeFileState', methods=['GET'])
def changeFileState():
    """
        根据id启用/禁用知识库
    """
    id = request.args.get('id')
    state = request.args.get('state')
    file_manager.changeFileState(id, state)
    return 'File state changed successfully!'