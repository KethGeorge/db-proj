from flask import Blueprint, request, current_app
from mysql.connector import Error

from utils.db import get_db_connection, execute_query, close_db_connection
from utils.response import success_response_wrap, fail_response_wrap
from utils.auth import token_required
from utils.helpers import generate_random_string

ns_bp = Blueprint('ns', __name__)



@ns_bp.route('/NS', methods=['POST'])
@token_required
def handle_ns_request():
    # 定义文件名
    # 假设只有 'admin' 权限的用户才能创建 NS
    # if request.user.get('permissions') != 'admin':
        # return fail_response_wrap(None, '权限不足，只有管理员才能添加标准', 40300)

    if not request.is_json:
        print("Request is not JSON. Content-Type:", request.headers.get('Content-Type'))
        return fail_response_wrap(None, 'Request must be JSON', 40000)

    data = request.get_json()
    if 'name' not in data or not data['name']:
        return fail_response_wrap(None, '缺少或空字段: "name"', 40001)
    if 'description' not in data or not data['description']:
        return fail_response_wrap(None, '缺少或空字段: "description"', 40002)

    standard_name_value = data['name']
    description_value = data['description']

    random_nsn = generate_random_string(10)
    final_material_code = 'MAT_MANUAL_001' # 保持与你代码中的一致

    print("--------------------------------------------------")
    print(f"User '{request.user.get('username')}' (Permissions: {request.user.get('permissions')}) is requesting NS creation.")
    print("Received JSON data:")
    print(f"Full request data: {data}")
    print(f"Extracted StandardName value: {standard_name_value}")
    print(f"Extracted Description value: {description_value}")
    print(f"Generated NSN: {random_nsn}")
    print(f"Using MaterialCode: {final_material_code}")
    print("--------------------------------------------------")

    conn = get_db_connection()
    if not conn:
        return fail_response_wrap(None, '数据库连接失败', 50000)

    try:
        insert_query = """
        INSERT INTO national_standard (NSN, StandardName, Description, MaterialCode)
        VALUES (%s, %s, %s, %s)
        """
        if execute_query(conn, insert_query, (random_nsn, standard_name_value, description_value, final_material_code), is_insert=True):
            return success_response_wrap({
                'inserted_standard_name': standard_name_value,
                'inserted_description': description_value,
                'inserted_nsn': random_nsn,
                'inserted_material_code': final_material_code
            }, 'Standard data inserted successfully!')
        else:
            return fail_response_wrap(None, 'Failed to insert standard data into database', 50000)
    except Error as db_error:
        print(f"数据库操作错误: {db_error}")
        if db_error.errno == 1062: # MySQL 错误码 1062 表示 Duplicate entry for key 'PRIMARY'
            return fail_response_wrap(None, f'标准编号 "{random_nsn}" 或其他唯一键已存在。', 40003)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        print(f"处理 /api/NS 请求错误: {e}")
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)
    finally:
        close_db_connection(conn)
