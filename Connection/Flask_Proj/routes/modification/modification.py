# routes/modification/modification.py

from utils.db import get_db_connection, execute_query
from mysql.connector import Error
from flask import current_app
from datetime import datetime

class ModificationModel:
    TABLE_NAME = "Modification"
    # 字段列表与您的数据库截图一致
    COLUMNS = [
        "ModificationID", "OperationType", "OperationTime", "UserNo",
        "EntityType", "EntityID", "FieldName", "OldValue", "NewValue"
    ]

    @staticmethod
    def get_paginated_list(filters, current, page_size):
        """获取分页和筛选后的审计日志列表"""
        conn = get_db_connection()
        if not conn:
            return [], 0
        try:
            # 基础查询语句
            base_query = f"FROM {ModificationModel.TABLE_NAME} WHERE 1=1"
            filter_clauses = []
            params = []

            # 构建筛选条件
            if filters.get('EntityType'):
                filter_clauses.append("EntityType LIKE %s")
                params.append(f"%{filters['EntityType']}%")
            if filters.get('EntityID'):
                filter_clauses.append("EntityID LIKE %s")
                params.append(f"%{filters['EntityID']}%")
            if filters.get('UserNo'):
                filter_clauses.append("UserNo LIKE %s")
                params.append(f"%{filters['UserNo']}%")
            if filters.get('OperationType'):
                filter_clauses.append("OperationType = %s")
                params.append(filters['OperationType'])

            if filter_clauses:
                base_query += " AND " + " AND ".join(filter_clauses)

            # 获取总数
            count_query = f"SELECT COUNT(*) {base_query}"
            total_count_result = execute_query(conn, count_query, tuple(params), fetch_one=True)
            total_count = total_count_result[0] if total_count_result else 0

            # 获取当前页数据，按操作时间降序排列
            offset = (current - 1) * page_size
            data_query = f"SELECT {', '.join(ModificationModel.COLUMNS)} {base_query} ORDER BY OperationTime DESC LIMIT %s OFFSET %s"
            params.append(page_size)
            params.append(offset)
            
            records_raw = execute_query(conn, data_query, tuple(params), fetch_all=True)
            
            # 格式化记录
            records = []
            for record_tuple in records_raw:
                record_dict = dict(zip(ModificationModel.COLUMNS, record_tuple))
                # 将 datetime 对象转换为 ISO 格式的字符串，便于前端处理
                if isinstance(record_dict.get('OperationTime'), datetime):
                    record_dict['OperationTime'] = record_dict['OperationTime'].isoformat()
                records.append(record_dict)
            
            return records, total_count
        except Error as e:
            current_app.logger.error(f"数据库错误 (ModificationModel.get_paginated_list): {e}", exc_info=True)
            raise e