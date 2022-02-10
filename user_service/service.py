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

    def get_user(self) -> Tuple[dict, int, dict]:
        flag, data = UserTable().get_user()
        if flag:
            return Http.commonReturnFormat(True, 'OK', data), 200, Http.postHeader('test')
        else:
            return Http.commonReturnFormat(False, 'OK', data), 400, Http.postHeader('test')
