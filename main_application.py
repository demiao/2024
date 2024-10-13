import ttkbootstrap as ttk
from base_page import BasePage  # 导入 BasePage
from order_query import OrderQueryPage  # 导入查询订单页面
from other_func import OtherFunc # 导入订单详情页面


# 主应用页面，继承自 BasePage
class MainApplication(BasePage):
    def __init__(self, root):

        # 获取当前屏幕的分辨率
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # 动态计算合适的窗口大小，比如屏幕分辨率的 80%
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)

        # 初始化 BasePage 类并设置窗口大小
        super().__init__(root, window_width=window_width, window_height=window_height)
        self.root.title("Main Application")  # 设置主窗口标题

        # 创建 Notebook 容器
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True)

        # 创建“查询订单”选项卡
        order_query_frame = ttk.Frame(notebook)
        notebook.add(order_query_frame, text="查询订单")

        # 在查询订单选项卡中嵌入 OrderQueryPage
        self.order_query_page = OrderQueryPage(order_query_frame)

        # 创建“其他功能”选项卡
        other_func_frame = ttk.Frame(notebook)
        notebook.add(other_func_frame, text="其他功能")

        # 在订单详情选项卡中嵌入 OrderDetailPage
        self.order_detail_page = OtherFunc(other_func_frame)

        # 可以添加其他选项卡
        extra_frame = ttk.Frame(notebook)
        notebook.add(extra_frame, text="其他功能2")
        ttk.Label(extra_frame, text="此处可以添加其他功能").pack(pady=20)

        # 绑定关闭窗口时的回调函数
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """在关闭主窗口时退出程序"""
        self.root.quit()  # 停止主循环
        self.root.destroy()  # 销毁主窗口


# 用于显示主应用页面的函数
# 用于显示主应用页面的函数
def show_main_application(root):
    app = MainApplication(root)  # 跳转到主应用界面