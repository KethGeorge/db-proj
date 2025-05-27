from flask import Blueprint, request, current_app
from mysql.connector import Error

from utils.db import get_db_connection, execute_query, close_db_connection
from utils.response import success_response_wrap, fail_response_wrap
from utils.auth import token_required
from utils.helpers import parse_combined_datetime_str

device_bp = Blueprint('device', __name__)


@device_bp.route('/device', methods=['POST'])
@token_required # 假设这个接口也需要认证
def add_device():
    print("data received")
    if not request.is_json:
        return fail_response_wrap(None, '请求必须是 JSON 格式', 40000)

    data = request.get_json()
    # 验证必填字段
    required_fields = ['deviceNo', 'deviceName']
    for field in required_fields:
        if field not in data or not data[field]:
            return fail_response_wrap(None, f'缺少或空字段: "{field}"', 40001)

    device_no = data.get('deviceNo')
    device_name = data.get('deviceName')
    device_usage = data.get('deviceUsage')
    # 从 JWT 中获取操作者用户名
    operator = request.user.get('username', 'unknown')

    d_start_time = parse_combined_datetime_str(data.get('dStartTime'))
    d_mt = parse_combined_datetime_str(data.get('dmt'))
    d_stop_time = parse_combined_datetime_str(data.get('dStopTime'))

    print("--------------------------------------------------")
    print(f"User '{operator}' is adding device information.")
    print(f"Received Device Data: {data}")
    print(f"Parsed Dates: Start={d_start_time}, MT={d_mt}, Stop={d_stop_time}")
    print("--------------------------------------------------")

    conn = get_db_connection()
    if not conn:
        return fail_response_wrap(None, '数据库连接失败', 50000)

    try:
        insert_query = """
        INSERT INTO devices (DeviceNo, DeviceName, DeviceUsage, DStartTime, DMT, DStopTime, Operator)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        if execute_query(conn, insert_query, (device_no, device_name, device_usage, d_start_time, d_mt, d_stop_time, operator), is_insert=True):
            print("设备信息插入成功")
            print(f"Inserted DeviceNo: {device_no}, DeviceName: {device_name}")
            return success_response_wrap({
                'deviceNo': device_no,
                'deviceName': device_name
            }, '设备信息添加成功！')
        else:
            return fail_response_wrap(None, '设备信息插入数据库失败', 50000)
    except Error as db_error:
        print(f"数据库操作错误: {db_error}")
        if db_error.errno == 1062: # MySQL 错误码 1062 表示 Duplicate entry for key 'PRIMARY'
            return fail_response_wrap(None, f'设备编号 "{device_no}" 已存在，请使用其他编号。', 40003)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        print(f"处理 /api/device 请求错误: {e}")
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)
    finally:
        close_db_connection(conn)