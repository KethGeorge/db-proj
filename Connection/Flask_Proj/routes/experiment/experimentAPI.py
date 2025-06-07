# backend/routes/experiment_api.py

from flask import Blueprint, request, current_app
from mysql.connector import Error
from datetime import datetime, time, timedelta

from utils.response import success_response_wrap, fail_response_wrap
from utils.auth import token_required
from routes.experiment.experiment import ExperimentModel
from utils.db import get_db_connection, execute_query

experiment_bp = Blueprint('experiment_api', __name__)

def _set_db_session_user_id(conn, user_id):
    if user_id is not None:
        try:
            execute_query(conn, "SET @current_user_id = %s;", (user_id,), fetch_one=False, fetch_all=False, is_insert=False)
            current_app.logger.debug(f"MySQL session variable @current_user_id set to {user_id} for current operation.")
        except Exception as e:
            current_app.logger.error(f"Failed to set @current_user_id to {user_id}: {e}", exc_info=True)
            raise

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
    elif isinstance(value, str) and not value.strip():
        return None
    current_app.logger.warning(f"字段 '{field_name}' 接收到非预期类型：{type(value).__name__}，值：'{value}'")
    return None

def _parse_time_or_none(value, field_name):
    if value is None:
        return None
    if isinstance(value, time):
        return value
    if isinstance(value, str) and value.strip():
        try:
            return time.fromisoformat(value)
        except ValueError:
            current_app.logger.warning(f"字段 '{field_name}' 必须是有效时间格式 (HH:MM:SS)，但接收到非时间字符串：'{value}'")
            raise ValueError(f"字段 '{field_name}' 必须是有效时间格式 (HH:MM:SS)")
    elif isinstance(value, str) and not value.strip():
        return None
    current_app.logger.warning(f"字段 '{field_name}' 接收到非预期类型：{type(value).__name__}，值：'{value}'")
    return None


@experiment_bp.route('/experiment', methods=['POST'])
@token_required
def add_experiment():
    current_app.logger.info("Experiment creation data received")
    if not request.is_json:
        return fail_response_wrap(None, '请求必须是 JSON 格式', 40000)

    data = request.get_json()
    
    required_fields = ['ExperimentNo', 'UserNo']
    for field in required_fields:
        if field not in data or not data[field] or (isinstance(data[field], str) and not data[field].strip()):
            current_app.logger.warning(f'字段 "{field}" 不能为空或仅包含空格')
            return fail_response_wrap(None, f'字段 "{field}" 不能为空', 40001)

    experiment_no = data.get('ExperimentNo')
    material_code = data.get('MaterialCode') if data.get('MaterialCode') else None
    protocol_no = data.get('ProtocolNo') if data.get('ProtocolNo') else None
    user_no = data.get('UserNo')

    try:
        heat_error = _parse_float_or_none(data.get('HeatError'), 'HeatError')
        mix_error = _parse_float_or_none(data.get('MixError'), 'MixError')
        start_time = _parse_time_or_none(data.get('StartTime'), 'StartTime')
        end_time = _parse_time_or_none(data.get('EndTime'), 'EndTime')
    except ValueError as e:
        return fail_response_wrap(None, str(e), 40005)

    # GelTime 不再存入数据库，仅在需要时计算用于前端显示或日志
    # 这里不需要计算gel_time，因为数据库中没有该列
    
    experiment_data_to_create = {
        'ExperimentNo': experiment_no,
        'MaterialCode': material_code,
        'HeatError': heat_error,
        'MixError': mix_error,
        'StartTime': start_time,
        'EndTime': end_time,
        'ProtocolNo': protocol_no,
        'UserNo': user_no
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

        existing_experiment_by_no = ExperimentModel.find_by_no(experiment_no)
        if existing_experiment_by_no:
            return fail_response_wrap(None, f'实验编号 "{experiment_no}" 已存在，请使用其他编号。', 40003)

        if ExperimentModel.create(experiment_data_to_create):
            current_app.logger.info(f"实验信息插入成功: ExperimentNo={experiment_no}")
            return success_response_wrap({
                'ExperimentNo': experiment_no,
                'UserNo': user_no
            }, '实验信息添加成功！')
        else:
            current_app.logger.error("实验信息插入数据库失败，模型返回 False")
            return fail_response_wrap(None, '实验信息插入数据库失败', 50000)
    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (add_experiment): {db_error}", exc_info=True)
        if db_error.errno == 1062:
            return fail_response_wrap(None, f'实验编号已存在。', 40003)
        if db_error.errno == 1452:
            return fail_response_wrap(None, '引用的材料编码、策略编码或账户编号不存在。', 40003)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except ValueError as val_error:
        current_app.logger.warning(f"请求数据校验失败: {val_error}")
        return fail_response_wrap(None, str(val_error), 40001)
    except Exception as e:
        current_app.logger.error(f"处理 /api/experiment POST 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)

@experiment_bp.route('/experiment', methods=['GET']) # 列表查询路径
@token_required
def get_experiments():
    current_app.logger.info("Received request for experiment list.")
    
    experiment_no = request.args.get('ExperimentNo')
    material_code = request.args.get('MaterialCode')
    protocol_no = request.args.get('ProtocolNo')
    user_no_filter = request.args.get('UserNo')

    try:
        current = int(request.args.get('current', 1))
        page_size = int(request.args.get('pageSize', 20))
    except ValueError:
        return fail_response_wrap(None, '分页参数格式不正确', 40004)

    filters = {
        'ExperimentNo': experiment_no,
        'MaterialCode': material_code,
        'ProtocolNo': protocol_no,
        'UserNo': user_no_filter,
    }

    try:
        protocols_list, total_count = ExperimentModel.get_paginated_list(filters, current, page_size)
        
        current_app.logger.info(f"Total experiments found: {total_count}")
        current_app.logger.debug(f"Filtered experiments: {protocols_list}")

        return success_response_wrap({
            'list': protocols_list,
            'total': total_count
        }, '实验列表获取成功')

    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (get_experiments): {db_error}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/experiments GET 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)


@experiment_bp.route('/experiment/<string:experiment_no>', methods=['GET'])
@token_required
def get_experiment_detail(experiment_no):
    current_app.logger.info(f"Received request for experiment detail: {experiment_no}")

    try:
        experiment_detail = ExperimentModel.find_by_no(experiment_no)

        if not experiment_detail:
            return fail_response_wrap(None, '实验不存在', 40400)

        return success_response_wrap(experiment_detail, '实验详情获取成功')

    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (get_experiment_detail): {db_error}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/experiment/<experiment_no> GET 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)


@experiment_bp.route('/experiment/<string:experiment_no>', methods=['PUT'])
@token_required
def update_experiment_info(experiment_no):
    current_app.logger.info(f"Received experiment info update request for ExperimentNo: {experiment_no}")

    if not request.is_json:
        return fail_response_wrap(None, '请求必须是 JSON 格式', 40000)

    data = request.get_json()

    update_fields = {}

    # 处理字符串字段
    string_fields = ["MaterialCode", "ProtocolNo", "UserNo"]
    for field in string_fields:
        if field in data:
            value = data[field]
            if isinstance(value, str) and not value.strip():
                update_fields[field] = None
            else:
                update_fields[field] = value
        else: # 如果前端没有发送，则显式设置为 None
            update_fields[field] = None

    # 处理浮点数字段
    float_fields = ["HeatError", "MixError"]
    for field in float_fields:
        if field in data:
            try:
                update_fields[field] = _parse_float_or_none(data[field], field)
            except ValueError as e:
                return fail_response_wrap(None, str(e), 40005)
        else: # 如果前端没有发送，则显式设置为 None
            update_fields[field] = None

    # 处理时间字段
    time_fields = ["StartTime", "EndTime"]
    # GelTime 不再直接从请求中获取或更新
    start_time_new = None
    end_time_new = None
    for field in time_fields:
        if field in data:
            try:
                parsed_time = _parse_time_or_none(data[field], field)
                update_fields[field] = parsed_time
                if field == "StartTime":
                    start_time_new = parsed_time
                elif field == "EndTime":
                    end_time_new = parsed_time
            except ValueError as e:
                return fail_response_wrap(None, str(e), 40005) # 时间格式错误
        else: # 如果前端没有发送，则显式设置为 None
            update_fields[field] = None

    # GelTime 不再后端计算并存储
    # 如果需要 GelTime，可以在前端列表或详情页的 computed property 中计算
    # 或者，如果后端需要日志/其他用途，可以根据 StartTime/EndTime 计算后用于内部逻辑

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
        existing_experiment = ExperimentModel.find_by_no(experiment_no)
        if not existing_experiment:
            return fail_response_wrap(None, f'实验编号 "{experiment_no}" 不存在', 40400)
        
        if ExperimentModel.update(experiment_no, update_fields):
            current_app.logger.info(f"实验信息更新成功: ExperimentNo={experiment_no}")
            return success_response_wrap(None, '实验信息更新成功！')
        else:
            current_app.logger.error(f"实验信息更新失败: ExperimentNo={experiment_no}")
            return fail_response_wrap(None, '实验信息更新失败', 50000)

    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (update_experiment_info): {db_error}", exc_info=True)
        if db_error.errno == 1452:
            return fail_response_wrap(None, '引用的材料编码、策略编码或账户编号不存在。', 40003)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/experiment/{experiment_no} PUT 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)

@experiment_bp.route('/experiment/<string:experiment_no>', methods=['DELETE'])
@token_required
def delete_experiment(experiment_no):
    current_app.logger.info(f"Received experiment delete request for ExperimentNo: {experiment_no}")

    operator_user_no = request.user.get('UserNo')
    if operator_user_no is None:
        current_app.logger.error("Operator UserNo not available from token, cannot record modification for delete.")
        return fail_response_wrap(None, '操作用户ID缺失，无法记录操作', 50001)

    conn = get_db_connection()
    if not conn:
        return fail_response_wrap(None, '数据库连接失败', 50000)

    _set_db_session_user_id(conn, operator_user_no)

    try:
        existing_experiment = ExperimentModel.find_by_no(experiment_no)
        if not existing_experiment:
            return fail_response_wrap(None, f'实验编号 "{experiment_no}" 不存在', 40400)
            
        if ExperimentModel.delete(experiment_no):
            current_app.logger.info(f"实验删除成功: ExperimentNo={experiment_no}")
            return success_response_wrap(None, '实验删除成功！')
        else:
            current_app.logger.error(f"实验删除失败: ExperimentNo={experiment_no}")
            return fail_response_wrap(None, '实验删除失败', 50000)

    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (delete_experiment): {db_error}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/experiment/{experiment_no} DELETE 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)