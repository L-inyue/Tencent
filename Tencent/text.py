"""
   名称：
        
   简介：
        1.
"""
# !/usr/bin/python3

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["tencent"]
mycol = mydb["tencentset"]

for x in mycol.find():
    print(x)