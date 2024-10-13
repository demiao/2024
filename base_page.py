import tkinter as tk


class BasePage:
    def __init__(self, root, window_width=800, window_height=600):
        self.root = root
        self.window_width = window_width
        self.window_height = window_height

        # 如果 root 是顶层窗口（Tk 或 Toplevel），则设置窗口大小和居中
        if isinstance(self.root, (tk.Tk, tk.Toplevel)):
            self.root.geometry(f'{self.window_width}x{self.window_height}')
            self.center_window()  # 让窗口居中

    # 让窗口居中显示
    def center_window(self):
        # 获取屏幕宽高
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # 计算窗口居中的位置
        x = int((screen_width / 2) - (self.window_width / 2))
        y = int((screen_height / 2) - (self.window_height / 2))

        # 设置窗口位置为居中
        self.root.geometry(f'{self.window_width}x{self.window_height}+{x}+{y}')
