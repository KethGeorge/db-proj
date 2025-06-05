# Flask_Proj/routes/User.py

from flask import Blueprint, request, current_app
from mysql.connector import Error

# 导入您的工具函数，路径基于 Flask_Proj 根目录
from utils.db import get_db_connection, execute_query
from utils.response import success_response_wrap, fail_response_wrap
from utils.auth import token_required
import string
import random
user_bp = Blueprint('user', __name__)

def generate_random_userno(length=8):
    characters = string.ascii_uppercase + string.digits # 大写字母和数字
    return ''.join(random.choice(characters) for i in range(length))


@user_bp.route('/user', methods=['POST'])
@token_required # 假设用户创建也需要认证，例如由管理员操作
def add_user():
    current_app.logger.info("User creation data received")
    if not request.is_json:
        return fail_response_wrap(None, '请求必须是 JSON 格式', 40000)

    data = request.get_json()
    
    required_fields = ['username', 'password', 'email', 'userPermissions']
    for field in required_fields:
        if field not in data or not data[field]:
            if isinstance(data.get(field), str) and not data.get(field).strip():
                current_app.logger.warning(f'字段 "{field}" 不能为空或仅包含空格')
                return fail_response_wrap(None, f'字段 "{field}" 不能为空', 40001)
            elif data.get(field) is None:
                current_app.logger.warning(f'缺少字段: "{field}"')
                return fail_response_wrap(None, f'缺少字段: "{field}"', 40001)

    username = data.get('username')
    password = data.get('password')  # ！！！保持明文密码处理！！！
    email = data.get('email')
    telephone = data.get('telephone')
    user_permissions = data.get('userPermissions')

    operator = request.user.get('username', 'unknown')

    current_app.logger.info(f"User '{operator}' is creating a new user.")
    current_app.logger.info(f"Received User Data: {data}")

    conn = get_db_connection()
    if not conn:
        return fail_response_wrap(None, '数据库连接失败', 50000)

    userno = None
    for _ in range(10):
        temp_userno = generate_random_userno()
        check_userno_query = "SELECT UserNo FROM users WHERE UserNo = %s"
        existing_userno = execute_query(conn, check_userno_query, (temp_userno,), fetch_one=True)
        if not existing_userno:
            userno = temp_userno
            break
    if userno is None:
        current_app.logger.error("无法生成唯一的 UserNo，请稍后重试。")
        return fail_response_wrap(None, '无法生成唯一的用户编号，请稍后重试。', 50001)
    current_app.logger.info(f"Generated unique UserNo: {userno}")

    try:
        check_user_query = "SELECT UserNo FROM users WHERE UserName = %s"
        existing_user = execute_query(conn, check_user_query, (username,), fetch_one=True)
        if existing_user:
            return fail_response_wrap(None, f'用户名 "{username}" 已存在，请使用其他用户名。', 40003)

        check_email_query = "SELECT UserNo FROM users WHERE Email = %s"
        existing_email = execute_query(conn, check_email_query, (email,), fetch_one=True)
        if existing_email:
            return fail_response_wrap(None, f'邮箱 "{email}" 已被注册，请使用其他邮箱。', 40003)

        insert_query = """
        INSERT INTO users (UserNo, UserName, UserPassword, UserPermissions, Email, Telephone)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        if execute_query(conn, insert_query, (userno, username, password, user_permissions, email, telephone), is_insert=True):
            current_app.logger.info(f"用户信息插入成功: UserName={username}, Email={email}")
            return success_response_wrap({
                'username': username,
                'email': email
            }, '用户信息添加成功！')
        else:
            current_app.logger.error("用户信息插入数据库失败，execute_query 返回 False")
            return fail_response_wrap(None, '用户信息插入数据库失败', 50000)
    except Error as db_error:
        current_app.logger.error(f"数据库操作错误: {db_error}")
        if db_error.errno == 1062:
            return fail_response_wrap(None, f'用户名或邮箱已存在，请检查。', 40003)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/user 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)