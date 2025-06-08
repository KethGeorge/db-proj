# backend/models/user.py

from utils.db import get_db_connection, execute_query
from mysql.connector import Error
from flask import current_app
import string
import random

class UserModel:
    TABLE_NAME = "users"
    COLUMNS_FOR_INSERT = [
        "UserNo", "UserName", "UserPassword", "UserPermissions", "Email", "Telephone"
    ]
    COLUMNS_FOR_SELECT = [
        "UserNo", "UserName", "UserPassword", "UserPermissions", "Email", "Telephone"
    ]

    # --- 辅助函数：生成唯一 UserNo (仅当UserNo为CHAR且非自增时需要) ---
    @staticmethod
    def _generate_unique_userno():
        characters = string.ascii_uppercase + string.digits
        conn = get_db_connection()
        if not conn:
            raise ConnectionError("数据库连接失败，无法生成唯一的UserNo。")
        for _ in range(100): # 尝试100次
            temp_userno = ''.join(random.choice(characters) for i in range(8)) # CHAR(8)
            query = "SELECT UserNo FROM users WHERE UserNo = %s"
            if not execute_query(conn, query, (temp_userno,), fetch_one=True):
                return temp_userno
        raise ValueError("无法生成唯一的UserNo，请稍后重试。")

    # --- CRUD 操作 ---
    @staticmethod
    def get_user_by_userno(userno):
        """根据 UserNo 查询单个用户详情"""
        conn = get_db_connection()
        if not conn: return None
        try:
            query = f"SELECT {', '.join(UserModel.COLUMNS_FOR_SELECT)} FROM {UserModel.TABLE_NAME} WHERE UserNo = %s"
            record = execute_query(conn, query, (userno,), fetch_one=True)
            if record:
                user_data = dict(zip(UserModel.COLUMNS_FOR_SELECT, record))
                user_data['UserPassword'] = '********' # 安全考虑，密码不应明文返回给前端
                return user_data
            return None
        except Error as e:
            current_app.logger.error(f"数据库错误 (UserModel.get_user_by_userno): {e}", exc_info=True)
            raise e

    @staticmethod
    def get_user_by_username(username):
        """根据 UserName 查询单个用户详情 (用于登录或检查用户名唯一性)"""
        conn = get_db_connection()
        if not conn: return None
        try:
            query = f"SELECT {', '.join(UserModel.COLUMNS_FOR_SELECT)} FROM {UserModel.TABLE_NAME} WHERE UserName = %s"
            record = execute_query(conn, query, (username,), fetch_one=True)
            if record:
                return dict(zip(UserModel.COLUMNS_FOR_SELECT, record))
            return None
        except Error as e:
            current_app.logger.error(f"数据库错误 (UserModel.get_user_by_username): {e}", exc_info=True)
            raise e

    @staticmethod
    def check_username_exists(username, exclude_userno=None):
        """检查用户名是否已存在，排除指定UserNo"""
        conn = get_db_connection()
        if not conn: return True
        try:
            query = "SELECT UserNo FROM users WHERE UserName = %s"
            params = [username]
            if exclude_userno:
                query += " AND UserNo != %s"
                params.append(exclude_userno)
            return execute_query(conn, query, tuple(params), fetch_one=True) is not None
        except Error as e:
            current_app.logger.error(f"数据库错误 (UserModel.check_username_exists): {e}", exc_info=True)
            raise e

    @staticmethod
    def check_email_exists(email, exclude_userno=None):
        """检查邮箱是否已存在，排除指定UserNo"""
        conn = get_db_connection()
        if not conn: return True
        try:
            query = "SELECT UserNo FROM users WHERE Email = %s"
            params = [email]
            if exclude_userno:
                query += " AND UserNo != %s"
                params.append(exclude_userno)
            return execute_query(conn, query, tuple(params), fetch_one=True) is not None
        except Error as e:
            current_app.logger.error(f"数据库错误 (UserModel.check_email_exists): {e}", exc_info=True)
            raise e

    @staticmethod
    def create_user(data):
        """创建新用户"""
        conn = get_db_connection()
        if not conn: return False, None
        try:
            user_no = data.get('UserNo')
            if not user_no:
                user_no = UserModel._generate_unique_userno()
                data['UserNo'] = user_no
            
            columns = []
            placeholders = []
            values = []
            
            for col_name in UserModel.COLUMNS_FOR_INSERT:
                if col_name in data and data[col_name] is not None:
                    columns.append(col_name)
                    placeholders.append("%s")
                    values.append(data[col_name])
                else:
                    columns.append(col_name)
                    placeholders.append("%s")
                    values.append(None)
            
            insert_query = f"INSERT INTO {UserModel.TABLE_NAME} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
            if execute_query(conn, insert_query, tuple(values), is_insert=True):
                return True, user_no
            return False, None
        except Error as e:
            current_app.logger.error(f"数据库操作错误 (UserModel.create_user): {e}", exc_info=True)
            raise e
        except ValueError as e:
            current_app.logger.warning(f"数据校验错误 (UserModel.create_user): {e}", exc_info=True)
            raise e

    @staticmethod
    def update_user(userno, data):
        """更新用户信息"""
        conn = get_db_connection()
        if not conn: return False
        try:
            set_clauses = []
            values = []
            
            updatable_cols = [
                "UserName", "UserPassword", "UserPermissions", "Email", "Telephone"
            ]
            
            for col_name in updatable_cols:
                if col_name in data:
                    set_clauses.append(f"{col_name} = %s")
                    values.append(data[col_name])
            
            if not set_clauses:
                return True 
            
            update_query = f"UPDATE {UserModel.TABLE_NAME} SET {', '.join(set_clauses)} WHERE UserNo = %s"
            values.append(userno)
            return execute_query(conn, update_query, tuple(values))
        except Error as e:
            current_app.logger.error(f"数据库错误 (UserModel.update_user): {e}", exc_info=True)
            raise e

    @staticmethod
    def delete_user(userno):
        """删除用户"""
        conn = get_db_connection()
        if not conn: return False
        try:
            delete_query = f"DELETE FROM {UserModel.TABLE_NAME} WHERE UserNo = %s"
            return execute_query(conn, delete_query, (userno,))
        except Error as e:
            current_app.logger.error(f"数据库错误 (UserModel.delete_user): {e}", exc_info=True)
            raise e

    @staticmethod
    def get_paginated_list(filters, current, pageSize):
        """获取分页和筛选后的用户列表"""
        conn = get_db_connection()
        if not conn: return [], 0
        try:
            # 核心修改：base_filter_clause 只包含 WHERE 部分，不包含 FROM
            base_filter_clause = "WHERE 1=1" # 这里不包含 FROM users
            filter_clauses = []
            params = []

            # 筛选条件严格匹配数据库字段名
            if filters.get('UserNo'):
                filter_clauses.append("UserNo LIKE %s")
                params.append(f"%{filters['UserNo']}%")
            if filters.get('UserName'):
                filter_clauses.append("UserName LIKE %s")
                params.append(f"%{filters['UserName']}%")
            if filters.get('Email'):
                filter_clauses.append("Email LIKE %s")
                params.append(f"%{filters['Email']}%")
            if filters.get('UserPermissions'):
                filter_clauses.append("UserPermissions = %s")
                params.append(filters['UserPermissions'])
            if filters.get('Telephone'):
                filter_clauses.append("Telephone LIKE %s")
                params.append(f"%{filters['Telephone']}%")

            # 拼接最终的 WHERE 子句
            final_where_clause = base_filter_clause
            if filter_clauses:
                final_where_clause += " AND " + " AND ".join(filter_clauses)

            # 获取总条数
            count_query = f"SELECT COUNT(*) FROM {UserModel.TABLE_NAME} {final_where_clause}"
            total_count = execute_query(conn, count_query, tuple(params), fetch_one=True)[0]

            # 获取分页数据
            offset = (current - 1) * pageSize
            # 核心修改：将 final_where_clause 直接拼接到 FROM 之后
            data_query = f"SELECT {', '.join(UserModel.COLUMNS_FOR_SELECT)} FROM {UserModel.TABLE_NAME} {final_where_clause} ORDER BY UserNo LIMIT %s OFFSET %s"
            params.append(pageSize)
            params.append(offset)
            
            records_raw = execute_query(conn, data_query, tuple(params), fetch_all=True)
            records = []
            for record_tuple in records_raw:
                user_dict = dict(zip(UserModel.COLUMNS_FOR_SELECT, record_tuple))
                user_dict['UserPassword'] = '********'
                records.append(user_dict)
            
            return records, total_count
        except Error as e:
            current_app.logger.error(f"数据库错误 (UserModel.get_paginated_list): {e}", exc_info=True)
            raise e
        
    @staticmethod
    def search_by_keyword(keyword, limit=10):
        """根据关键词搜索用户，并返回 UserNo 和 UserName"""
        conn = get_db_connection()
        if not conn: return []
        try:
            search_query = f"""
            SELECT UserNo, UserName
            FROM {UserModel.TABLE_NAME}
            WHERE UserNo LIKE %s OR UserName LIKE %s
            LIMIT %s
            """
            params = (f"%{keyword}%", f"%{keyword}%", limit)
            
            results_raw = execute_query(conn, search_query, params, fetch_all=True)
            
            users = []
            for row in results_raw:
                users.append({
                    'UserNo': row[0],
                    'UserName': row[1]
                })
            return users
        except Error as e:
            current_app.logger.error(f"数据库错误 (UserModel.search_by_keyword): {e}", exc_info=True)
            raise e
    
    @staticmethod
    def search_by_keyword(keyword, limit=10):
        """根据关键词搜索用户，并返回 UserNo 和 UserName"""
        conn = get_db_connection()
        if not conn: return []
        try:
            search_query = f"""
            SELECT UserNo, UserName
            FROM {UserModel.TABLE_NAME}
            WHERE UserNo LIKE %s OR UserName LIKE %s
            LIMIT %s
            """
            params = (f"%{keyword}%", f"%{keyword}%", limit)
            
            results_raw = execute_query(conn, search_query, params, fetch_all=True)
            
            users = []
            for row in results_raw:
                users.append({
                    'UserNo': row[0],
                    'UserName': row[1]
                })
            return users
        except Error as e:
            current_app.logger.error(f"数据库错误 (UserModel.search_by_keyword): {e}", exc_info=True)
            raise e