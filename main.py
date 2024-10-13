import ttkbootstrap as ttk
from login_page import LoginPage  # 导入 LoginPage

if __name__ == "__main__":
    root = ttk.Window(title="Order Management System")  # 创建主窗口
    style = ttk.Style()
    style.theme_use('flatly')  # 设置主题
    # 显示登录页面
    login_page = LoginPage(root)

    # 启动主循环
    root.mainloop()
