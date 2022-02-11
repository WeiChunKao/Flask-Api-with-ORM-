from user_service.repository import UserTable
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
        UserClass.__flag = True

    def getUser(self) -> Tuple[dict, int, dict]:
        flag, data = UserTable().getUser()
        if flag:
            return Http.commonReturnFormat(True, 'OK', data), 200, Http.postHeader('test')
        else:
            return Http.commonReturnFormat(False, 'NG', data), 400, Http.postHeader('test')

    def updateOneUser(self, updateData: dict, **kwargs: dict) -> Tuple[dict, int, dict]:
        filterString: str = "name= :name"
        flag = UserTable().updateOneUser(filterString, updateData, **kwargs)
        if flag:
            return Http.commonReturnFormat(True, 'OK', {}), 200, Http.postHeader('test')
        else:
            return Http.commonReturnFormat(False, 'NG', {}), 400, Http.postHeader('test')

    def updateAllUser(self, updateData: dict, **kwargs: dict) -> Tuple[dict, int, dict]:
        filterString: str = "name= :name"
        flag = UserTable().updateAllUser(filterString, updateData, **kwargs)
        if flag:
            return Http.commonReturnFormat(True, 'OK', {}), 200, Http.postHeader('test')
        else:
            return Http.commonReturnFormat(False, 'NG', {}), 400, Http.postHeader('test')

    def deleteOne(self, **kwargs: dict) -> Tuple[dict, int, dict]:
        filterString: str = "name= :name"
        flag = UserTable().deleteOneUser(filterString, **kwargs)
        if flag:
            return Http.commonReturnFormat(True, 'OK', {}), 200, Http.postHeader('test')
        else:
            return Http.commonReturnFormat(False, 'NG', {}), 400, Http.postHeader('test')

    def deleteAllUser(self, **kwargs: dict) -> Tuple[dict, int, dict]:
        filterString: str = "name= :name"
        flag = UserTable().deleteOneUser(filterString, **kwargs)
        if flag:
            return Http.commonReturnFormat(True, 'OK', {}), 200, Http.postHeader('test')
        else:
            return Http.commonReturnFormat(False, 'NG', {}), 400, Http.postHeader('test')
