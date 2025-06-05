from utils.db import get_db_connection, execute_query
from mysql.connector import Error
from flask import current_app

class NationalStandardModel:
    TABLE_NAME = "national_standard"
    COLUMNS = ["NSN", "StandardName", "Description", "MaterialCode"]

    @staticmethod
    def find_by_nsn(nsn):
        """根据 NSN 查询单个标准详情"""
        conn = get_db_connection()
        if not conn: return None
        try:
            query = f"SELECT {', '.join(NationalStandardModel.COLUMNS)} FROM {NationalStandardModel.TABLE_NAME} WHERE NSN = %s"
            record = execute_query(conn, query, (nsn,), fetch_one=True)
            if record:
                # 将元组转换为字典
                return dict(zip(NationalStandardModel.COLUMNS, record))
            return None
        except Error as e:
            current_app.logger.error(f"数据库错误 (find_by_nsn): {e}")
            raise e

    @staticmethod
    def find_by_name(name, exclude_nsn=None):
        """根据 StandardName 查询，检查名称是否重复"""
        conn = get_db_connection()
        if not conn: return None
        try:
            query = f"SELECT NSN FROM {NationalStandardModel.TABLE_NAME} WHERE StandardName = %s"
            params = [name]
            if exclude_nsn:
                query += " AND NSN != %s"
                params.append(exclude_nsn)
            return execute_query(conn, query, tuple(params), fetch_one=True)
        except Error as e:
            current_app.logger.error(f"数据库错误 (find_by_name): {e}")
            raise e

    @staticmethod
    def create(data):
        """创建新标准记录"""
        conn = get_db_connection()
        if not conn: return False
        try:
            columns = []
            placeholders = []
            values = []
            
            # NSN是主键，必须存在
            if 'NSN' not in data or not data['NSN']:
                raise ValueError("NSN is required.")
            
            for col_name in NationalStandardModel.COLUMNS:
                if col_name in data and data[col_name] is not None:
                    columns.append(col_name)
                    placeholders.append("%s")
                    values.append(data[col_name])
            
            insert_query = f"INSERT INTO {NationalStandardModel.TABLE_NAME} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
            return execute_query(conn, insert_query, tuple(values), is_insert=True)
        except Error as e:
            current_app.logger.error(f"数据库错误 (create): {e}")
            raise e
        except ValueError as e:
            current_app.logger.error(f"数据校验错误 (create): {e}")
            raise e

    @staticmethod
    def update(nsn, data):
        """更新标准记录"""
        conn = get_db_connection()
        if not conn: return False
        try:
            set_clauses = []
            values = []
            
            # NSN 是主键，不更新它本身，只根据它来定位记录
            for col_name in ["StandardName", "Description", "MaterialCode"]:
                if col_name in data:
                    set_clauses.append(f"{col_name} = %s")
                    values.append(data[col_name])
            
            if not set_clauses: # 没有提供任何可更新的字段
                return True 
            
            update_query = f"UPDATE {NationalStandardModel.TABLE_NAME} SET {', '.join(set_clauses)} WHERE NSN = %s"
            values.append(nsn)
            return execute_query(conn, update_query, tuple(values))
        except Error as e:
            current_app.logger.error(f"数据库错误 (update): {e}")
            raise e

    @staticmethod
    def delete(nsn):
        """删除标准记录"""
        conn = get_db_connection()
        if not conn: return False
        try:
            delete_query = f"DELETE FROM {NationalStandardModel.TABLE_NAME} WHERE NSN = %s"
            return execute_query(conn, delete_query, (nsn,))
        except Error as e:
            current_app.logger.error(f"数据库错误 (delete): {e}")
            raise e

    @staticmethod
    def get_paginated_list(filters, current, page_size):
        """获取分页和筛选后的标准列表"""
        conn = get_db_connection()
        if not conn: return [], 0
        try:
            base_query = f"FROM {NationalStandardModel.TABLE_NAME} WHERE 1=1"
            filter_clauses = []
            params = []

            # 根据过滤器构建WHERE子句
            if filters.get('NSN'):
                filter_clauses.append("NSN LIKE %s")
                params.append(f"%{filters['NSN']}%")
            if filters.get('StandardName'):
                filter_clauses.append("StandardName LIKE %s")
                params.append(f"%{filters['StandardName']}%")
            if filters.get('Description'):
                filter_clauses.append("Description LIKE %s")
                params.append(f"%{filters['Description']}%")
            if filters.get('MaterialCode'):
                filter_clauses.append("MaterialCode LIKE %s")
                params.append(f"%{filters['MaterialCode']}%")

            if filter_clauses:
                base_query += " AND " + " AND ".join(filter_clauses)

            # 获取总条数
            count_query = f"SELECT COUNT(*) {base_query}"
            total_count = execute_query(conn, count_query, tuple(params), fetch_one=True)[0]

            # 获取分页数据
            offset = (current - 1) * page_size
            data_query = f"SELECT {', '.join(NationalStandardModel.COLUMNS)} {base_query} ORDER BY NSN LIMIT %s OFFSET %s"
            params.append(page_size)
            params.append(offset)
            
            records_raw = execute_query(conn, data_query, tuple(params), fetch_all=True)
            records = []
            for record_tuple in records_raw:
                records.append(dict(zip(NationalStandardModel.COLUMNS, record_tuple)))
            
            return records, total_count
        except Error as e:
            current_app.logger.error(f"数据库错误 (get_paginated_list): {e}")
            raise e