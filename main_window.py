import tkinter
from tkinter import ttk

from PIL import ImageTk

from wallpaper import *


class ControlView:
    w_box = 600  # 期望图像显示的大小（窗口大小）
    h_box = 510
    LOCK = Lock()

    def __init__(self, win, pic=None):
        self.pic = pic
        self.main_window = win
        self.pic_label_height = ControlView.h_box - 45 - 122
        self.like_tag = tkinter.StringVar()

        # 显示图片Label
        self.tk_image = self.pic_data('loading.gif')  # 把PIL图像对象转变为Tkinter的PhotoImage对象  【转换格式，方便在窗口展示】
        self.image_lable = tkinter.Label(main_window, image=self.tk_image, height=self.pic_label_height, bg='black')
        self.image_lable.pack(fill=tkinter.X, side=tkinter.TOP)

        # 图片详情
        self.pic_info_text = tkinter.Text(main_window, spacing1=15, width=65,
                                          height=ControlView.h_box - self.pic_label_height,
                                          bg='black', fg='DeepSkyBlue')
        self.pic_info_text.pack(side=tkinter.LEFT)

        # 壁纸切换时间选择
        self.change_lable = tkinter.Label(main_window, text='自动切换壁纸间隔', width=35, bg='GreenYellow')
        self.change_lable.pack()

        self.change_com = ttk.Combobox(main_window)
        self.change_com['value'] = ('1分钟', '5分钟', '10分钟', '20分钟', '30分钟', '1小时', '3小时')
        self.change_com.set(self.change_time_conversion(second=Wallpaper.CHANGE_WALLPER_INTERVAL))
        self.change_com.bind('<<ComboboxSelected>>', self.select_time)
        self.change_com.config(state='readonly')
        self.change_com.pack()

        # 手动切换
        self.hand_button = tkinter.Button(main_window, text='手动切换', width=35, bg='GreenYellow',
                                          command=self.hand_change_button)
        self.hand_button.pack()

        # 标记喜欢
        like_rad = tkinter.Radiobutton(main_window, text='喜 欢', variable=self.like_tag, value='1', bg='DeepSkyBlue',
                                       width=35,
                                       indicatoron=False,
                                       selectcolor='DeepPink',
                                       command=self.set_like_tag)
        # 这里的command即是对应单选按钮的处理函数
        like_rad.pack(pady=1)

        unlike_rad = tkinter.Radiobutton(main_window, text='讨 厌', variable=self.like_tag, value='0', bg='DeepSkyBlue',
                                         width=35,
                                         indicatoron=False,
                                         selectcolor='DeepPink',
                                         command=self.set_like_tag)
        unlike_rad.pack(pady=1)

        nosense_rad = tkinter.Radiobutton(main_window, text='无 感', variable=self.like_tag, value='', bg='DeepSkyBlue',
                                          width=35,
                                          indicatoron=False,
                                          selectcolor='DeepPink',
                                          command=self.set_like_tag)
        nosense_rad.pack(pady=1)

        # self.refresh_view(self.pic)

    def change_time_conversion(self, second=None, select=None):
        if second is not None:
            if second < 60:
                return '%d秒' % second
            elif second < 3600:
                return '%d分钟' % (second / 60)
            else:
                return '%d小时' % (second / 3600)
        elif select is not None:
            if '分钟' in select:
                return int(select[:-2]) * 60
            elif '小时' in select:
                return int(select[:-2]) * 3600
            else:
                return None
        else:
            return None

    # 对一个pil_image对象进行缩放，让它在一个矩形框内，还能保持比例
    def resize(self, w_box, h_box, pil_image):  # 参数是：要适应的窗口宽、高、Image.open后的图片
        w, h = pil_image.size  # 获取图像的原始大小
        f1 = 1.0 * w_box / w
        f2 = 1.0 * h_box / h
        factor = min([f1, f2])
        width = int(w * factor)
        height = int(h * factor)
        return pil_image.resize((width, height), Image.ANTIALIAS)

    def pic_data(self, picfile):
        pil_image = Image.open(picfile)  # 以一个PIL图像对象打开  【调整待转图片格式】
        pil_image_resized = self.resize(ControlView.w_box, self.pic_label_height,
                                        pil_image)  # 缩放图像让它保持比例，同时限制在一个矩形框范围内  【调用函数，返回整改后的图片】
        return ImageTk.PhotoImage(pil_image_resized)

    def select_time(self, event):
        interval = self.change_time_conversion(select=self.change_com.get())
        print(interval)
        Wallpaper.CHANGE_WALLPER_INTERVAL = interval
        set_change_wallper_interval(interval)

    def hand_change_thread(self):
        self.hand_button['text'] = '下载中'
        self.hand_button.config(state=tkinter.DISABLED)
        random_set_wallpaper(True)
        self.refresh_view(True)
        self.hand_button['text'] = '手动切换'
        self.hand_button.config(state=tkinter.NORMAL)

    def hand_change_button(self):
        print('手动切换')
        t_hand = Thread(target=self.hand_change_thread, daemon=True)
        t_hand.start()

    def set_like_tag(self):
        select_tag = self.like_tag.get()
        if select_tag != self.pic.islike:
            print(select_tag)
            mark_like_tag(self.pic, self.like_tag.get())
            self.pic.islike = select_tag

    def refresh_view(self, hand_set=False):
        if hand_set:
            self.pic = Wallpaper.VIEW_HAND_PICTURES.get()
        else:
            self.pic = Wallpaper.VIEW_AUTO_PICTURES.get()
        # 更换详情
        self.pic_info_text.config(state=tkinter.NORMAL)
        self.pic_info_text.delete(1.0, tkinter.END)
        self.pic_info_text.insert(tkinter.INSERT,
                                  '路径：%s\n分辨率：%s\n文件大小：%s\n发布日期：%s' % (
                                      self.pic.file_path, self.pic.resolution_ratio, self.pic.file_size,
                                      self.pic.release_date))
        self.pic_info_text.config(state=tkinter.DISABLED)
        # 更换图片
        self.tk_image = self.pic_data(self.pic.file_path)
        self.image_lable.config(image=self.tk_image)
        # 更换喜欢标签
        self.like_tag.set(self.pic.islike)

    def refresh_thread(self):
        while True:
            self.refresh_view()


if __name__ == '__main__':
    # 核心程序 ====================================================
    # 创建图片文件夹
    if not os.path.exists(Picture.DOWNLOAD_DIR):
        os.mkdir(Picture.DOWNLOAD_DIR)

    # 爬虫线程
    t_spider = Thread(target=spider_thread, daemon=True)
    t_spider.start()
    # 预准备壁纸线程
    t_spare = Thread(target=prepare_wallpapers, daemon=True)
    t_spare.start()
    # 随机换壁纸
    t_wallpaper = Thread(target=set_wallpaper_thread, daemon=True)
    t_wallpaper.start()

    # 界面程序 ======================================================
    main_window = tkinter.Tk()  # 创建窗口，必须在ImageTk.PhotoImage()之前！
    main_window.geometry('%dx%d' % (ControlView.w_box, ControlView.h_box))  ## 规定窗口大小500*500像素
    main_window.resizable(False, False)  ## 规定窗口不可缩放

    # 设置窗口标题
    main_window.title('二次元壁纸')
    # 设置窗口图标
    main_window.iconbitmap('favicon.ico')
    control_view = ControlView(main_window)
    # 更新窗口
    t_refresh = Thread(target=control_view.refresh_thread, daemon=True)
    t_refresh.start()

    main_window.mainloop()
