import multiprocessing
class FloatChannel(object):
    def __init__(self, maxsize):
        self.buffer = multiprocessing.RawArray('d', maxsize)
        self.buffer_len = multiprocessing.Value('i')
        self.empty = multiprocessing.Semaphore(1)
        self.full = multiprocessing.Semaphore(0)
    def send(self, values):
        # 等待缓冲区为空的信号
        self.empty.acquire()
        n = len(values)
        self.buffer_len = n
        self.buffer[:n] = values
        # 设置缓冲区已满的标记
        self.full.release()
    def recv(self):
        self.full.acquire()
        # 复制缓冲区中的值，注意可以使用切片语法
        values = self.buffer[:self.buffer_len.value]
        # 设置缓冲区已空的标记
        self.empty.release()
        return values

def consumer(count , fc):
    for i in range(count):
        fc.recv()

if __name__ == '__main__':
    fc = FloatChannel(100000)
    p = multiprocessing.Process(target=consumer, args=(1000, fc))
    p.start()

    values = [float(x) for x in range(100000)]
    for i in range(1000):
        fc.send(values)
    print ("Produce done")
    p.join()