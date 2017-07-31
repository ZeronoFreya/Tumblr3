from multiprocessing import Process,Queue

def main():
    Process(target = asyncLoadTumblr, args = ( self.imgListQ, self.Gui_HWND, self.tumblr, self.cfg )).start()
    pass
if __name__ == '__main__':
    main()