# -*- coding: utf-8  -*-
# -*- author: jokker -*-


import tkinter as tk  # 使用Tkinter前需要先导入

window = tk.Tk()
window.title('My Window')
window.geometry('500x300')  # 这里的乘是小x

# 输入框
e1 = tk.Entry(window, show='*', font=(u'宋体', 14))  # 显示成密文形式
e2 = tk.Entry(window, show=None, font=(u'宋体', 14))  # 显示成明文形式
e1.pack()
e2.pack()

var = tk.StringVar()
l = tk.Label(window, textvariable=var, bg='green', fg='white', font=('Arial', 12), width=30, height=2)
l.pack()

var.set('123456')

# 第5步，主窗口循环显示
window.mainloop()
