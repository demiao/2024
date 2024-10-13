import ttkbootstrap as ttk
from ttkbootstrap.constants import PRIMARY
from base_page import BasePage  # 继承 BasePage

class OtherFunc(BasePage):  # 继承 BasePage
    def __init__(self, root):
        super().__init__(root)  # 调用 BasePage 的构造函数
        ttk.Label(self.root, text="其他功能页面", style="primary.TLabel").pack(pady=20)
        # 创建输入框
        self.entries = []
        for i in range(5):
            entry = ttk.Entry(self.root)
            entry.pack(pady=5)
            self.entries.append(entry)
        # 创建保存按钮
        save_button = ttk.Button(self.root, text="保存订单", style="primary.TButton", command=self.save_order)
        save_button.pack(pady=10)

    def save_order(self):
        details = [entry.get() for entry in self.entries]
        print("保存订单详细信息:", details)
