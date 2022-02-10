# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask_cors import CORS
from user_service.service import UserClass
import common.handleApiProcess as handleApiProcess
app = Flask(__name__)
CORS(app, supports_credentials=True, cors_allowed_origins='*')


@app.route('/get_user', methods=['POST'])
def get_version() -> dict:
    return UserClass().get_user()

if __name__ == '__main__':
    app.run(threaded=True, use_reloader=False, host='0.0.0.0',
            port=5000, debug=False)  # use_reloader=True,