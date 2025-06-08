# backend/routes/Users/user_api.py

from flask import Blueprint, request, current_app
from mysql.connector import Error
# from werkzeug.security import generate_password_hash # 密码明文存储，不再需要哈希
import string
import random

from utils.response import success_response_wrap, fail_response_wrap
from utils.auth import token_required
from routes.userAdmin.userAdmin import UserModel # 导入用户模型
from utils.db import get_db_connection, execute_query # 用于设置会话变量

user_admin_bp = Blueprint('user_admin_api', __name__)

def _set_db_session_user_id(conn, user_id):
    if user_id is not None:
        try:
            execute_query(conn, "SET @current_user_id = %s;", (user_id,), fetch_one=False, fetch_all=False, is_insert=False)
            current_app.logger.debug(f"MySQL session variable @current_user_id set to {user_id} for current operation.")
        except Exception as e:
            current_app.logger.error(f"Failed to set @current_user_id to {user_id}: {e}", exc_info=True)
            raise

# --- API for User Creation (POST /api/user) ---
@user_admin_bp.route('/user', methods=['POST'])
@token_required # 假设创建用户需要认证，例如由管理员操作
# @has_role(['admin']) # 可选：只有admin才能创建
def add_user():
    current_app.logger.info("User creation request received")
    if not request.is_json:
        return fail_response_wrap(None, '请求必须是 JSON 格式', 40000)

    data = request.get_json()
    
    # 必填字段校验
    required_fields_check = ['UserName', 'UserPassword', 'Email'] 
    for field in required_fields_check:
        if field not in data or not data[field]:
            if isinstance(data.get(field), str) and not data.get(field).strip():
                current_app.logger.warning(f'字段 "{field}" 不能为空或仅包含空格')
                return fail_response_wrap(None, f'字段 "{field}" 不能为空', 40001)
            elif data.get(field) is None:
                current_app.logger.warning(f'缺少字段: "{field}"')
                return fail_response_wrap(None, f'缺少字段: "{field}"', 40001)

    username = data.get('UserName')
    password = data.get('UserPassword') # 明文密码
    email = data.get('Email')

    # 密码长度校验
    if len(password) < 6:
        return fail_response_wrap(None, '密码不能少于6位', 40002)
    if len(password) > 20: # char(20)
        return fail_response_wrap(None, '密码长度不能超过20位', 40002)


    # 可选字段处理 (确保空字符串转为None)
    user_permissions = data.get('UserPermissions')
    if isinstance(user_permissions, str) and not user_permissions.strip(): user_permissions = None
    if user_permissions and len(user_permissions) > 5: # char(5)
        return fail_response_wrap(None, '账户权限长度不能超过5位', 40002)

    telephone = data.get('Telephone')
    if isinstance(telephone, str) and not telephone.strip(): telephone = None
    if telephone and len(telephone) > 13: # char(13)
        return fail_response_wrap(None, '电话长度不能超过13位', 40002)


    operator_user_no = request.user.get('UserNo')
    if operator_user_no is None:
        current_app.logger.error("Operator UserNo not available from token, cannot record modification.")
        return fail_response_wrap(None, '操作用户ID缺失，无法记录操作', 50001)

    conn = get_db_connection()
    if not conn:
        return fail_response_wrap(None, '数据库连接失败', 50000)

    try:
        _set_db_session_user_id(conn, operator_user_no)

        # 检查UserName和Email的唯一性
        if UserModel.check_username_exists(username):
            return fail_response_wrap(None, f'用户名 "{username}" 已存在，请使用其他用户名。', 40003)
        if UserModel.check_email_exists(email):
            return fail_response_wrap(None, f'邮箱 "{email}" 已被注册，请使用其他邮箱。', 40003)

        # UserNo：如果数据库是 CHAR(8) 且非自增，则需要在这里生成
        userno = data.get('UserNo') # 优先使用前端提供的 UserNo
        if not userno:
            try:
                userno = UserModel._generate_unique_userno() # 后端生成唯一的UserNo
            except ValueError as e:
                return fail_response_wrap(None, str(e), 50001)
        else:
            if len(userno) > 8: # char(8)
                return fail_response_wrap(None, '账户编号长度不能超过8位', 40002)
            # 如果前端提供了 UserNo，检查其唯一性
            if UserModel.get_user_by_userno(userno):
                return fail_response_wrap(None, f'用户编号 "{userno}" 已存在，请使用其他编号。', 40003)


        user_data_to_create = {
            'UserNo': userno,
            'UserName': username,
            'UserPassword': password, # 明文密码
            'UserPermissions': user_permissions,
            'Email': email,
            'Telephone': telephone,
        }

        success, actual_userno = UserModel.create_user(user_data_to_create)
        if success:
            current_app.logger.info(f"用户信息插入成功: UserName={username}, UserNo={actual_userno}")
            return success_response_wrap({
                'UserNo': actual_userno,
                'UserName': username,
                'Email': email
            }, '用户信息添加成功！')
        else:
            current_app.logger.error("用户信息插入数据库失败，模型返回 False")
            return fail_response_wrap(None, '用户信息插入数据库失败', 50000)
    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (add_user): {db_error}", exc_info=True)
        if db_error.errno == 1062:
            return fail_response_wrap(None, '用户名、邮箱或用户编号已存在，请检查。', 40003)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/user POST 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)


# --- API for User List & Detail (GET /api/users, GET /api/users/<userno>) ---
@user_admin_bp.route('/users', methods=['GET'])
@token_required
def get_users():
    current_app.logger.info("Received request for user list.")
    
    filters = {
        'UserNo': request.args.get('UserNo'),
        'UserName': request.args.get('UserName'),
        'Email': request.args.get('Email'),
        'UserPermissions': request.args.get('UserPermissions'),
        'Telephone': request.args.get('Telephone'),
    }
    filters = {k: v for k, v in filters.items() if v is not None and v != ''}

    try:
        current = int(request.args.get('current', 1))
        page_size = int(request.args.get('pageSize', 20))
    except ValueError:
        return fail_response_wrap(None, '分页参数格式不正确', 40004)

    try:
        users_list, total_count = UserModel.get_paginated_list(filters, current, page_size)
        
        current_app.logger.info(f"Total users found: {total_count}")

        return success_response_wrap({
            'list': users_list,
            'total': total_count
        }, '用户列表获取成功')

    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (get_users): {db_error}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/users GET 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)

@user_admin_bp.route('/users/<string:userno>', methods=['GET'])
@token_required
def get_user_detail(userno):
    current_app.logger.info(f"Received request for user detail: {userno}")

    try:
        user_detail = UserModel.get_user_by_userno(userno)

        if not user_detail:
            return fail_response_wrap(None, '用户不存在', 40400)

        return success_response_wrap(user_detail, '用户详情获取成功')

    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (get_user_detail): {db_error}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/users/<userno> GET 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)


# --- API for User Update (PUT /api/users/<userno>) ---
@user_admin_bp.route('/users/<string:userno>', methods=['PUT'])
@token_required
# @has_role(['admin']) # 可选：只有admin才能修改
def update_user_info(userno):
    current_app.logger.info(f"Received user info update request for UserNo: {userno}")

    if not request.is_json:
        return fail_response_wrap(None, '请求必须是 JSON 格式', 40000)

    data = request.get_json()

    update_fields = {}
    allowed_fields = [
        'UserName', 'UserPassword', 'UserPermissions', 'Email', 'Telephone'
    ]
    for field in allowed_fields:
        if field in data:
            value = data[field]
            # 对字符串字段，如果传过来是空字符串，也统一转为 None
            if isinstance(value, str) and not value.strip():
                update_fields[field] = None
            else:
                update_fields[field] = value
        # else: 如果字段不在data中，保持不更新

    # 密码长度校验（如果更新密码）
    if 'UserPassword' in update_fields and update_fields['UserPassword']:
        if len(update_fields['UserPassword']) < 6:
            return fail_response_wrap(None, '新密码不能少于6位', 40002)
        if len(update_fields['UserPassword']) > 20: # char(20)
            return fail_response_wrap(None, '新密码长度不能超过20位', 40002)

    # 可选字段的长度校验
    if 'UserPermissions' in update_fields and update_fields['UserPermissions'] and len(update_fields['UserPermissions']) > 5: # char(5)
        return fail_response_wrap(None, '账户权限长度不能超过5位', 40002)
    if 'Email' in update_fields and update_fields['Email'] and len(update_fields['Email']) > 20: # varchar(20)
        return fail_response_wrap(None, '邮箱长度不能超过20位', 40002)
    if 'Telephone' in update_fields and update_fields['Telephone'] and len(update_fields['Telephone']) > 13: # char(13)
        return fail_response_wrap(None, '电话长度不能超过13位', 40002)


    if not update_fields:
        return success_response_wrap(None, '没有提供任何要更新的字段', 20000)

    operator_user_no = request.user.get('UserNo')
    if operator_user_no is None:
        current_app.logger.error("Operator UserNo not available from token, cannot record modification.")
        return fail_response_wrap(None, '操作用户ID缺失，无法记录操作', 50001)

    conn = get_db_connection()
    if not conn:
        return fail_response_wrap(None, '数据库连接失败', 50000)

    try:
        _set_db_session_user_id(conn, operator_user_no)

        existing_user = UserModel.get_user_by_userno(userno)
        if not existing_user:
            return fail_response_wrap(None, f'用户编号 "{userno}" 不存在', 40400)

        # 检查 UserName 和 Email 的唯一性（如果它们在更新字段中）
        if 'UserName' in update_fields and update_fields['UserName'] != existing_user.get('UserName'):
            if UserModel.check_username_exists(update_fields['UserName'], userno):
                return fail_response_wrap(None, f'用户名 "{update_fields["UserName"]}" 已存在。', 40003)
        
        if 'Email' in update_fields and update_fields['Email'] != existing_user.get('Email'):
            if UserModel.check_email_exists(update_fields['Email'], userno):
                return fail_response_wrap(None, f'邮箱 "{update_fields["Email"]}" 已被注册。', 40003)

        if UserModel.update_user(userno, update_fields):
            current_app.logger.info(f"用户信息更新成功: UserNo={userno}")
            return success_response_wrap(None, '用户信息更新成功！')
        else:
            current_app.logger.error(f"用户信息更新失败: UserNo={userno}")
            return fail_response_wrap(None, '用户信息更新失败', 50000)

    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (update_user_info): {db_error}", exc_info=True)
        if db_error.errno == 1062:
            return fail_response_wrap(None, '用户名或邮箱已存在，请检查。', 40003)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/users/<userno> PUT 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)


# --- API for User Deletion (DELETE /api/users/<userno>) ---
@user_admin_bp.route('/users/<string:userno>', methods=['DELETE'])
@token_required
# @has_role(['admin']) # 可选：只有admin才能删除
def delete_user(userno):
    current_app.logger.info(f"Received user delete request for UserNo: {userno}")

    operator_user_no = request.user.get('UserNo')
    if operator_user_no is None:
        current_app.logger.error("Operator UserNo not available from token, cannot record modification.")
        return fail_response_wrap(None, '操作用户ID缺失，无法记录操作', 50001)

    conn = get_db_connection()
    if not conn:
        return fail_response_wrap(None, '数据库连接失败', 50000)

    _set_db_session_user_id(conn, operator_user_no)

    try:
        existing_user = UserModel.get_user_by_userno(userno)
        if not existing_user:
            return fail_response_wrap(None, f'用户编号 "{userno}" 不存在', 40400)
            
        if UserModel.delete_user(userno):
            current_app.logger.info(f"用户删除成功: UserNo={userno}")
            return success_response_wrap(None, '用户删除成功！')
        else:
            current_app.logger.error(f"用户删除失败: UserNo={userno}")
            return fail_response_wrap(None, '用户删除失败', 50000)

    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (delete_user): {db_error}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/users/<userno> DELETE 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)


# --- API for User Search (GET /api/users/search) ---
@user_admin_bp.route('/users/search', methods=['GET'])
@token_required
def search_users_api():
    query_param = request.args.get('query', '').strip()
    limit = int(request.args.get('limit', 10))
    current_app.logger.info(f"Received search request for users with query: '{query_param}'")

    try:
        # 调用 Model 层方法
        users = UserModel.search_by_keyword(query_param, limit)
        
        return success_response_wrap(users, '用户搜索成功')
    except Error as db_error:
        current_app.logger.error(f"搜索用户失败: {db_error}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/users/search GET 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)
