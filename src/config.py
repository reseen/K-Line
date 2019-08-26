import json

PATH_PUBLIC    = 'D:/K-Line/data/public.json'        # 公有配置文件
PATH_PRIVATE   = 'D:/K-Line/data/private.json'       # 私有配置文件

PATH_DB_STOCKA = 'D:/K-Line/data/stockA.db'          # A股数据库
PATH_DB_ENERGY = 'D:/K-Line/data/energy.db'          # 能源期货数据库


class config():

    def __init__(self):
        self.pubPath = PATH_PUBLIC
        self.prvPath = PATH_PRIVATE

    # 获取配置文件
    def __getConfig(self, path):
        try:
            with open(path, 'r', encoding = 'UTF-8') as f:    # 打开文件
                sconfig = f.read()                            # 读取文件
                return json.loads(sconfig)
        except:
            print('配置文件"%s"不存在，请检查。' % path)

    # 读取公有配置文件
    def public(self):
        return self.__getConfig(self.pubPath)

    # 读取私有配置文件
    def private(self):
        return self.__getConfig(self.prvPath)