import jwt
import datetime
from flask import request, current_app
from functools import wraps
from werkzeug.security import check_password_hash # 仅在登录逻辑需要，此处无需

from utils.response import fail_response_wrap # 导入失败响应封装

def token_required(f):
    @wraps(f) # 关键：确保保留原始函数名称和元数据，避免端点冲突
    def decorated(*args, **kwargs):
        token = None
        # 从请求头中获取 Token
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return fail_response_wrap(None, 'Token缺失或格式不正确', 40100)

        try:
            # 解码 Token
            # 注意：current_app 只能在应用上下文中访问
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            # 将解码后的用户信息（payload）存储到 request.user
            request.user = data
        except jwt.ExpiredSignatureError:
            return fail_response_wrap(None, 'Token已过期', 40101)
        except jwt.InvalidTokenError:
            return fail_response_wrap(None, '无效的Token', 40102)
        except Exception as e:
            print(f"Token 验证错误: {e}")
            return fail_response_wrap(None, 'Token验证失败', 40103)

        return f(*args, **kwargs)
    return decorated