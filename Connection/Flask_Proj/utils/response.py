from flask import jsonify

def success_response_wrap(data=None, message="成功", code=20000):
    """封装成功的 API 响应"""
    return jsonify({
        'code': code,
        'msg': message,
        'data': data
    })

def fail_response_wrap(data=None, message="失败", code=50000):
    """封装失败的 API 响应"""
    return jsonify({
        'code': code,
        'msg': message,
        'data': data
    })