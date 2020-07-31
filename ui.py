import tkinter as tk
from tkinter import *
from tkinter import filedialog


from nltk import data
print(data.find('.'))
#设计文件上传
def upload():
    selectFile = tk.filedialog.askopenfilename()  # askopenfilename 1次上传1个；askopenfilenames1次上传多个
    e1.insert(0, selectFile)

#设计结果下载
def download():
    print("download")

#退出
def exit():
    window.destroy()

def match():
    print('match')


# 第1步，实例化object，建立窗口window
window = tk.Tk()

# 第2步，给窗口的可视化起名字
window.title('通讯作者匹配系统')

# 第3步，设定窗口的大小(长 * 宽)
window.geometry('1000x800')  # 这里的乘是小x

# 第4步，在图形界面上设定并放置标签
l = tk.Label(window, text='通讯作者匹配系统', bg='green', font=('Arial', 12), width=30, height=2)
# 说明： bg为背景，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高

l.pack()  # Label内容content区域放置位置，自动调节尺寸
# 放置lable的方法有：1）l.pack(); 2)l.place();

# 第5步，在窗口界面设置放置Button按键
b1 = tk.Button(window, text='上传文件', font=('Arial', 12), width=10, height=1, command=upload)
b2 = tk.Button(window, text='下载匹配结果', font=('Arial', 12), width=10, height=1, command=download)
#在图形界面上设定输入框控件entry并放置控件
e1 = tk.Entry(window, show=None, font=('Arial', 12),width=50)   # 显示成明文

b4 = tk.Button(window, text='匹配', font=('Arial', 12), width=10, height=1, command=match)
b1.place(x=100,y=50)
e1.place(x=230,y=55)

b2.place(x=650, y=550)
b4.place(x=650, y=500)


l2 = tk.Label(window, text='使用说明：\n1.将需要匹配的文件导入到系统中\n2.点击下载按钮可以得到拥有匹配信息excel文件\n3.在系统中可以查看匹配结果图', font=('Arial', 12), height=4, fg='red')
l2.place(x=400, y=650)

b3 = tk.Button(window, text='返回', font=('Arial', 12), width=10, height=1, command=exit)
b3.place(x=650, y=600)

# 第6步，主窗口循环显示
window.mainloop()
# 注意，loop因为是循环的意思，window.mainloop就会让window不断的刷新，如果没有mainloop,就是一个静态的window,传入进去的值就不会有循环，mainloop就相当于一个很大的while循环，有个while，每点击一次就会更新一次，所以我们必须要有循环
# 所有的窗口文件都必须有类似的mainloop函数，mainloop是窗口文件的关键的关键。