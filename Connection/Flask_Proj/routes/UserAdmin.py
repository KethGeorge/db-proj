# Flask_Proj/routes/User.py

from flask import Blueprint, request, current_app
from mysql.connector import Error

# 导入您的工具函数，路径基于 Flask_Proj 根目录
from utils.db import get_db_connection, execute_query, close_db_connection
from utils.response import success_response_wrap, fail_response_wrap
from utils.auth import token_required
# from utils.helpers import parse_combined_datetime_str # 前端已发送标准格式，后端可直接解析，故不再需要
import string
import random
user_bp = Blueprint('user', __name__)

def generate_random_userno(length=8):
    characters = string.ascii_uppercase + string.digits # 大写字母和数字
    return ''.join(random.choice(characters) for i in range(length))


@user_bp.route('/user', methods=['POST'])
@token_required  # 假设用户创建也需要认证，例如由管理员操作
def add_user():
    current_app.logger.info("User creation data received") # 使用 Flask 的 logger
    if not request.is_json:
        return fail_response_wrap(None, '请求必须是 JSON 格式', 40000)

    data = request.get_json()

    # 验证必填字段，与 Vue 前端表单的必填项对应
    required_fields = ['username', 'password', 'email', 'userPermissions']
    for field in required_fields:
        if field not in data or not data[field]:
            # 对于空字符串也视为缺失
            if isinstance(data.get(field), str) and not data.get(field).strip():
                return fail_response_wrap(None, f'字段 "{field}" 不能为空', 40001)
            elif data.get(field) is None: # 对于非字符串类型，直接检查 None
                return fail_response_wrap(None, f'缺少字段: "{field}"', 40001)


    username = data.get('username')
    password = data.get('password')  # ！！！注意：这里是明文密码，生产环境务必加密！！！
    email = data.get('email')
    telephone = data.get('telephone') # 电话字段，可以为空
    user_permissions = data.get('userPermissions')

    # 注册日期，前端如果禁用则发送 null，否则发送 'YYYY-MM-DDTHH:mm:ss' 格式字符串
    # MySQL 的 DATETIME 类型可以直接处理这种格式，也可以接受 NULL
    # registration_date = data.get('registrationDate')
    # 如果 registration_date 是空字符串，转换为 None，以便数据库处理
    # if registration_date == "":
        # registration_date = None

    # 从 JWT 中获取操作者用户名 (创建此用户的管理员)
    operator = request.user.get('username', 'unknown') # 假设 token_required 装饰器将用户信息添加到 request.user

    current_app.logger.info(f"User '{operator}' is creating a new user.")
    current_app.logger.info(f"Received User Data: {data}")
    # current_app.logger.info(f"Processed Registration Date: {registration_date}")

    conn = get_db_connection()
    if not conn:
        return fail_response_wrap(None, '数据库连接失败', 50000)

    userno = None
    for _ in range(10): # 尝试生成10次，防止冲突，实际冲突概率很低
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
        # 检查用户名是否已存在，防止重复创建
        check_user_query = "SELECT UserNo FROM users WHERE UserName = %s"
        existing_user = execute_query(conn, check_user_query, (username,), fetch_one=True)
        if existing_user:
            return fail_response_wrap(None, f'用户名 "{username}" 已存在，请使用其他用户名。', 40003)

        # 检查邮箱是否已存在（如果邮箱也是唯一索引）
        check_email_query = "SELECT UserNo FROM users WHERE Email = %s"
        existing_email = execute_query(conn, check_email_query, (email,), fetch_one=True)
        if existing_email:
            return fail_response_wrap(None, f'邮箱 "{email}" 已被注册，请使用其他邮箱。', 40003)


        # 插入新用户数据到 users 表
        # 假设您的用户表名为 'users'，字段与图片中的一致
        insert_query = """
        INSERT INTO users (UserNo, UserName, UserPassword, UserPermissions, Email, Telephone)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        # UserNo 通常是 AUTO_INCREMENT，所以不需要在 INSERT 语句中指定
        
        # 将数据按顺序传入，注意顺序与 SQL 语句中的字段顺序一致
        if execute_query(conn, insert_query, (userno, username, password, user_permissions, email, telephone), is_insert=True):
            current_app.logger.info(f"用户信息插入成功: UserName={username}, Email={email}")
            return success_response_wrap({
                'username': username,
                'email': email # 返回一些关键信息给前端
            }, '用户信息添加成功！')
        else:
            current_app.logger.error("用户信息插入数据库失败，execute_query 返回 False")
            return fail_response_wrap(None, '用户信息插入数据库失败', 50000)
    except Error as db_error:
        current_app.logger.error(f"数据库操作错误: {db_error}")
        # MySQL 错误码 1062 表示 Duplicate entry for key
        if db_error.errno == 1062: 
            return fail_response_wrap(None, f'用户名或邮箱已存在，请检查。', 40003)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/user 请求错误: {e}", exc_info=True) # exc_info=True 打印堆栈信息
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)
    finally:
        close_db_connection(conn)