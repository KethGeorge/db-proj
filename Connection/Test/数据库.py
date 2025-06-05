import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("登录")
        self.root.geometry("300x200")
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(expand=True)
        ttk.Label(main_frame, text="用户名:").grid(row=0, column=0, pady=5)
        username_entry = ttk.Entry(main_frame, textvariable=self.username)
        username_entry.grid(row=0, column=1)
        ttk.Label(main_frame, text="密码:").grid(row=1, column=0, pady=5)
        password_entry = ttk.Entry(main_frame, textvariable=self.password, show="*")
        password_entry.grid(row=1, column=1)
        login_btn = ttk.Button(main_frame, text="登录", command=self.authenticate)
        login_btn.grid(row=2, columnspan=2, pady=15)

    def authenticate(self):
        username = self.username.get()
        password = self.password.get()
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="tumu1t",
                password="tumumu1tt",
                database="凝胶时间测定"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT UserNo FROM Users WHERE UserName = %s AND UserPassword = %s", (username, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            if user:
                self.root.destroy()
                main_root = tk.Tk()
                DatabaseApp(main_root, user[0])  # 传递UserNo给主界面
                main_root.mainloop()
            else:
                messagebox.showerror("错误", "用户名或密码无效")
        except Exception as e:
            messagebox.showerror("数据库错误", str(e))

class DatabaseApp:
    def __init__(self, root, user_no):
        self.root = root
        self.user_no = user_no
        self.db = mysql.connector.connect(
            host="localhost",
            user="tumu1t",
            password="tumumu1tt",
            database="凝胶时间测定"
        )
        self.cursor = self.db.cursor()
        # 初始化会话变量
        self._reset_session_variable()
        self.create_main_interface()

    def _reset_session_variable(self):
        """ 每次操作前重置会话变量 """
        self.cursor.execute(f"SET @current_user = '{self.user_no}'")
        self.db.commit()

    def execute_query(self, query):
        """ 封装数据库操作 """
        try:
            self._reset_session_variable()
            self.cursor.execute(query)
            self.db.commit()
            return True
        except Exception as e:
            messagebox.showerror("数据库错误", str(e))
            return False

    def create_main_interface(self):
        nav_frame = ttk.Frame(self.root)
        nav_frame.pack(pady=10)
        tables = ["Users", "Material", "Device", "Protocol", "Experiment"]
        for table in tables:
            btn = ttk.Button(nav_frame, text=table, command=lambda t=table: self.show_table_interface(t))
            btn.pack(side=tk.LEFT, padx=5)
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def show_table_interface(self, table_name):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        ttk.Label(self.main_frame, text=f"{table_name} 管理", font=('Arial', 14, 'bold')).pack(pady=10)
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="添加记录", command=lambda: self.show_add_form(table_name)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="修改记录", command=lambda: self.show_edit_form(table_name)).pack(side=tk.LEFT, padx=5)
        columns = self.get_table_columns(table_name)
        self.tree = ttk.Treeview(self.main_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.load_table_data(table_name)

    def get_table_columns(self, table_name):
        self._reset_session_variable()
        self.cursor.execute(f"DESCRIBE {table_name}")
        return [col[0] for col in self.cursor.fetchall()]

    def load_table_data(self, table_name):
        self.tree.delete(*self.tree.get_children())
        self._reset_session_variable()
        self.cursor.execute(f"SELECT * FROM {table_name}")
        for row in self.cursor.fetchall():
            self.tree.insert("", tk.END, values=row)

    def show_add_form(self, table_name):
        form_window = tk.Toplevel(self.root)
        form_window.title(f"添加 {table_name} 记录")
        self._reset_session_variable()
        self.cursor.execute(f"DESCRIBE {table_name}")
        fields = self.cursor.fetchall()
        entries = {}
        for i, field in enumerate(fields):
            ttk.Label(form_window, text=field[0]).grid(row=i, column=0, padx=5, pady=5)
            entry = ttk.Entry(form_window)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[field[0]] = entry

        def submit():
            try:
                columns = ", ".join(entries.keys())
                values = ", ".join([f"'{e.get()}'" for e in entries.values()])
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
                if self.execute_query(query):
                    self.load_table_data(table_name)
                    form_window.destroy()
                    messagebox.showinfo("成功", "记录添加成功")
            except Exception as e:
                messagebox.showerror("错误", str(e))

        ttk.Button(form_window, text="提交", command=submit).grid(row=len(fields), columnspan=2, pady=10)

    def show_edit_form(self, table_name):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要修改的记录")
            return
        edit_window = tk.Toplevel(self.root)
        edit_window.title("编辑记录")
        self._reset_session_variable()
        self.cursor.execute(f"DESCRIBE {table_name}")
        fields = self.cursor.fetchall()
        values = self.tree.item(selected[0])['values']
        entries = {}
        for i, (field, value) in enumerate(zip(fields, values)):
            ttk.Label(edit_window, text=field[0]).grid(row=i, column=0, padx=5, pady=5)
            entry = ttk.Entry(edit_window)
            entry.insert(0, value)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[field[0]] = entry
        def update():
            try:
                set_clause = ", ".join([f"{k} = '{v.get()}'" for k, v in entries.items()])
                primary_key = fields[0][0]
                query = f"UPDATE {table_name} SET {set_clause} WHERE {primary_key} = '{values[0]}'"
                if self.execute_query(query):
                    self.load_table_data(table_name)
                    edit_window.destroy()
                    messagebox.showinfo("成功", "记录更新成功")
            except Exception as e:
                messagebox.showerror("错误", str(e))

        ttk.Button(edit_window, text="更新", command=update).grid(row=len(fields), columnspan=2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    login_app = LoginWindow(root)
    root.mainloop()