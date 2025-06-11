## 本地 Build 指南

### 所需环境

- Node.js
- MySQL
- Python

### 下载

从右边的 release 下载

### 配置前端

首先移动到解压好的代码根目录，运行：

```
npm install
```

> 这一步可能需要管理员权限

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

### 配置数据库

数据库的名字为 `devexp`, 可以通过 `\Connection\MySQL_Commands\DBRevised.sql` 的备份文件创建。

数据库操作的账户如下，你可以通过如下的命令创建：

```
CREATE USER 'tumu1t'@'localhost' IDENTIFIED BY 'tumumu1tt';
GRANT USAGE ON *.* TO `tumu1t`@`localhost`;
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, REFERENCES, EXECUTE ON `devexp`.* TO `tumu1t`@`localhost`;
```


