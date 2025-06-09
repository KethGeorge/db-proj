# Flask_Proj/app.py

import os
from flask import Flask, jsonify, request, g
from flask_cors import CORS

from cfg import Config  # 从 cfg.py 中导入配置类
from utils.db import create_initial_tables_and_users # 负责创建数据库表和初始数据
from utils.response import fail_response_wrap
import logging
# 导入所有蓝图
from routes.auth import auth_bp
# from routes.NS import ns_bp
# from routes.Device import device_bp
# from routes.Users.UserAdmin import user_bp  # 导入我们为用户创建的蓝图
# from routes.Users.UserQuery import user_bp as user_query_bp  # 如果需要查询用户的蓝图
# from routes.Users.UserModify import user_modify_bp  # 用户修改的蓝图
from routes.userAdmin.userAdminAPI import user_admin_bp  # 用户管理相关的蓝图

from routes.NationalStandard.NationalStandardAPI import national_standard_bp  # 国家标准相关的蓝图
from routes.Material.materialAPI import material_bp  # 材料相关的蓝图
from routes.device.deviceAPI import device_bp  # 设备相关的蓝图
from routes.protocol.protocolAPI import protocol_bp  # 协议相关的蓝图
from routes.experiment.experimentAPI import experiment_bp  # 实验相关的蓝图
from routes.expReport.expReportAPI import report_bp  # 实验报告相关的蓝图
from routes.modification.modificationAPI import modification_bp  # 审计日志相关的蓝图

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config) # 从 Config 类加载配置
    app.logger.setLevel(logging.DEBUG)
    # 初始化 CORS
    # 仅对 /api/* 路径启用 CORS，允许来自配置中 CORS_ORIGINS 的源
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}}) 

    # 注册蓝图
    # url_prefix 参数为蓝图中的所有路由添加 /api 前缀
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(user_admin_bp, url_prefix='/api')  # 注册用户管理相关蓝图
    app.register_blueprint(national_standard_bp, url_prefix='/api')  # 注册国家标准相关蓝图
    app.register_blueprint(material_bp, url_prefix='/api')  # 注册材料相关蓝图
    app.register_blueprint(device_bp, url_prefix='/api')  # 注册设备相关蓝图
    app.register_blueprint(protocol_bp, url_prefix='/api')  # 注册协议相关蓝图
    app.register_blueprint(experiment_bp, url_prefix='/api')  # 注册实验相关蓝图
    app.register_blueprint(report_bp, url_prefix='/api')  # 注册实验报告相关蓝图
    app.register_blueprint(modification_bp, url_prefix='/api')  # 注册审计日志相关蓝图
    # 错误处理器
    app.logger.info("应用上下文已创建，数据库表和初始用户已设置。")
    @app.errorhandler(404)
    def not_found_error(error):
        app.logger.warning(f"404 Not Found: {request.url}") # 记录 404 错误
        return fail_response_wrap(None, 'API 地址不存在', 40400), 404

    @app.errorhandler(500)
    def internal_error(error):
        import traceback
        traceback.print_exc() # 打印详细错误信息到控制台，便于调试
        app.logger.error(f"500 Internal Server Error: {request.url}", exc_info=True) # 记录 500 错误，并包含堆栈信息
        return fail_response_wrap(None, '服务器内部错误', 50000), 500

    @app.teardown_appcontext
    def teardown_db(exception):
        db = g.pop('db', None)
        if db is not None:
            db.close()
            app.logger.info("数据库连接在请求结束时关闭。")
    return app

if __name__ == '__main__':
    app = create_app()
    # 在开发模式下，可以自动创建表和初始用户
    # 注意：生产环境不建议在应用启动时自动创建表，应通过数据库迁移工具管理
    with app.app_context(): # 确保在应用上下文中执行数据库操作
        create_initial_tables_and_users() # 这个函数需要包含创建 users 表的逻辑
    # 运行 Flask 应用
    # debug=True 会在代码更改时自动重载，并提供更详细的错误信息
    # port=5000 是默认的 Flask 端口
    app.run(host='0.0.0.0', debug=True, port=5000)