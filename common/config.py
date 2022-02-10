# -*- coding: utf-8 -*-
from typing import Any
import os


class Config:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.dbHost = os.getenv('dbHost', '127.0.0.1')  # 資料庫 Ip
        self.dbPort = os.getenv('dbPort', '3306')  # 資料庫 Port
        self.dbUserName = os.getenv('dbUserName', 'root')  # 資料庫使用者帳號
        self.dbUserPassword = os.getenv('dbUserPassword', '5190')  # 資料庫使用者密碼
        self.dbDatabase = os.getenv('dbDatabase', 'testdb')  # 資料庫使用的DB
        # POST方法使用的驗證方式 1:api_key 2: bearer token
        self.postMode = os.getenv('postMode', 1)
        # GET方法使用的驗證方式 1:api_key 2: bearer token
        self.getMode = os.getenv('getMode', 1)
        # api_key的Key Name
        self.apiKeyName = os.getenv('apiKeyName', 'api_key')
        # 選擇使用的資料庫 1: Mysql(Maria) 2: Postgresql 3: Sql Server
        self.dbMode = os.getenv('dbMode', 1)
        # 回傳建立資料庫連線字串
        self.conn = self.switch(self.dbMode)
    def switch(self, dbMode: int = 1) -> str:
        switcher = {
            1: f'mysql+pymysql://{self.dbUserName}:{self.dbUserPassword}@{self.dbHost}:{self.dbPort}/{self.dbDatabase}',
            2: f"postgresql://{self.dbUserName}:{self.dbUserPassword}@{self.dbHost}:{self.dbPort}/{self.dbDatabase}",
            3: f'mssql+pymssql://{self.dbUserName}:{self.dbUserPassword}@{self.dbHost}:{self.dbPort}/{self.dbDatabase}'
        }
        return switcher.get(dbMode, 1)
