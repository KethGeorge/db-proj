## 本地 Build 指南

### 所需环境

- Node.js
- MySQL
- Python

### 下载

上面有包可以下载，下载全套代码。

### 配置前端

首先移动到解压好的代码根目录，运行：

```
npm install
```
随后启动服务：
```
npm run dev
```

### 配置后端

后端所需的 Python 包：

```
pip install Flask Flask-CORS PyJWT mysql-connector-python Werkzeug
```

在 `/Connection/Flask_Proj` 下，运行：
```
python app.py
```


## 存在的问题（Updated 2025/05/28）

- 实验报告中格式需要统一，不能出现疑似 AI 生成的格式吧。
