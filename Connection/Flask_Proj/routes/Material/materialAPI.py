# backend/routes/material_api.py

from flask import Blueprint, request, current_app
from mysql.connector import Error

# 导入您的工具函数和模型
from utils.response import success_response_wrap, fail_response_wrap
from utils.auth import token_required # 假设需要认证
from routes.Material.material import MaterialModel # 导入新的材料模型

material_bp = Blueprint('material', __name__)

@material_bp.route('/material', methods=['POST'])
@token_required # 假设创建材料需要认证
# @has_role(['admin']) # 可选：如果只有管理员能创建
def add_material():
    current_app.logger.info("Material creation data received")
    if not request.is_json:
        return fail_response_wrap(None, '请求必须是 JSON 格式', 40000)

    data = request.get_json()
    
    required_fields = ['MaterialCode', 'MaterialName']
    for field in required_fields:
        if field not in data or not data[field] or (isinstance(data[field], str) and not data[field].strip()):
            current_app.logger.warning(f'字段 "{field}" 不能为空或仅包含空格')
            return fail_response_wrap(None, f'字段 "{field}" 不能为空', 40001)

    material_code = data.get('MaterialCode')
    material_name = data.get('MaterialName')
    
    operator = request.user.get('username', 'unknown') # 模拟操作者信息
    current_app.logger.info(f"User '{operator}' is creating a new material.")
    current_app.logger.info(f"Received Material Data: {data}")

    try:
        # 检查 MaterialCode 是否已存在（主键唯一性）
        existing_material_by_code = MaterialModel.find_by_code(material_code)
        if existing_material_by_code:
            return fail_response_wrap(None, f'材料编码 "{material_code}" 已存在，请使用其他编码。', 40003)

        # 检查 MaterialName 是否已存在（如果 MaterialName 要求唯一）
        # 假设 MaterialName 强制唯一
        existing_material_by_name = MaterialModel.find_by_name(material_name)
        if existing_material_by_name:
             return fail_response_wrap(None, f'材料名称 "{material_name}" 已存在，请使用其他名称。', 40003)

        if MaterialModel.create(data):
            current_app.logger.info(f"材料信息插入成功: MaterialCode={material_code}, MaterialName={material_name}")
            return success_response_wrap({
                'MaterialCode': material_code,
                'MaterialName': material_name
            }, '材料信息添加成功！')
        else:
            current_app.logger.error("材料信息插入数据库失败，模型返回 False")
            return fail_response_wrap(None, '材料信息插入数据库失败', 50000)
    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (add_material): {db_error}")
        if db_error.errno == 1062: # Duplicate entry for key (MaterialCode or MaterialName)
            return fail_response_wrap(None, f'材料编码或材料名称已存在，请检查。', 40003)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except ValueError as val_error:
        current_app.logger.warning(f"请求数据校验失败: {val_error}")
        return fail_response_wrap(None, str(val_error), 40001)
    except Exception as e:
        current_app.logger.error(f"处理 /api/material POST 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)

@material_bp.route('/materials', methods=['GET'])
@token_required # 假设查询列表需要认证
def get_materials():
    current_app.logger.info("Received request for material list.")
    
    # 获取查询参数
    material_code = request.args.get('MaterialCode')
    material_name = request.args.get('MaterialName')
    
    # 分页参数
    try:
        current = int(request.args.get('current', 1)) # 默认第一页
        page_size = int(request.args.get('pageSize', 20)) # 默认每页20条
    except ValueError:
        return fail_response_wrap(None, '分页参数格式不正确', 40004)

    filters = {
        'MaterialCode': material_code,
        'MaterialName': material_name,
    }

    try:
        materials_list, total_count = MaterialModel.get_paginated_list(filters, current, page_size)
        
        current_app.logger.info(f"Total materials found: {total_count}")

        return success_response_wrap({
            'list': materials_list,
            'total': total_count
        }, '材料列表获取成功')

    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (get_materials): {db_error}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/materials GET 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)


@material_bp.route('/materials/<string:material_code>', methods=['GET'])
@token_required
def get_material_detail(material_code):
    current_app.logger.info(f"Received request for material detail: {material_code}")

    try:
        material_detail = MaterialModel.find_by_code(material_code)

        if not material_detail:
            return fail_response_wrap(None, '材料不存在', 40400)

        return success_response_wrap(material_detail, '材料详情获取成功')

    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (get_material_detail): {db_error}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/materials/<material_code> GET 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)


@material_bp.route('/materials/<string:material_code>', methods=['PUT'])
@token_required # 假设更新材料需要认证
# @has_role(['admin']) # 可选：如果只有管理员能更新
def update_material_info(material_code):
    current_app.logger.info(f"Received material info update request for MaterialCode: {material_code}")

    if not request.is_json:
        return fail_response_wrap(None, '请求必须是 JSON 格式', 40000)

    data = request.get_json()

    allowed_fields = ['MaterialName'] # 只有 MaterialName 是可修改的字段
    update_fields = {}
    for field in allowed_fields:
        if field in data:
            update_fields[field] = data[field]

    if not update_fields:
        return success_response_wrap(None, '没有提供任何要更新的字段', 20000)

    try:
        # 1. 验证 MaterialCode 是否存在，并获取当前记录的完整信息
        existing_material = MaterialModel.find_by_code(material_code)
        if not existing_material:
            return fail_response_wrap(None, f'材料编码 "{material_code}" 不存在', 40400)

        # 2. 只有当请求中包含 MaterialName 字段，并且新值与旧值不同时，才进行重复性检查
        if 'MaterialName' in update_fields:
            original_material_name = existing_material.get('MaterialName')
            new_material_name = update_fields['MaterialName']

            if new_material_name != original_material_name:
                current_app.logger.debug(f"MaterialName is being changed from '{original_material_name}' to '{new_material_name}'. Checking for duplicates...")
                
                # 检查新名称是否与其他记录重复（排除当前记录）
                existing_material_by_name_elsewhere = MaterialModel.find_by_name(new_material_name, exclude_code=material_code)
                if existing_material_by_name_elsewhere:
                    return fail_response_wrap(None, f'材料名称 "{new_material_name}" 已存在，请使用其他名称。', 40003)
            else:
                current_app.logger.debug(f"MaterialName in update_fields is the same as the original. Skipping duplicate check for MaterialName.")


        # 3. 执行实际的更新操作
        if MaterialModel.update(material_code, update_fields):
            current_app.logger.info(f"材料信息更新成功: MaterialCode={material_code}")
            return success_response_wrap(None, '材料信息更新成功！')
        else:
            current_app.logger.error(f"材料信息更新失败: MaterialCode={material_code}")
            return fail_response_wrap(None, '材料信息更新失败', 50000)

    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (update_material_info): {db_error}", exc_info=True)
        if db_error.errno == 1062: # Duplicate entry for unique key (MaterialName if it's unique)
            return fail_response_wrap(None, '材料名称已存在，请检查。', 40003)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/materials/{material_code} PUT 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)

@material_bp.route('/materials/<string:material_code>', methods=['DELETE'])
@token_required # 假设删除材料需要认证
# @has_role(['admin']) # 可选：如果只有管理员能删除
def delete_material(material_code):
    current_app.logger.info(f"Received material delete request for MaterialCode: {material_code}")

    try:
        # 验证 MaterialCode 是否存在
        existing_material = MaterialModel.find_by_code(material_code)
        if not existing_material:
            return fail_response_wrap(None, f'材料编码 "{material_code}" 不存在', 40400)
            
        if MaterialModel.delete(material_code):
            current_app.logger.info(f"材料删除成功: MaterialCode={material_code}")
            return success_response_wrap(None, '材料删除成功！')
        else:
            current_app.logger.error(f"材料删除失败: MaterialCode={material_code}")
            return fail_response_wrap(None, '材料删除失败', 50000)

    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (delete_material): {db_error}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/materials/{material_code} DELETE 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)