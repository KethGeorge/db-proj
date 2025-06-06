# backend/routes/protocol_api.py

from flask import Blueprint, request, current_app
from mysql.connector import Error

from utils.response import success_response_wrap, fail_response_wrap
from utils.auth import token_required
from routes.protocol.protocol import ProtocolModel
from utils.db import get_db_connection, execute_query
protocol_bp = Blueprint('protocol_api', __name__)

def _set_db_session_user_id(conn, user_id):
    if user_id is not None:
        try:
            execute_query(conn, "SET @current_user_id = %s;", (user_id,), fetch_one=False, fetch_all=False, is_insert=False)
            current_app.logger.debug(f"MySQL session variable @current_user_id set to {user_id} for current operation.")
        except Exception as e:
            current_app.logger.error(f"Failed to set @current_user_id to {user_id}: {e}", exc_info=True)
            raise

# 辅助函数：将字符串或 None 转换为 float 或 None
def _parse_float_or_none(value, field_name):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str) and value.strip():
        try:
            return float(value.strip())
        except ValueError:
            current_app.logger.warning(f"字段 '{field_name}' 必须是有效数字，但接收到非数字字符串：'{value}'")
            raise ValueError(f"字段 '{field_name}' 必须是有效数字")
    elif isinstance(value, str) and not value.strip(): # 空字符串也转为 None
        return None
    # 如果是非数字类型且非字符串，返回None或抛出错误，取决于需求
    current_app.logger.warning(f"字段 '{field_name}' 接收到非预期类型：{type(value).__name__}，值：'{value}'")
    return None # 或者可以抛出更严格的错误

@protocol_bp.route('/protocol', methods=['POST'])
@token_required
def add_protocol():
    current_app.logger.info("Protocol creation data received")
    if not request.is_json:
        return fail_response_wrap(None, '请求必须是 JSON 格式', 40000)

    data = request.get_json()
    
    required_fields = ['ProtocolNo', 'MaterialCode', 'UserNo']
    for field in required_fields:
        if field not in data or not data[field] or (isinstance(data[field], str) and not data[field].strip()):
            current_app.logger.warning(f'字段 "{field}" 不能为空或仅包含空格')
            return fail_response_wrap(None, f'字段 "{field}" 不能为空', 40001)

    # 获取所有字段数据，并进行类型转换
    protocol_no = data.get('ProtocolNo')
    nsn = data.get('NSN') if data.get('NSN') else None # NSN如果为空字符串也设为None
    
    # 浮点数类型字段通过辅助函数处理
    try:
        sht = _parse_float_or_none(data.get('SHT'), 'SHT')
        sms = _parse_float_or_none(data.get('SMS'), 'SMS')
        mixing_angle = _parse_float_or_none(data.get('MixingAngle'), 'MixingAngle')
        mixing_radius = _parse_float_or_none(data.get('MixingRadius'), 'MixingRadius')
        measurement_interval = _parse_float_or_none(data.get('MeasurementInterval'), 'MeasurementInterval')
    except ValueError as e:
        return fail_response_wrap(None, str(e), 40005) # 40005: 数字格式错误

    material_code = data.get('MaterialCode')
    user_no_protocol = data.get('UserNo') # 这是协议的UserNo，不是操作员UserNo

    protocol_data_to_create = {
        'ProtocolNo': protocol_no,
        'NSN': nsn,
        'SHT': sht,
        'SMS': sms,
        'MixingAngle': mixing_angle,
        'MixingRadius': mixing_radius,
        'MeasurementInterval': measurement_interval,
        'MaterialCode': material_code,
        'UserNo': user_no_protocol
    }

    operator_user_no = request.user.get('UserNo')
    if operator_user_no is None:
        current_app.logger.error("Operator UserNo not available from token, cannot record modification.")
        return fail_response_wrap(None, '操作用户ID缺失，无法记录操作', 50001)

    conn = get_db_connection()
    if not conn:
        return fail_response_wrap(None, '数据库连接失败', 50000)

    try:
        _set_db_session_user_id(conn, operator_user_no)

        existing_protocol_by_no = ProtocolModel.find_by_no(protocol_no)
        if existing_protocol_by_no:
            return fail_response_wrap(None, f'协议编码 "{protocol_no}" 已存在，请使用其他编码。', 40003)

        if ProtocolModel.create(protocol_data_to_create):
            current_app.logger.info(f"协议信息插入成功: ProtocolNo={protocol_no}")
            return success_response_wrap({
                'ProtocolNo': protocol_no,
                'MaterialCode': material_code,
                'UserNo': user_no_protocol
            }, '协议信息添加成功！')
        else:
            current_app.logger.error("协议信息插入数据库失败，模型返回 False")
            return fail_response_wrap(None, '协议信息插入数据库失败', 50000)
    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (add_protocol): {db_error}", exc_info=True)
        if db_error.errno == 1062:
            return fail_response_wrap(None, f'协议编码已存在或外键约束失败，请检查。', 40003)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except ValueError as val_error: # 捕获 _parse_float_or_none 抛出的 ValueError
        current_app.logger.warning(f"请求数据校验失败: {val_error}")
        return fail_response_wrap(None, str(val_error), 40001)
    except Exception as e:
        current_app.logger.error(f"处理 /api/protocol POST 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)

# ... (get_protocols 和 get_protocol_detail 保持不变) ...

@protocol_bp.route('/protocol', methods=['GET']) # 列表查询路径
@token_required
def get_protocols():
    current_app.logger.info("Received request for protocol list.")
    
    # 获取查询参数
    protocol_no = request.args.get('ProtocolNo')
    nsn = request.args.get('NSN')
    material_code = request.args.get('MaterialCode')
    user_no_filter = request.args.get('UserNo') # 过滤UserNo

    # 分页参数
    try:
        current = int(request.args.get('current', 1))
        page_size = int(request.args.get('pageSize', 20))
    except ValueError:
        return fail_response_wrap(None, '分页参数格式不正确', 40004)

    filters = {
        'ProtocolNo': protocol_no,
        'NSN': nsn,
        'MaterialCode': material_code,
        'UserNo': user_no_filter,
    }

    try:
        protocols_list, total_count = ProtocolModel.get_paginated_list(filters, current, page_size)
        
        current_app.logger.info(f"Total protocols found: {total_count}")

        return success_response_wrap({
            'list': protocols_list,
            'total': total_count
        }, '协议列表获取成功')

    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (get_protocols): {db_error}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/protocol GET 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)


@protocol_bp.route('/protocol/<string:protocol_no>', methods=['GET']) # 详情查询路径
@token_required
def get_protocol_detail(protocol_no):
    current_app.logger.info(f"Received request for protocol detail: {protocol_no}")

    try:
        protocol_detail = ProtocolModel.find_by_no(protocol_no)

        if not protocol_detail:
            return fail_response_wrap(None, '协议不存在', 40400)

        return success_response_wrap(protocol_detail, '协议详情获取成功')

    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (get_protocol_detail): {db_error}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/protocol/<protocol_no> GET 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)



@protocol_bp.route('/protocol/<string:protocol_no>', methods=['PUT'])
@token_required
def update_protocol_info(protocol_no):
    current_app.logger.info(f"Received protocol info update request for ProtocolNo: {protocol_no}")
    
    if not request.is_json:
        return fail_response_wrap(None, '请求必须是 JSON 格式', 40000)

    data = request.get_json()

    update_fields = {}

    # 处理字符串字段
    string_fields = ["NSN", "MaterialCode", "UserNo"] # NSN允许为None，MaterialCode和UserNo不允许为None
    for field in string_fields:
        if field in data:
            value = data[field]
            if isinstance(value, str) and not value.strip():
                update_fields[field] = None
            else:
                update_fields[field] = value

    # 处理浮点数字段
    float_fields = ["SHT", "SMS", "MixingAngle", "MixingRadius", "MeasurementInterval"]
    for field in float_fields:
        if field in data: # 只要前端有发送这个字段，就把它加进来
            try:
                update_fields[field] = _parse_float_or_none(data[field], field)
            except ValueError as e: # 捕获 _parse_float_or_none 抛出的 ValueError
                return fail_response_wrap(None, str(e), 40005) # 40005: 数字格式错误
        else:
            # 如果前端没有发送这个字段（例如未填写），显式将其设置为 None
            update_fields[field] = None


    if not update_fields:
        return success_response_wrap(None, '没有提供任何要更新的字段', 20000)

    operator_user_no = request.user.get('UserNo')
    if operator_user_no is None:
        current_app.logger.error("Operator UserNo not available from token, cannot record modification for update.")
        return fail_response_wrap(None, '操作用户ID缺失，无法记录操作', 50001)

    conn = get_db_connection()
    if not conn:
        return fail_response_wrap(None, '数据库连接失败', 50000)

    _set_db_session_user_id(conn, operator_user_no)

    try:
        existing_protocol = ProtocolModel.find_by_no(protocol_no)
        if not existing_protocol:
            return fail_response_wrap(None, f'协议编码 "{protocol_no}" 不存在', 40400)
        
        if ProtocolModel.update(protocol_no, update_fields):
            current_app.logger.info(f"协议信息更新成功: ProtocolNo={protocol_no}")
            return success_response_wrap(None, '协议信息更新成功！')
        else:
            current_app.logger.error(f"协议信息更新失败: ProtocolNo={protocol_no}")
            return fail_response_wrap(None, '协议信息更新失败', 50000)

    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (update_protocol_info): {db_error}", exc_info=True)
        if db_error.errno == 1452:
            return fail_response_wrap(None, '引用的材料编码或账户编号不存在。', 40003)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/protocol/{protocol_no} PUT 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)

@protocol_bp.route('/protocol/<string:protocol_no>', methods=['DELETE'])
@token_required
def delete_protocol(protocol_no):
    # ... (删除逻辑保持不变) ...
    current_app.logger.info(f"Received protocol delete request for ProtocolNo: {protocol_no}")

    operator_user_no = request.user.get('UserNo')
    if operator_user_no is None:
        current_app.logger.error("Operator UserNo not available from token, cannot record modification for delete.")
        return fail_response_wrap(None, '操作用户ID缺失，无法记录操作', 50001)

    conn = get_db_connection()
    if not conn:
        return fail_response_wrap(None, '数据库连接失败', 50000)

    _set_db_session_user_id(conn, operator_user_no)

    try:
        existing_protocol = ProtocolModel.find_by_no(protocol_no)
        if not existing_protocol:
            return fail_response_wrap(None, f'协议编码 "{protocol_no}" 不存在', 40400)
            
        if ProtocolModel.delete(protocol_no):
            current_app.logger.info(f"协议删除成功: ProtocolNo={protocol_no}")
            return success_response_wrap(None, '协议删除成功！')
        else:
            current_app.logger.error(f"协议删除失败: ProtocolNo={protocol_no}")
            return fail_response_wrap(None, '协议删除失败', 50000)

    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (delete_protocol): {db_error}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/protocol/{protocol_no} DELETE 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)

