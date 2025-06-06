# backend/models/device.py

from utils.db import get_db_connection, execute_query
from mysql.connector import Error
from flask import current_app
from datetime import datetime

class DeviceModel:
    TABLE_NAME = "device"
    # COLUMNS 列表中不再包含 "Operator"，因为我们不再从前端接收/向前端返回此字段
    # 并且它不作为核心业务字段参与模型操作
    COLUMNS_FOR_CRUD = ["DeviceNo", "DeviceName", "DeviceUsage", "DStartTime", "DMT", "DStopTime"]

    @staticmethod
    def find_by_no(device_no):
        """根据 DeviceNo 查询单个设备详情"""
        conn = get_db_connection()
        if not conn: return None
        try:
            # 查询时也只选择 COLUMNS_FOR_CRUD 中定义的字段
            query = f"SELECT {', '.join(DeviceModel.COLUMNS_FOR_CRUD)} FROM {DeviceModel.TABLE_NAME} WHERE DeviceNo = %s"
            record = execute_query(conn, query, (device_no,), fetch_one=True)
            if record:
                device_data = dict(zip(DeviceModel.COLUMNS_FOR_CRUD, record))
                for key in ["DStartTime", "DMT", "DStopTime"]:
                    if isinstance(device_data.get(key), datetime):
                        device_data[key] = device_data[key].isoformat()
                return device_data
            return None
        except Error as e:
            current_app.logger.error(f"数据库错误 (DeviceModel.find_by_no): {e}")
            raise e

    @staticmethod
    def find_by_name(device_name, exclude_no=None):
        """根据 DeviceName 查询，检查名称是否重复"""
        conn = get_db_connection()
        if not conn: return None
        try:
            query = f"SELECT DeviceNo FROM {DeviceModel.TABLE_NAME} WHERE DeviceName = %s"
            params = [device_name]
            if exclude_no:
                query += " AND DeviceNo != %s"
                params.append(exclude_no)
            return execute_query(conn, query, tuple(params), fetch_one=True)
        except Error as e:
            current_app.logger.error(f"数据库错误 (DeviceModel.find_by_name): {e}")
            raise e

    @staticmethod
    def create(data):
        """创建新设备记录"""
        conn = get_db_connection()
        if not conn: return False
        try:
            columns = []
            placeholders = []
            values = []
            
            if 'DeviceNo' not in data or not data['DeviceNo'].strip():
                raise ValueError("DeviceNo is required and cannot be empty.")
            if 'DeviceName' not in data or not data['DeviceName'].strip():
                raise ValueError("DeviceName is required and cannot be empty.")
            
            # 只处理 COLUMNS_FOR_CRUD 中定义的字段
            for col_name in DeviceModel.COLUMNS_FOR_CRUD:
                if col_name in data and data[col_name] is not None:
                    columns.append(col_name)
                    placeholders.append("%s")
                    values.append(data[col_name])
                elif col_name in data and data[col_name] is None:
                    columns.append(col_name)
                    placeholders.append("%s")
                    values.append(None)
            
            insert_query = f"INSERT INTO {DeviceModel.TABLE_NAME} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
            return execute_query(conn, insert_query, tuple(values), is_insert=True)
        except Error as e:
            current_app.logger.error(f"数据库错误 (DeviceModel.create): {e}")
            raise e
        except ValueError as e:
            current_app.logger.warning(f"数据校验错误 (DeviceModel.create): {e}")
            raise e

    @staticmethod
    def update(device_no, data):
        """更新设备记录"""
        conn = get_db_connection()
        if not conn: return False
        try:
            set_clauses = []
            values = []
            current_app.logger.debug(f"更新设备 {device_no} 的数据: {data}")
            # updatable_cols 中不再包含 "Operator"
            updatable_cols = ["DeviceName", "DeviceUsage", "DStartTime", "DMT", "DStopTime"]
            for col_name in updatable_cols:
                if col_name in data:
                    set_clauses.append(f"{col_name} = %s")
                    values.append(data[col_name])
            
            if not set_clauses:
                return True 
            
            update_query = f"UPDATE {DeviceModel.TABLE_NAME} SET {', '.join(set_clauses)} WHERE DeviceNo = %s"
            values.append(device_no)
            return execute_query(conn, update_query, tuple(values))
        except Error as e:
            current_app.logger.error(f"数据库错误 (DeviceModel.update): {e}")
            raise e

    @staticmethod
    def delete(device_no):
        """删除设备记录"""
        conn = get_db_connection()
        if not conn: return False
        try:
            delete_query = f"DELETE FROM {DeviceModel.TABLE_NAME} WHERE DeviceNo = %s"
            return execute_query(conn, delete_query, (device_no,))
        except Error as e:
            current_app.logger.error(f"数据库错误 (DeviceModel.delete): {e}")
            raise e

    @staticmethod
    def get_paginated_list(filters, current, page_size):
        """获取分页和筛选后的设备列表"""
        conn = get_db_connection()
        if not conn: return [], 0
        try:
            base_query = f"FROM {DeviceModel.TABLE_NAME} WHERE 1=1"
            filter_clauses = []
            params = []

            if filters.get('DeviceNo'):
                filter_clauses.append("DeviceNo LIKE %s")
                params.append(f"%{filters['DeviceNo']}%")
            if filters.get('DeviceName'):
                filter_clauses.append("DeviceName LIKE %s")
                params.append(f"%{filters['DeviceName']}%")
            if filters.get('DeviceUsage'):
                filter_clauses.append("DeviceUsage LIKE %s")
                params.append(f"%{filters['DeviceUsage']}%")

            if filter_clauses:
                base_query += " AND " + " AND ".join(filter_clauses)

            count_query = f"SELECT COUNT(*) {base_query}"
            total_count = execute_query(conn, count_query, tuple(params), fetch_one=True)[0]

            offset = (current - 1) * page_size
            # 查询时也只选择 COLUMNS_FOR_CRUD 中定义的字段
            data_query = f"SELECT {', '.join(DeviceModel.COLUMNS_FOR_CRUD)} {base_query} ORDER BY DeviceNo LIMIT %s OFFSET %s"
            params.append(page_size)
            params.append(offset)
            
            records_raw = execute_query(conn, data_query, tuple(params), fetch_all=True)
            records = []
            for record_tuple in records_raw:
                record_dict = dict(zip(DeviceModel.COLUMNS_FOR_CRUD, record_tuple))
                for key in ["DStartTime", "DMT", "DStopTime"]:
                    if isinstance(record_dict.get(key), datetime):
                        record_dict[key] = record_dict[key].isoformat()
                records.append(record_dict)
            
            return records, total_count
        except Error as e:
            current_app.logger.error(f"数据库错误 (DeviceModel.get_paginated_list): {e}")
            raise e