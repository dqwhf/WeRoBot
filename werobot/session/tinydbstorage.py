# -*- coding: utf-8 -*-
from tinydb import import TinyDB, where,Query
import uuid

from werobot.session import import SessionStorage
from werobot.utils import import json_loads, json_dumps

class TinydbStorage(SessionStorage):
   """
    FileStorage 会把你的 Session 数据以 dbm 形式储存在文件中。

    :param filename: 文件名， 默认为 ``werobot_session``
    """
    def __init__(self,filename="./werobot_session.json", TABLE_NAME='user_profile'):
        _db = TinyDB(filename)
        self._table = _db.table(TABLE_NAME)

    def _get_record(self,open_id): # id是用户openid
        Record = Query()
        record = self._table.get(Record.open_id==open_id) # dict
        return record

    def get(self, open_id): # record_id
        print(open_id)
        record = self._get_record(open_id)
        print(record)
        if record:
            session_json = record["session"]
            return session_json
        return {}


    def set(self, open_id, value):
        record = self._get_record(open_id) #肯定存在
        User = Query()
        session = value
        #print("session:",session) # last
        if record:
            record["session"] = session #存储一个对象
            self._table.update(record,User.open_id==open_id)
            # update
        else:
            # 创建记录
            new_record = {}
            new_record["open_id"] = open_id
            new_record["session"] = session
            print("new_record:",new_record)
            self._table.insert(new_record)

    def delete(self,open_id):
        Record = Query()
        self._table.remove(Record.open_id==open_id)

