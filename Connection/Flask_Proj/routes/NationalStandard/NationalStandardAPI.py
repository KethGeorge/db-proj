
from flask import Blueprint, request, current_app
from mysql.connector import Error
import string
import random

# 导入您的工具函数和模型
from utils.db import get_db_connection, execute_query
from utils.response import success_response_wrap, fail_response_wrap
from utils.auth import token_required
from routes.NationalStandard.NationalStandard import NationalStandardModel # 导入新的模型

national_standard_bp = Blueprint('national_standard', __name__)

def generate_random_nsn(length=12, prefix="STD-"):
    """生成随机NSN，为了与UserNo类似，但考虑标准号的特点加入前缀"""
    characters = string.ascii_uppercase + string.digits
    unique_part = ''.join(random.choice(characters) for i in range(length - len(prefix)))
    return f"{prefix}{unique_part}"

@national_standard_bp.route('/national_standard', methods=['POST'])
@token_required # 假设创建标准需要认证
# @has_role(['admin']) # 可选：如果只有管理员能创建
def add_national_standard():
    current_app.logger.info("National standard creation data received")
    if not request.is_json:
        return fail_response_wrap(None, '请求必须是 JSON 格式', 40000)

    data = request.get_json()
    
    # 检查必填字段
    required_fields = ['StandardName'] # NSN可以由后端生成，Description和MaterialCode可选
    for field in required_fields:
        if field not in data or not data[field] or (isinstance(data[field], str) and not data[field].strip()):
            current_app.logger.warning(f'字段 "{field}" 不能为空或仅包含空格')
            return fail_response_wrap(None, f'字段 "{field}" 不能为空', 40001)

    standard_name = data.get('StandardName')
    description = data.get('Description')
    material_code = data.get('MaterialCode')
    
    # 模拟操作者信息
    operator = request.user.get('username', 'unknown')
    current_app.logger.info(f"User '{operator}' is creating a new national standard.")
    current_app.logger.info(f"Received Standard Data: {data}")

    nsn = None
    # 尝试生成唯一的NSN，重试机制
    for _ in range(10): # 最多尝试10次
        temp_nsn = generate_random_nsn()
        existing_nsn_record = NationalStandardModel.find_by_nsn(temp_nsn)
        if not existing_nsn_record:
            nsn = temp_nsn
            break
    if nsn is None:
        current_app.logger.error("无法生成唯一的NSN，请稍后重试。")
        return fail_response_wrap(None, '无法生成唯一的标准编号，请稍后重试。', 50001)
    current_app.logger.info(f"Generated unique NSN: {nsn}")
    data['NSN'] = nsn # 将生成的NSN添加到数据中

    try:
        # 检查 StandardName 是否已存在（如果 StandardName 要求唯一）
        # 假设 StandardName 不强制唯一，如果需要唯一，请取消注释以下代码
        existing_standard_by_name = NationalStandardModel.find_by_name(standard_name)
        if existing_standard_by_name:
             return fail_response_wrap(None, f'标准名称 "{standard_name}" 已存在，请使用其他名称。', 40003)

        if NationalStandardModel.create(data):
            current_app.logger.info(f"国家标准信息插入成功: NSN={nsn}, StandardName={standard_name}")
            return success_response_wrap({
                'NSN': nsn,
                'StandardName': standard_name
            }, '国家标准信息添加成功！')
        else:
            current_app.logger.error("国家标准信息插入数据库失败，模型返回 False")
            return fail_response_wrap(None, '国家标准信息插入数据库失败', 50000)
    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (add_national_standard): {db_error}")
        if db_error.errno == 1062: # Duplicate entry for key
            return fail_response_wrap(None, f'NSN或标准名称已存在，请检查。', 40003)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except ValueError as val_error:
        current_app.logger.warning(f"请求数据校验失败: {val_error}")
        return fail_response_wrap(None, str(val_error), 40001)
    except Exception as e:
        current_app.logger.error(f"处理 /api/national_standard 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)

@national_standard_bp.route('/national_standards', methods=['GET'])
@token_required # 假设查询列表需要认证
def get_national_standards():
    current_app.logger.info("Received request for national standard list.")
    
    # 获取查询参数
    nsn = request.args.get('NSN')
    standard_name = request.args.get('StandardName')
    description = request.args.get('Description')
    material_code = request.args.get('MaterialCode')
    
    # 分页参数
    try:
        current = int(request.args.get('current', 1)) # 默认第一页
        page_size = int(request.args.get('pageSize', 20)) # 默认每页20条
    except ValueError:
        return fail_response_wrap(None, '分页参数格式不正确', 40004)

    filters = {
        'NSN': nsn,
        'StandardName': standard_name,
        'Description': description,
        'MaterialCode': material_code
    }

    try:
        standards_list, total_count = NationalStandardModel.get_paginated_list(filters, current, page_size)
        
        current_app.logger.info(f"Total standards found: {total_count}")

        return success_response_wrap({
            'list': standards_list,
            'total': total_count
        }, '国家标准列表获取成功')

    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (get_national_standards): {db_error}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/national_standards GET 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)


@national_standard_bp.route('/national_standards/<string:nsn>', methods=['GET'])
@token_required
def get_national_standard_detail(nsn):
    current_app.logger.info(f"Received request for national standard detail: {nsn}")

    try:
        standard_detail = NationalStandardModel.find_by_nsn(nsn)

        if not standard_detail:
            return fail_response_wrap(None, '国家标准不存在', 40400)

        return success_response_wrap(standard_detail, '国家标准详情获取成功')

    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (get_national_standard_detail): {db_error}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/national_standards/<nsn> GET 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)


@national_standard_bp.route('/national_standards/<string:nsn>', methods=['PUT'])
@token_required # 假设更新标准需要认证
# @has_role(['admin']) # 可选：如果只有管理员能更新
def update_national_standard_info(nsn):
    current_app.logger.info(f"Received national standard info update request for NSN: {nsn}")

    if not request.is_json:
        return fail_response_wrap(None, '请求必须是 JSON 格式', 40000)

    data = request.get_json()

    # 允许修改的字段
    allowed_fields = ['StandardName', 'Description', 'MaterialCode']
    update_fields = {}
    for field in allowed_fields:
        if field in data:
            update_fields[field] = data[field]

    if not update_fields:
        return success_response_wrap(None, '没有提供任何要更新的字段', 20000)

    try:
        # 验证 NSN 是否存在
        existing_standard = NationalStandardModel.find_by_nsn(nsn)
        if not existing_standard:
            return fail_response_wrap(None, f'国家标准编号 "{nsn}" 不存在', 40400)

        # 如果更新 StandardName，需要检查是否与其他现有标准冲突（如果 StandardName 要求唯一）
        if 'StandardName' in update_fields:
            # 获取原始的标准名称
            original_standard_name = existing_standard.get('StandardName')
            # 获取请求中的新标准名称
            new_standard_name = update_fields['StandardName']

            # 如果新旧名称不同，才需要检查是否与数据库中其他记录冲突
            if new_standard_name != original_standard_name:
                current_app.logger.debug(f"StandardName is being changed from '{original_standard_name}' to '{new_standard_name}'. Checking for duplicates...")
                
                # 检查新名称是否与其他记录重复（排除当前记录）
                existing_standard_by_name_elsewhere = NationalStandardModel.find_by_name(new_standard_name, exclude_nsn=nsn)
                if existing_standard_by_name_elsewhere:
                    return fail_response_wrap(None, f'标准名称 "{new_standard_name}" 已存在，请使用其他名称。', 40003)
            else:
                current_app.logger.debug(f"StandardName in update_fields is the same as the original. Skipping duplicate check for StandardName.")
        if NationalStandardModel.update(nsn, update_fields):
            current_app.logger.info(f"国家标准信息更新成功: NSN={nsn}")
            return success_response_wrap(None, '国家标准信息更新成功！')
        else:
            current_app.logger.error(f"国家标准信息更新失败: NSN={nsn}")
            return fail_response_wrap(None, '国家标准信息更新失败', 50000)

    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (update_national_standard_info): {db_error}", exc_info=True)
        if db_error.errno == 1062: # Duplicate entry for unique key
            return fail_response_wrap(None, '标准名称已存在，请检查。', 40003)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/national_standards/{nsn} PUT 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)

@national_standard_bp.route('/national_standards/<string:nsn>', methods=['DELETE'])
@token_required # 假设删除标准需要认证
# @has_role(['admin']) # 可选：如果只有管理员能删除
def delete_national_standard(nsn):
    current_app.logger.info(f"Received national standard delete request for NSN: {nsn}")

    try:
        # 验证 NSN 是否存在
        existing_standard = NationalStandardModel.find_by_nsn(nsn)
        if not existing_standard:
            return fail_response_wrap(None, f'国家标准编号 "{nsn}" 不存在', 40400)
            
        if NationalStandardModel.delete(nsn):
            current_app.logger.info(f"国家标准删除成功: NSN={nsn}")
            return success_response_wrap(None, '国家标准删除成功！')
        else:
            current_app.logger.error(f"国家标准删除失败: NSN={nsn}")
            return fail_response_wrap(None, '国家标准删除失败', 50000)

    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (delete_national_standard): {db_error}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/national_standards/{nsn} DELETE 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)