import mysql.connector
from mysql.connector import Error
from flask import current_app, g, request # 导入 request 对象，用于获取当前请求的用户信息
import logging # 确保 logging 模块被导入

# 获取 logger 实例，这样可以在没有 current_app 的地方也打印日志，尽管在web请求中current_app是可用的
logger = logging.getLogger(__name__)

def get_db_connection():
    """
    获取数据库连接并存储在 g 对象中，确保每个请求使用一个连接。
    同时，在连接创建时，尝试从请求上下文中获取 UserNo 并设置 MySQL 会话变量 @current_user_id。
    """
    if 'db' not in g:
        try:
            conn = mysql.connector.connect(
                host=current_app.config['DB_HOST'],
                user=current_app.config['DB_USER'],
                password=current_app.config['DB_PASSWORD'],
                database=current_app.config['DB_DATABASE'],
                raise_on_warnings=False
            )
            g.db = conn
            current_app.logger.info("数据库连接成功并存储在 g.db 中。")

            # --- 安全地设置 MySQL 会话变量 ---
            user_no = None
            # 检查是否处于请求上下文
            # Flask 的 request 对象只有在请求上下文中才可用
            from flask import has_request_context # 导入这个辅助函数

            if has_request_context(): # <-- 关键改变：先检查是否有请求上下文
                if hasattr(request, 'user') and request.user and 'UserNo' in request.user:
                    user_no = request.user['UserNo']
            else:
                current_app.logger.debug("Not in request context. Skipping @current_user_id setup for initial connection.")

            if user_no is not None:
                temp_cursor = conn.cursor()
                try:
                    temp_cursor.execute("SET @current_user_id = %s;", (user_no,))
                    current_app.logger.debug(f"MySQL session variable @current_user_id set to {user_no}.")
                except Exception as set_var_ex:
                    current_app.logger.error(f"Failed to set @current_user_id for user {user_no}: {set_var_ex}", exc_info=True)
                finally:
                    temp_cursor.close()
            # else: 如果 user_no 是 None，不设置会话变量，这是正常的（例如未登录用户或初始化时）
            # ----------------------------------

        except Error as err:
            current_app.logger.error(f"连接MySQL数据库失败: {err}", exc_info=True)
            g.db = None
            raise
    return g.db
def execute_query(conn, query, params=None, fetch_one=False, fetch_all=False, is_insert=False):
    """
    执行 SQL 查询并处理结果。
    对于 SELECT 语句，它会根据 fetch_one/fetch_all 参数返回结果。
    对于非 SELECT 语句 (INSERT/UPDATE/DELETE)，它会执行并提交事务。
    """
    if not conn:
        current_app.logger.error("数据库连接不可用，无法执行查询。")
        raise ConnectionError("Database connection not available.")

    cursor = None
    try:
        cursor = conn.cursor()
        current_app.logger.debug(f"Executing query: {query} with params: {params}")
        cursor.execute(query, params or ()) # 确保 params 是一个元组或列表

        if query.strip().upper().startswith("SELECT"):
            # 核心改变：无论 fetch_one 还是 fetch_all，都先 fetchall() 来消耗所有结果
            results = cursor.fetchall() 
            
            if fetch_one:
                return results[0] if results else None
            elif fetch_all:
                return results
            else:
                # 如果是 SELECT 但没有明确指定 fetch_one 或 fetch_all，默认返回所有
                current_app.logger.warning(f"SELECT query executed without fetch_one or fetch_all specified. Returning all results for query: {query}")
                return results
        else: # 对于 UPDATE, DELETE 等非 SELECT 操作
            conn.commit()
            if is_insert:
                return cursor.lastrowid if cursor.lastrowid else True # 对于无自增ID的表，lastrowid可能是0
            return True # 对于 UPDATE/DELETE，返回 True 表示成功
    except Error as e:
        conn.rollback() # 出现数据库错误时回滚事务
        current_app.logger.error(f"执行查询失败: {query} -> {e}", exc_info=True)
        raise # 抛出异常，让上层调用者处理
    except Exception as e: # 捕获其他非数据库错误
        conn.rollback() # 确保回滚
        current_app.logger.error(f"执行查询时发生非数据库错误: {e}", exc_info=True)
        raise e
    finally:
        if cursor: # 确保 cursor 存在才关闭
            cursor.close()

# 辅助函数，用于首次运行或测试时创建数据库表和初始数据
def create_initial_tables_and_users():
    from werkzeug.security import generate_password_hash # 仅在此处需要，避免循环导入
    
    # 注意：这里调用 get_db_connection() 会将连接放入 g.db，
    # 并在 app.app_context() 结束后由 teardown_appcontext 关闭。
    conn = get_db_connection()
    if not conn:
        current_app.logger.error("无法连接数据库，跳过创建初始用户和表。")
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
        current_app.logger.info("'users' table checked/created.")

        # 检查用户是否存在，如果不存在则插入
        users_to_create = [
            ('admin', 'admin_pass', 'admin', 'https://s.arco.design/changelog-item-image/avatar.png', '项目经理', '凝胶科技', '上海', 'admin@example.com', 1),
            ('user', 'user_pass', 'user', None, '工程师', '凝胶科技', '北京', 'user@example.com', 0)
        ]

        for username, password, permissions, avatar, job, org, loc, email, cert in users_to_create:
            # 检查 UserNo 是否已经存在，因为后面可能会自动生成，或者我们希望UserNo是固定的
            # 对于演示，这里我们假设UserNo是自增的，因此只检查UserName是否存在
            cursor.execute("SELECT UserNo FROM users WHERE UserName = %s", (username,))
            if not cursor.fetchone():
                hashed_password = generate_password_hash(password) # 使用 werkzeug.security 哈希密码
                insert_query = """
                INSERT INTO users (UserName, UserPassword, UserPermissions, Avatar, Job, Organization, Location, Email, Certification)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                # 使用 execute_query 来执行插入，它会提交事务
                execute_query(conn, insert_query, (username, hashed_password, permissions, avatar, job, org, loc, email, cert), is_insert=True)
                current_app.logger.info(f"用户 '{username}' 已创建。")
            else:
                current_app.logger.info(f"用户 '{username}' 已存在。")
        # 提交所有用户插入的事务（如果循环中有多个，execute_query 每次插入后会提交，但这里可以再确认一次）
        # conn.commit() # execute_query 已经处理了提交，此处可省略
        current_app.logger.info("Initial users checked/created.")


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
        current_app.logger.info("'devices' table checked/created.")

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
        current_app.logger.info("'national_standard' table checked/created.")

        # 检查并创建 'material' 表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS material (
                MaterialCode CHAR(16) PRIMARY KEY NOT NULL,
                MaterialName VARCHAR(20) NOT NULL
            );
        """)
        conn.commit()
        current_app.logger.info("'material' table checked/created.")

        # 检查并创建 'Modification' 表 (用于审计触发器)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Modification (
                ModificationID VARCHAR(50) PRIMARY KEY,
                OperationType VARCHAR(10) NOT NULL, -- 'INSERT', 'UPDATE', 'DELETE'
                OperationTime DATETIME NOT NULL,
                UserNo INT NOT NULL,              -- 确保是 INT 和 NOT NULL
                EntityType VARCHAR(50) NOT NULL,  -- 'Material', 'User', 'Experiment' 等
                EntityID VARCHAR(50) NOT NULL,    -- 被操作实体的ID (MaterialCode, UserNo, ExperimentCode等)
                FieldName VARCHAR(50),            -- 变更的字段名，DELETE操作可为NULL
                OldValue TEXT,                    -- 字段旧值，INSERT/DELETE操作可为NULL
                NewValue TEXT,                    -- 字段新值，DELETE操作可为NULL
                FOREIGN KEY (UserNo) REFERENCES users(UserNo) ON DELETE CASCADE
            );
        """)
        conn.commit()
        current_app.logger.info("'Modification' table checked/created.")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS device ( -- 表名改为 device
                DeviceNo CHAR(20) PRIMARY KEY NOT NULL,    -- 你的图示是 char(20)
                DeviceName CHAR(8) NOT NULL,              -- 你的图示是 char(8)
                DeviceUsage VARCHAR(10),                  -- 你的图示是 Varchar(10)
                DStartTime DATETIME,
                DMT DATETIME,
                DStopTime DATETIME,
                Operator VARCHAR(100)
            );
        """)
        conn.commit()
        current_app.logger.info("'device' table checked/created.")

    except Error as e:
        current_app.logger.error(f"创建初始用户或表失败: {e}", exc_info=True)
        conn.rollback() # 出现错误时回滚
    except Exception as e: # 捕获其他非数据库错误
        current_app.logger.error(f"创建初始用户或表时发生未知错误: {e}", exc_info=True)
        conn.rollback() # 确保回滚
    # 移除 finally: cursor.close(); conn.close()
    # 因为 get_db_connection() 已经把连接放到了 g.db，
    # 会在 app.py 的 @app.teardown_appcontext 中被关闭。