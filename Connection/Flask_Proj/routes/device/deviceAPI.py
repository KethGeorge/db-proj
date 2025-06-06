# backend/routes/device_api.py

from flask import Blueprint, request, current_app
from mysql.connector import Error
from datetime import datetime

from utils.response import success_response_wrap, fail_response_wrap
from utils.auth import token_required
from routes.device.device import DeviceModel # 导入设备模型
from utils.db import get_db_connection, execute_query # 用于设置会话变量

device_bp = Blueprint('device_api', __name__)

def _set_db_session_user_id(conn, user_id):
    if user_id is not None:
        try:
            execute_query(conn, "SET @current_user_id = %s;", (user_id,), fetch_one=False, fetch_all=False, is_insert=False)
            current_app.logger.debug(f"MySQL session variable @current_user_id set to {user_id} for current operation.")
        except Exception as e:
            current_app.logger.error(f"Failed to set @current_user_id to {user_id}: {e}", exc_info=True)
            raise

@device_bp.route('/device', methods=['POST']) # <-- POST 请求路径为 /api/device
@token_required
def add_device():
    current_app.logger.info("Device creation data received")
    if not request.is_json:
        return fail_response_wrap(None, '请求必须是 JSON 格式', 40000)

    data = request.get_json()
    
    required_fields = ['DeviceNo', 'DeviceName']
    for field in required_fields:
        if field not in data or not data[field] or (isinstance(data[field], str) and not data[field].strip()):
            current_app.logger.warning(f'字段 "{field}" 不能为空或仅包含空格')
            return fail_response_wrap(None, f'字段 "{field}" 不能为空', 40001)

    device_no = data.get('DeviceNo')
    device_name = data.get('DeviceName')
    device_usage = data.get('DeviceUsage')
    d_start_time = data.get('DStartTime')
    dmt = data.get('DMT')
    d_stop_time = data.get('DStopTime')
    # Operator 字段不再从请求中获取，因为不插入
    # operator = data.get('Operator')
    
    # 将空字符串转换为None，以便数据库能正确存储NULL
    if isinstance(device_usage, str) and not device_usage.strip(): device_usage = None
    if isinstance(d_start_time, str) and not d_start_time.strip(): d_start_time = None
    if isinstance(dmt, str) and not dmt.strip(): dmt = None
    if isinstance(d_stop_time, str) and not d_stop_time.strip(): d_stop_time = None
    # Operator 字段不再处理
    # if isinstance(operator, str) and not operator.strip(): operator = None

    # 日期时间字符串转换为 datetime 对象或保持 None
    try:
        if d_start_time: d_start_time = datetime.fromisoformat(d_start_time)
        if dmt: dmt = datetime.fromisoformat(dmt)
        if d_stop_time: d_stop_time = datetime.fromisoformat(d_stop_time)
    except ValueError as e:
        current_app.logger.warning(f"日期时间格式错误: {e}")
        return fail_response_wrap(None, f'日期时间格式不正确: {e}', 40002)

    # 构造要传递给模型的完整数据
    device_data_to_create = {
        'DeviceNo': device_no,
        'DeviceName': device_name,
        'DeviceUsage': device_usage,
        'DStartTime': d_start_time,
        'DMT': dmt,
        'DStopTime': d_stop_time,
        # 'Operator': operator # Operator 字段不再包含在创建数据中
    }

    user_no = request.user.get('UserNo')
    if user_no is None:
        current_app.logger.error("UserNo not available from token, cannot record modification.")
        return fail_response_wrap(None, '用户ID缺失，无法记录操作', 50001)

    conn = get_db_connection()
    if not conn:
        return fail_response_wrap(None, '数据库连接失败', 50000)

    try:
        _set_db_session_user_id(conn, user_no)

        existing_device_by_no = DeviceModel.find_by_no(device_no)
        if existing_device_by_no:
            return fail_response_wrap(None, f'设备编号 "{device_no}" 已存在，请使用其他编号。', 40003)

        existing_device_by_name = DeviceModel.find_by_name(device_name)
        if existing_device_by_name:
             return fail_response_wrap(None, f'设备名称 "{device_name}" 已存在，请使用其他名称。', 40003)

        if DeviceModel.create(device_data_to_create):
            current_app.logger.info(f"设备信息插入成功: DeviceNo={device_no}, DeviceName={device_name}")
            return success_response_wrap({
                'DeviceNo': device_no,
                'DeviceName': device_name
            }, '设备信息添加成功！')
        else:
            current_app.logger.error("设备信息插入数据库失败，模型返回 False")
            return fail_response_wrap(None, '设备信息插入数据库失败', 50000)
    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (add_device): {db_error}")
        if db_error.errno == 1062:
            return fail_response_wrap(None, f'设备编号或设备名称已存在，请检查。', 40003)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except ValueError as val_error:
        current_app.logger.warning(f"请求数据校验失败: {val_error}")
        return fail_response_wrap(None, str(val_error), 40001)
    except Exception as e:
        current_app.logger.error(f"处理 /api/device POST 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)

@device_bp.route('/device', methods=['GET']) # <-- GET 列表请求路径为 /api/device
@token_required
def get_devices():
    current_app.logger.info("Received request for device list.")
    
    device_no = request.args.get('DeviceNo')
    device_name = request.args.get('DeviceName')
    device_usage = request.args.get('DeviceUsage')
    
    try:
        current = int(request.args.get('current', 1))
        page_size = int(request.args.get('pageSize', 20))
    except ValueError:
        return fail_response_wrap(None, '分页参数格式不正确', 40004)

    filters = {
        'DeviceNo': device_no,
        'DeviceName': device_name,
        'DeviceUsage': device_usage,
    }

    try:
        devices_list, total_count = DeviceModel.get_paginated_list(filters, current, page_size)
        
        current_app.logger.info(f"Total devices found: {total_count}")

        return success_response_wrap({
            'list': devices_list,
            'total': total_count
        }, '设备列表获取成功')

    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (get_devices): {db_error}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/device GET 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)


@device_bp.route('/device/<string:device_no>', methods=['GET']) # <-- GET 详情请求路径为 /api/device/{id}
@token_required
def get_device_detail(device_no):
    current_app.logger.info(f"Received request for device detail: {device_no}")

    try:
        device_detail = DeviceModel.find_by_no(device_no)

        if not device_detail:
            return fail_response_wrap(None, '设备不存在', 40400)

        return success_response_wrap(device_detail, '设备详情获取成功')

    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (get_device_detail): {db_error}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/device/<device_no> GET 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)


@device_bp.route('/device/<string:device_no>', methods=['PUT']) # <-- PUT 请求路径为 /api/device/{id}
@token_required
def update_device_info(device_no):
    current_app.logger.info(f"Received device info update request for DeviceNo: {device_no}")

    if not request.is_json:
        return fail_response_wrap(None, '请求必须是 JSON 格式', 40000)

    data = request.get_json()

    # 所有可更新的字段列表，包括 Operator (如果存在且要处理)
    # 假设前端只发送 DeviceName, DeviceUsage, DStartTime, DMT, DStopTime
    # 而 Operator 是一个特殊情况，这里不从前端获取
    allowed_fields = ["DeviceName", "DeviceUsage"] # 非日期时间字段

    update_fields = {}
    for field in allowed_fields:
        if field in data:
            # 对于字符串字段，如果传过来是空字符串，也统一转为 None
            if isinstance(data[field], str) and not data[field].strip():
                update_fields[field] = None
            else:
                update_fields[field] = data[field]
        # else: 如果字段不在data中，保持不更新（除非是日期时间字段，我们希望将其设为NULL）
        # 对于非日期时间字段，如果前端不传，就让数据库保持原值，不设为NULL

    # --- 关键修改：处理日期时间字段 ---
    datetime_fields = ["DStartTime", "DMT", "DStopTime"]
    for key in datetime_fields:
        if key in data: # 如果前端发送了这个字段 (即使是null或空字符串)
            value = data[key]
            if isinstance(value, str) and not value.strip(): # 空字符串转为 None
                update_fields[key] = None
            elif isinstance(value, str): # 有内容的字符串尝试转换为 datetime
                try:
                    update_fields[key] = datetime.fromisoformat(value)
                except ValueError as e:
                    current_app.logger.warning(f"日期时间格式错误 for {key}: {e}")
                    return fail_response_wrap(None, f'日期时间格式不正确 ({key}): {e}', 40002)
            elif value is None: # 如果前端明确发送了 null
                update_fields[key] = None
        else:
            # <--- 关键！如果字段不在请求数据中，则显式将其设置为 None (对应数据库的 NULL)
            update_fields[key] = None
    # ----------------------------------

    if not update_fields:
        return success_response_wrap(None, '没有提供任何要更新的字段', 20000)

    user_no = request.user.get('UserNo')
    if user_no is None:
        current_app.logger.error("UserNo not available from token, cannot record modification for update.")
        return fail_response_wrap(None, '用户ID缺失，无法记录操作', 50001)

    conn = get_db_connection()
    if not conn:
        return fail_response_wrap(None, '数据库连接失败', 50000)

    _set_db_session_user_id(conn, user_no)

    try:
        existing_device = DeviceModel.find_by_no(device_no)
        if not existing_device:
            return fail_response_wrap(None, f'设备编号 "{device_no}" 不存在', 40400)

        if 'DeviceName' in update_fields: # 这里的 DeviceName 已经在上面处理过了，确保不再重复处理
            original_device_name = existing_device.get('DeviceName')
            new_device_name = update_fields['DeviceName']

            if new_device_name != original_device_name:
                current_app.logger.debug(f"DeviceName is being changed from '{original_device_name}' to '{new_device_name}'. Checking for duplicates...")
                
                existing_device_by_name_elsewhere = DeviceModel.find_by_name(new_device_name, exclude_no=device_no)
                if existing_device_by_name_elsewhere:
                    return fail_response_wrap(None, f'设备名称 "{new_device_name}" 已存在，请使用其他名称。', 40003)
            else:
                current_app.logger.debug(f"DeviceName in update_fields is the same as the original. Skipping duplicate check for DeviceName.")
        
        # 再次检查 update_fields 是否包含要更新的字段，因为上面可能已经处理过了
        # 如果经过上述处理后 update_fields 仍然为空，说明没有有效字段需要更新
        if not update_fields: # 再次检查 update_fields 是否为空
            return success_response_wrap(None, '没有提供任何要更新的字段', 20000)

        if DeviceModel.update(device_no, update_fields):
            current_app.logger.info(f"设备信息更新成功: DeviceNo={device_no}")
            return success_response_wrap(None, '设备信息更新成功！')
        else:
            current_app.logger.error(f"设备信息更新失败: DeviceNo={device_no}")
            return fail_response_wrap(None, '设备信息更新失败', 50000)

    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (update_device_info): {db_error}", exc_info=True)
        if db_error.errno == 1062:
            return fail_response_wrap(None, '设备名称已存在，请检查。', 40003)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/device/{device_no} PUT 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)

@device_bp.route('/device/<string:device_no>', methods=['DELETE']) # <-- DELETE 请求路径为 /api/device/{id}
@token_required
def delete_device(device_no):
    current_app.logger.info(f"Received device delete request for DeviceNo: {device_no}")

    user_no = request.user.get('UserNo')
    if user_no is None:
        current_app.logger.error("UserNo not available from token, cannot record modification for delete.")
        return fail_response_wrap(None, '用户ID缺失，无法记录操作', 50001)

    conn = get_db_connection()
    if not conn:
        return fail_response_wrap(None, '数据库连接失败', 50000)

    _set_db_session_user_id(conn, user_no)

    try:
        existing_device = DeviceModel.find_by_no(device_no)
        if not existing_device:
            return fail_response_wrap(None, f'设备编号 "{device_no}" 不存在', 40400)
            
        if DeviceModel.delete(device_no):
            current_app.logger.info(f"设备删除成功: DeviceNo={device_no}")
            return success_response_wrap(None, '设备删除成功！')
        else:
            current_app.logger.error(f"设备删除失败: DeviceNo={device_no}")
            return fail_response_wrap(None, '设备删除失败', 50000)

    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (delete_device): {db_error}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/device/{device_no} DELETE 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)