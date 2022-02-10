# -*- coding: utf-8 -*-
from typing import Any
from functools import wraps
from flask import request


def apiLoginProcess(func: Any) -> Any:
    """[summary]
    處理驗證
    Args:
        func ([type]): 方法

    Returns:
        Any: 回傳、狀態碼、Header
    """
    @wraps(func)
    def wrapper(*args: tuple, **kwargs: dict) -> Any:
        print(f"args:{args}")
        print(f"kwargs:{kwargs}")
        print(request.json)
        return func(*args, **kwargs)
    return wrapper
