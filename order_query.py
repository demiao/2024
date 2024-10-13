import random
import ttkbootstrap as ttk
from tkinter import Scrollbar, messagebox
import tkinter as tk
import pandas as pd


class OrderQueryPage:
    def __init__(self, frame):
        self.frame = frame
        # Dokumentation：
        # 1.Kunde：
        # 2.Typ-Kurzbezeichung
        # 3.Fertigungsdatum
        # 4.Prüfer
        # 5.Prüfungsdatum
        # 6.Musternummer
        # 7.Prüfnummer
        # 第二部分
        # Prüfling
        # 1.Prüfling-Nr:
        # 2.Bemerkung
        # 第三部分
        # Prüfaufbau
        # 1.Prüfaufbau（下拉的可能性：Schaum，frei aufgehängt, Unter Last)
        # 2.Bemerkung
        # 第四部分
        # Prüfvorgaben
        # 1.Prüfvorschrift
        # 2.Prüfspannung
        # 3.Test dauer
        # 4.Prüf-Art
        # 5.Mikrofon Abstand
        # 6.Drehrichtung
        # 7.Drehzahl
        # 第五部分
        # Toleranzprüfung
        # 1.Luftschall-Summegrenzwert :
        # 2.Luftschall-Summe-Straffrequenz:
        # 3.Luftschall-Summe-Endfrequenz:

        self.columns = [
            "Kunde", "Typ-Kurzbezeichung", "Fertigungsdatum", "Prüfer", "Prüfungsdatum", "Musternummer", "Prüfnummer",
            "Prüfling-Nr", "Bemerkung", "Prüfaufbau", "Bemerkung", "Prüfvorschrift", "Prüfspannung", "Test dauer",
            "Prüf-Art", "Mikrofon Abstand", "Drehrichtung", "Drehzahl", "Luftschall-Summegrenzwert",
            "Luftschall-Summe-Straffrequenz", "Luftschall-Summe-Endfrequenz"
        ]
        self.test_typs = ["A", "Q", "Z", "Null-Serie", "Claim（TKU）", "Sonder", "BlockForce"]
        self.data = self.generate_mock_data()  # 生成 1000 条测试数据
        self.df = pd.DataFrame(self.data, columns=self.columns)  # 创建 pandas DataFrame
        self.items_per_page = 50  # 每页显示 50 条
        self.current_page = 1  # 当前页数
        self.total_pages = (len(self.data) + self.items_per_page - 1) // self.items_per_page  # 计算总页数
        self.create_order_query_page()

    def create_order_query_page(self):
        # 创建顶部布局区域，输入框、下拉框、按钮
        top_frame = ttk.Frame(self.frame)
        top_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        # 输入框和下拉框
        ttk.Label(top_frame, text="Test Number:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10,
                                                                           sticky="e")
        self.sachnummer_entry = ttk.Entry(top_frame, font=("Arial", 12), width=30)
        self.sachnummer_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        ttk.Label(top_frame, text="Type of Measurement:", font=("Arial", 12)).grid(row=0, column=2, padx=10, pady=10,
                                                                                   sticky="e")

        self.test_typ_entry = ttk.Combobox(top_frame, font=("Arial", 12), width=30,
                                           values=self.test_typs)
        self.test_typ_entry.grid(row=0, column=3, padx=10, pady=10, sticky="w")

        # 查询按钮
        query_button = ttk.Button(top_frame, text="Query", command=self.query_order)
        query_button.grid(row=0, column=4, padx=10, pady=10, sticky="w")

        # 设置全局的表格行高
        style = ttk.Style()
        style.configure("Treeview", rowheight=40)

        # 确保顶部框架自动调整大小，分配最小权重
        self.frame.grid_rowconfigure(0, weight=0)

        # 创建表格部分
        self.create_table()

        # 添加翻页按钮和分页信息
        self.create_pagination_controls()

    def create_table(self):
        # 创建表格 (ttk.Treeview)
        style = ttk.Style()

        # 设置Treeview的表头样式
        style.configure(
            "Treeview.Heading",
            background="gray",
            foreground="black",
            font=("Arial", 8, "bold"),
            relief="solid", )

        self.tree = ttk.Treeview(self.frame, columns=self.columns, show="headings")

        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", )

        # Binding double-click event
        self.tree.bind("<Double-1>", self.on_row_double_click)

        self.tree.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        # 设置行和列权重
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # 创建垂直滚动条
        scrollbar = Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky="ns")

        # 创建水平滚动条
        hscrollbar = Scrollbar(self.frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=hscrollbar.set)
        hscrollbar.grid(row=2, column=0, sticky="ew")

        # 填充数据
        self.populate_table()

    def populate_table(self):
        # 清空表格
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 计算当前页显示的数据
        start_index = (self.current_page - 1) * self.items_per_page
        end_index = start_index + self.items_per_page
        current_page_data = self.data[start_index:end_index]

        # 填充当前页数据
        for row in current_page_data:
            self.tree.insert("", "end", values=row)

    def on_row_double_click(self, event):
        # 获取双击的行
        item = self.tree.selection()[0]
        row_data = self.tree.item(item, "values")

        # 创建一个新的窗口
        edit_window = tk.Toplevel(self.frame)

        # 不能调整窗口大小
        edit_window.resizable(False, False)
        edit_window.title("Edit Row Data")

        # 不可编辑字段的列表
        readonly_fields = [
            "Kunde", "Typ-Kurzbezeichung", "Prüfer", "Prüfungsdatum", "Musternummer", "Prüfnummer",
            "Prüfling-Nr", "Prüfvorschrift", "Prüfspannung", "Test dauer",
            "Prüf-Art", "Mikrofon Abstand", "Drehrichtung", "Drehzahl", "Luftschall-Summegrenzwert",
            "Luftschall-Summe-Straffrequenz", "Luftschall-Summe-Endfrequenz"
        ]

        # 第一部分: Dokumentation
        tk.Label(edit_window, text="Dokumentation").grid(row=0, column=0, columnspan=2, padx=10, pady=5)

        labels_part_1 = ["Kunde", "Typ-Kurzbezeichung", "Fertigungsdatum", "Prüfer", "Prüfungsdatum", "Musternummer",
                         "Prüfnummer"]
        entries_part_1 = {}
        for idx, label in enumerate(labels_part_1):
            tk.Label(edit_window, text=label).grid(row=idx + 1, column=0, padx=10, pady=5)
            entry = tk.Entry(edit_window)
            entry.grid(row=idx + 1, column=1, padx=10, pady=5)
            entry.insert(0, row_data[idx])
            if label in readonly_fields:
                entry.config(state="readonly")
            entries_part_1[label] = entry

        # 第二部分: Prüfling
        tk.Label(edit_window, text="Prüfling").grid(row=len(labels_part_1) + 1, column=0, columnspan=2, padx=10, pady=5)

        labels_part_2 = ["Prüfling-Nr", "Bemerkung"]
        entries_part_2 = {}
        for idx, label in enumerate(labels_part_2):
            tk.Label(edit_window, text=label).grid(row=len(labels_part_1) + idx + 2, column=0, padx=10, pady=5)
            entry = tk.Entry(edit_window)
            entry.insert(0, row_data[len(labels_part_1) + idx])
            if label in readonly_fields:
                entry.config(state="readonly")
            entries_part_2[label] = entry
            entry.grid(row=len(labels_part_1) + idx + 2, column=1, padx=10, pady=5)


        # 第三部分: Prüfaufbau
        tk.Label(edit_window, text="Prüfaufbau").grid(row=len(labels_part_1) + len(labels_part_2) + 2, column=0,
                                                      columnspan=2, padx=10, pady=5)

        labels_part_3 = ["Prüfaufbau", "Bemerkung"]
        entries_part_3 = {}

        for idx, label in enumerate(labels_part_3):
            tk.Label(edit_window, text=label).grid(row=len(labels_part_1) + len(labels_part_2) + idx + 3, column=0,
                                                   padx=10, pady=5)
            if label == "Prüfaufbau":
                options = ["Schaum", "frei aufgehängt", "Unter Last"]
                entry = ttk.Combobox(edit_window, values=options)

            else:
                entry = tk.Entry(edit_window)
            entry.insert(0, row_data[len(labels_part_1) + len(labels_part_2) + idx])
            if label in readonly_fields:
                entry.config(state="readonly")  # 设置为只读状态
            entry.grid(row=len(labels_part_1) + len(labels_part_2) + idx + 3, column=1, padx=10, pady=5)
            entries_part_3[label] = entry

        # 第四部分: Prüfvorgaben
        tk.Label(edit_window, text="Prüfvorgaben").grid(
            row=len(labels_part_1) + len(labels_part_2) + len(labels_part_3) + 3, column=0, columnspan=2, padx=10,
            pady=5)

        labels_part_4 = ["Prüfvorschrift", "Prüfspannung", "Test dauer", "Prüf-Art", "Mikrofon Abstand", "Drehrichtung",
                         "Drehzahl"]
        entries_part_4 = {}
        for idx, label in enumerate(labels_part_4):
            tk.Label(edit_window, text=label).grid(
                row=len(labels_part_1) + len(labels_part_2) + len(labels_part_3) + idx + 4, column=0, padx=10, pady=5)
            entry = tk.Entry(edit_window)
            entry.insert(0, row_data[len(labels_part_1) + len(labels_part_2) + len(labels_part_3) + idx])
            if label in readonly_fields:
                entry.config(state="readonly")
            entry.grid(row=len(labels_part_1) + len(labels_part_2) + len(labels_part_3) + idx + 4, column=1, padx=10,
                       pady=5)
            entries_part_4[label] = entry

        # 第五部分: Toleranzprüfung
        tk.Label(edit_window, text="Toleranzprüfung").grid(
            row=len(labels_part_1) + len(labels_part_2) + len(labels_part_3) + len(labels_part_4) + 4, column=0,
            columnspan=2, padx=10, pady=5)

        labels_part_5 = ["Luftschall-Summegrenzwert", "Luftschall-Summe-Straffrequenz", "Luftschall-Summe-Endfrequenz"]
        entries_part_5 = {}
        for idx, label in enumerate(labels_part_5):
            tk.Label(edit_window, text=label).grid(
                row=len(labels_part_1) + len(labels_part_2) + len(labels_part_3) + len(labels_part_4) + idx + 5,
                column=0, padx=10, pady=5)
            entry = tk.Entry(edit_window)
            entry.insert(0, row_data[
                len(labels_part_1) + len(labels_part_2) + len(labels_part_3) + len(labels_part_4) + idx])
            if label in readonly_fields:
                entry.config(state="readonly")
            entry.grid(row=len(labels_part_1) + len(labels_part_2) + len(labels_part_3) + len(labels_part_4) + idx + 5,
                       column=1, padx=10, pady=5)
            entries_part_5[label] = entry

        # 保存按钮
        def save_data():
            # 获取新的数据
            new_data = [
                *[entries_part_1[label].get() for label in labels_part_1],
                *[entries_part_2[label].get() for label in labels_part_2],
                *[entries_part_3[label].get() for label in labels_part_3],
                *[entries_part_4[label].get() for label in labels_part_4],
                *[entries_part_5[label].get() for label in labels_part_5]
            ]

            # 更新 Treeview 中的内容
            self.tree.item(item, values=new_data)

            # 更新 DataFrame 中对应的行
            row_index = self.tree.index(item) + (self.current_page - 1) * self.items_per_page  # 找到在原 DataFrame 中的索引
            self.df.loc[row_index] = new_data  # 使用新的数据更新 DataFrame

            # 关闭编辑窗口
            edit_window.destroy()
            print("Data saved successfully")

        save_button = tk.Button(edit_window, text="Save", command=save_data)
        save_button.grid(row=len(labels_part_1) + len(labels_part_2) + len(labels_part_3) + len(labels_part_4) + len(
            labels_part_5) + 5, column=0, columnspan=2, pady=10)

        # 弹出窗口居中显示
        edit_window.transient(self.frame.master)  # 使用根窗口作为父窗口
        edit_window.grab_set()
        edit_window.wait_window()  # 确保窗口显示后再关闭

    def create_pagination_controls(self):
        # 创建翻页控件
        pagination_frame = ttk.Frame(self.frame)
        pagination_frame.grid(row=3, column=0, pady=10, sticky="ew")  # 确保分页控件占满横向空间

        # Configure columns for centering buttons
        pagination_frame.grid_columnconfigure(0, weight=1)
        pagination_frame.grid_columnconfigure(1, weight=1)
        pagination_frame.grid_columnconfigure(2, weight=1)
        pagination_frame.grid_columnconfigure(3, weight=1)
        pagination_frame.grid_columnconfigure(4, weight=1)

        # 上一页按钮
        self.prev_button = ttk.Button(pagination_frame, text="Previous Page", command=self.prev_page)
        self.prev_button.grid(row=0, column=1, padx=10)

        # 分页信息
        self.page_label = ttk.Label(pagination_frame, text=f"Page {self.current_page} / {self.total_pages}",
                                    font=("Arial", 12))
        self.page_label.grid(row=0, column=2, padx=10)

        # 下一页按钮
        self.next_button = ttk.Button(pagination_frame, text="Next Page", command=self.next_page)
        self.next_button.grid(row=0, column=3, padx=10)

        # 更新按钮状态
        self.update_pagination_buttons()

    def update_pagination_buttons(self):
        # 根据当前页数更新翻页按钮状态
        if self.current_page == 1:
            self.prev_button["state"] = "disabled"
        else:
            self.prev_button["state"] = "normal"

        if self.current_page == self.total_pages:
            self.next_button["state"] = "disabled"
        else:
            self.next_button["state"] = "normal"

        # 更新分页信息
        self.page_label.config(text=f"Page {self.current_page} / {self.total_pages}")

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.populate_table()
            self.update_pagination_buttons()

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.populate_table()
            self.update_pagination_buttons()

    def generate_mock_data(self):
        # 生成 1000 条数据
        data = []
        for i in range(1000):
            data.append([
                f"Customer-{i}", random.choice(self.test_typs), f"2021-01-{i + 1}", f"Tester-{i}", f"2021-01-{i + 1}",
                f"Pattern-{i}", f"Test-{i}", f"Test-{i}", f"Remark-{i}", random.choice(["Schaum", "frei aufgehängt", "Unter Last"]),
                f"Remark-{i}", f"Test-{i}", f"Voltage-{i}", f"Duration-{i}", f"Type-{i}", f"Distance-{i}", f"Direction-{i}",
                f"Speed-{i}", f"Limit-{i}", f"Frequency-{i}", f"End-{i}"
            ])
        return data

    def query_order(self):
        # 获取输入内容
        motor_serial = self.sachnummer_entry.get()  # 获取 Motor Serial Number
        test_typ = self.test_typ_entry.get()

        # 如果两个输入框都有值，则使用 pandas 筛选
        if motor_serial and test_typ:
            filtered_df = self.df[(self.df["Motor Serial Number"].str.contains(motor_serial)) & (
                    self.df["Type of Measurement"] == test_typ)]

            if not filtered_df.empty:
                self.data = filtered_df.values.tolist()  # 转换为列表以显示
                self.total_pages = (len(self.data) + self.items_per_page - 1) // self.items_per_page
                self.current_page = 1  # 重新从第一页开始显示
                self.populate_table()  # 更新表格
                self.update_pagination_buttons()  # 更新翻页控件状态
                messagebox.showinfo("info", "Query successful")
            else:
                messagebox.showwarning("warn", "No results found")
        else:
            messagebox.showwarning("warn", "Please enter complete query information")

    def import_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.df = pd.read_csv(file_path)
            self.data = self.df.values.tolist()
            self.total_pages = (len(self.data) + self.items_per_page - 1) // self.items_per_page
            self.current_page = 1
            self.populate_table()
            self.update_pagination_buttons()
            messagebox.showinfo("info", "Data imported successfully")
