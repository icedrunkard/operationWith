# -*- coding: utf8 -*-
import pymongo
from bson.code import Code

client = pymongo.MongoClient('localhost:27009')
db = client['cnki']




col= db['papers']


if col.find():
    print(col.find().count())
else:
    print('none')
