import os
import datetime

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_super_secret_jwt_key_here_for_prod') # 生产环境请务必通过环境变量设置
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)

    # 数据库配置
    DB_HOST = "localhost"
    DB_USER = "tumu1t"
    DB_PASSWORD = "tumumu1tt"
    DB_DATABASE = "凝胶时间测定"

    # CORS 配置
    CORS_ORIGINS = ["http://localhost:5173"] # 生产环境请限制为您的前端部署地址