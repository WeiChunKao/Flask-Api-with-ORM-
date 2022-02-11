
# -*- coding: utf-8 -*-
from sqlalchemy import Table, Column, String, Integer
from common.common import Orm, Log
from user_service.model import User
from typing import Tuple, Any, List
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

    def addUser(self, data: List[Any]) -> Tuple[bool, str]:
        """[summary]
        新增使用者
        Args:
            data (list): 新增使用者陣列 [{}]
        Returns:
            Tuple[bool, str]: 1:(True,"") 2:(False,ErrorMessage)
        """
        try:
            self.log.writeLog(
                f"{sys._getframe().f_code.co_name}=>data{data}")
            return self.orm.insert(data)
        except Exception as e:
            self.orm.close()
            error_class = e.__class__.__name__  # 取得錯誤類型
            detail = e.args[0]  # 取得詳細內容
            cl, exc, tb = sys.exc_info()  # 取得Call Stack
            lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
            fileName = lastCallStack[0]  # 取得發生的檔案名稱
            lineNum = lastCallStack[1]  # 取得發生的行號
            funcName = lastCallStack[2]  # 取得發生的函數名稱
            self.log.writeError(
                f"{sys._getframe().f_code.co_name}=>detail{detail}，fileName:{fileName}，lineNum:{lineNum}")
            return False, f"detail:{detail}，fileName:{fileName}，lineNum:{lineNum}，funcName:{funcName}"
        finally:
            self.orm.close()

    def getAllUser(self) -> Tuple[bool, list]:
        """[summary]
        取得所有使用者
        Returns:
            Tuple[bool, list]: 1:(True,[{userdata}]) 2:(False, list[{ErrorMessage}])
        """
        try:
            query = self.orm.getSessions().query(User).order_by(User.id)
            df = pd.read_sql(query.statement, self.orm.getSessions().bind)
            if df.empty:
                return False, []
            self.log.writeLog(
                f"{sys._getframe().f_code.co_name}=>df{df.to_dict(orient='records')}")
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
            self.log.writeError(
                f"{sys._getframe().f_code.co_name}=>detail{detail}，fileName:{fileName}，lineNum:{lineNum}")
            return False, [{"detail": detail, 'fileName': fileName, 'lineNum': lineNum, 'funcName': funcName}]
        finally:
            self.orm.close()

    def updateOneUser(self, filterString: str, updateData: dict, **kwargs: dict) -> Tuple[bool, str]:
        """[summary]
        更新單一使用者
        Args:
            filterString (str): where條件式
            updateData (dict): 更新欄位資料{column:value}
            kwargs:where條件式的值
        Returns:
            Tuple[bool, str]: 1:(True,"") 2:(False,ErrorMessage)
        """
        try:
            self.log.writeLog(
                f"{sys._getframe().f_code.co_name}=>className:{User.__name__}，filterString:{filterString}，updateData:{updateData}，kwargs:{kwargs}")
            return self.orm.updateOne(User, filterString, updateData, **kwargs)
        except Exception as e:
            self.orm.close()
            error_class = e.__class__.__name__  # 取得錯誤類型
            detail = e.args[0]  # 取得詳細內容
            cl, exc, tb = sys.exc_info()  # 取得Call Stack
            lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
            fileName = lastCallStack[0]  # 取得發生的檔案名稱
            lineNum = lastCallStack[1]  # 取得發生的行號
            funcName = lastCallStack[2]  # 取得發生的函數名稱
            self.log.writeError(
                f"{sys._getframe().f_code.co_name}=>detail:{detail}，fileName:{fileName}，lineNum:{lineNum}，funcName{funcName}->className:{User.__name__}，\
                    filterString:{filterString}，updateData:{updateData}，kwargs:{kwargs}")
            return False, f"{sys._getframe().f_code.co_name}=>detail:{detail}，fileName:{fileName}，lineNum:{lineNum}，funcName{funcName}"
        finally:
            self.orm.close()

    def updateAllUser(self, filterString: str, updateData: dict, **kwargs: dict) -> Tuple[bool, str]:
        """[summary]
        更新所有使用者
        Args:
            filterString (str): where條件式
            updateData (dict): 更新欄位資料{column:value}
            kwargs:where條件式的值
        Returns:
            Tuple[bool, str]: 1:(True,"") 2:(False,ErrorMessage)
        """
        try:
            self.log.writeLog(
                f"{sys._getframe().f_code.co_name}=>className:{User.__name__}，filterString:{filterString}，updateData:{updateData}，kwargs:{kwargs}")
            return self.orm.updateAll(User, filterString, updateData, **kwargs)
        except Exception as e:
            self.orm.close()
            error_class = e.__class__.__name__  # 取得錯誤類型
            detail = e.args[0]  # 取得詳細內容
            cl, exc, tb = sys.exc_info()  # 取得Call Stack
            lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
            fileName = lastCallStack[0]  # 取得發生的檔案名稱
            lineNum = lastCallStack[1]  # 取得發生的行號
            funcName = lastCallStack[2]  # 取得發生的函數名稱
            self.log.writeError(
                f"{sys._getframe().f_code.co_name}=>detail:{detail}，fileName:{fileName}，lineNum:{lineNum}，funcName:{funcName}->className:{User.__name__}，\
                    filterString:{filterString}，updateData:{updateData}，kwargs:{kwargs}")
            return False, f"{sys._getframe().f_code.co_name}=>detail:{detail}，fileName:{fileName}，lineNum:{lineNum}，funcName:{funcName}"
        finally:
            self.orm.close()

    def deleteOneUser(self, filterString: str, **kwargs: dict) -> Tuple[bool, str]:
        """[summary]
        刪除單一使用者
        Args:
            filterString (str): where條件式
            kwargs:where條件式的值
        Returns:
            Tuple[bool, str]: 1:(True,"") 2:(False,ErrorMessage)
        """
        try:
            self.log.writeLog(
                f"{sys._getframe().f_code.co_name}=>className:{User.__name__}，filterString:{filterString}，kwargs:{kwargs}")
            return self.orm.deleteOne(User, filterString, **kwargs)
        except Exception as e:
            self.orm.close()
            error_class = e.__class__.__name__  # 取得錯誤類型
            detail = e.args[0]  # 取得詳細內容
            cl, exc, tb = sys.exc_info()  # 取得Call Stack
            lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
            fileName = lastCallStack[0]  # 取得發生的檔案名稱
            lineNum = lastCallStack[1]  # 取得發生的行號
            funcName = lastCallStack[2]  # 取得發生的函數名稱
            self.log.writeError(
                f"{sys._getframe().f_code.co_name}=>detail:{detail}，fileName:{fileName}，lineNum:{lineNum}，funcName:{funcName}->className:{User.__name__}，\
                    filterString:{filterString}，kwargs:{kwargs}")
            return False, f"{sys._getframe().f_code.co_name}=>detail:{detail}，fileName:{fileName}，lineNum:{lineNum}，funcName:{funcName}"
        finally:
            self.orm.close()

    def deleteOneUser(self, filterString: str, **kwargs: dict) -> Tuple[bool, str]:
        """[summary]
        刪除所有使用者
        Args:
            filterString (str): where條件式
            kwargs:where條件式的值
        Returns:
            Tuple[bool, str]: 1:(True,"") 2:(False,ErrorMessage)
        """
        try:
            self.log.writeLog(
                f"{sys._getframe().f_code.co_name}=>className:{User.__name__}，filterString:{filterString}，kwargs:{kwargs}")
            return self.orm.deleteAll(User, filterString, **kwargs)
        except Exception as e:
            self.orm.close()
            error_class = e.__class__.__name__  # 取得錯誤類型
            detail = e.args[0]  # 取得詳細內容
            cl, exc, tb = sys.exc_info()  # 取得Call Stack
            lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
            fileName = lastCallStack[0]  # 取得發生的檔案名稱
            lineNum = lastCallStack[1]  # 取得發生的行號
            funcName = lastCallStack[2]  # 取得發生的函數名稱
            self.log.writeError(
                f"{sys._getframe().f_code.co_name}=>detail:{detail}，fileName:{fileName}，lineNum:{lineNum}，funcName:{funcName}->className:{User.__name__}，\
                    filterString:{filterString}，kwargs:{kwargs}")
            return False, f"{sys._getframe().f_code.co_name}=>detail:{detail}，fileName:{fileName}，lineNum:{lineNum}，funcName:{funcName}"
        finally:
            self.orm.close()
