from flask import Blueprint, request, abort
from user_service.service import UserClass
from common.common import Http
import common.handleApiProcess as handleApiProcess
user_service = Blueprint('user_service', __name__)


@user_service.route('/getUser', methods=['POST'])
# @handleApiProcess.apiLoginProcess()
def getUser() -> dict:
    if not request:
        abort(400)
    return UserClass().getUser()


@user_service.route('/updateOneUser', methods=['POST'])
# @handleApiProcess.apiLoginProcess()
def updateOneUser() -> dict:
    if not request:
        abort(400)
    elif "updateData" not in request.json or 'name' not in request.json:
        return Http.commonReturnFormat(True, '缺少參數', {}), 400, Http.postHeader('')
    elif not isinstance(request.json['updateData'], dict) or not isinstance(request.json['name'], str):
        return Http.commonReturnFormat(True, '參數型別不正確', {}), 400, Http.postHeader('')
    return UserClass().updateOneUser(request.json['updateData'], name=request.json['name'])


@user_service.route('/updateAllUser', methods=['POST'])
# @handleApiProcess.apiLoginProcess()
def updateAllUser() -> dict:
    if not request:
        abort(400)
    elif "updateData" not in request.json or 'name' not in request.json:
        return Http.commonReturnFormat(True, '缺少參數', {}), 400, Http.postHeader('')
    elif not isinstance(request.json['updateData'], dict) or not isinstance(request.json['name'], str):
        return Http.commonReturnFormat(True, '參數型別不正確', {}), 400, Http.postHeader('')
    return UserClass().updateAllUser(request.json['updateData'], name=request.json['name'])

@user_service.route('/deleteOneUser', methods=['POST'])
# @handleApiProcess.apiLoginProcess()
def deleteOneUser() -> dict:
    if not request:
        abort(400)
    elif  'name' not in request.json:
        return Http.commonReturnFormat(True, '缺少參數', {}), 400, Http.postHeader('')
    elif not isinstance(request.json['name'], str):
        return Http.commonReturnFormat(True, '參數型別不正確', {}), 400, Http.postHeader('')
    return UserClass().deleteOne(name=request.json['name'])

@user_service.route('/deleteAllUser', methods=['POST'])
# @handleApiProcess.apiLoginProcess()
def deleteAllUser() -> dict:
    if not request:
        abort(400)
    elif  'name' not in request.json:
        return Http.commonReturnFormat(True, '缺少參數', {}), 400, Http.postHeader('')
    elif not isinstance(request.json['name'], str):
        return Http.commonReturnFormat(True, '參數型別不正確', {}), 400, Http.postHeader('')
    return UserClass().deleteAllUser(name=request.json['name'])