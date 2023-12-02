# DigitalMyself

`DigitalMyself`是一个面向个人用户的个性化数字知识分身。

`DigitalMyself`将实现对占据个人移动设备的大量数据进行数据图谱构建，站在用户自身角度，充分利用各类数据进行管理。实现对自身数据的解析管理、事务安排助手并使其具备简单的补充性人际交往能力。

项目将以私人微信/QQ聊天记录与语音作为数据来源，经隐私信息脱敏后，放入大语言模型中进行参数微调，并采用文本、语音、XR多模态交互方式，实现计算驱动型实时人机交互原型，创建个人用户的虚拟世界生活化社交第二分身。

## 文档地址
https://www.wolai.com/mawxuan/sspE2LDT6NDquaGr4HuWbx
## ATTENTION
`DigitalMyself`是CSU-2023FALL-SoftwareEngineering的课程设计，指导老师为ZUDE
## 环境要求
* python = 3.9
## install
```shell
pip install flask
pip install torch # conda install pytorch
pip install -U similarities
```
如果要使用前端，则在front_end/web/digital_myself_fronted_vue目录中执行
```shell
npm install 
```
## run
如果要运行后端，则在back_end/目录中执行
```shell
flask run
```
如果要运行前端，则在front_end/web/digital_myself_fronted_vue目录中执行
```shell
npm run dev
```
## THANKS
### 参考项目
todo
### 开源项目使用
* element：UI组件支持
* axios：前端请求构建
* flask：Python后端框架
* [similarities](https://github.com/shibing624/similarities)：本地搜索
### api使用
* openAI：CHATGPT大语言模型