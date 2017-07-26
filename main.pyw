"""Minimalistic PySciter sample for Windows."""
import json
import sciter
import ctypes
import win32con
# import os

from os import path as osPath, getcwd
from multiprocessing import Process,Pool,Manager
# from threading import Thread

import asyncio
from asyncio import Queue as asQ

ctypes.windll.user32.SetProcessDPIAware(2)
postMessage = ctypes.windll.user32.PostMessageW
loadImgListMsg = win32con.WM_USER+10
loadImgMsg = win32con.WM_USER+20

def asyncLoadTumblr(imgListQ, f_hwnd):
    print("asyncLoadTumblr")
    # imgList = tumblrCtrl.loadImgList()
    imgList = [{'link_url': 'http://kitkhsh69.tumblr.com/tagged/%E6%9F%B3%E7%BE%8E%E7%A8%80', 'source_url': '', 'id': '163313406078[1]', 'original_size': 'https://68.media.tumblr.com/8f64f8f7885f57b02b66d59695d21003/tumblr_otcacsCHN21qgdydto1_1280.jpg', 'preview_size': 'https://68.media.tumblr.com/8f64f8f7885f57b02b66d59695d21003/tumblr_otcacsCHN21qgdydto1_400.jpg', 'alt_sizes': 'https://68.media.tumblr.com/8f64f8f7885f57b02b66d59695d21003/tumblr_otcacsCHN21qgdydto1_250.jpg'}, {'link_url': '', 'source_url': 'https://yamato2520.tumblr.com/post/163247811228/yurina-ゆりな', 'id': '163313235630[1]', 'original_size': 'https://68.media.tumblr.com/c663f97b89bd8ce44cf8d1bc777ed580/tumblr_otfszhN3Qf1s3f5u5o1_1280.jpg', 'preview_size': 'https://68.media.tumblr.com/c663f97b89bd8ce44cf8d1bc777ed580/tumblr_otfszhN3Qf1s3f5u5o1_400.jpg', 'alt_sizes': 'https://68.media.tumblr.com/c663f97b89bd8ce44cf8d1bc777ed580/tumblr_otfszhN3Qf1s3f5u5o1_250.jpg'}, {'link_url': 'http://www.dmm.co.jp/digital/videoa/-/detail/=/cid=snis00944/loltumblrlol-001', 'source_url': '', 'id': '163312030869[1]', 'original_size': 'https://68.media.tumblr.com/a2761ea359be62d2cdf4aab6547db9cc/tumblr_ot4b4vpkhD1qgdydto1_540.jpg', 'preview_size': 'https://68.media.tumblr.com/a2761ea359be62d2cdf4aab6547db9cc/tumblr_ot4b4vpkhD1qgdydto1_400.jpg', 'alt_sizes': 'https://68.media.tumblr.com/a2761ea359be62d2cdf4aab6547db9cc/tumblr_ot4b4vpkhD1qgdydto1_250.jpg'}, {'link_url': '', 'source_url': 'https://yamato2520.tumblr.com/post/163247439028/yuikawa-misaki-唯川みさき', 'id': '163311979203[1]', 'original_size': 'https://68.media.tumblr.com/a4696ec707a8e12f5be2850cffcfe1bf/tumblr_otfs0tb7yq1s3f5u5o1_1280.jpg', 'preview_size': 'https://68.media.tumblr.com/a4696ec707a8e12f5be2850cffcfe1bf/tumblr_otfs0tb7yq1s3f5u5o1_400.jpg', 'alt_sizes': 'https://68.media.tumblr.com/a4696ec707a8e12f5be2850cffcfe1bf/tumblr_otfs0tb7yq1s3f5u5o1_250.jpg'}, {'link_url': 'http://img.bakufu.jp/wp-content/uploads/2017/07/170714b_0012.jpg', 'source_url': 'http://destrudo.tumblr.com/post/163247366353/170714b0012jpg', 'id': '163310726341[1]', 'original_size': 'https://68.media.tumblr.com/e22b9d2bb31d4c582d889b79b8001d2e/tumblr_ot2n98vTa91qz9aigo1_1280.jpg', 'preview_size': 'https://68.media.tumblr.com/e22b9d2bb31d4c582d889b79b8001d2e/tumblr_ot2n98vTa91qz9aigo1_400.jpg', 'alt_sizes': 'https://68.media.tumblr.com/e22b9d2bb31d4c582d889b79b8001d2e/tumblr_ot2n98vTa91qz9aigo1_250.jpg'}]
    imgListQ.put( imgList )
    # eachImgList( imgList )
    postMessage(f_hwnd, loadImgListMsg, 0, 0)
    return

def asyncImgList(imgDoneQ, t, f_hwnd):
    async def work(q2):
        # print('work',d)
        # await asyncio.sleep(2)
        # await q.put( {'id':d['id'],'fpath':d['fpath']} )
        # tumblrCtrl.downloadImg(d['http'], d['fpath'])
        # postMessage(f_hwnd, loadImgMsg, 0, 0)
        # return
        for i in range(q2.qsize()):
        # while True:
            if not q2.empty():
                d = await q2.get()
                print(d)
                # tumblrCtrl.downloadImg(d['http'], d['fpath'])
                # imgDoneQ.put( {'id':d['id'],'fpath':d['fpath']} )
                # postMessage(f_hwnd, loadImgMsg, 0, 0)

    async def run():
        q2 = asQ()
        # tasks = []
        await asyncio.wait([q2.put(i) for i in t])
        tasks = [asyncio.ensure_future(work(q2))]
        # for d in t:
            # tasks.append( asyncio.ensure_future(work(q, d)) )
        # asyncio.wait(tasks)
        print('wait join')
        await q2.join()
        postMessage(f_hwnd, loadImgMsg, 0, 0)
        print('end join')
        for task in tasks:
            task.cancel()

    print('asyncImgList')
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(run())
    # loop.close()
    try:
        loop.run_until_complete(run())
    except Exception as e:
        # print(asyncio.Task.all_tasks())
        # print(asyncio.gather(*asyncio.Task.all_tasks()).cancel())
        loop.stop()
        loop.run_forever()
    finally:
        loop.close()


class Frame(sciter.Window):
    def __init__(self):
        '''
            ismain=False, ispopup=False, ischild=False, resizeable=True,
            parent=None, uni_theme=False, debug=True,
            pos=None,  pos=(x, y)
            size=None
        '''
        super().__init__(ismain=True, debug=True)
        self.set_dispatch_options(enable=True, require_attribute=False)

    def _document_ready(self, target):
        # Set window title based on <title> content, if any
        print('创建队列...')
        self.imgListQ = Manager().Queue(1)
        self.imgDoneQ = Manager().Queue(50)
        print('Over')
        print('开启进程池...')
        self.pool = Pool(processes=1)
        print('Over')
        self.current_folder = getcwd()
        self.target_folder = osPath.join(self.current_folder, 'imgTemp')
        # self.target_folder='imgTemp'
        # if self._title_changed:
        #     return
        # root = sciter.Element(target)
        # title = root.find_first('html > head > title')
        # if title:
        #     self.set_title(title.get_text())

        # self.root = self.get_root()
        # self.ul = self.root.find_first('#ul')
        self.cfg = {"tumblr":{"alt_sizes":-3,"preview_size":-4,"dashboard_param":{"limit":5,"offset":0},"posts_param":{"limit":5,"offset":0}},"proxies":{}}
        with open('data.json', 'r') as f:
            self.cfg.update( json.load(f) )
        pass

        # new_loop = asyncio.new_event_loop()
        # t = Thread(target=do_some_work, args=(self.imgDoneQ,))
        # t.start()
        # asyncio.run_coroutine_threadsafe(do_some_work(self.imgDoneQ), new_loop)

    def on_message(self, hwnd, msg, wparam, lparam):
        if msg == loadImgListMsg:
            print("loadImgListMsg")
            if not self.imgListQ.empty():
                # print(self.q.get())
                # return
                return self.eachImgList( self.imgListQ.get() )
        elif msg == loadImgMsg:
            print('loadImgMsg')
            if not self.imgDoneQ.empty():
                print(self.imgDoneQ.get())

    def eachImgList(self, img_list ):
        print('eachImgList')
        # self.q1 = Manager().Queue()
        tasks = []
        for d in img_list:
            # print(d)
            file_name = d['id'] + '_' + d['alt_sizes'].split("_")[-1]
            file_path = osPath.join( self.target_folder, file_name )
            self.call_function('setImgId', d['id'] )
            if not osPath.isfile(file_path):
                print(file_path)
                # html = htmlTemplate.format( d['id'], 'img/loading.png', d['original_size'], d['preview_size'] )
                # self.call_function('appendImgList', html )
                tasks.append({
                    'id': d['id'],
                    'http': d['alt_sizes'],
                    'fpath': file_path
                })
            else:
                # html = htmlTemplate.format( d['id'], file_path, d['original_size'], d['preview_size'] )
                # self.call_function('appendImgList', html )
                pass
            self.pool.apply_async(asyncImgList,args=(self.imgDoneQ, tasks, self.hwnd))

        return

    def setTumblrLi(self):
        html = ''
        limit = self.cfg['tumblr']['dashboard_param']['limit']
        i = 0
        while i < limit:
            html += '<li.loading></li>'
            i += 1
        self.call_function('appendImgLoading', html )
        pass
    def loadTumblr(self):
        self.setTumblrLi()
        self.pool.apply_async(asyncLoadTumblr,args=(self.imgListQ, self.hwnd))
        pass

if __name__ == '__main__':
    frame = Frame()
    frame.load_file("Gui/main.html")
    frame.run_app()
