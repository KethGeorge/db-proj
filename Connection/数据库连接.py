import mysql.connector
from mysql.connector import Error

config = {
    "host": "localhost",      # 数据库服务器地址
    "user": "tumu1t",  # 数据库用户名
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
        return False
    finally:
        if cursor:
            cursor.close()

def main():
    # 1. 连接到数据库
    conn = connect_to_database()
    if not conn:
        return

    try:
        # 2. 示例1：查询User表数据
        print("\n查询User表前3条数据:")
        query = "SELECT * FROM User LIMIT 3"
        results = execute_query(conn, query)
        for row in results:
            print(row)

        # 3. 示例2：插入新用户
        insert_query = """
        INSERT INTO User (UserNo, UserName, UserPassword, UserPermissions, Email, Telephone)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        new_user = (
            "U031", 
            "新用户", 
            "newpassword123", 
            "user", 
            "newuser@lab.com", 
            "13800000031"
        )
        if execute_query(conn, insert_query, new_user):
            print("新用户插入成功")

        # 4. 示例3：带条件的查询
        print("\n查询权限为admin的用户:")
        admin_query = "SELECT UserNo, UserName FROM User WHERE UserPermissions = 'admin'"
        admins = execute_query(conn, admin_query)
        for admin in admins:
            print(admin)

    finally:
        # 5. 关闭连接
        if conn.is_connected():
            conn.close()
            print("\n数据库连接已关闭")

if __name__ == "__main__":
    main()