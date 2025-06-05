import mysql.connector
from mysql.connector import Error
from flask import current_app, g # 导入 g 对象

# 1. 修改 get_db_connection() 以使用 g 对象
def get_db_connection():
    """获取数据库连接并存储在 g 对象中，确保每个请求使用一个连接"""
    if 'db' not in g: # 如果当前请求上下文还没有数据库连接
        try:
            conn = mysql.connector.connect(
                host=current_app.config['DB_HOST'],
                user=current_app.config['DB_USER'],
                password=current_app.config['DB_PASSWORD'],
                database=current_app.config['DB_DATABASE'],
                # 可以添加其他参数，如 raise_on_warnings=True
            )
            g.db = conn # 将连接存储在 g 对象中
            current_app.logger.info("数据库连接成功并存储在 g.db 中")
        except Error as err:
            current_app.logger.error(f"连接MySQL数据库失败: {err}", exc_info=True)
            g.db = None # 连接失败也设为 None，保持 g.db 状态一致
    return g.db

# 2. 移除 close_db_connection() 函数
# 这个函数将不再需要，因为连接的关闭由 app.py 中的 @app.teardown_appcontext 统一管理。
# 如果其他地方有调用这个函数，需要一并删除。

# 3. 保持 execute_query() 不变，因为它已经包含了对 Unread result found 的修复 (fetchall() 逻辑)
#    并确保 cursor.close() 在 finally 中。
def execute_query(conn, query, params=None, fetch_one=False, fetch_all=False, is_insert=False):
    """执行 SQL 查询并处理结果"""
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

# 4. 修改 create_initial_tables_and_users()
#    由于它在 app.app_context() 中运行，其获取的连接也会在 teardown_appcontext 时关闭。
#    因此，它自己的 finally 块中不需要显式关闭连接。
def create_initial_tables_and_users():
    from werkzeug.security import generate_password_hash # 仅在此处需要，避免循环导入
    # 注意：这里调用 get_db_connection() 会将连接放入 g.db
    conn = get_db_connection()
    if not conn:
        current_app.logger.error("无法连接数据库，跳过创建初始用户和表。")
        return

    try:
        cursor = conn.cursor()
        # ... (创建 users, devices, national_standard 表的逻辑保持不变) ...
        current_app.logger.info("'users' table checked/created.")

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
                # 注意：这里调用 execute_query 时传入了 conn，而 conn 实际上是 g.db
                execute_query(conn, insert_query, (username, hashed_password, permissions, avatar, job, org, loc, email, cert), is_insert=True)
                current_app.logger.info(f"用户 '{username}' 已创建。")
            else:
                current_app.logger.info(f"用户 '{username}' 已存在。")
        conn.commit() # 提交插入用户的事务
        current_app.logger.info("Initial users checked/created.")

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

    except Error as e:
        current_app.logger.error(f"创建初始用户或表失败: {e}", exc_info=True)
        conn.rollback() # 出现错误时回滚
    # 移除 finally: cursor.close(); conn.close()
    # 因为 get_db_connection() 已经把连接放到了 g.db，
    # 会在 app.py 的 @app.teardown_appcontext 中被关闭。