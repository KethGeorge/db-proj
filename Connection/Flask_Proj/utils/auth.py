# utils/auth.py (当前版本，保持不变)

import jwt
import datetime
from flask import request, current_app
from functools import wraps
from utils.response import fail_response_wrap

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return fail_response_wrap(None, 'Token缺失或格式不正确', 40100)

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            request.user = data # <-- 这里已经把 UserNo 从 Payload 传递给了 request.user
            
            # (可选) 在这里添加一个检查，确保 UserNo 存在，如果它对你的触发器是严格必须的
            if 'UserNo' not in request.user or request.user['UserNo'] is None:
                 current_app.logger.error(f"JWT payload missing or null UserNo for user: {request.user.get('username')}")
                 return fail_response_wrap(None, 'Token缺少用户ID信息', 40104)

        except jwt.ExpiredSignatureError:
            return fail_response_wrap(None, 'Token已过期', 40101)
        except jwt.InvalidTokenError:
            return fail_response_wrap(None, '无效的Token', 40102)
        except Exception as e:
            current_app.logger.error(f"Token 验证错误: {e}", exc_info=True) # 使用 current_app.logger
            return fail_response_wrap(None, 'Token验证失败', 40103)

        return f(*args, **kwargs)
    return decorated