from flask import Flask, request, jsonify
from flask_cors import CORS # 导入 CORS

app = Flask(__name__)
CORS(app) # 启用 CORS，允许所有来源。生产环境请更精细配置。

@app.route('/api/NS', methods=['POST'])
@app.route('/api/Protocol', methods=['POST'])  # 支持带斜杠的路径
@app.route('/api/Mat', methods=['POST'])   # 支持不带斜杠的路径
def handle_ns_request():
    # 1. 检查请求是否为 JSON 格式
    if not request.is_json:
        print("Request is not JSON. Content-Type:", request.headers.get('Content-Type'))
        return jsonify({'message': 'Request must be JSON', 'code': 400}), 400

    # 2. 获取 JSON 数据
    data = request.get_json()

    # 3. 检查 'model' 字段是否存在
    # 4. 获取 model 数据
    model_data = data
     # 3. 获取请求的路径，以便区分来源
    # request.path 会返回请求的完整路径，例如 '/api/NS', '/api/Protocol', '/api/Mat'
    request_source_path = request.path

    # 4. 根据路径判断来源
    source_module = "Unknown"
    if request_source_path == '/api/NS':
        source_module = "NS"
    elif request_source_path == '/api/Protocol':
        source_module = "Protocol"
    elif request_source_path == '/api/Mat':
        source_module = "Mat"

    print("--------------------------------------------------")
    print(f"Received JSON data from: {request_source_path} ({source_module} module)")
    print(f"Full request data: {data}") # 打印完整的请求数据
    print("\n--- Model Content ---")
    # 为了更好地打印嵌套结构，可以使用 json.dumps
    import json
    print(json.dumps(model_data, indent=2, ensure_ascii=False)) # 打印 model 字段的内容
    print("--------------------------------------------------")

    # 5. 返回成功响应
    return jsonify({
        'message': 'Model data received and processed successfully!',
        'code': 20000,
        'received_model': model_data # 也可以将收到的 model 返回给前端确认
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)