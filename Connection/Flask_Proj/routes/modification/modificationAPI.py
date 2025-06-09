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
    current_app.logger.info("收到审计日志列表请求")
    
    # 解析筛选参数
    entity_type = request.args.get('EntityType')
    entity_id = request.args.get('EntityID')
    user_no = request.args.get('UserNo')
    operation_type = request.args.get('OperationType')

    # 解析分页参数
    try:
        current = int(request.args.get('current', 1))
        page_size = int(request.args.get('pageSize', 20))
    except ValueError:
        return fail_response_wrap(None, '分页参数格式不正确', 40004)

    filters = {
        'EntityType': entity_type,
        'EntityID': entity_id,
        'UserNo': user_no,
        'OperationType': operation_type
    }
    # 移除值为None的键，避免在模型中处理
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