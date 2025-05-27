# ... (现有导入)
import mysql.connector
from mysql.connector import Error
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random # 导入 random 模块
import string # 导入 string 模块，用于生成随机字符串
import jwt # pip install PyJWT
from werkzeug.security import generate_password_hash, check_password_hash # pip install Flask
from functools import wraps
import mysql.connector
from mysql.connector import Error

# 数据库配置
config = {
    "host": "localhost",
    "user": "tumu1t",
    "password": "tumumu1tt",
    "database": "凝胶时间测定"
}

def connect_to_database():
    """连接数据库并返回连接对象"""
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("成功连接到MySQL数据库")
            return connection
    except Error as e:
        print(f"连接错误: {e}")
        return None

def execute_query(connection, query, params=None):
    """执行查询并返回结果"""
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute(query, params or ())

        # 如果是SELECT查询，返回结果
        if query.strip().upper().startswith("SELECT"):
            return cursor.fetchall()
        else:
            connection.commit()
            print("操作成功")
            return True

    except Error as e:
        print(f"查询错误: {e}")
        connection.rollback() # 发生错误时回滚事务
        return False
    finally:
        if cursor:
            cursor.close()

# ... (数据库配置)

app = Flask(__name__)
CORS(app)

def generate_random_string(length):

    if not isinstance(length, int) or length < 0:
        raise ValueError("Length must be a non-negative integer.")

    # 定义所有可能的字符：大小写字母、数字
    characters = string.ascii_letters + string.digits
    
    # 从定义的字符集中随机选择字符，并拼接成字符串
    random_string = ''.join(random.choice(characters) for i in range(length))
    return random_string

# JWT 密钥，生产环境请使用复杂且安全的密钥，并通过环境变量管理
app.config['SECRET_KEY'] = 'your_super_secret_jwt_key_here_for_prod'

# 辅助函数，模拟你的 successResponseWrap 和 failResponseWrap
def success_response_wrap(data=None, message="Success", code=20000): # 调整默认code
    return jsonify({"code": code, "message": message, "data": data})

def fail_response_wrap(data=None, message="Failure", code=50000): # 调整默认code
    return jsonify({"code": code, "message": message, "data": data})

# ----------------- 登录接口 (与你之前前端的登录功能对应) -----------------
@app.route('/api/user/login', methods=['POST'])
def login():
    if not request.is_json:
        return fail_response_wrap(None, 'Request must be JSON', 40000) # 更具体的错误码

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    print(f"Received login request for user: {username}")
    if not username or not password:
        return fail_response_wrap(None, '用户名和密码不能为空', 40000)

    conn = connect_to_database()
    if not conn:
        return fail_response_wrap(None, '数据库连接失败', 50000)

    try:
        # 查询数据库获取用户
        query = "SELECT UserNo, UserName, UserPassword, UserPermissions FROM users WHERE UserName = %s"
        result = execute_query(conn, query, (username,))

        if result and len(result) > 0:
            user_data = result[0] # 获取第一条匹配的用户数据
            db_username = user_data[1]
            db_hashed_password = user_data[2] # 假设 UserPassword 存储的是哈希后的密码
            user_permissions = user_data[3]

            # 校验密码 (这里假设 UserPassword 已经是哈希后的密码)
            # 如果是明文密码，直接比较即可，但强烈不推荐
            # 如果数据库中存储的是明文，可以这样：
            if password == db_hashed_password:
            # 如果数据库中存储的是哈希密码（推荐）：
            # if check_password_hash(db_hashed_password, password): # 需要数据库中存储哈希密码
                # 登录成功，生成 JWT Token
                token_payload = {
                    'user_id': user_data[0], # UserNo
                    'username': db_username,
                    'permissions': user_permissions
                }
                # 设置 token 过期时间，例如 1 小时
                import datetime
                import time
                token_payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm="HS256")
                print(f"用户 '{db_username}' 登录成功，生成的 Token: {token}")
                return success_response_wrap({
                    "token": token,
                    "userRole": user_permissions, # 返回用户角色
                    "username": db_username
                }, '登录成功')
            else:
                print(f"登录失败：密码错误，用户 {username} 尝试登录。")   
                return fail_response_wrap(None, '账号或者密码错误', 50000)
        else:
            return fail_response_wrap(None, '账号不存在', 50000)
    except Exception as e:
        print(f"登录处理错误: {e}")
        return fail_response_wrap(None, '服务器内部错误', 50000)
    finally:
        if conn.is_connected():
            conn.close()
            print("数据库连接已关闭")

# ----------------- JWT 认证装饰器 -----------------
def token_required(f):
    @wraps(f) # 这一行非常重要！
    def decorator(*args, **kwargs):
        token = None
        # 尝试从 Authorization header 中获取 token
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return fail_response_wrap(None, '缺少认证令牌', 40100) # 401 Unauthorized

        try:
            # 验证 token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            # 将用户信息存储在 request.user 中，以便后续路由访问
            request.user = data
        except jwt.ExpiredSignatureError:
            return fail_response_wrap(None, '认证令牌已过期', 40101)
        except jwt.InvalidTokenError:
            return fail_response_wrap(None, '无效的认证令牌', 40102)
        except Exception as e:
            print(f"Token 验证错误: {e}")
            return fail_response_wrap(None, '认证失败', 40103)

        return f(*args, **kwargs) # 继续处理请求
    return decorator

# ----------------- /api/NS 接口应用认证 -----------------
@app.route('/api/NS', methods=['POST'])
@token_required # 应用认证装饰器
def handle_ns_request():
    # 假设只有 'admin' 权限的用户才能创建 NS
    if request.user.get('permissions') != 'admin':
        return fail_response_wrap(None, '权限不足，只有管理员才能添加标准', 40300) # 403 Forbidden

    # ... (原有处理逻辑不变)
    # 1. 检查请求是否为 JSON 格式
    if not request.is_json:
        print("Request is not JSON. Content-Type:", request.headers.get('Content-Type'))
        return fail_response_wrap(None, 'Request must be JSON', 40000)

    # 2. 获取 JSON 数据
    data = request.get_json()

    # 3. 检查 'name' 和 'description' 字段是否存在于 JSON 文档中
    if 'name' not in data:
        return fail_response_wrap(None, 'Missing "name" field in JSON data', 40001)
    if 'description' not in data:
        return fail_response_wrap(None, 'Missing "description" field in JSON data', 40002)
    # 4. 获取 'name' 和 'description' 字段的值
    standard_name_value = data['name']
    description_value = data['description']

    # 5. 生成随机的 NSN 和 MaterialCode
    random_nsn = generate_random_string(10)
    # 修正：你原代码中虽然生成了 random_material_code，但插入数据库时使用了硬编码。
    # 这里根据你的意图，决定是使用生成的还是硬编码的。
    # 如果想使用生成的：
    # final_material_code = str(generate_random_number(10000, 99999))
    # 如果想继续使用硬编码但更清晰：
    final_material_code = 'MAT_MANUAL_001' # 保持与你代码中的一致

    print("--------------------------------------------------")
    print(f"User '{request.user.get('username')}' (Permissions: {request.user.get('permissions')}) is requesting NS creation.")
    print("Received JSON data:")
    print(f"Full request data: {data}")
    print(f"Extracted StandardName value: {standard_name_value}")
    print(f"Extracted Description value: {description_value}")
    print(f"Generated NSN: {random_nsn}")
    print(f"Using MaterialCode: {final_material_code}") # 打印实际使用的 MaterialCode
    print("--------------------------------------------------")

    # 6. 连接数据库
    conn = connect_to_database()
    if not conn:
        return fail_response_wrap(None, 'Database connection failed', 50000)

    try:
        # 7. 准备 SQL 插入语句
        insert_query = """
        INSERT INTO national_standard (NSN, StandardName, Description, MaterialCode)
        VALUES (%s, %s, %s, %s)
        """
        # 8. 执行插入操作，传入所有参数
        if execute_query(conn, insert_query, (random_nsn, standard_name_value, description_value, final_material_code)):
            return success_response_wrap({
                'inserted_standard_name': standard_name_value,
                'inserted_description': description_value,
                'inserted_nsn': random_nsn,
                'inserted_material_code': final_material_code # 返回实际使用的 MaterialCode
            }, 'Standard data inserted successfully!')
        else:
            return fail_response_wrap(None, 'Failed to insert standard data into database', 50000)
    except Exception as e:
        print(f"处理 /api/NS 请求错误: {e}")
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)
    finally:
        # 9. 关闭数据库连接
        if conn.is_connected():
            conn.close()
            print("数据库连接已关闭")

# ----------------- 其他可以添加的 API -----------------
@app.route('/api/standards', methods=['GET'])
@token_required # 保护这个接口
def get_standards():
    conn = connect_to_database()
    if not conn:
        return fail_response_wrap(None, '数据库连接失败', 50000)

    try:
        # 允许所有登录用户查看
        query = "SELECT NSN, StandardName, Description, MaterialCode FROM national_standard LIMIT 100" # 限制返回数量
        standards = execute_query(conn, query)

        if standards is not False: # 检查 execute_query 是否成功
            # 将结果转换为字典列表，方便前端处理
            columns = ['nsn', 'standardName', 'description', 'materialCode']
            standards_list = [dict(zip(columns, row)) for row in standards]
            return success_response_wrap(standards_list, '标准数据获取成功')
        else:
            return fail_response_wrap(None, '获取标准数据失败', 50000)
    except Exception as e:
        print(f"获取标准数据错误: {e}")
        return fail_response_wrap(None, '服务器内部错误', 50000)
    finally:
        if conn.is_connected():
            conn.close()

@app.route('/api/user/logout', methods=['POST'])
@token_required # 登出也应该要求认证，以确保是合法用户在操作
def logout():
    # 后端对于 JWT 登出通常不需要做太多。
    # 客户端会自行清除其本地存储的 token。
    # 如果有 JWT 黑名单机制，可以在这里将 token 加入黑名单。
    # 这里我们只返回成功响应。
    print(f"用户 '{request.user.get('username')}' 已登出。")
    return success_response_wrap(None, '登出成功')

# ----------------- 新增：用户菜单接口 -----------------
@app.route('/api/user/menu', methods=['GET'])
@token_required # 这个接口需要用户认证才能访问
def get_user_menu():
    user_permissions = request.user.get('permissions') # 从 JWT token 中获取用户权限

    # 根据 Mock.js 中的菜单结构定义基础菜单
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
                # 可以根据权限决定是否包含这个外部链接
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
        # 根据权限添加更多菜单项
        # 例如，只有管理员才能访问的“用户管理”或“系统设置”菜单
        # {
        #     'path': '/admin',
        #     'name': 'adminManagement',
        #     'meta': {
        #         'locale': 'menu.admin.management',
        #         'requiresAuth': True,
        #         'icon': 'icon-settings',
        #     },
        #     'children': [
        #         {
        #             'path': 'users',
        #             'name': 'userList',
        #             'meta': {
        #                 'locale': 'menu.admin.users',
        #                 'requiresAuth': True,
        #             },
        #         },
        #     ],
        # }
    ]

    return success_response_wrap(base_menu_list)
@app.route('/api/user/info', methods=['POST']) # <--- 这里改为 POST
@token_required # 保护这个接口，只有认证用户才能访问
def get_user_simple_info():
    conn = connect_to_database()
    if not conn:
        return fail_response_wrap(None, '数据库连接失败', 50000)

    try:
        # 即使是 POST 请求，对于 /info 接口，通常也不期望有重要的请求体数据。
        # 但为了规范性，可以尝试获取，如果不需要则忽略。
        # if request.is_json:
        #    request_data = request.get_json()
        # else:
        #    request_data = {}

        # 从JWT token中获取用户ID和权限
        user_id = request.user.get('user_id')
        username_from_token = request.user.get('username')
        permissions_from_token = request.user.get('permissions') # JWT中的权限，通常是字符串

        # 根据用户ID从数据库查询更多详细信息
        # 假设您的 users 表有 UserName, UserNo, UserPermissions, Certification 等字段
        query = """
        SELECT UserName, UserNo, UserPermissions
        FROM users
        WHERE UserNo = %s
        """
        result = execute_query(conn, query, (user_id,))

        if result and len(result) > 0:
            user_db_data = result[0]
            # 假设结果对应关系：UserName, UserNo, UserPermissions
            actual_username = user_db_data[0]
            actual_account_id = str(user_db_data[1]) # accountId通常是字符串
            actual_role = user_db_data[2] # 从数据库获取的权限

            # 根据前端Mock.js的结构构建响应
            user_info = {
                'name': actual_username, # 使用数据库中的实际用户名
                'accountId': actual_account_id, # 使用数据库中的实际UserNo
                'certification': 1, # Mock.js 中是固定值 1，可以根据实际情况从数据库获取或固定
                'role': actual_role, # 使用数据库中的实际角色
            }
            return success_response_wrap(user_info)
        else:
            # 如果在数据库中没找到用户（理论上不会发生，因为token已验证），返回错误
            return fail_response_wrap(None, '用户信息未找到', 40400)
    except Exception as e:
        print(f"获取用户信息错误: {e}")
        return fail_response_wrap(None, '服务器内部错误', 50000)
    finally:
        if conn and conn.is_connected():
            conn.close()


# ----------------- 错误处理器 -----------------
@app.errorhandler(404)
def not_found_error(error):
    return fail_response_wrap(None, 'API 地址不存在', 40400), 404

@app.errorhandler(500)
def internal_error(error):
    # 捕获所有未被处理的内部服务器错误
    return fail_response_wrap(None, '服务器内部错误', 50000), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)