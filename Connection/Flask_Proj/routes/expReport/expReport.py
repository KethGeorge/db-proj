# models/report.py

from utils.db import get_db_connection, execute_query
from mysql.connector import Error
from flask import current_app
import datetime

def record_to_dict(record, columns):
    """
    一个健壮的辅助函数，用于将数据库记录（元组）和列名转换为字典，
    并在此过程中格式化特定类型的数据。
    """
    if not record:
        return None
    
    # 使用列名和记录值创建一个初始字典
    record_dict = dict(zip(columns, record))
    
    # 遍历字典中的每一项，进行类型转换
    for key, value in record_dict.items():
        if value is None:
            continue # 如果值是 None，跳过处理

        # 1. 将 datetime.timedelta (来自 TIME 类型) 转换为 'HH:MM:SS' 字符串
        if isinstance(value, datetime.timedelta):
            total_seconds = int(value.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            record_dict[key] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        # 2. 将整数 1/0 (来自 BOOL/TINYINT(1) 类型) 转换为布尔值 true/false
        #    我们通过检查列名来精确匹配 'IsGel' 字段
        elif key.lower() == 'isgel' and isinstance(value, int):
            record_dict[key] = bool(value)
            
    return record_dict


class ReportModel:
    # 定义各表的列名，必须与数据库查询出的顺序完全一致
    # 使用 SELECT * 时，顺序是表定义的顺序
    EXPREPORT_COLS = ["ExperimentCode", "ExperimentNo", "ExperimentName", "ExperimentalStatus"]
    HEC_COLS = ["HEC", "Temperature", "Time1", "SafeArea", "ExperimentCode"]
    MEC_COLS = ["MEC", "HeightError", "PlainError", "ErrorArea", "SpeedError", "Time2", "ExperimentCode"]
    MTEC_COLS = ["MTEC", "PhotoPath", "Is_solid", "Time3", "ExperimentCode"]

    @staticmethod
    def get_report_by_experiment_no(experiment_no):
        """
        根据实验编号 (ExperimentNo) 获取完整的实验报告数据。
        查询所有相关表，并使用 record_to_dict 进行格式化。
        """
        conn = get_db_connection()
        if not conn:
            raise ConnectionError("数据库连接失败")
        
        try:
            # 1. 查询主报告信息，并格式化
            report_query = f"SELECT {', '.join(ReportModel.EXPREPORT_COLS)} FROM ExpReport WHERE ExperimentNo = %s"
            report_record = execute_query(conn, report_query, (experiment_no,), fetch_one=True)
            
            if not report_record:
                return None
            
            # 主报告也经过格式化（尽管它可能没有特殊类型字段，但保持一致性是好习惯）
            report_details = record_to_dict(report_record, ReportModel.EXPREPORT_COLS)
            experiment_code = report_details['ExperimentCode']

            # 2. 查询并格式化 HEC 子报告
            hec_query = f"SELECT {', '.join(ReportModel.HEC_COLS)} FROM HEC WHERE ExperimentCode = %s"
            hec_record = execute_query(conn, hec_query, (experiment_code,), fetch_one=True)
            hec_data = record_to_dict(hec_record, ReportModel.HEC_COLS)

            # 3. 查询并格式化 MEC 子报告
            mec_query = f"SELECT {', '.join(ReportModel.MEC_COLS)} FROM MEC WHERE ExperimentCode = %s"
            mec_record = execute_query(conn, mec_query, (experiment_code,), fetch_one=True)
            mec_data = record_to_dict(mec_record, ReportModel.MEC_COLS)

            # 4. 查询并格式化 MTEC 子报告 (这是关键)
            mtec_query = f"SELECT {', '.join(ReportModel.MTEC_COLS)} FROM MTEC WHERE ExperimentCode = %s"
            mtec_record = execute_query(conn, mtec_query, (experiment_code,), fetch_one=True)
            mtec_data = record_to_dict(mtec_record, ReportModel.MTEC_COLS)

            # 5. 组装最终结果
            full_report = {
                "reportDetails": report_details,
                "hecData": hec_data,
                "mecData": mec_data,
                "mtecData": mtec_data
            }
            return full_report

        except Error as e:
            current_app.logger.error(f"查询实验报告失败 (ExperimentNo: {experiment_no}): {e}", exc_info=True)
            raise e
            


# 辅助函数，将数据库记录（元组）和列名转换为字典
    @staticmethod
    def get_paginated_list(filters, current, pageSize):
        """获取分页和筛选后的实验报告列表"""
        conn = get_db_connection()
        if not conn: return [], 0
        try:
            # 构建筛选条件
            where_clauses = []
            params = []
            
            # 筛选条件基于 ExpReport 表的字段
            if filters.get('ExperimentCode'):
                where_clauses.append("ExperimentCode LIKE %s")
                params.append(f"%{filters['ExperimentCode']}%")
            if filters.get('ExperimentNo'):
                where_clauses.append("ExperimentNo LIKE %s")
                params.append(f"%{filters['ExperimentNo']}%")
            if filters.get('ExperimentName'):
                where_clauses.append("ExperimentName LIKE %s")
                params.append(f"%{filters['ExperimentName']}%")
            if filters.get('ExperimentalStatus'):
                where_clauses.append("ExperimentalStatus = %s")
                params.append(filters['ExperimentalStatus'])

            where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
            
            # 获取总条数
            count_query = f"SELECT COUNT(*) FROM ExpReport WHERE {where_sql}"
            total_count_record = execute_query(conn, count_query, tuple(params), fetch_one=True)
            total_count = total_count_record[0] if total_count_record else 0

            # 获取分页数据
            offset = (current - 1) * pageSize
            data_query = f"SELECT {', '.join(ReportModel.EXPREPORT_COLS)} FROM ExpReport WHERE {where_sql} ORDER BY ExperimentCode DESC LIMIT %s OFFSET %s"
            final_params = tuple(params) + (pageSize, offset)
            
            records_raw = execute_query(conn, data_query, final_params, fetch_all=True)
            
            # 将元组列表转换为字典列表
            records = [dict(zip(ReportModel.EXPREPORT_COLS, row)) for row in records_raw]
            
            return records, total_count

        except Error as e:
            current_app.logger.error(f"数据库错误 (ReportModel.get_paginated_list): {e}", exc_info=True)
            raise e