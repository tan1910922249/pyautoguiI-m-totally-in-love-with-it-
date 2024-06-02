import pyautogui
import time
import threading
import tkinter as tk
from datetime import datetime

# 全局变量用于存储坐标
coordinates = []

class CoordinateLogger:
    def __init__(self, root):
        self.root = root
        self.recording = False  # 记录状态标志
        self.coordinates_label = tk.Label(root, text="No coordinates recorded yet")
        self.coordinates_label.pack()

        # 创建一个文本框来显示坐标
        self.coordinates_text = tk.Text(root, height=10, width=50)
        self.coordinates_text.pack()

        # 创建一个按钮，用于开始记录坐标
        self.start_button = tk.Button(root, text="Start Logging", command=self.start_recording)
        self.start_button.pack()

        # 创建一个按钮，用于停止记录坐标和保存到文件
        self.stop_button = tk.Button(root, text="Stop Logging and Save", command=self.stop_recording)
        self.stop_button.pack()

        # 创建一个按钮，用于清除坐标记录
        self.clear_button = tk.Button(root, text="Clear Log", command=self.clear_log)
        self.clear_button.pack()

        # 设置快捷键
        self.root.bind('<Control-s>', self.start_recording)  # Ctrl+S 开始记录
        self.root.bind('<Control-q>', self.stop_recording)   # Ctrl+Q 停止记录
        self.root.bind('<Control-w>', self.close_program)   # Ctrl+W 关闭程序

        # 绑定鼠标左键点击事件
        self.root.bind('<Button-1>', self.log_coordinate)  # 当用户点击窗口时记录坐标

    def start_recording(self, event=None):
        global coordinates  # 使用全局变量
        coordinates = []     # 清空之前的坐标记录
        self.recording = True
        self.start_button.config(state=tk.DISABLED)  # 禁用开始按钮
        self.stop_button.config(state=tk.NORMAL)     # 启用停止按钮
        self.coordinates_label.config(text="Recording...")

    def stop_recording(self, event=None):
        global coordinates  # 使用全局变量
        self.recording = False
        self.start_button.config(state=tk.NORMAL)    # 启用开始按钮
        self.stop_button.config(state=tk.DISABLED)   # 禁用停止按钮
        self.save_coordinates_to_file()
        self.coordinates_label.config(text=f"Total coordinates: {len(coordinates)}")

    def log_coordinate(self, event):
        global coordinates  # 使用全局变量
        if self.recording:
            current_time = datetime.now().strftime("%H:%M:%S")
            x, y = pyautogui.position()
            coordinates.append((current_time, x, y))
            self.update_log()

    def update_log(self):
        self.coordinates_text.delete('1.0', tk.END)  # 清除文本框内容
        for time, x, y in coordinates:
            self.coordinates_text.insert(tk.END, f"{time} - Coordinates: ({x}, {y})\n")

    def save_coordinates_to_file(self):
        global coordinates  # 使用全局变量
        if not coordinates:
            print("No coordinates to save.")
            return

        with open("coordinates.txt", "w") as file:
            for time, x, y in coordinates:
                file.write(f"{time} - Coordinates: ({x}, {y})\n")
        print("Coordinates saved to coordinates.txt")

    def clear_log(self, event=None):
        global coordinates  # 使用全局变量
        coordinates = []
        self.coordinates_text.delete('1.0', tk.END)  # 清除文本框内容
        self.coordinates_label.config(text="No coordinates recorded yet")

    def close_program(self, event):
        self.root.destroy()  # 关闭程序

# 创建应用程序窗口
root = tk.Tk()
app = CoordinateLogger(root)
root.mainloop()
# import pyautogui
# import time
# import pyperclip
# import itertools
# import keyboard
# pyautogui.FAILSAFE = True
# pyautogui.PAUSE = 3.5
# import tkinter as tk
# from datetime import datetime
# import tkinter as tk
# from datetime import datetime
#
