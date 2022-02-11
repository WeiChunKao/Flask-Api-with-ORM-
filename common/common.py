# -*- coding: utf-8 -*-
from common.config import Config
from typing import Any, List
from logging import handlers
from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, ForeignKey, text
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.exc import DatabaseError
import sys
import logging
import os
import datetime
import json


def mkdirLogFolder():
    """[summary]
       當前路徑建立LOG資料夾
    """
    if not os.path.exists('log'):
        os.mkdir('log')


class LoggerSetting(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日誌級別關係對映

    def __init__(self, filename, level='info', when='D', backCount=1, fmt='%(asctime)s -[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 設定日誌格式
        self.logger.setLevel(self.level_relations.get(level))  # 設定日誌級別
        sh = logging.StreamHandler()  # 往螢幕上輸出
        sh.setFormatter(format_str)  # 設定螢幕上顯示的格式
        th = handlers.TimedRotatingFileHandler(
            filename=filename, when=when, backupCount=backCount, encoding='utf-8')  # 往檔案裡寫入#指定間隔時間自動生成檔案的處理器
        # 例項化TimedRotatingFileHandler
        # interval是時間間隔，backupCount是備份檔案的個數，如果超過這個個數，就會自動刪除，when是間隔的時間單位，單位有以下幾種：
        # S 秒
        # M 分
        # H 小時、
        # D 天、
        # W 每星期（interval==0時代表星期一）
        # midnight 每天凌晨
        # 如果已經存在則清掉，重新加一個
        if (self.logger.hasHandlers()):
            self.logger.handlers.clear()
        th.setFormatter(format_str)  # 設定檔案裡寫入的格式
        self.logger.addHandler(sh)  # 把物件加到logger裡
        self.logger.addHandler(th)


class Log:
    def __init__(self, filename: str = None):
        """[summary]
           初始化Logger物件
        Args:
            filename ([string], optional): 如果是繼承此物件，filename為NONE反之傳入檔名 Defaults to None.
        """
        if not filename:
            self.__log = LoggerSetting(
                './log/' + self.__class__.__name__ + '.log', level='debug')
        else:
            self.__log = LoggerSetting(
                './log/' + filename + '.log', level='debug')

    def writeLog(self, text: str):
        """[summary]
            Write Info
        Args:
            text ([string]): messages
        """
        self.__log.logger.info(text)

    def writeError(self, text: str):
        """[summary]
            Write Error
        Args:
            text ([string]): messages
        """
        self.__log.logger.error(text)

    def writeWarning(self, text: str):
        """[summary]
            Write Warning
        Args:
            text ([string]): messages
        """
        self.__log.logger.warning(text)

    def writeDebug(self, text: str):
        """[summary]
            Write Debug
        Args:
            text ([string]): messages
        """
        self.__log.logger.debug(text)

    def writeCritical(self, text: str):
        """[summary]
            Write Critical
        Args:
            text ([string]): messages
        """
        self.__log.logger.critical(text)


class Http:
    @staticmethod
    def postHeader(*args, **kwargs) -> dict:
        """[summary]
        POST方法回傳Header，預設使用Config的設定決定使用驗證方式
        Args:
            args: api_key驗證方式，只需要傳入驗證碼
            kwargs: bearer token驗證方式，需要傳入Authorization='xxx'
        Returns:
            dict: api header
        """
        header = {
            "Content-Type": "application/json",
            'Connection': 'close',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'x-requested-with,content-type'
        }
        if Config().postMode == 1:
            header[Config().apiKeyName] = args[0]
        elif Config().postMode == 2:
            header.update(kwargs)
        return header

    @staticmethod
    def getHeaders(*args, **kwargs) -> dict:
        """[summary]
        GET方法回傳Header，預設使用Config的設定決定使用驗證方式
        Args:
            args: api_key驗證方式，只需要傳入驗證碼
            kwargs: bearer token驗證方式，需要傳入Authorization='xxx'
        Returns:
            dict: api header
        """
        header = {
            "Content-Type": "application/json",
            'Connection': 'close',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'x-requested-with,content-type'
        }
        if Config().getMode == 1:
            header[Config().apiKeyName] = args[0]
        elif Config().getMode == 2:
            header.update(kwargs)
        return header

    @staticmethod
    def commonReturnFormat(success: bool = True, message: str = 'xxxx', data: Any = {} or []) -> dict:
        """[summary]
        通用回傳格式
        Args:
            success (bool, optional): True or False. Defaults to True.
            message (str, optional): 訊息. Defaults to 'xxxx'.
            data (Any, optional): 內文，型別可以list or dict. Defaults to {}or[].

        Returns:
            dict: {'success':true, 'message':'xxxxx', 'data':{} 或者[] }
        """
        return {'success': success, 'message': message, 'data': data}


class TimeUtils:

    @staticmethod
    def strToDatetime(date_str: str, date_format: str = '%Y-%m-%d %H:%M:%S') -> datetime.datetime:
        """[summary]
        時間字串轉Datetime
        Args:
            date_str (str): 時間字串
            date_format (str, optional): 轉換格式. Defaults to '%Y-%m-%d %H:%M:%S'.

        Returns:
            datetime.datetime:Datetime
        """
        return datetime.datetime.strptime(date_str, date_format)

    @staticmethod
    def datetimeToStr(date: datetime.datetime, date_format: str = '%Y-%m-%d %H:%M:%S') -> str:
        """[summary]
        Datetime轉時間字串
        Args:
            date (datetime.datetime): Datetime
            date_format (str, optional): 轉換格式. Defaults to '%Y-%m-%d %H:%M:%S'.

        Returns:
            str: 時間字串
        """
        return date.strftime(date_format)

    @staticmethod
    def nowToStr(date_format: str = '%Y-%m-%d %H:%M:%S') -> str:
        """[summary]
        現在時間轉換字串
        Args:
            date_format (str, optional): 轉換格式. Defaults to '%Y-%m-%d %H:%M:%S'.

        Returns:
            str: 時間字串
        """
        return datetime.datetime.now().strftime(date_format)

    @staticmethod
    def nowToDatetime() -> datetime.datetime:
        """[summary]
        現在時間
        Returns:
            datetime.datetime: Datetime
        """
        return datetime.datetime.now()

    @staticmethod
    def beforeDays(days: int = 1, date_format: str = '%Y-%m-%d %H:%M:%S') -> str:
        """[summary]
        當下日期往前推的幾天
        Args:
            days (int, optional): 天數. Defaults to 1.
            date_format (str, optional): 轉換格式. Defaults to '%Y-%m-%d %H:%M:%S'.

        Returns:
            str: 時間字串
        """
        return (datetime.date.today() - datetime.timedelta(days=days)).strftime(date_format)

    @staticmethod
    def futureDays(days: int = 1, date_format: str = '%Y-%m-%d %H:%M:%S') -> str:
        """[summary]
        當下日期往後推的幾天
        Args:
            days (int, optional): 天數. Defaults to 1.
            date_format (str, optional): 轉換格式. Defaults to '%Y-%m-%d %H:%M:%S'.

        Returns:
            str: 時間字串
        """
        return (datetime.date.today() + datetime.timedelta(days=days)).strftime(date_format)

    @staticmethod
    def utcToTaipei(date: datetime.datetime) -> datetime.datetime:
        """[summary]
        UTC時間轉換成台北時間
        Args:
            date (datetime.datetime): Datetime

        Returns:
            datetime.datetime: 轉換後Datetime
        """
        return date + datetime.timedelta(hours=8)


class JsonUtils:
    @staticmethod
    def strToDictOrList(data: str) -> Any:
        """[summary]
        字串轉成Dict Or List
        Args:
            data (str): 字串

        Returns:
            dict: Dict Or List
        """
        return json.loads(data)

    @staticmethod
    def dictOrListToStr(data: Any, sort_keys: bool = False, ensure_ascii: bool = True,
                        indent: int = 1) -> str:
        """[summary]
        Dict Or List轉成字串
        Args:
            data (Any): Dict Or List
            sort_keys (bool, optional): 排序. Defaults to False.
            ensure_ascii (bool, optional): 預設使用的ascii編碼(想輸出中文的話要False). Defaults to True.
            indent (int, optional): 字串間隔. Defaults to 1.

        Returns:
            str: 字串
        """
        return json.dumps(data, sort_keys=sort_keys, ensure_ascii=ensure_ascii, indent=indent)


class Orm:
    def __init__(self, *args, **kwargs):
        self.engine = create_engine(Config().conn, echo=False)
        # 取得資料庫資料
        self.metadata = MetaData()
        # 設定資料庫連線
        self.sessionMaker = sessionmaker(bind=self.engine)
        # 建立連線
        self.session = self.sessionMaker()
        # 建立log物件
        #self.logger = Log(self.__class__.__name__)

    def getSessions(self):
        """[summary]
        ORM 連線
        Returns:
            [sessionmaker]: [description]
        """
        return self.session

    def getMetaData(self):
        """[summary]
        取得資料庫資料
        Returns:
            [MetaData]: 
        """
        return self.metadata

    def setMapper(self, className: Any, table: Table) -> None:
        """[summary]
        設定Class與資料庫對應
        Args:
            className (Any):class
            table (Table): Table
        """
        self.mapper = mapper(className, table)

    def close(self):
        """[summary]
        關閉連線
        """
        self.session.close()

    def insert(self, data: List[Any]) -> None:
        try:
            # self.logger.writeLog(
            #     f"{sys._getframe().f_code.co_name}=>data:{data}")
            self.session.add_all(data)
        except DatabaseError as de:
            # self.logger.writeError(
            #     f"{sys._getframe().f_code.co_name}=>{de}")
            self.session.rollback()
        except Exception as e:
            # self.logger.writeError(
            #     f"{sys._getframe().f_code.co_name}=>{e}")
            self.session.rollback()
        finally:
            self.session.commit()

    def deleteOne(self, className: Any, filterString: str, **kwargs: dict) -> None:
        """[summary]
        刪除單筆資料
        Args:
            className (Any): class物件
            filterString (Any): where條件式
            kwargs (Any): where條件的值
        """
        try:
            # self.logger.writeLog(
            #     f"{sys._getframe().f_code.co_name}=>className:{className.__name__}，filterString:{filterString}，kwargs:{kwargs}")
            row = self.session.query(className).filter(
                text(filterString)
            ).params(**kwargs).one()
            self.session.delete(row)
        except DatabaseError as de:
            # self.logger.writeError(
            #     f"{sys._getframe().f_code.co_name}=>DatabaseError:{de}，className:{className.__name__}，filterString:{filterString}，kwargs:{kwargs}")
            self.session.rollback()
        except Exception as e:
            # self.logger.writeError(
            #     f"{sys._getframe().f_code.co_name}=>Exception:{e}，className:{className.__name__}，filterString:{filterString}，kwargs:{kwargs}")
            self.session.rollback()
        finally:
            self.session.commit()

    def deleteAll(self, className: Any, filterString: String, **kwargs: dict) -> None:
        """[summary]
        刪除多筆資料
        Args:
            className (Any): class物件
            filterString (Any): where條件式
            kwargs (Any): where條件的值
        """
        try:
            # self.logger.writeLog(
            #     f"{sys._getframe().f_code.co_name}=>className:{className.__name__}，filterString:{filterString}，kwargs:{kwargs}")
            row = self.session.query(className).filter(
                text(filterString)
            ).params(**kwargs).delete(synchronize_session=False)
        except DatabaseError as de:
            # self.logger.writeError(
            #     f"{sys._getframe().f_code.co_name}=>DatabaseError:{de}，className:{className.__name__}，filterString:{filterString}，kwargs:{kwargs}")
            self.session.rollback()
            self.close()
        except Exception as e:
            # self.logger.writeError(
            #     f"{sys._getframe().f_code.co_name}=>Exception:{e}，className:{className.__name__}，filterString:{filterString}，kwargs:{kwargs}")
            self.session.rollback()
            self.close()
        finally:
            self.session.commit()

    def updateOne(self, className: Any, filterString: str, updateData: dict, **kwargs: dict) -> None:
        """[summary]
        更新單筆資料
        Args:
            className (Any): class物件
            filterString (Any):  where條件式
            updateData (dict): 更新的資料
            kwargs (Any): where條件的值
        """
        try:
            # self.logger.writeLog(
            #     f"{sys._getframe().f_code.co_name}=>className:{className.__name__}，filterString:{filterString}，kwargs:{kwargs}")
            row = self.session.query(className).filter(
                text(filterString)
            ).params(**kwargs).one()
            for k, v in updateData.items():
                setattr(row, k, v)
            self.session.add(row)
        except DatabaseError as de:
            # self.logger.writeError(
            #     f"{sys._getframe().f_code.co_name}=>DatabaseError:{de}，className:{className.__name__}，filterString:{filterString}，kwargs:{kwargs}")
            self.session.rollback()
        except Exception as e:
            # self.logger.writeError(
            #     f"{sys._getframe().f_code.co_name}=>Exception:{e}，className:{className.__name__}，filterString:{filterString}，kwargs:{kwargs}")
            self.session.rollback()
        finally:
            self.session.commit()

    def updateAll(self, className: Any, filterString: Any, updateData: dict, **kwargs: dict) -> None:
        """[summary]
        更新多筆資料
        Args:
            className (Any): class物件
            filterString (Any): where條件式
            updateData (dict): 需要更新的欄位名稱及值
            kwargs:where條件式的值
        """
        try:
            # self.logger.writeLog(
            #     f"{sys._getframe().f_code.co_name}=>className:{className.__name__}，filterString:{filterString}，kwargs:{kwargs}")
            updata: dict = {}
            for k, v in updateData.items():
                updata[className.__dict__.get(k, '')] = v
            self.session.query(className).filter(
                text(filterString).params(**kwargs)
            ).update(
                updata, synchronize_session=False)
        except DatabaseError as de:
            # self.logger.writeError(
            #     f"{sys._getframe().f_code.co_name}=>DatabaseError:{de}，className:{className.__name__}，filterString:{filterString}，kwargs:{kwargs}")
            self.session.rollback()
        except Exception as e:
            # self.logger.writeError(
            #     f"{sys._getframe().f_code.co_name}=>Exception:{e}，className:{className.__name__}，filterString:{filterString}，kwargs:{kwargs}")
            self.session.rollback()
        finally:
            self.session.commit()


if __name__ == '__main__':
    mkdirLogFolder()
else:
    mkdirLogFolder()
