import datetime
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash # 用于密码哈希
import jwt

from utils.db import get_db_connection, execute_query
from utils.response import success_response_wrap, fail_response_wrap
from utils.auth import token_required # 导入认证装饰器

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/user/login', methods=['POST'])
def login():
    if not request.is_json:
        return fail_response_wrap(None, '请求必须是 JSON 格式', 40000)

    data = request.get_json()
    username = data.get('username') # 注意：前端传的是 userName
    password = data.get('password')

    print(f"Received login request for user: {username}")

    if not username or not password:
        return fail_response_wrap(None, '用户名或密码不能为空', 40000)

    conn = get_db_connection()
    if not conn:
        return fail_response_wrap(None, '数据库连接失败', 50000)

    try:
        query = "SELECT UserNo, UserName, UserPassword, UserPermissions FROM users WHERE UserName = %s"
        # execute_query 的 fetch_one 参数控制是获取单个结果还是所有
        user_record = execute_query(conn, query, (username,), fetch_one=True)

        if user_record:
            user_no, db_username, db_password_plain, user_permissions = user_record
    # 直接比较明文密码
            if password == db_password_plain:
        # ... 登录成功逻辑
                # 创建 JWT Payload
                payload = {
                    'UserNo': user_no,
                    'username': db_username,
                    'permissions': user_permissions,
                    'exp': datetime.datetime.now(datetime.timezone.utc) + current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
                }
                token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")

                print(f"用户 '{db_username}' 登录成功，生成的 Token: {token}")
                return success_response_wrap({
                    'token': token,
                    'userInfo': {
                        'name': db_username,
                        'role': user_permissions
                    }
                }, '登录成功')
            else:
                print(f"登录失败：密码错误，用户 {username} 尝试登录。")
                return fail_response_wrap(None, '用户名或密码错误', 40100)
        else:
            return fail_response_wrap(None, '用户不存在', 40100)
    except Exception as e:
        print(f"登录处理错误: {e}")
        return fail_response_wrap(None, '服务器内部错误', 50000)


@auth_bp.route('/user/info', methods=['POST'])
@token_required
def get_user_simple_info():
    conn = get_db_connection()
    if not conn:
        return fail_response_wrap(None, '数据库连接失败', 50000)

    try:
        user_id = request.user.get('UserNo')
        username_from_token = request.user.get('username')
        permissions_from_token = request.user.get('permissions')

        query = """
        SELECT UserName, UserNo, UserPermissions 
        FROM users
        WHERE UserNo = %s
        """
        # execute_query 的 fetch_one 参数控制是获取单个结果还是所有
        result = execute_query(conn, query, (user_id,), fetch_one=True)

        if result: # result 是元组，非空即为真
            # 假设结果对应关系：UserName, UserNo, UserPermissions, Certification
            actual_username, actual_account_id, actual_role = result

            user_info = {
                'name': actual_username,
                'accountId': str(actual_account_id), # 确保是字符串
                'role': actual_role,
            }
            return success_response_wrap(user_info)
        else:
            return fail_response_wrap(None, '用户信息未找到', 40400)
    except Exception as e:
        print(f"获取用户信息错误: {e}")
        return fail_response_wrap(None, '服务器内部错误', 50000)

@auth_bp.route('/user/logout', methods=['POST'])
@token_required
def logout():
    print(f"用户 '{request.user.get('username')}' 已登出。")
    return success_response_wrap(None, '登出成功')

@auth_bp.route('/user/menu', methods=['GET'])
@token_required
def get_user_menu():
    user_permissions = request.user.get('permissions')

    base_menu_list = [
        {
            'path': '/dashboard',
            'name': 'dashboard',
            'meta': {
                'locale': 'menu.server.dashboard',
                'requiresAuth': True,
                'icon': 'icon-dashboard',
                'order': 1,
            },
            'children': [
                {
                    'path': 'workplace',
                    'name': 'Workplace',
                    'meta': {
                        'locale': 'menu.server.workplace',
                        'requiresAuth': True,
                    },
                },
                {
                    'path': 'https://arco.design',
                    'name': 'arcoWebsite',
                    'meta': {
                        'locale': 'menu.arcoWebsite',
                        'requiresAuth': True,
                    },
                },
            ],
        },
    ]

    # 根据权限动态添加菜单，例如，设备管理和国家标准表单
    if user_permissions in ['admin', 'user']: # 假设两者都可以访问设备和国家标准表单
        base_menu_list.append({
            'path': '/national-standard',
            'name': 'nationalStandardParent',
            'meta': {
                'locale': 'menu.nationalStandard',
                'requiresAuth': True,
                'icon': 'icon-file',
                'order': 2,
            },
            'children': [
                {
                    'path': 'create',
                    'name': 'nationalStandardCreate',
                    'meta': {
                        'locale': 'menu.nationalStandard.index',
                        'requiresAuth': True,
                    },
                },
            ],
        })

        base_menu_list.append({
            'path': '/device',
            'name': 'deviceParent',
            'meta': {
                'locale': 'menu.device',
                'requiresAuth': True,
                'icon': 'icon-desktop',
                'order': 3,
            },
            'children': [
                {
                    'path': 'add',
                    'name': 'deviceAdd',
                    'meta': {
                        'locale': 'menu.device.form',
                        'requiresAuth': True,
                    },
                },
            ],
        })


    return success_response_wrap(base_menu_list)