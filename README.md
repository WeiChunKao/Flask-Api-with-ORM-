# Python-Flask-ORM
## common資料夾提供基本py檔函式。  
### commom.py:內有Log、Http、TimeUtils、JsonUtils、Orm等等函式可以呼叫，可以供不同service呼叫  
### config.py:設定相關參數，使用os.getenv未來轉到k8s或是docker-compose啟動時可以定義在YAML檔。K8S可以用secret yaml將敏感參數加密  
### handleApiProccess.py: 定義裝飾器做為驗證token的方法，只需要在每個route掛上即可在request進到邏輯層前先驗證token  
## user_serive資料夾定義相關使用者的邏輯  
### model.py: 定義資料庫 table欄位  
### controller.py: 定義route  
### repository.py: 資料庫相關操作  
### service.py: 邏輯層處理  
## POST  
### getUser:curl --location --request POST 'http://127.0.0.1:5000/user/getUser' \
--header 'id: eyJtYWNoaW5lTmFtZSI6ICJ0ZXN0IiwgInRpbWUiOiAiMTIzIn0='  
### updateOneUser:
