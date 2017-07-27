"""Minimalistic PySciter sample for Windows."""
import json
import sciter
import ctypes
import random
import time
# import win32con
# import os

from win32con import WM_USER

from os import path as osPath, getcwd
from multiprocessing import Process,Pool,Manager
# from threading import Thread

import asyncio
from asyncio import Queue as asQ

ctypes.windll.user32.SetProcessDPIAware(2)
postMessage = ctypes.windll.user32.PostMessageW
loadImgListMsg = WM_USER+10
loadImgMsg = WM_USER+20
loadtest = WM_USER+30

def asyncLoadTumblr(imgListQ, f_hwnd):
    print("asyncLoadTumblr")
    # imgList = tumblrCtrl.loadImgList()
    imgList = [{
        'link_url': 'xx',
        'source_url': '',
        'id': str( random.randint(1,999999) ),
        'original_size': 'xx',
        'preview_size': 'x',
        'alt_sizes': 'x'
    },{
        'link_url': 'xx',
        'source_url': '',
        'id': str( random.randint(1,999999) ),
        'original_size': 'xx',
        'preview_size': 'x',
        'alt_sizes': 'x'
    },{
        'link_url': 'xx',
        'source_url': '',
        'id': str( random.randint(1,999999) ),
        'original_size': 'xx',
        'preview_size': 'x',
        'alt_sizes': 'x'
    },{
        'link_url': 'xx',
        'source_url': '',
        'id': str( random.randint(1,999999) ),
        'original_size': 'xx',
        'preview_size': 'x',
        'alt_sizes': 'x'
    },{
        'link_url': 'xx',
        'source_url': '',
        'id': str( random.randint(1,999999) ),
        'original_size': 'xx',
        'preview_size': 'x',
        'alt_sizes': 'x'
    }]
    imgListQ.put( imgList )
    # eachImgList( imgList )
    postMessage(f_hwnd, loadImgListMsg, 0, 0)
    return

# async def work(q2,imgDoneQ,f_hwnd):
#     # print('work',d)
#     # await asyncio.sleep(2)
#     # await q.put( {'id':d['id'],'fpath':d['fpath']} )
#     # tumblrCtrl.downloadImg(d['http'], d['fpath'])
#     # postMessage(f_hwnd, loadImgMsg, 0, 0)
#     # return
#     # for i in range(q2.qsize()):
#     while True:
#         # print(i)
#         d = await q2.get()
#         time.sleep( random.randint(1,5) )
#         try:
#             # tumblrCtrl.downloadImg(d['http'], d['fpath'])
#             imgDoneQ.put( {'id':d['id'],'fpath':d['fpath']} )
#             postMessage(f_hwnd, loadImgMsg, 0, 0)
#         finally:
#             q2.task_done()

# async def run(imgDoneQ, t, f_hwnd):
#     q2 = asQ()
#     # tasks = []
#     await asyncio.wait([q2.put(i) for i in t])
#     tasks = [asyncio.ensure_future(work(q2,imgDoneQ,f_hwnd))]
#     # for d in t:
#         # tasks.append( asyncio.ensure_future(work(q, d)) )
#     # asyncio.wait(tasks)
#     print('wait join')
#     await q2.join()
#     # postMessage(f_hwnd, loadImgMsg, 0, 0)
#     print('end join')
#     for task in tasks:
#         task.cancel()

async def wget(imgDoneQ, d, f_hwnd):
    r = random.randint(1,5)
    await asyncio.sleep( r )
    # print( r, host )
    imgDoneQ.put( {'id':d['id'],'fpath':d['fpath']} )
    postMessage(f_hwnd, loadImgMsg, 0, 0)
    return

def asyncImgList(imgDoneQ, t, f_hwnd):
    print('asyncImgList')
    loop = asyncio.get_event_loop()
    tasks = [wget(imgDoneQ, d, f_hwnd) for d in t]
    try:
        loop.run_until_complete( asyncio.wait(tasks) )
    except Exception as e:
        # print('0',asyncio.Task.all_tasks())
        # print('1',asyncio.gather(*asyncio.Task.all_tasks()).cancel())
        loop.stop()
        loop.run_forever()
    finally:
        loop.close()
    print('end')
    # for task in tasks:
        # task.cancel()
    # postMessage(f_hwnd, loadtest, 0, 0)
    return


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
        # self.pool = Pool()
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
                # self.pool.terminate()
                return self.eachImgList( self.imgListQ.get() )
        elif msg == loadImgMsg:
            print('loadImgMsg')
            # if not self.imgDoneQ.empty():
                # print(self.imgDoneQ.get())
                # return self.setImgBg( self.imgDoneQ.get() )
            d = self.imgDoneQ.get()
            # print(d)
            try:
                self.setImgBg( d['id'], d['fpath'] )
            finally:
                self.imgDoneQ.task_done()
        elif msg == loadtest:
            print("loadtest")
            self.pool.close()

    def document_close(self):
        print("close")
        self.pool.close()
        # self.pool.terminate()
        self.pool.join()
        return True

    def eachImgList(self, img_list ):
        print('eachImgList')
        # self.q1 = Manager().Queue()
        tasks = []
        i = 0
        for d in img_list:
            # print(d)
            file_name = d['id'] + '_' + d['alt_sizes'].split("_")[-1]
            file_path = osPath.join( self.target_folder, file_name )
            self.call_function('setImgId', d['id'], i )
            i+=1
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
    def setImgBg(self, id, fpath):
        print('setImgBg')
        self.call_function('setImgBg', id, fpath )

    def setTumblrLi(self):
        html = ''
        limit = self.cfg['tumblr']['dashboard_param']['limit']
        i = 0
        while i < limit:
            html += '<li.loading imgid="' + str(i) + '"></li>'
            i += 1
        self.call_function('appendImgLoading', html )
        pass
    def loadTumblr(self):
        # self.pool.terminate()
        # self.pool = Pool(processes=1)
        self.setTumblrLi()
        self.pool.apply_async(asyncLoadTumblr,args=(self.imgListQ, self.hwnd))
        pass

if __name__ == '__main__':
    frame = Frame()
    frame.load_file("Gui/main.html")
    frame.run_app()
