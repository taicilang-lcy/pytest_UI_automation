# src/my_project/utils/db_manager.py
import sqlite3


#conftest.py里 @pytest.fixture(scope='session') def db():的定义
#这里这个写法，用了生成器 生成 db_manager ，而且是 scope='session' 基本的，所以我理解这个写法 在一个进程里执行 pytest的test case，即使不用单例模式，也不会有重复的DatabaseManager()类被实例化
class DatabaseManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_name="test.db"):
        if not hasattr(self, "connection"):  # 防止重复初始化
            self.connection = sqlite3.connect(db_name)
            self.cursor = self.connection.cursor()
            print(f"Database {db_name} connected")

    def execute_query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.connection.commit()

    def close_connection(self):
        self.connection.close()
        print("Database connection closed")

