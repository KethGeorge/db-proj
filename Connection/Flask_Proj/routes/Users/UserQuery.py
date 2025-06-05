
from flask import Blueprint, request, current_app
from mysql.connector import Error

# 导入您的工具函数，路径基于 Flask_Proj 根目录
from utils.db import get_db_connection, execute_query
from utils.response import success_response_wrap, fail_response_wrap
from utils.auth import token_required
# from utils.helpers import parse_combined_datetime_str # 前端已发送标准格式，后端可直接解析，故不再需要
import string
import random
user_bp = Blueprint('userQ', __name__)

@user_bp.route('/users', methods=['GET']) # 注意这里用 '/users' 区分 'POST /user'
@token_required # 假设用户列表查询也需要认证
def get_users():
    current_app.logger.info("Received request for user list.")
    
    # 获取查询参数
    # Flask 的 request.args 获取 URL 中的查询参数
    userno = request.args.get('userno')
    username = request.args.get('username')
    email = request.args.get('email')
    user_permissions = request.args.get('userPermissions') # 对应前端的 filterType
    telephone = request.args.get('telephone') # 对应前端的 createdTime
    
    # 分页参数
    try:
        current = int(request.args.get('current', 1)) # 默认第一页
        page_size = int(request.args.get('pageSize', 20)) # 默认每页20条
    except ValueError:
        return fail_response_wrap(None, '分页参数格式不正确', 40004)

    conn = get_db_connection()
    if not conn:
        return fail_response_wrap(None, '数据库连接失败', 50000)

    try:
        # 构建动态 SQL 查询
        query = "SELECT UserNo, UserName, UserPermissions, Email, Telephone FROM users WHERE 1=1"
        count_query = "SELECT COUNT(*) FROM users WHERE 1=1"
        query_params = []

        if userno:
            query += " AND UserNo LIKE %s"
            count_query += " AND UserNo LIKE %s"
            query_params.append(f"%{userno}%")
        if username:
            query += " AND UserName LIKE %s"
            count_query += " AND UserName LIKE %s"
            query_params.append(f"%{username}%")
        if email:
            query += " AND Email LIKE %s"
            count_query += " AND Email LIKE %s"
            query_params.append(f"%{email}%")
        if user_permissions:
            query += " AND UserPermissions = %s"
            count_query += " AND UserPermissions = %s"
            query_params.append(user_permissions)
        if telephone:
            # 假设电话号码是精确匹配或者也用 LIKE
            query += " AND Telephone LIKE %s"
            count_query += " AND Telephone LIKE %s"
            query_params.append(f"%{telephone}%")
        
        # 为了安全，password 不应该被查询出来
        # if password: # 密码不应该在查询中直接作为筛选条件
        #     query += " AND UserPassword = %s"
        #     count_query += " AND UserPassword = %s"
        #     query_params.append(password) # ！！！注意：明文密码查询非常不安全

        # 获取总条数
        total_count = execute_query(conn, count_query, tuple(query_params), fetch_one=True)[0]
        current_app.logger.info(f"Total users found: {total_count}")
        # 添加分页
        offset = (current - 1) * page_size
        query += f" LIMIT %s OFFSET %s"
        query_params.append(page_size)
        query_params.append(offset)

        users_raw = execute_query(conn, query, tuple(query_params), fetch_all=True)
        
        # 格式化数据以匹配前端 PolicyRecord 结构
        user_list = []
        for user in users_raw:
            user_list.append({
                'id': user[0], # UserNo 作为 id
                'number': user[0], # UserNo 也作为 number
                'name': user[1], # UserName 作为 name
                'userPermissions': user[2], # UserPermissions
                'email': user[3], # Email
                'telephone': user[4], # Telephone
                'password': '***' # 密码不应该直接返回
                # 这里没有 'contentType', 'filterType', 'count', 'createdTime', 'status'
                # 需根据实际需求调整或映射，以下是根据 PolicyRecord 推断的映射
                # 'contentType': 'text', # 示例默认值
                # 'filterType': 'system', # 示例默认值
                # 'count': 1, # 示例默认值
                # 'createdTime': '2023-01-01T00:00:00', # 假设用户表有创建时间字段
                # 'status': 'online' # 示例默认值
            })

        return success_response_wrap({
            'list': user_list,
            'total': total_count
        }, '用户列表获取成功')

    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (get_users): {db_error}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/users 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)

@user_bp.route('/users/<string:userno>', methods=['GET']) # 定义动态路由参数
@token_required
def get_user_detail(userno):
    current_app.logger.info(f"Received request for user detail: {userno}")

    conn = get_db_connection()
    if not conn:
        return fail_response_wrap(None, '数据库连接失败', 50000)

    try:
        # 这里不查询密码字段
        query = "SELECT UserNo, UserName, UserPermissions, Email, Telephone FROM users WHERE UserNo = %s"
        user_raw = execute_query(conn, query, (userno,), fetch_one=True)

        if not user_raw:
            return fail_response_wrap(None, '用户不存在', 40400)

        user_detail = {
            'id': user_raw[0],
            'number': user_raw[0],
            'username': user_raw[1],
            'userPermissions': user_raw[2],
            'email': user_raw[3],
            'telephone': user_raw[4],
            'password': '' # 密码字段留空，不返回实际密码，因为在编辑页面是空的
        }

        return success_response_wrap(user_detail, '用户详情获取成功')

    except Error as db_error:
        current_app.logger.error(f"数据库操作错误 (get_user_detail): {db_error}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误（数据库）: {db_error}', 50000)
    except Exception as e:
        current_app.logger.error(f"处理 /api/users/<userno> 请求错误: {e}", exc_info=True)
        return fail_response_wrap(None, f'服务器内部错误: {e}', 50000)