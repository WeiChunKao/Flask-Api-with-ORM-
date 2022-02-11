# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import CORS
from user_service.controller import user_service
app = Flask(__name__)
app.register_blueprint(user_service, url_prefix='/user') # 註冊user_service route
CORS(app, supports_credentials=True, cors_allowed_origins='*')


if __name__ == '__main__':
    app.run(threaded=True, use_reloader=False, host='0.0.0.0',
            port=5000, debug=False)  # use_reloader=True,
