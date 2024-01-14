# -*- coding: utf-8 -*-
# @Time    : 2023.12.2
# @Author  : Xuan
# @Email   : 2022134346@qq.com
# @File    : globalSetting.py
# @Software: Vscode

"""
    全局配置文件
"""

from pathlib import Path
LOCAL_PATH = str(Path(__file__).parent)
INPUT_FOLDER: str = LOCAL_PATH + '/store/databank/input/'
OUTPUT_FOLDER: str = LOCAL_PATH + '/store/databank/output/'
STORE_FOLDER: str = LOCAL_PATH + '/store/'
DB_FOLDER: str = LOCAL_PATH + '/store/database/'

from enum import Enum
class FileState(Enum):
    DISENABLE = 0    
    ENABLE = 1