# backend/models/protocol.py

from utils.db import get_db_connection, execute_query
from mysql.connector import Error
from flask import current_app

class ProtocolModel:
    TABLE_NAME = "protocol"
    COLUMNS = [
        "ProtocolNo", "NSN", "SHT", "SMS", "MixingAngle",
        "MixingRadius", "MeasurementInterval", "MaterialCode", "UserNo"
    ]

    @staticmethod
    def find_by_no(protocol_no):
        """根据 ProtocolNo 查询单个协议详情"""
        conn = get_db_connection()
        if not conn: return None
        try:
            query = f"SELECT {', '.join(ProtocolModel.COLUMNS)} FROM {ProtocolModel.TABLE_NAME} WHERE ProtocolNo = %s"
            record = execute_query(conn, query, (protocol_no,), fetch_one=True)
            if record:
                # 将元组转换为字典
                protocol_data = dict(zip(ProtocolModel.COLUMNS, record))
                # 浮点数可以直接序列化，不需要特殊处理
                return protocol_data
            return None
        except Error as e:
            current_app.logger.error(f"数据库错误 (ProtocolModel.find_by_no): {e}")
            raise e

    @staticmethod
    def create(data):
        """创建新协议记录"""
        conn = get_db_connection()
        if not conn: return False
        try:
            columns = []
            placeholders = []
            values = []
            
            # 必填字段校验
            if 'ProtocolNo' not in data or not data['ProtocolNo'].strip():
                raise ValueError("ProtocolNo is required and cannot be empty.")
            if 'MaterialCode' not in data or not data['MaterialCode'].strip():
                raise ValueError("MaterialCode is required and cannot be empty.")
            if 'UserNo' not in data or not data['UserNo'].strip():
                raise ValueError("UserNo is required and cannot be empty.")
            
            for col_name in ProtocolModel.COLUMNS:
                if col_name in data and data[col_name] is not None:
                    columns.append(col_name)
                    placeholders.append("%s")
                    values.append(data[col_name])
                elif col_name not in data or data[col_name] is None:
                    # 如果字段不在数据中或其值为None，则插入NULL
                    columns.append(col_name)
                    placeholders.append("%s")
                    values.append(None)
            
            insert_query = f"INSERT INTO {ProtocolModel.TABLE_NAME} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
            return execute_query(conn, insert_query, tuple(values), is_insert=True)
        except Error as e:
            current_app.logger.error(f"数据库操作错误 (ProtocolModel.create): {e}")
            raise e
        except ValueError as e:
            current_app.logger.warning(f"数据校验错误 (ProtocolModel.create): {e}")
            raise e

    @staticmethod
    def update(protocol_no, data):
        """更新协议记录"""
        conn = get_db_connection()
        if not conn: return False
        try:
            set_clauses = []
            values = []
            
            # 可更新的字段 (ProtocolNo 不可更新)
            updatable_cols = [
                "NSN", "SHT", "SMS", "MixingAngle",
                "MixingRadius", "MeasurementInterval", "MaterialCode", "UserNo"
            ]
            for col_name in updatable_cols:
                if col_name in data:
                    set_clauses.append(f"{col_name} = %s")
                    values.append(data[col_name])
            
            if not set_clauses:
                return True 
            
            update_query = f"UPDATE {ProtocolModel.TABLE_NAME} SET {', '.join(set_clauses)} WHERE ProtocolNo = %s"
            values.append(protocol_no)
            return execute_query(conn, update_query, tuple(values))
        except Error as e:
            current_app.logger.error(f"数据库错误 (ProtocolModel.update): {e}")
            raise e

    @staticmethod
    def delete(protocol_no):
        """删除协议记录"""
        conn = get_db_connection()
        if not conn: return False
        try:
            delete_query = f"DELETE FROM {ProtocolModel.TABLE_NAME} WHERE ProtocolNo = %s"
            return execute_query(conn, delete_query, (protocol_no,))
        except Error as e:
            current_app.logger.error(f"数据库错误 (ProtocolModel.delete): {e}")
            raise e

    @staticmethod
    def get_paginated_list(filters, current, page_size):
        """获取分页和筛选后的协议列表"""
        conn = get_db_connection()
        if not conn: return [], 0
        try:
            base_query = f"FROM {ProtocolModel.TABLE_NAME} WHERE 1=1"
            filter_clauses = []
            params = []

            # 根据过滤器构建WHERE子句 (只筛选主要字段)
            if filters.get('ProtocolNo'):
                filter_clauses.append("ProtocolNo LIKE %s")
                params.append(f"%{filters['ProtocolNo']}%")
            if filters.get('NSN'):
                filter_clauses.append("NSN LIKE %s")
                params.append(f"%{filters['NSN']}%")
            if filters.get('MaterialCode'):
                filter_clauses.append("MaterialCode LIKE %s")
                params.append(f"%{filters['MaterialCode']}%")
            if filters.get('UserNo'):
                filter_clauses.append("UserNo LIKE %s")
                params.append(f"%{filters['UserNo']}%")

            if filter_clauses:
                base_query += " AND " + " AND ".join(filter_clauses)

            count_query = f"SELECT COUNT(*) {base_query}"
            total_count = execute_query(conn, count_query, tuple(params), fetch_one=True)[0]

            offset = (current - 1) * page_size
            data_query = f"SELECT {', '.join(ProtocolModel.COLUMNS)} {base_query} ORDER BY ProtocolNo LIMIT %s OFFSET %s"
            params.append(page_size)
            params.append(offset)
            
            records_raw = execute_query(conn, data_query, tuple(params), fetch_all=True)
            records = []
            for record_tuple in records_raw:
                record_dict = dict(zip(ProtocolModel.COLUMNS, record_tuple))
                records.append(record_dict) # 浮点数类型直接可序列化
            
            return records, total_count
        except Error as e:
            current_app.logger.error(f"数据库错误 (ProtocolModel.get_paginated_list): {e}")
            raise e
    @staticmethod
    def search_by_keyword(keyword, limit=10):
        """根据关键词搜索协议，并返回 ProtocolNo 和 NSN"""
        conn = get_db_connection()
        if not conn: return []
        try:
            search_query = f"""
            SELECT ProtocolNo, NSN
            FROM {ProtocolModel.TABLE_NAME}
            WHERE ProtocolNo LIKE %s OR NSN LIKE %s
            LIMIT %s
            """
            params = (f"%{keyword}%", f"%{keyword}%", limit)
            
            results_raw = execute_query(conn, search_query, params, fetch_all=True)
            
            protocols = []
            for row in results_raw:
                protocols.append({
                    'ProtocolNo': row[0],
                    'NSN': row[1] # NSN 作为描述性字段
                })
            return protocols
        except Error as e:
            current_app.logger.error(f"数据库错误 (ProtocolModel.search_by_keyword): {e}", exc_info=True)
            raise e