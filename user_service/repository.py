
# -*- coding: utf-8 -*-
from sqlalchemy import Table, Column, String, Integer
from common.common import Orm, Log
from user_service.model import User
from typing import Tuple
import pandas as pd
import sys
import traceback


class UserTable:
    __instance = None
    __flag = False

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self,):
        if UserTable.__flag:
            return
        self.orm = Orm()
        self.user = Table('user', self.orm.getMetaData(),
                          Column('id', String(50), primary_key=True),
                          Column('name', String(50)),
                          Column('test', Integer())
                          )
        self.orm.setMapper(User, self.user)
        self.log = Log(self.__class__.__name__)
        UserTable.__flag = True

    def get_user(self) -> Tuple[bool, list]:
        try:

            query = self.orm.getSessions().query(User).order_by(User.id)
            df = pd.read_sql(query.statement, self.orm.getSessions().bind)
            if df.empty:
                return {}
            return True, df.to_dict(orient='records')
        except Exception as e:
            self.orm.close()
            error_class = e.__class__.__name__  # 取得錯誤類型
            detail = e.args[0]  # 取得詳細內容
            cl, exc, tb = sys.exc_info()  # 取得Call Stack
            lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
            fileName = lastCallStack[0]  # 取得發生的檔案名稱
            lineNum = lastCallStack[1]  # 取得發生的行號
            funcName = lastCallStack[2]  # 取得發生的函數名稱
            return False, [{"detail": detail, 'fileName': fileName, 'lineNum': lineNum, 'funcName': funcName}]
        finally:
            self.orm.close()
