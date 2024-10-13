import ttkbootstrap as ttk
from tkinter import messagebox
from main_application import show_main_application  # 导入显示主界面的函数

class LoginPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.window_width = 600
        self.window_height = 400
        # 动态计算窗口位置
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        x = int((screen_width - self.window_width) / 2)
        y = int((screen_height - self.window_height) / 2)
        parent.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        self.font = ("Arial", 14)
        self.pack(fill='both', expand=True)

        # 配置行列，使内容垂直和水平居中
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)

        # 使用 grid 布局
        ttk.Label(self, text="Username:", font=self.font).grid(row=1, column=1, sticky="e")
        self.username_entry = ttk.Entry(self, font=self.font, width=20)
        self.username_entry.grid(row=1, column=2, sticky="w")

        ttk.Label(self, text="Password:", font=self.font).grid(row=2, column=1, sticky="e")
        self.password_entry = ttk.Entry(self, show='*', font=self.font, width=20)
        self.password_entry.grid(row=2, column=2, sticky="w")

        login_button = ttk.Button(self, text="Login", command=self.login, width=10)
        self.bind("<Return>", self.login)  # 绑定回车键到登录操作
        login_button.grid(row=3, column=1, columnspan=2)

        # 为所有元素设置全局的 padx 和 pady
        for widget in self.grid_slaves():
            widget.grid_configure(padx=10, pady=10)

    def login(self, event=None):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # 登录验证逻辑
        if username == "admin" and password == "1234":  # 示例条件
            messagebox.showinfo("Info", "Login successful")
            self.pack_forget()  # 隐藏登录窗口
            # 设置主题
            show_main_application(self.master)
        else:
            messagebox.showerror("Error", "Login failed")