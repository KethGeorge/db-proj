# backend/models/material.py

from utils.db import get_db_connection, execute_query
from mysql.connector import Error
from flask import current_app

class MaterialModel:
    TABLE_NAME = "material"
    COLUMNS = ["MaterialCode", "MaterialName"] # 定义表的所有列

    @staticmethod
    def find_by_code(material_code):
        """根据 MaterialCode 查询单个材料详情"""
        conn = get_db_connection()
        if not conn: return None
        try:
            query = f"SELECT {', '.join(MaterialModel.COLUMNS)} FROM {MaterialModel.TABLE_NAME} WHERE MaterialCode = %s"
            record = execute_query(conn, query, (material_code,), fetch_one=True)
            if record:
                # 将元组转换为字典
                return dict(zip(MaterialModel.COLUMNS, record))
            return None
        except Error as e:
            current_app.logger.error(f"数据库错误 (MaterialModel.find_by_code): {e}")
            raise e
        # 注意：这里不关闭连接，由 app.py 的 teardown_appcontext 统一管理

    @staticmethod
    def find_by_name(material_name, exclude_code=None):
        """根据 MaterialName 查询，检查名称是否重复"""
        conn = get_db_connection()
        if not conn: return None
        try:
            query = f"SELECT MaterialCode FROM {MaterialModel.TABLE_NAME} WHERE MaterialName = %s"
            params = [material_name]
            if exclude_code:
                query += " AND MaterialCode != %s"
                params.append(exclude_code)
            return execute_query(conn, query, tuple(params), fetch_one=True)
        except Error as e:
            current_app.logger.error(f"数据库错误 (MaterialModel.find_by_name): {e}")
            raise e
        # 注意：这里不关闭连接，由 app.py 的 teardown_appcontext 统一管理

    @staticmethod
    def create(data):
        """创建新材料记录"""
        conn = get_db_connection()
        if not conn: return False
        try:
            columns = []
            placeholders = []
            values = []
            
            # MaterialCode 是主键，必须存在且非空
            if 'MaterialCode' not in data or not data['MaterialCode'].strip():
                raise ValueError("MaterialCode is required and cannot be empty.")
            # MaterialName 必须存在且非空
            if 'MaterialName' not in data or not data['MaterialName'].strip():
                raise ValueError("MaterialName is required and cannot be empty.")
            
            for col_name in MaterialModel.COLUMNS:
                if col_name in data and data[col_name] is not None:
                    columns.append(col_name)
                    placeholders.append("%s")
                    values.append(data[col_name])
            
            insert_query = f"INSERT INTO {MaterialModel.TABLE_NAME} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
            return execute_query(conn, insert_query, tuple(values), is_insert=True)
        except Error as e:
            current_app.logger.error(f"数据库错误 (MaterialModel.create): {e}")
            raise e
        except ValueError as e:
            current_app.logger.warning(f"数据校验错误 (MaterialModel.create): {e}")
            raise e
        # 注意：这里不关闭连接

    @staticmethod
    def update(material_code, data):
        """更新材料记录"""
        conn = get_db_connection()
        if not conn: return False
        try:
            set_clauses = []
            values = []
            
            # MaterialCode 是主键，不更新它本身
            for col_name in ["MaterialName"]: # 只有 MaterialName 是可更新的字段
                if col_name in data:
                    set_clauses.append(f"{col_name} = %s")
                    values.append(data[col_name])
            
            if not set_clauses: # 没有提供任何可更新的字段
                return True 
            
            update_query = f"UPDATE {MaterialModel.TABLE_NAME} SET {', '.join(set_clauses)} WHERE MaterialCode = %s"
            values.append(material_code)
            return execute_query(conn, update_query, tuple(values))
        except Error as e:
            current_app.logger.error(f"数据库错误 (MaterialModel.update): {e}")
            raise e
        # 注意：这里不关闭连接

    @staticmethod
    def delete(material_code):
        """删除材料记录"""
        conn = get_db_connection()
        if not conn: return False
        try:
            delete_query = f"DELETE FROM {MaterialModel.TABLE_NAME} WHERE MaterialCode = %s"
            return execute_query(conn, delete_query, (material_code,))
        except Error as e:
            current_app.logger.error(f"数据库错误 (MaterialModel.delete): {e}")
            raise e
        # 注意：这里不关闭连接

    @staticmethod
    def get_paginated_list(filters, current, page_size):
        """获取分页和筛选后的材料列表"""
        conn = get_db_connection()
        if not conn: return [], 0
        try:
            base_query = f"FROM {MaterialModel.TABLE_NAME} WHERE 1=1"
            filter_clauses = []
            params = []

            # 根据过滤器构建WHERE子句
            if filters.get('MaterialCode'):
                filter_clauses.append("MaterialCode LIKE %s")
                params.append(f"%{filters['MaterialCode']}%")
            if filters.get('MaterialName'):
                filter_clauses.append("MaterialName LIKE %s")
                params.append(f"%{filters['MaterialName']}%")

            if filter_clauses:
                base_query += " AND " + " AND ".join(filter_clauses)

            # 获取总条数
            count_query = f"SELECT COUNT(*) {base_query}"
            total_count = execute_query(conn, count_query, tuple(params), fetch_one=True)[0]

            # 获取分页数据
            offset = (current - 1) * page_size
            data_query = f"SELECT {', '.join(MaterialModel.COLUMNS)} {base_query} ORDER BY MaterialCode LIMIT %s OFFSET %s"
            params.append(page_size)
            params.append(offset)
            
            records_raw = execute_query(conn, data_query, tuple(params), fetch_all=True)
            records = []
            for record_tuple in records_raw:
                records.append(dict(zip(MaterialModel.COLUMNS, record_tuple)))
            
            return records, total_count
        except Error as e:
            current_app.logger.error(f"数据库错误 (MaterialModel.get_paginated_list): {e}")
            raise e
        # 注意：这里不关闭连接