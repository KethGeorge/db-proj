import mysql.connector
from mysql.connector import Error
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random # 导入 random 模块
import string # 导入 string 模块，用于生成随机字符串

# 数据库配置
config = {
    "host": "localhost",      # 数据库服务器地址
    "user": "tumu1t",         # 数据库用户名
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

# 用于生成随机字符串的辅助函数
def generate_random_string(length=8):
    """生成指定长度的随机字母数字字符串"""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for i in range(length))

# 用于生成随机数字的辅助函数
def generate_random_number(min_val=1000, max_val=9999):
    """生成指定范围内的随机整数"""
    return random.randint(min_val, max_val)

app = Flask(__name__)
CORS(app) # 启用 CORS，允许所有来源。生产环境请更精细配置。

@app.route('/api/NS', methods=['POST'])
def handle_ns_request():
    # 1. 检查请求是否为 JSON 格式
    if not request.is_json:
        print("Request is not JSON. Content-Type:", request.headers.get('Content-Type'))
        return jsonify({'message': 'Request must be JSON', 'code': 400}), 400

    # 2. 获取 JSON 数据
    data = request.get_json()

    # 3. 检查 'name' 和 'description' 字段是否存在于 JSON 文档中
    if 'name' not in data:
        return jsonify({'message': 'Missing "name" field in JSON data', 'code': 400}), 400
    if 'description' not in data:
        return jsonify({'message': 'Missing "description" field in JSON data', 'code': 400}), 400

    # 4. 获取 'name' 和 'description' 字段的值
    standard_name_value = data['name']
    description_value = data['description']

    # 5. 生成随机的 NSN 和 MaterialCode
    random_nsn = generate_random_string(10) # 例如，生成10位随机字母数字作为 NSN
    random_material_code = str(generate_random_number(10000, 99999)) # 例如，生成5位随机数字作为 MaterialCode

    print("--------------------------------------------------")
    print("Received JSON data:")
    print(f"Full request data: {data}")
    print(f"Extracted StandardName value: {standard_name_value}")
    print(f"Extracted Description value: {description_value}")
    print(f"Generated NSN: {random_nsn}")
    print(f"Generated MaterialCode: {random_material_code}")
    print("--------------------------------------------------")

    # 6. 连接数据库
    conn = connect_to_database()
    if not conn:
        return jsonify({'message': 'Database connection failed', 'code': 500}), 500

    try:
        # 7. 准备 SQL 插入语句，同时插入 StandardName, Description, NSN, 和 MaterialCode
        # 确保 national_standard 表包含 NSN, StandardName, Description, MaterialCode 这四列
        insert_query = """
        INSERT INTO national_standard (NSN, StandardName, Description, MaterialCode)
        VALUES (%s, %s, %s, %s)
        """

        # 8. 执行插入操作，传入所有参数
        if execute_query(conn, insert_query, (random_nsn, standard_name_value, description_value, 'MAT_MANUAL_001')):
            return jsonify({
                'message': 'Standard data inserted successfully!',
                'code': 20000,
                'inserted_standard_name': standard_name_value,
                'inserted_description': description_value,
                'inserted_nsn': random_nsn,
                'inserted_material_code': random_material_code
            }), 200
        else:
            return jsonify({'message': 'Failed to insert standard data into database', 'code': 500}), 500
    finally:
        # 9. 关闭数据库连接
        if conn.is_connected():
            conn.close()
            print("数据库连接已关闭")

if __name__ == '__main__':
    app.run(debug=True, port=5000)