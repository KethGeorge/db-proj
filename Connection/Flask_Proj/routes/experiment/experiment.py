# backend/models/experiment.py

from utils.db import get_db_connection, execute_query
from mysql.connector import Error
from flask import current_app
from datetime import time, timedelta # 导入time

class ExperimentModel:
    TABLE_NAME = "experiment"
    # COLUMNS 列表中不再包含 "GelTime"
    COLUMNS = [
        "ExperimentNo", "MaterialCode", "HeatError", "MixError",
        "StartTime", "EndTime", "ProtocolNo", "UserNo"
    ]

    @staticmethod
    def find_by_no(experiment_no):
        """根据 ExperimentNo 查询单个实验详情"""
        conn = get_db_connection()
        if not conn: return None
        try:
            query = f"SELECT {', '.join(ExperimentModel.COLUMNS)} FROM {ExperimentModel.TABLE_NAME} WHERE ExperimentNo = %s"
            record = execute_query(conn, query, (experiment_no,), fetch_one=True)
            if record:
                experiment_data = dict(zip(ExperimentModel.COLUMNS, record))
                # 核心修改：判断类型从 time 改为 timedelta
                for key in ["StartTime", "EndTime"]:
                    if isinstance(experiment_data.get(key), timedelta): # <-- 这里
                        # 将 timedelta 转换为 HH:MM:SS 字符串
                        total_seconds = int(experiment_data[key].total_seconds())
                        hours, remainder = divmod(total_seconds, 3600)
                        minutes, seconds = divmod(remainder, 60)
                        # 确保小时数在0-23范围内，防止 timedelta 过大导致小时数溢出
                        experiment_data[key] = f"{hours % 24:02}:{minutes:02}:{seconds:02}"
                return experiment_data
            return None
        except Error as e:
            current_app.logger.error(f"数据库错误 (ExperimentModel.find_by_no): {e}")
            raise e

    @staticmethod
    def create(data):
        """创建新实验记录"""
        conn = get_db_connection()
        if not conn: return False
        try:
            columns = []
            placeholders = []
            values = []
            
            if 'ExperimentNo' not in data or not data['ExperimentNo'].strip():
                raise ValueError("ExperimentNo is required and cannot be empty.")
            if 'UserNo' not in data or not data['UserNo'].strip():
                raise ValueError("UserNo is required and cannot be empty.")
            
            for col_name in ExperimentModel.COLUMNS: # 使用更新后的COLUMNS
                if col_name in data and data[col_name] is not None:
                    columns.append(col_name)
                    placeholders.append("%s")
                    values.append(data[col_name])
                elif col_name not in data or data[col_name] is None:
                    columns.append(col_name)
                    placeholders.append("%s")
                    values.append(None)
            
            insert_query = f"INSERT INTO {ExperimentModel.TABLE_NAME} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
            return execute_query(conn, insert_query, tuple(values), is_insert=True)
        except Error as e:
            current_app.logger.error(f"数据库操作错误 (ExperimentModel.create): {e}")
            raise e
        except ValueError as e:
            current_app.logger.warning(f"数据校验错误 (ExperimentModel.create): {e}")
            raise e

    @staticmethod
    def update(experiment_no, data):
        """更新实验记录"""
        conn = get_db_connection()
        if not conn: return False
        try:
            set_clauses = []
            values = []
            
            # updatable_cols 列表中不再包含 "GelTime"
            updatable_cols = [
                "MaterialCode", "HeatError", "MixError",
                "StartTime", "EndTime", "ProtocolNo", "UserNo"
            ]
            for col_name in updatable_cols:
                if col_name in data:
                    set_clauses.append(f"{col_name} = %s")
                    values.append(data[col_name])
            
            if not set_clauses:
                return True 
            
            update_query = f"UPDATE {ExperimentModel.TABLE_NAME} SET {', '.join(set_clauses)} WHERE ExperimentNo = %s"
            values.append(experiment_no)
            return execute_query(conn, update_query, tuple(values))
        except Error as e:
            current_app.logger.error(f"数据库错误 (ExperimentModel.update): {e}")
            raise e

    @staticmethod
    def delete(experiment_no):
        """删除实验记录"""
        conn = get_db_connection()
        if not conn: return False
        try:
            delete_query = f"DELETE FROM {ExperimentModel.TABLE_NAME} WHERE ExperimentNo = %s"
            return execute_query(conn, delete_query, (experiment_no,))
        except Error as e:
            current_app.logger.error(f"数据库错误 (ExperimentModel.delete): {e}")
            raise e

    @staticmethod
    def get_paginated_list(filters, current, page_size):
        """获取分页和筛选后的实验列表"""
        conn = get_db_connection()
        if not conn: return [], 0
        try:
            base_query = f"FROM {ExperimentModel.TABLE_NAME} WHERE 1=1"
            filter_clauses = []
            params = []

            if filters.get('ExperimentNo'):
                filter_clauses.append("ExperimentNo LIKE %s")
                params.append(f"%{filters['ExperimentNo']}%")
            if filters.get('MaterialCode'):
                filter_clauses.append("MaterialCode LIKE %s")
                params.append(f"%{filters['MaterialCode']}%")
            if filters.get('ProtocolNo'):
                filter_clauses.append("ProtocolNo LIKE %s")
                params.append(f"%{filters['ProtocolNo']}%")
            if filters.get('UserNo'):
                filter_clauses.append("UserNo LIKE %s")
                params.append(f"%{filters['UserNo']}%")

            if filter_clauses:
                base_query += " AND " + " AND ".join(filter_clauses)

            count_query = f"SELECT COUNT(*) {base_query}"
            total_count = execute_query(conn, count_query, tuple(params), fetch_one=True)[0]

            offset = (current - 1) * page_size
            data_query = f"SELECT {', '.join(ExperimentModel.COLUMNS)} {base_query} ORDER BY ExperimentNo LIMIT %s OFFSET %s" # 使用更新后的COLUMNS
            params.append(page_size)
            params.append(offset)
            
            records_raw = execute_query(conn, data_query, tuple(params), fetch_all=True)
            records = []
            for record_tuple in records_raw:
                record_dict = dict(zip(ExperimentModel.COLUMNS, record_tuple))
                # 处理TIME类型字段为字符串
                record_dict = dict(zip(ExperimentModel.COLUMNS, record_tuple))
                # 核心修改：判断类型从 time 改为 timedelta
                for key in ["StartTime", "EndTime"]:
                    if isinstance(record_dict.get(key), timedelta): # <-- 这里
                        # 将 timedelta 转换为 HH:MM:SS 字符串
                        total_seconds = int(record_dict[key].total_seconds())
                        hours, remainder = divmod(total_seconds, 3600)
                        minutes, seconds = divmod(remainder, 60)
                        record_dict[key] = f"{hours % 24:02}:{minutes:02}:{seconds:02}"
                records.append(record_dict)
            
            return records, total_count
        except Error as e:
            current_app.logger.error(f"数据库错误 (ExperimentModel.get_paginated_list): {e}")
            raise e