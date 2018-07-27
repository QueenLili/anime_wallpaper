import time
from queue import Queue
from threading import Thread

q = Queue(5)  # 指定队列大小


def prepare_wallpapers():
    for i in range(10):
        print('%d  put' % q.qsize())
        q.put(i)


# 预准备壁纸线程
t_spare = Thread(target=prepare_wallpapers)
t_spare.start()

while True:
    print('-----------------')
    print(q.get())
    time.sleep(1)
