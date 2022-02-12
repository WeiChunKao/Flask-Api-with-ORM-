from this import s
from user_service.repository import UserTable
from user_service.model import User
from common.common import Http, Log
from typing import Tuple


class UserClass:
    __instance = None
    __flag = False

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        if UserClass.__flag:
            return
        self.log = Log(self.__class__.__name__)
        self.userTable = UserTable()
        UserClass.__flag = True

    def getUser(self) -> Tuple[dict, int, dict]:
        flag, msg = self.userTable.getAllUser()
        if flag:
            return Http.commonReturnFormat(flag, 'OK', msg), 200, Http.postHeader('test')
        else:
            return Http.commonReturnFormat(flag, 'NG', msg), 400, Http.postHeader('test')

    def addUser(self, data: list) -> Tuple[dict, int, dict]:
        rows: list = []
        # where條件式
        filterString = "name=: name"
        for d in data:
            # 判斷傳入List內的dict是否為Model User的子集，如果是子集為True，則False
            if not set(d.keys()) < set(User.__dict__.keys()):
                return Http.commonReturnFormat(flag, 'NG', {"message": f'第{data.index(d) + 1}使用者缺少參數'}), 404, Http.postHeader('test')
            # 先select資料庫是否存在資料
            sflag, sdata = self.userTable.getOneUser(
                filterString, name=d['name'])
            if not sflag and not sdata:
                rows.append(User(d['id'], d['name'], d['test']))
            else:
                return Http.commonReturnFormat(sflag, f"{d['name']} field data duplicated", {}), 404, Http.postHeader('test')
        flag, msg = self.userTable.addUser(rows)
        if flag:
            return Http.commonReturnFormat(flag, 'OK', {"message": msg}), 200, Http.postHeader('test')
        else:
            return Http.commonReturnFormat(flag, 'NG', {"message": msg}), 400, Http.postHeader('test')

    def updateOneUser(self, updateData: dict, **kwargs: dict) -> Tuple[dict, int, dict]:
        # where條件式
        filterString: str = "name= :name"
        flag, msg = self.userTable.updateOneUser(
            filterString, updateData, **kwargs)
        if flag:
            return Http.commonReturnFormat(flag, 'OK', {"message": msg}), 200, Http.postHeader('test')
        else:
            return Http.commonReturnFormat(flag, 'NG', {"message": msg}), 400, Http.postHeader('test')

    def updateAllUser(self, updateData: dict, **kwargs: dict) -> Tuple[dict, int, dict]:
        # where條件式
        filterString: str = "name= :name"
        flag, msg = self.userTable.updateAllUser(
            filterString, updateData, **kwargs)
        if flag:
            return Http.commonReturnFormat(True, 'OK', {"message": msg}), 200, Http.postHeader('test')
        else:
            return Http.commonReturnFormat(False, 'NG', {"message": msg}), 400, Http.postHeader('test')

    def deleteOne(self, **kwargs: dict) -> Tuple[dict, int, dict]:
        # where條件式
        filterString: str = "name= :name"
        flag, msg = self.userTable.deleteOneUser(filterString, **kwargs)
        if flag:
            return Http.commonReturnFormat(flag, 'OK',  {"message": msg}), 200, Http.postHeader('test')
        else:
            return Http.commonReturnFormat(flag, 'NG',  {"message": msg}), 400, Http.postHeader('test')

    def deleteAllUser(self, **kwargs: dict) -> Tuple[dict, int, dict]:
        # where條件式
        filterString: str = "name= :name"
        flag, msg = self.userTable.deleteOneUser(filterString, **kwargs)
        if flag:
            return Http.commonReturnFormat(flag, 'OK', {"message": msg}), 200, Http.postHeader('test')
        else:
            return Http.commonReturnFormat(flag, 'NG', {"message": msg}), 400, Http.postHeader('test')
