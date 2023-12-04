#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import hmac
import ctypes
import hashlib
import argparse
import ProgressBar
#import pyaes
from Crypto.Cipher import AES


def decrypt_msg(path, password, taskid ,tasktotal):
    
    KEY_SIZE = 32
    DEFAULT_ITER = 64000
    DEFAULT_PAGESIZE = 4096  # 4048数据 + 16IV + 20 HMAC + 12
    SQLITE_FILE_HEADER = bytes("SQLite format 3", encoding="ASCII") + bytes(1)  # SQLite 文件头
    
    password = bytes.fromhex(password)
    with open(path, "rb") as f:
        # TODO: 优化，考虑超大文件
        blist = f.read()

    salt = blist[:16]  # 前16字节为盐
    key = hashlib.pbkdf2_hmac("sha1", password, salt, DEFAULT_ITER, KEY_SIZE)  # 获得Key

    page1 = blist[16:DEFAULT_PAGESIZE]  # 丢掉salt

    mac_salt = bytes([x ^ 0x3a for x in salt])
    mac_key = hashlib.pbkdf2_hmac("sha1", key, mac_salt, 2, KEY_SIZE)

    hash_mac = hmac.new(mac_key, digestmod="sha1")
    hash_mac.update(page1[:-32])
    hash_mac.update(bytes(ctypes.c_int(1)))

    if hash_mac.digest() != page1[-32:-12]:
        raise RuntimeError("[-]解密失败 密码错误: ",password)
    
    
    pages = [blist[i:i+DEFAULT_PAGESIZE] for i in range(DEFAULT_PAGESIZE, len(blist), DEFAULT_PAGESIZE)]
    pages.insert(0, page1)  # 把第一页补上
    with open(f"{path}.dec.db", "wb") as f:
        f.write(SQLITE_FILE_HEADER)  # 写入文件头

        count = 0
        for i in pages:
            t = AES.new(key, AES.MODE_CBC, i[-48:-32])
            f.write(t.decrypt(i[:-48]))
            f.write(i[-48:])
            count += 1
            ProgressBar.progress_bar("正在解密第"+str(taskid)+"项, 共"+str(tasktotal)+"项",count,len(pages))
