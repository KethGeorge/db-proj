# routes/modification/modification.py

from utils.db import get_db_connection, execute_query
from mysql.connector import Error
from flask import current_app
from datetime import datetime

def record_to_dict(record, columns):
    """
    一个健壮的辅助函数，用于将数据库记录（元组）和列名转换为字典，
    并在此过程中格式化日期时间。
    """
    if not record:
        return None
    
    record_dict = dict(zip(columns, record))
    
    for key, value in record_dict.items():
        if isinstance(value, datetime):
            # 将 datetime 对象转换为 ISO 格式的字符串 (e.g., "2024-05-23T10:30:00")
            record_dict[key] = value.isoformat()
            
    return record_dict


class ModificationModel:
    # 视图名
    VIEW_NAME = "v_modification_details"
    
    # 【重要】列名列表现在必须与视图的列名完全对应
    VIEW_COLUMNS = [
        "ModificationID", "OperationType", "OperationTime", "OperatorUserNo",
        "OperatorUserName", "EntityType", "EntityID", "FieldName", "OldValue", "NewValue"
    ]

    @staticmethod
    def get_paginated_list(filters, current, page_size):
        """获取分页和筛选后的审计日志列表（查询视图）"""
        conn = get_db_connection()
        if not conn:
            return [], 0
        
        try:
            # 查询目标从表改为视图
            base_query = f"FROM {ModificationModel.VIEW_NAME} WHERE 1=1"
            filter_clauses = []
            params = []
            
            # 筛选条件也基于视图的列名
            if filters.get('EntityType'):
                filter_clauses.append("EntityType LIKE %s")
                params.append(f"%{filters['EntityType']}%")
            if filters.get('EntityID'):
                filter_clauses.append("EntityID LIKE %s")
                params.append(f"%{filters['EntityID']}%")
            if filters.get('OperatorUserNo'):
                filter_clauses.append("OperatorUserNo LIKE %s")
                params.append(f"%{filters['OperatorUserNo']}%")
            if filters.get('OperatorUserName'):
                filter_clauses.append("OperatorUserName LIKE %s")
                params.append(f"%{filters['OperatorUserName']}%")
            if filters.get('OperationType'):
                filter_clauses.append("OperationType = %s")
                params.append(filters['OperationType'])

            if filter_clauses:
                base_query += " AND " + " AND ".join(filter_clauses)
            
            # 获取总数
            count_query = f"SELECT COUNT(*) {base_query}"
            total_count_record = execute_query(conn, count_query, tuple(params), fetch_one=True)
            total_count = total_count_record[0] if total_count_record else 0

            # 获取分页数据
            offset = (current - 1) * page_size
            data_query = f"SELECT {', '.join(ModificationModel.VIEW_COLUMNS)} {base_query} ORDER BY OperationTime DESC LIMIT %s OFFSET %s"
            final_params = tuple(params) + (page_size, offset)
            
            records_raw = execute_query(conn, data_query, final_params, fetch_all=True)
            
            # 将元组列表转换为字典列表
            records = [record_to_dict(row, ModificationModel.VIEW_COLUMNS) for row in records_raw]
            
            return records, total_count
        except Error as e:
            current_app.logger.error(f"数据库错误 (ModificationModel.get_paginated_list): {e}", exc_info=True)
            raise e

    @staticmethod
    def get_logs_for_user(user_no, current, page_size):
        """获取与特定用户相关的所有审计日志（查询视图）"""
        conn = get_db_connection()
        if not conn:
            return [], 0
        
        try:
            # 查询条件现在可以直接在视图上执行
            where_clause = "(OperatorUserNo = %s )"
            params = (user_no,)

            # 获取总数
            count_query = f"SELECT COUNT(*) FROM {ModificationModel.VIEW_NAME} WHERE {where_clause}"
            total_count_record = execute_query(conn, count_query, params, fetch_one=True)
            total_count = total_count_record[0] if total_count_record else 0

            # 获取分页数据
            offset = (current - 1) * page_size
            data_query = f"""
                SELECT {', '.join(ModificationModel.VIEW_COLUMNS)} 
                FROM {ModificationModel.VIEW_NAME} 
                WHERE {where_clause}
                ORDER BY OperationTime DESC 
                LIMIT %s OFFSET %s
            """
            final_params = params + (page_size, offset)
            
            records_raw = execute_query(conn, data_query, final_params, fetch_all=True)
            
            # 将元组列表转换为字典列表
            records = [record_to_dict(row, ModificationModel.VIEW_COLUMNS) for row in records_raw]
            
            return records, total_count
        except Error as e:
            current_app.logger.error(f"数据库错误 (ModificationModel.get_logs_for_user for {user_no}): {e}", exc_info=True)
            raise e