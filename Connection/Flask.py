from flask import Flask, request, jsonify
from flask_cors import CORS # 导入 CORS

app = Flask(__name__)
CORS(app) # 在这里初始化 CORS，允许所有来源访问所有路由。
          # 生产环境中，你应该更精细地配置允许的源。

@app.route('/api/NS', methods=['POST'])
def handle_channel_form_submit():
    # ... (其余代码不变)
    if 'file' not in request.files:
        print("No file part in the request")
        return jsonify({'message': 'No file part in the request', 'code': 400}), 400

    file = request.files['file']
    # ...
    if file.filename == '':
        print("No selected file")
        return jsonify({'message': 'No selected file', 'code': 400}), 400

    # 确保文件存在且可读取
    if file:
        try:
            # 读取文件内容
            # file.read() 会读取文件的所有内容到内存中。
            # 如果文件非常大，这可能会消耗大量内存。
            # 对于大型文件，你可能需要分块读取或保存到磁盘。
            file_content = file.read().decode('utf-8') # 假设文件是文本文件，使用 utf-8 解码

            print("--------------------------------------------------")
            print(f"Received file: {file.filename}")
            print(f"File mimetype: {file.mimetype}")
            print("\n--- File Content ---")
            print(file_content)
            print("--------------------------------------------------")

            # 你也可以打印表单中的其他字段 (如果存在的话)
            print("\n--- Other Form Fields (if any) ---")
            for key, value in request.form.items():
                print(f"{key}: {value}")
            print("--------------------------------------------------")


            return jsonify({'message': f'File {file.filename} received and processed successfully!', 'code': 200}), 200
        except Exception as e:
            # 捕获读取或解码文件时可能发生的错误
            print(f"Error processing file: {e}")
            return jsonify({'message': f'Error processing file: {str(e)}', 'code': 500}), 500
    else:
        # 理论上这个分支在上面的检查中已经覆盖，但作为防范
        return jsonify({'message': 'Unexpected error with file upload', 'code': 500}), 500
if __name__ == '__main__':
    app.run(debug=True, port=5000)