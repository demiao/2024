import random
import ttkbootstrap as ttk
from tkinter import Scrollbar, messagebox, filedialog
import tkinter as tk
import pandas as pd
import chardet


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

        # Dokumentation
        # 1.Kunde==‘Kunden‘
        # 2,Tpy-kurzbezeichnung==‘Typ‘
        # 3.Fertigungsdatum自己输入
        # 4.Prüfer 自己输入
        # 5.Prüfungsdatum==‘Prüfdatum‘
        # 6.Prüfung==‘Type of Measurment ‘
        # 7.Musternummer== ‘Musternummer’
        # 8.Prüfnummer  自己输入

        # Prüfling
        # 1.	Prüfling-Nr.==Prüfdatum_Musternummer_W711Bue_空着
        # 2.	Bemerkung 自己输入
        #
        # Prüfaufbau
        # 1.	Prüfaufbau
        # 2.	Last==‘SOLL Prüflast BODY ‘
        #
        # Prüfvorgabe
        # 1.	Prüfvorschrift==‘PV-Nummer ‘
        # 2.	Prüfspannung==‘SOLL Prüfspannung AIR ‘
        # 3.	Test dauer==‘Prüfzeit IST AIR ‘
        # 4.	Prüf-Art dropdawn 自己输入
        # 5.	Mikrofon Abstand==‘SOLL MikrofonAbstand AIR ‘
        # 6.	Drehrichtung==‘Drehrichtung ‘
        # 7.	Drehzahl==‘SOLL Drehzahl BODY ‘
        #
        # Toleranzprüfung
        # 1.	Luftschall-Summengrenzwert==‘Summenpegel SOLL AIR ‘
        # 2.	Luftschall-Summe-Straffrequenz==‘Frequenzband min AIR ‘
        # 3.	Luftschall-Summe-Endfrequenz==‘Frequenzband Max AIR‘

        self.test_typs = ["A", "Q", "Z", "Null-Serie", "Claim（TKU）", "Sonder", "BlockForce"]
        self.column_mapping = {
            "Prüfnummer": "Prüfnummer",
            "Motorsachnummer": "Motorsachnummer",
            "Prüfdatum": "Prüfungsdatum",
            "Kunde": "Kunden",
            "Typ-Kurzbezeichung": "Typ",
            "Prüfungsdatum": "Prüfdatum",
            "Musternummer": "Musternummer",
            "Prüfling-Nr": "Prüfdatum_Musternummer_W711Bue_空着",
            "Last": "SOLL Prüflast BODY",
            "Prüfvorschrift": "PV-Nummer",
            "Prüfspannung": "SOLL Prüfspannung AIR",
            "Test dauer": "Prüfzeit IST AIR",
            "Mikrofon Abstand": "SOLL MikrofonAbstand AIR",
            "Drehrichtung": "Drehrichtung",
            "Drehzahl": "SOLL Drehzahl BODY",
            "Luftschall-Summegrenzwert": "Summenpegel SOLL AIR",
            "Luftschall-Summe-Straffrequenz": "Frequenzband min AIR",
            "Luftschall-Summe-Endfrequenz": "Frequenzband Max AIR"
        }

        self.column_mapping_reverse = {v: k for k, v in self.column_mapping.items()}
        self.display_columns = [
            "Prüfnummer", "Motorsachnummer", "Prüfdatum", "Type of Measurment", "Musternummer", "PV-Nummer"
        ]
        self.df = self.generate_mock_data()  # 创建 pandas DataFrame
        # 重命名
        self.df.rename(columns=self.column_mapping_reverse, inplace=True)
        self.filtered_df = pd.DataFrame()
        # 展示页的数据
        self.items_per_page = 50  # 每页显示 50 条
        self.current_page = 1  # 当前页数
        self.total_pages = (len(self.df) + self.items_per_page - 1) // self.items_per_page  # 计算总页数
        self.current_page_data = self.df[:self.items_per_page]  # 当前页的数据
        self.create_order_query_page()

    def create_order_query_page(self):
        # 创建顶部布局区域，输入框、下拉框、按钮
        top_frame = ttk.Frame(self.frame)
        top_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        # 输入框和下拉框
        ttk.Label(top_frame, text="Motorsachnummer:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10,
                                                                               sticky="e")
        self.motorsachnummer_entry = ttk.Entry(top_frame, font=("Arial", 12), width=30)
        self.motorsachnummer_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        ttk.Label(top_frame, text="Type of Measurement:", font=("Arial", 12)).grid(row=0, column=2, padx=10, pady=10,
                                                                                   sticky="e")

        self.test_typ_entry = ttk.Combobox(top_frame, font=("Arial", 12), width=30,
                                           values=self.test_typs)
        self.test_typ_entry.grid(row=0, column=3, padx=10, pady=10, sticky="w")

        # 清空按钮
        clear_button = ttk.Button(top_frame, text="Clear", command=self.clear_query)
        clear_button.grid(row=0, column=4, padx=10, pady=10, sticky="w")

        # 查询按钮
        query_button = ttk.Button(top_frame, text="Query", command=self.query_order)
        query_button.grid(row=0, column=5, padx=10, pady=10, sticky="w")

        # 导入文件按钮
        import_button = ttk.Button(top_frame, text="Import File", command=self.import_file)
        import_button.grid(row=0, column=6, padx=10, pady=10, sticky="w")

        # 导出文件按钮
        export_button = ttk.Button(top_frame, text="Export File", command=self.export_file)
        export_button.grid(row=0, column=7, padx=10, pady=10, sticky="w")

        # 设置全局的表格行高
        style = ttk.Style()
        style.configure("Treeview", rowheight=40)

        # 确保顶部框架自动调整大小，分配最小权重
        self.frame.grid_rowconfigure(0, weight=0)

        # 创建表格部分
        self.create_table()

        # 添加翻页按钮和分页信息
        self.create_pagination_controls()

    def clear_query(self):
        self.motorsachnummer_entry.delete(0, tk.END)
        self.test_typ_entry.set("")
        self.current_page = 1
        self.total_pages = (len(self.df) + self.items_per_page - 1) // self.items_per_page
        self.current_page_data = self.df[:self.items_per_page]
        self.filtered_df = pd.DataFrame()
        self.populate_table()
        self.update_pagination_buttons()

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

        self.tree = ttk.Treeview(self.frame, columns=self.display_columns, show="headings")

        for col in self.display_columns:
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
        if not self.filtered_df.empty:
            current_page_data = self.filtered_df[start_index:end_index]
        else:
            current_page_data = self.df[start_index:end_index]
        current_page_data.fillna("", inplace=True)
        # 填充当前页数据
        for index, row in current_page_data.iterrows():
            row = row.tolist()
            self.tree.insert("", "end", values=row)

    def on_row_double_click(self, event):
        # 获取双击的行
        items = self.tree.selection()
        if not items:
            return
        item = items[0]
        row_data = self.tree.item(item, "values")
        # 获取测试id
        test_id = row_data[0]  # Prüfnummer
        # 从数据集中获取完整的行数据
        row_data = self.df[self.df["Prüfnummer"] == test_id]
        # 转字典
        row_data = row_data.to_dict(orient="records")[0]

        # 创建一个新的窗口
        edit_window = tk.Toplevel(self.frame)

        # 设置窗口大小和布局
        edit_window.resizable(False, False)
        edit_window.title("Edit Row Data")

        # 不可编辑字段的列表
        readonly_fields = [
            "Motorsachnummer","Kunde", "Typ-Kurzbezeichung", "Prüfer", "Prüfungsdatum", "Musternummer", "Prüfnummer",
            "Prüfling-Nr", "Prüfvorschrift", "Prüfspannung", "Test dauer",
            "Prüf-Art", "Mikrofon Abstand", "Drehrichtung", "Drehzahl", "Luftschall-Summegrenzwert",
            "Luftschall-Summe-Straffrequenz", "Luftschall-Summe-Endfrequenz"
        ]

        # 用于存储所有输入框，以便在保存时提取数据
        entries = {}

        # 设置每个部分的标签和字段
        sections = {
            "Dokumentation": ["Motorsachnummer","Kunde", "Typ-Kurzbezeichung", "Fertigungsdatum", "Prüfer", "Prüfungsdatum",
                              "Musternummer", "Prüfnummer"],
            "Prüfling": ["Prüfling-Nr", "Prüfling Bemerkung"],
            "Prüfaufbau": ["Prüfaufbau", "Prüfaufbau Bemerkung"],
            "Prüfvorgaben": ["Prüfvorschrift", "Prüfspannung", "Test dauer", "Prüf-Art", "Mikrofon Abstand",
                             "Drehrichtung", "Drehzahl"],
            "Toleranzprüfung": ["Luftschall-Summegrenzwert", "Luftschall-Summe-Straffrequenz",
                                "Luftschall-Summe-Endfrequenz"]
        }

        # 创建每个部分的框架
        for section, labels in sections.items():
            # 添加分区标题
            frame_section = tk.Frame(edit_window, padx=10, pady=10, relief="groove", borderwidth=2)
            frame_section.pack(fill="x")

            # 设置分区标题
            tk.Label(frame_section, text=section, font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=4,
                                                                                   sticky="w")

            # 水平布局每个字段
            for idx, label in enumerate(labels):
                tk.Label(frame_section, text=label).grid(row=1 + idx // 2, column=(idx % 2) * 2, padx=5, pady=5,
                                                         sticky="w")
                if section == "Prüfaufbau" and label == "Prüfaufbau":
                    # 添加下拉框
                    entry = ttk.Combobox(frame_section, width=30, values=["Schaum", "frei aufgehängt", "Unter Last"])
                    entry.grid(row=1 + idx // 2, column=(idx % 2) * 2 + 1, padx=5, pady=5)
                    entry.set(row_data.get(label, ""))
                else:
                    entry = tk.Entry(frame_section, width=30)
                    entry.grid(row=1 + idx // 2, column=(idx % 2) * 2 + 1, padx=5, pady=5)
                    entry.insert(0, row_data.get(label, ""))  # 填充数据

                # 如果是只读字段
                if label in readonly_fields:
                    entry.config(state="readonly")

                # 保存每个字段的输入框到 entries 字典中
                entries[label] = entry

        # 保存按钮的布局
        def save_data():
            # 从每个输入框中提取新数据
            new_data = {}
            for label, entry in entries.items():
                if entry.cget("state") == "readonly":
                    continue
                elif entry.get() in ["NaN", "nan", None, ""]:
                    new_data[label] = ""
                else:
                    new_data[label] = entry.get()

            # 更新数据框中的对应行
            for label, value in new_data.items():
                self.df.loc[self.df["Prüfnummer"] == test_id, label] = value

            # 更新 Treeview 显示
            self.populate_table()

            # 关闭编辑窗口
            edit_window.destroy()
            print("Data saved successfully")

        save_button = tk.Button(edit_window, text="Save", command=save_data)
        save_button.pack(pady=20)

        # 居中窗口
        edit_window.transient(self.frame.master)
        edit_window.grab_set()
        edit_window.wait_window()

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
            dic = {}
            for display_column in self.column_mapping.keys():
                if display_column == "Prüfnummer":
                    dic[display_column] = f"Test-{i}"
                elif display_column == "Type of Measurment":
                    dic[display_column] = random.choice(self.test_typs)
                else:
                    dic[display_column] = random.randint(1000, 9999)

            data.append(dic)
        data = pd.DataFrame(data)
        # "Fertigungsdatum", "Bemerkung", "Prüfaufbau"
        data["Prüfungsdatum"] = pd.to_datetime(data["Prüfungsdatum"], unit="D", origin="2021-01-01")
        data["Prüfling Bemerkung"] = ""
        data["Prüfaufbau Bemerkung"] = ""
        return data

    def query_order(self):
        # 获取输入内容
        motor_serial = self.motorsachnummer_entry.get()  # 获取 Motor Serial Number
        test_typ = self.test_typ_entry.get()

        # 如果两个输入框都有值，则使用 pandas 筛选
        if motor_serial and test_typ:
            self.filtered_df = self.df[(self.df["Motorsachnummer"] == motor_serial) & (
                    self.df["Type of Measurment"] == test_typ)]

            if not self.filtered_df.empty:
                self.current_page_data = self.filtered_df[:self.items_per_page]
                self.total_pages = (len(self.filtered_df) + self.items_per_page - 1) // self.items_per_page
                self.current_page = 1  # 重新从第一页开始显示
                self.populate_table()  # 更新表格
                self.update_pagination_buttons()  # 更新翻页控件状态
                messagebox.showinfo("info", "Query successful")
            else:
                messagebox.showwarning("warn", "No results found")
        else:
            messagebox.showwarning("warn", "Please enter complete query information")

    def refresh_table(self):
        # 清空表格
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.df.fillna("", inplace=True)
        # 获取当前页数据
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page
        page_data = self.df.iloc[start_idx:end_idx]

        # 插入新数据
        for _, row in page_data.iterrows():
            self.tree.insert("", "end", values=row.tolist())

    def import_file(self):
        # 打开文件选择对话框，限制文件类型为 xlsx 和 csv
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")],
            title="Select a file"
        )
        if file_path:
            try:
                if file_path.endswith('.xlsx'):
                    # 读取 Excel 文件
                    new_data = pd.read_excel(file_path)
                elif file_path.endswith('.csv'):
                    # 读取 CSV 文件
                    with open(file_path, 'rb') as f:
                        result = chardet.detect(f.read())
                        encoding = result['encoding']
                    new_data = pd.read_csv(file_path, encoding=encoding)
                else:
                    messagebox.showerror("Error", "Unsupported file format.")
                    return
                self.df = new_data  # 更新 DataFrame
                self.df.rename(columns=self.column_mapping_reverse, inplace=True)  # 重命名列
                self.current_page = 1  # 重置到第一页
                self.total_pages = (len(self.df) + self.items_per_page - 1) // self.items_per_page
                self.refresh_table()  # 刷新表格
                messagebox.showinfo("Success", "File imported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while importing the file:\n{e}")

    def export_file(self):
        # 打开文件保存对话框，限制文件类型为 xlsx 和 csv
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",  # 默认文件扩展名
            filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")],
            title="Save the file as"
        )

        if file_path:
            print(file_path)
            try:
                if not (file_path.endswith('.xlsx') or file_path.endswith('.csv')):
                    # 根据选定的文件类型自动添加扩展名
                    if file_path.endswith('.xlsx'):
                        file_path += '.xlsx'
                    else:
                        file_path += '.csv'
                self.df.rename(columns=self.column_mapping, inplace=True)  # 重命名列
                self.df.fillna("", inplace=True)  # 填充空值
                if file_path.endswith('.xlsx'):
                    # 导出为 Excel 文件
                    self.df.to_excel(file_path, index=False)
                elif file_path.endswith('.csv'):
                    # 导出为 CSV 文件
                    self.df.to_csv(file_path, index=False, encoding='utf-8-sig')

                messagebox.showinfo("Success", "File exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while exporting the file:\n{e}")
