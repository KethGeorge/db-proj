# Flask_Proj/routes/UserModify.py

from flask import Blueprint, request, current_app
from mysql.connector import Error

# 导入您的工具函数，路径基于 Flask_Proj 根目录
from utils.db import get_db_connection, execute_query
from utils.response import success_response_wrap, fail_response_wrap
from utils.auth import token_required

# 创建一个新的 Blueprint 用于用户修改操作
user_modify_bp = Blueprint('user_modify', __name__)




@user_modify_bp.route('/users/<string:userno>', methods=['PUT'])
@token_required # 假设用户修改也需要认证，例如由管理员操作
def update_user_info(userno):
    current_app.logger.info(f"Received user info update request for UserNo: {userno}")

    if not request.is_json:
        return fail_response_wrap(None, '请求必须是 JSON 格式', 40000)

    data = request.get_json()

    # 允许修改的字段
    allowed_fields = ['username', 'email', 'telephone', 'userPermissions', 'password'] # 包含 password 以便后续处理
    update_fields = {}
    for field in allowed_fields:
        if field in data:
            update_fields[field] = data[field]

    if not update_fields:
        return fail_response_wrap(None, '没有提供任何要更新的字段', 40000)

    conn = get_db_connection()
    if not conn:
        return fail_response_wrap(None, '数据库连接失败', 50000)

    try:
        # 验证 userno 是否存在
        check_userno_query = "SELECT UserNo FROM users WHERE UserNo = %s"
        existing_user_by_userno = execute_query(conn, check_userno_query, (userno,), fetch_one=True)
        if not existing_user_by_userno:
            return fail_response_wrap(None, f'用户编号 "{userno}" 不存在', 40400)

        # 构建动态 UPDATE SQL 语句
        set_clauses = []
        params = []
        
        # 特别处理密码字段：如果提供了且不为空，则更新
        if 'password' in update_fields and update_fields['password']:
            set_clauses.append("UserPassword = %s")
            params.append(update_fields['password']) # 明文密码

        # 处理其他非密码字段
        for field, value in update_fields.items():
            if field != 'password': # 排除密码，因为它已经单独处理
                set_clauses.append(f"{field.capitalize()} = %s") # 假设数据库字段名是首字母大写
                params.append(value)

        # 如果更新用户名或邮箱，需要检查是否与其他现有用户冲突
        if 'username' in update_fields:
            check_username_query = "SELECT UserNo FROM users WHERE UserName = %s AND UserNo != %s"
            existing_user_by_username = execute_query(conn, check_username_query, (update_fields['username'], userno), fetch_one=True)
            if existing_user_by_username:
                return fail_response_wrap(None, f'用户名 "{update_fields["username"]}" 已存在', 40003)
        if 'email' in update_fields:
            check_email_query = "SELECT UserNo FROM users WHERE Email = %s AND UserNo != %s"
            existing_user_by_email = execute_query(conn, check_email_query, (update_fields['email'], userno), fetch_one=True)
            if existing_user_by_email:
                return fail_response_wrap(None, f'邮箱 "{update_fields["email"]}" 已被注册', 40003)

        if not set_clauses: # 如果除了 userno 没有其他字段要更新
            return success_response_wrap(None, '没有提供任何要更新的字段', 20000) # 也可以返回 40000

        sql_query = f"UPDATE users SET {', '.join(set_clauses)} WHERE UserNo = %s"
        params.append(userno) # WHERE 子句的参数

        if execute_query(conn, sql_query, tuple(params)):
            current_app.logger.info(f"用户信息更新成功: UserNo={userno}")
            return success_response_wrap(None, '用户信息更新成功！')
        else:
            current_app.logger.error(f"用户信息更新失败: UserNo={userno}")
            return fail_response_wrap(None, '用户信息更新失败', 50000)

    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (update_user_info): {db_error}", exc_info=True)
        if db_error.errno == 1062: # Duplicate entry for key
            return fail_response_wrap(None, '用户名或邮箱已存在，请检查。', 40003)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/users/{userno} PUT 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)



### API 2: 更新用户密码 (PUT `/api/users/<userno>/password`)




@user_modify_bp.route('/users/<string:userno>/password', methods=['PUT'])
@token_required # 假设密码修改也需要认证
def update_user_password(userno):
    current_app.logger.info(f"Received password update request for UserNo: {userno}")

    if not request.is_json:
        return fail_response_wrap(None, '请求必须是 JSON 格式', 40000)

    data = request.get_json()
    # current_password = data.get('current_password') # 明文存储，这里不再需要验证旧密码
    new_password = data.get('new_password')     # 用户输入的新密码

    if not new_password:
        return fail_response_wrap(None, '新密码不能为空', 40000)
    if len(new_password) < 6: # 示例：密码长度至少6位
        return fail_response_wrap(None, '新密码长度至少需要6位', 40000)

    conn = get_db_connection()
    if not conn:
        return fail_response_wrap(None, '数据库连接失败', 50000)

    try:
        # 验证 userno 是否存在
        check_userno_query = "SELECT UserNo FROM users WHERE UserNo = %s"
        existing_user_by_userno = execute_query(conn, check_userno_query, (userno,), fetch_one=True)
        if not existing_user_by_userno:
            return fail_response_wrap(None, f'用户编号 "{userno}" 不存在', 40400)

        # 直接更新数据库中的密码（明文存储）
        update_query = "UPDATE users SET UserPassword = %s WHERE UserNo = %s"
        if execute_query(conn, update_query, (new_password, userno)):
            current_app.logger.info(f"用户 '{userno}' 密码修改成功。")
            return success_response_wrap(None, '密码修改成功！')
        else:
            current_app.logger.error(f"用户 '{userno}' 密码更新失败。")
            return fail_response_wrap(None, '密码更新失败', 50000)

    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (update_user_password): {db_error}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/users/{userno}/password PUT 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)