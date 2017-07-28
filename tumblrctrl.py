from multiprocessing import Process,Queue
class TumblrCtrl(object):
    def __init__(self):
        super(TumblrCtrl, self).__init__()
        print('创建Tumblr队列...')
        self.imgListQ = Queue(1)
        self.imgDoneQ = Queue(50)
        print('Over')
