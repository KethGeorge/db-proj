# routes/report/reportAPI.py

from flask import Blueprint, request, current_app
from mysql.connector import Error

from utils.response import success_response_wrap, fail_response_wrap
from utils.auth import token_required
from routes.expReport.expReport import ReportModel # 导入新的报告模型

report_bp = Blueprint('report_api', __name__)

@report_bp.route('/report/<string:experiment_no>', methods=['GET'])
@token_required
def get_experiment_report(experiment_no):
    """
    获取指定实验编号的详细报告
    """
    current_app.logger.info(f"收到实验报告请求: {experiment_no}")
    
    if not experiment_no:
        return fail_response_wrap(None, "实验编号不能为空", 40000)

    try:
        report_data = ReportModel.get_report_by_experiment_no(experiment_no)
        
        if report_data is None:
            return fail_response_wrap(None, "未找到对应的实验报告", 40400)
            
        return success_response_wrap(report_data, "实验报告获取成功")

    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (get_experiment_report): {db_error}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/report/<experiment_no> GET 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)

@report_bp.route('/reports', methods=['GET'])
@token_required
def get_reports_list():
    current_app.logger.info("收到实验报告列表请求。")
    
    try:
        # 解析查询参数
        current = int(request.args.get('current', 1))
        page_size = int(request.args.get('pageSize', 20))
        
        # 解析筛选参数
        filters = {
            'ExperimentCode': request.args.get('ExperimentCode'),
            'ExperimentNo': request.args.get('ExperimentNo'),
            'ExperimentName': request.args.get('ExperimentName'),
            'ExperimentalStatus': request.args.get('ExperimentalStatus'),
        }
        # 移除值为 None 或空字符串的筛选条件
        filters = {k: v for k, v in filters.items() if v}

        report_list, total = ReportModel.get_paginated_list(filters, current, page_size)
        
        return success_response_wrap({
            'list': report_list,
            'total': total,
        }, '实验报告列表获取成功')

    except ValueError:
        return fail_response_wrap(None, "分页参数格式不正确", 40000)
    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (get_reports_list): {db_error}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/reports GET 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)