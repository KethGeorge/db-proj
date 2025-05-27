import os
from flask import Flask, jsonify
from flask_cors import CORS

from cfg import Config
from utils.db import create_initial_tables_and_users
from utils.response import fail_response_wrap
from routes.auth import auth_bp
from routes.NS import ns_bp
from routes.Device import device_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config) # 从 Config 类加载配置

    # 初始化 CORS
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}}) # 仅对 /api/* 路径启用 CORS

    # 注册蓝图
    # url_prefix 参数为蓝图中的所有路由添加前缀
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(ns_bp, url_prefix='/api')
    app.register_blueprint(device_bp, url_prefix='/api')
    # 错误处理器
    @app.errorhandler(404)
    def not_found_error(error):
        return fail_response_wrap(None, 'API 地址不存在', 40400), 404

    @app.errorhandler(500)
    def internal_error(error):
        import traceback
        traceback.print_exc() # 打印详细错误信息到控制台，便于调试
        return fail_response_wrap(None, '服务器内部错误', 50000), 500

    return app

if __name__ == '__main__':
    app = create_app()
    # 在开发模式下，可以自动创建表和初始用户
    # 注意：生产环境不建议在应用启动时自动创建，应通过数据库迁移工具管理
    with app.app_context(): # 确保在应用上下文中执行数据库操作
        create_initial_tables_and_users()

    app.run(debug=True, port=5000)