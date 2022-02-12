
# 定義對應Table的Model
class User:
    def __init__(self, id, name, test, *args, **kwargs):
        self.id = id
        self.name = name
        self.test = test
