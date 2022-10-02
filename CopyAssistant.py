from pynput.keyboard import Controller, Key
import time
import tkinter as tk
from tkinter import messagebox
import threading


keyboard = Controller()
window = tk.Tk()
window.title('Crown You 拷贝助手')
window.geometry('720x280')
window.wm_attributes('-topmost', 1)
font = ('Noto Sans Mono', 11)
mid_font = ('Noto Sans Mono', 13)
colors = ['blue', 'green', 'purple', 'orange']
ind = 0
_continue = True
finished = True


def _stop():
    global _continue
    _continue = False


def call_stop():
    t2 = threading.Thread(target=_stop)
    t2.start()


def reset():
    text1.delete(1.0, 'end')


frm2 = tk.Frame(window)
frm2.pack()
label1 = tk.Label(frm2, text="请在下方输入要拷贝的文字:", font=mid_font)
label1.grid(row=1, column=1, padx=20)
button3 = tk.Button(frm2, text='重置文字', font=mid_font, command=reset)
button3.grid(row=1, column=2, padx=20)
button2 = tk.Button(frm2, text='停止输入', font=mid_font, command=call_stop, fg='red')
button2.grid(row=1, column=3, padx=20)
text1 = tk.Text(window, width=86, height=14, font=font)
text1.pack()
intro = '''欢迎使用 CrownYou 拷贝助手 3.0 版
下方的延迟时间可以修改，记得要输入正实数
点击“开始拷贝”后，按钮会变色，表示程序已开始运行，应在设定时间内将光标置于要输入的地方
软件开始拷贝文字时，如果发现输入错误，可以点击“停止输入”来终止当前进程
拷贝完成后，点击“重置文字”，即可输入新的内容啦'''
text1.insert('end', intro)


def _start():
    global ind, finished, _continue
    ind = (ind + 1) % 4
    button1.config(fg=colors[ind])
    _continue = True
    window.update()
    try:
        sec = float(entry1.get())
        if sec < 0:
            raise IOError
    except Exception:
        messagebox.showerror(title='数据错误', message='秒数应该为正实数')
        finished = True
        return 0
    time.sleep(sec)
    word = text1.get(1.0, 'end').rstrip("\n")
    for i in word:
        if not _continue:
            finished = True
            break
        if i == "\n":
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
        else:
            keyboard.press(i)
            keyboard.release(i)
        time.sleep(0.02)
        finished = True


def call_start():
    global finished
    if finished:
        finished = False
        t1 = threading.Thread(target=_start)
        t1.start()


frm1 = tk.Frame(window)
frm1.pack()

label2 = tk.Label(frm1, text="单击“开始拷贝”后", font=mid_font)
label2.grid(row=1, column=1)
entry1 = tk.Entry(frm1, width=4, font=mid_font)
entry1.grid(row=1, column=2)
entry1.insert("end", '2')
label3 = tk.Label(frm1, text="秒开始运行，请在时间内将光标放于需要拷贝的地方", font=mid_font)
label3.grid(row=1, column=3)
button1 = tk.Button(frm1, text="开始拷贝", font=mid_font, command=call_start, fg=colors[ind])
button1.grid(row=1, column=4, padx=15)

window.mainloop()
