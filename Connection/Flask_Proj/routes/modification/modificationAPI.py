# routes/modification/modificationAPI.py

from flask import Blueprint, request, current_app
from mysql.connector import Error

from utils.response import success_response_wrap, fail_response_wrap
from utils.auth import token_required
from routes.modification.modification import ModificationModel

modification_bp = Blueprint('modification_api', __name__)

@modification_bp.route('/modification', methods=['GET'])
@token_required
def get_modifications():
    """
    获取全局审计日志列表的API端点。
    """
    current_app.logger.info("收到全局审计日志列表请求")
    
    try:
        current = int(request.args.get('current', 1))
        page_size = int(request.args.get('pageSize', 20))
    except ValueError:
        return fail_response_wrap(None, '分页参数格式不正确', 40004)

    # 从请求参数中获取所有可能的筛选条件
    filters = {
        'EntityType': request.args.get('EntityType'),
        'EntityID': request.args.get('EntityID'),
        'OperatorUserNo': request.args.get('UserNo'),  # 前端传 UserNo，后端用 OperatorUserNo
        'OperatorUserName': request.args.get('UserName'), # 也可以按用户名筛选
        'OperationType': request.args.get('OperationType')
    }
    # 移除值为None或空字符串的键，避免在模型中处理
    filters = {k: v for k, v in filters.items() if v}

    try:
        log_list, total_count = ModificationModel.get_paginated_list(filters, current, page_size)
        
        return success_response_wrap({
            'list': log_list,
            'total': total_count
        }, '审计日志列表获取成功')

    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (get_modifications): {db_error}", exc_info=True)
        return fail_response_wrap(None, '服务器内部错误（数据库）', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/modification GET 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, '服务器内部错误', 50000)


@modification_bp.route('/modification/by-user/<string:user_no>', methods=['GET'])
@token_required
def get_modifications_by_user(user_no):
    """
    根据指定的用户ID，获取其相关的审计日志。
    """
    current_app.logger.info(f"收到用户 {user_no} 的审计日志请求")

    try:
        current = int(request.args.get('current', 1))
        page_size = int(request.args.get('pageSize', 10))
    except ValueError:
        return fail_response_wrap(None, '分页参数格式不正确', 40004)

    if not user_no:
        return fail_response_wrap(None, '用户ID不能为空', 40001)

    try:
        log_list, total_count = ModificationModel.get_logs_for_user(user_no, current, page_size)
        
        return success_response_wrap({
            'list': log_list,
            'total': total_count
        }, '用户相关审计日志获取成功')
    
    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (get_modifications_by_user for {user_no}): {db_error}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误（数据库）', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/modification/by-user/{user_no} GET 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误', 50000)