from PIL import Image, ImageTk
import tkinter
from tkinter import ttk

w_box = 600  # 期望图像显示的大小（窗口大小）
h_box = 520


# 对一个pil_image对象进行缩放，让它在一个矩形框内，还能保持比例
def resize(w_box, h_box, pil_image):  # 参数是：要适应的窗口宽、高、Image.open后的图片
    w, h = pil_image.size  # 获取图像的原始大小
    f1 = 1.0 * w_box / w
    f2 = 1.0 * h_box / h
    factor = min([f1, f2])
    width = int(w * factor)
    height = int(h * factor)
    return pil_image.resize((width, height), Image.ANTIALIAS)


def pic_data(pic, w_box, h_box):
    pil_image = Image.open(pic)  # 以一个PIL图像对象打开  【调整待转图片格式】
    pil_image_resized = resize(w_box, h_box, pil_image)  # 缩放图像让它保持比例，同时限制在一个矩形框范围内  【调用函数，返回整改后的图片】
    return pil_image_resized


def select_time(event):
    print(change_com.get())


def hand_change():
    print('手动切换')


def print_selection():
    print(tag.get())
    # 当点击Radiobutton时，标签中会显示对应你选择的选项


main_window = tkinter.Tk()  # 创建窗口，必须在ImageTk.PhotoImage()之前！
main_window.geometry('%dx%d' % (w_box, h_box))  ## 规定窗口大小500*500像素
main_window.resizable(False, False)  ## 规定窗口不可缩放

pictures = ['Gallery\\545140-1920x1080-yurucamp-kagamihara+nadeshiko-shima+rin-natori+youkai-long+hair-blush.png',
            'Gallery\\552593-4667x2625-fate+%28series%29-fategrand+order-jeanne+d%26%2339%3Barc+%28fate%29+%28all%29-jeanne+d%26%2339%3Barc+%28alter%29+%28fate%29-tsuki+no+i-min-long+hair.jpg']

pic_label_height = h_box - 45 - 122

# 显示图片Label
tk_image = ImageTk.PhotoImage(
    pic_data(pictures[0], w_box, pic_label_height))  # 把PIL图像对象转变为Tkinter的PhotoImage对象  【转换格式，方便在窗口展示】

image_lable = tkinter.Label(main_window, image=tk_image, height=pic_label_height, bg='black')
image_lable.pack(fill=tkinter.X, side=tkinter.TOP)

pic_info_text = tkinter.Text(main_window, spacing1=15, width=65, height=h_box - pic_label_height, bg='DeepSkyBlue')
pic_info_text.pack(side=tkinter.LEFT)

pic_info_text.insert(tkinter.INSERT,
         '路径：Gallery\\552593-4667x2625-fate+%28series%29-fategrand+order-jeanne+d%26%2339%3Barc+%28fate%29+%28all%29-jeanne+d%26%2339%3Barc+%28alter%29+%28fate%29-tsuki+no+i-min-long+hair.jpg\n分辨率：1920x1080\n文件大小：1.7MB\n发布日期：2018-07-25 17:41:00')
pic_info_text.config(state=tkinter.DISABLED)

# 壁纸切换时间选择
change_lable = tkinter.Label(main_window, text='切换壁纸间隔', width=35, bg='GreenYellow')
change_lable.pack()

change_com = ttk.Combobox(main_window)
change_com['value'] = ('1分钟', '5分钟', '10分钟', '20分钟', '30分钟', '1小时', '3小时')
change_com.current('0')
change_com.bind('<<ComboboxSelected>>', select_time)
change_com.config(state='readonly')
change_com.pack()

# 手动切换
hand_button = tkinter.Button(main_window, text='手动切换', width=35, bg='ForestGreen',

                    command=hand_change)
hand_button.pack()

# 标记喜欢
tag = tkinter.StringVar()
tag.set('')
like_rad = tkinter.Radiobutton(main_window, text='喜 欢', variable=tag, value='1', bg='DeepSkyBlue', width=35,
                         indicatoron=False,
                         selectcolor='DeepPink',
                         command=print_selection)
# 这里的command即是对应单选按钮的处理函数
like_rad.pack(pady=1)

unlike_rad = tkinter.Radiobutton(main_window, text='讨 厌', variable=tag, value='0', bg='DeepSkyBlue', width=35,
                         indicatoron=False,
                         selectcolor='DeepPink',
                         command=print_selection)
unlike_rad.pack(pady=1)

nosense_rad = tkinter.Radiobutton(main_window, text='无 感', variable=tag, value='', bg='DeepSkyBlue', width=35,
                         indicatoron=False,
                         selectcolor='DeepPink',
                         command=print_selection)
nosense_rad.pack(pady=1)


main_window.mainloop()
