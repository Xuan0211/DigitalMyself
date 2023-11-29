from flask import Flask,request
from flask_cors import CORS
import json
from sendToOpenAI import sendMsgToOpenAI
app = Flask(__name__)
# 解决跨域问题
CORS(app)


@app.route('/manager/sendMsg', methods=['GET', 'POST'])
def hi():
    getData = request.get_json()
    res = sendMsgToOpenAI(getData)
    data = {
        "ans": res,
    }
    res_json = json.dumps(data)

    return res_json