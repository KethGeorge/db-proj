import mysql.connector
from mysql.connector import Error
from flask import current_app # 用于获取 app.config

def get_db_connection():
    """建立数据库连接并返回连接对象"""
    try:
        conn = mysql.connector.connect(
            host=current_app.config['DB_HOST'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            database=current_app.config['DB_DATABASE']
        )
        if conn.is_connected():
            print("成功连接到MySQL数据库")
            return conn
    except Error as e:
        print(f"连接MySQL数据库失败: {e}")
        return None

""" def execute_query(conn, query, params=None, fetch_one=False, is_insert=False):
    执行 SQL 查询并处理结果
    cursor = conn.cursor()
    try:
        cursor.execute(query, params or ()) # 确保 params 是一个元组或列表

        if is_insert:
            conn.commit()
            return cursor.lastrowid if cursor.lastrowid else True # 对于无自增ID的表，lastrowid可能是0
        elif query.strip().upper().startswith("SELECT"):
            result = cursor.fetchone() if fetch_one else cursor.fetchall()
            return result
        else:
            conn.commit()
            return True
    except Error as e:
        print(f"执行查询失败: {query} -> {e}")
        conn.rollback() # 出现错误时回滚事务
        raise # 抛出异常，让上层调用者处理
    finally:
#   """       #cursor.close()

def execute_query(conn, query, params=None, fetch_one=False, fetch_all=False, is_insert=False):
    """执行 SQL 查询并处理结果"""
    cursor = conn.cursor()
    try:
        cursor.execute(query, params or ()) # 确保 params 是一个元组或列表

        if is_insert:
            conn.commit()
            return cursor.lastrowid if cursor.lastrowid else True # 对于无自增ID的表，lastrowid可能是0
        elif query.strip().upper().startswith("SELECT"):
            # 根据 fetch_one 或 fetch_all 来决定获取一个还是所有结果
            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all: # 新增的逻辑
                result = cursor.fetchall()
            else: # 默认行为，如果两个都为False，可以考虑抛出错误或设定默认行为
                result = None # 或者你可以定义一个默认行为，比如 fetch_all = True
            return result
        else: # 对于 UPDATE, DELETE 等非 SELECT 操作
            conn.commit()
            return True
    except Error as e:
        print(f"执行查询失败: {query} -> {e}")
        conn.rollback() # 出现错误时回滚事务
        raise # 抛出异常，让上层调用者处理
    finally:
        cursor.close()


def close_db_connection(conn):
    """关闭数据库连接"""
    if conn and conn.is_connected():
        conn.close()
        print("数据库连接已关闭")

# 辅助函数，用于首次运行或测试时创建用户和设备表
def create_initial_tables_and_users():
    from werkzeug.security import generate_password_hash # 仅在此处需要，避免循环导入
    conn = get_db_connection()
    if not conn:
        print("无法连接数据库，跳过创建初始用户和表。")
        return

    try:
        cursor = conn.cursor()

        # 检查并创建 'users' 表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                UserNo INT PRIMARY KEY AUTO_INCREMENT,
                UserName VARCHAR(50) NOT NULL UNIQUE,
                UserPassword VARCHAR(255) NOT NULL, -- 存储哈希后的密码
                UserPermissions VARCHAR(20) DEFAULT 'user', -- 'admin' 或 'user'
                Avatar VARCHAR(255),
                Job VARCHAR(100),
                Organization VARCHAR(100),
                Location VARCHAR(100),
                Email VARCHAR(100),
                Certification TINYINT(1) DEFAULT 0 -- 0 未认证，1 已认证
            );
        """)
        conn.commit()
        print("'users' table checked/created.")

        # 检查用户是否存在，如果不存在则插入
        users_to_create = [
            ('admin', 'admin_pass', 'admin', 'https://s.arco.design/changelog-item-image/avatar.png', '项目经理', '凝胶科技', '上海', 'admin@example.com', 1),
            ('user', 'user_pass', 'user', None, '工程师', '凝胶科技', '北京', 'user@example.com', 0)
        ]

        for username, password, permissions, avatar, job, org, loc, email, cert in users_to_create:
            cursor.execute("SELECT UserNo FROM users WHERE UserName = %s", (username,))
            if not cursor.fetchone():
                hashed_password = generate_password_hash(password) # 使用 werkzeug.security 哈希密码
                insert_query = """
                INSERT INTO users (UserName, UserPassword, UserPermissions, Avatar, Job, Organization, Location, Email, Certification)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                execute_query(conn, insert_query, (username, hashed_password, permissions, avatar, job, org, loc, email, cert), is_insert=True)
                print(f"用户 '{username}' 已创建。")
            else:
                print(f"用户 '{username}' 已存在。")
        conn.commit()

        # 检查并创建 'devices' 表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS devices (
                DeviceNo VARCHAR(50) PRIMARY KEY,
                DeviceName VARCHAR(100) NOT NULL,
                DeviceUsage TEXT,
                DStartTime DATETIME,
                DMT DATETIME,
                DStopTime DATETIME,
                Operator VARCHAR(100)
            );
        """)
        conn.commit()
        print("'devices' table checked/created.")

        # 检查并创建 'national_standard' 表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS national_standard (
                NSN VARCHAR(50) PRIMARY KEY,
                StandardName VARCHAR(255) NOT NULL,
                Description TEXT,
                MaterialCode VARCHAR(50)
            );
        """)
        conn.commit()
        print("'national_standard' table checked/created.")

    except Error as e:
        print(f"创建初始用户或表失败: {e}")
        conn.rollback()
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()