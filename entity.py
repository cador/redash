from flask_login import UserMixin
import psycopg2
from psycopg2 import extras as ex
import threading
from DBUtils.PooledDB import PooledDB
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())


class X2(object):
    # 设置锁
    _instance_lock = threading.Lock()

    def __init__(self):
        self.pool = PooledDB(
            creator=psycopg2,
            maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
            maxshared=3,  # 链接池中最多共享的链接数量，0和None表示全部共享
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=[],
            ping=0,
            host=os.getenv('x2_host_local') if os.getenv('type') == 'local' else os.getenv('x2_host'),
            port=int(os.getenv('x2_port')),
            user=os.getenv('x2_user'),
            password=os.getenv('x2_password'),
            database=os.getenv('x2_database')
        )

    # 当程序初始化之前,会先调用__new__方法.实现单例模式
    def __new__(cls):
        if not hasattr(X2, "_instance"):
            with X2._instance_lock:
                if not hasattr(X2, "_instance"):
                    X2._instance = object.__new__(cls)
        return X2._instance

    # 设置连接方法
    def connect(self):
        return self.pool.connection()


class DbBase:
    def __init__(self):
        self.conn = X2().connect()

    def query(self, sql, args, fetch=False):
        cur = self.conn.cursor()
        cur.execute(sql, args)
        rows = None
        if fetch:
            rows = cur.fetchall()
        self.conn.commit()
        return rows

    def execute_values(self, sql, args, fetch=False):
        cursor = self.conn.cursor()
        ex.execute_values(cursor, sql, args, page_size=2000)
        rows = None
        if fetch:
            rows = cursor.fetchall()
        self.conn.commit()
        return rows

    def close(self):
        self.conn.close()
