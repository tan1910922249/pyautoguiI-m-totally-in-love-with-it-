import tkinter as tk
import threading
from pynput import mouse

# 全局变量
coordinates = []
recording = False
save_on_exit = False  # 新增标志，用于控制在关闭时保存坐标

# 鼠标监听器
class MouseListener:
    def __init__(self):
        self.listener = None

    def start(self):
        global coordinates, recording
        if not recording:
            self.listener = mouse.Listener(on_click=self.on_click)
            self.listener.start()
            recording = True

    def stop(self):
        global coordinates, recording
        if recording:
            self.listener.stop()
            self.listener = None
            coordinates = []
            recording = False

    def on_click(self, x, y, button, pressed):
        global coordinates
        if button == mouse.Button.left and pressed:
            coordinates.append((x, y))

# 创建tkinter窗口
def create_window(exit_program=None):
    window = tk.Tk()
    window.title("Mouse Click Logger")

    # 创建按钮和文本区域
    start_button = tk.Button(window, text="Start Recording", command=listener.start)
    start_button.pack()

    stop_button = tk.Button(window, text="Stop Recording", command=listener.stop)
    stop_button.pack()

    # 定义 clear_coordinates 函数
    def clear_coordinates():
        global coordinates
        coordinates = []
        update_text_widget()  # 更新文本区域以反映清除后的状态

    clear_button = tk.Button(window, text="Clear Coordinates", command=clear_coordinates)
    clear_button.pack()

    exit_button = tk.Button(window, text="Exit Program", command=exit_program)
    exit_button.pack()

    # 设置快捷键
    window.bind("<Control-s>", lambda event: listener.start())
    window.bind("<Control-q>", lambda event: listener.stop())
    window.bind("<Control-e>", lambda event: exit_program())  # 绑定Ctrl+E作为退出快捷键

    text_widget = tk.Text(window, height=10, width=50)
    text_widget.pack()

    # 更新文本区域
    def update_text_widget():
        text_widget.delete('1.0', tk.END)
        for coord in coordinates:
            text_widget.insert(tk.END, f"({coord}, {coord[1]})\n")
        window.after(1000, update_text_widget)
    # 关闭程序的函数
    def exit_program():
        global save_on_exit
        save_on_exit = True  # 设置标志，表示在退出时要保存坐标
        window.quit()  # 调用quit方法来触发窗口关闭
        if save_on_exit:
            with open('mouse_coordinates.txt', 'w') as file:
                for coord in coordinates:
                    file.write(f"({coord}, {coord[1]})\n")

    # 注册窗口关闭事件
    window.protocol("WM_DELETE_WINDOW", exit_program)

    return window, text_widget
    # 注册窗口关闭事件
    window.protocol("WM_DELETE_WINDOW", exit_program)

    # 启动窗口更新线程
    update_text_widget()

    return window, text_widget

# 主函数
def main():
    global listener, window, text_widget
    listener = MouseListener()
    window, text_widget = create_window()
    window.mainloop()

    # 检查是否需要在退出时保存坐标
    if save_on_exit:
        with open('mouse_coordinates.txt', 'w') as file:
            for coord in coordinates:
                file.write(f"({coord}, {coord[1]})\n")

if __name__ == "__main__":
    main()