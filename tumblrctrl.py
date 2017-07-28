from multiprocessing import Process,Queue
import ctypes
import random
import asyncio
from os import path as osPath
from json import load as JLoad
from win32con import WM_USER
from tumblpy import Tumblpy

postMessage = ctypes.windll.user32.PostMessageW
loadImgListMsg = WM_USER+10
loadImgMsg = WM_USER+20
loadtest = WM_USER+30

async def wget(imgDoneQ, d, f_hwnd):
    r = random.randint(1,3)
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
    postMessage(f_hwnd, loadtest, 0, 0)
    return

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

class TumblrCtrl(object):
    def __init__(self, param):
        super(TumblrCtrl, self).__init__()
        print('创建Tumblr队列...')
        self.Gui_HWND = param['Gui_HWND']
        self.cfg = param['cfg']['tumblr']
        self.proxies = param['cfg']['proxies']
        self.call = param['call']
        self.target_folder = param['target_folder']
        self.imgListQ = Queue(1)
        self.imgDoneQ = Queue(50)
        with open('tumblr_credentials.json', 'r') as f:
            self.tumblr_key = JLoad(f)
        self.tumblr = Tumblpy(
            self.tumblr_key['consumer_key'],
            self.tumblr_key['consumer_secret'],
            self.tumblr_key['oauth_token'],
            self.tumblr_key['oauth_token_secret'],
            proxies=self.proxies
        )
        print('Over')

    def getDashboards(self):
        self.setTumblrLi()
        Process(target = asyncLoadTumblr, args = ( self.imgListQ, self.Gui_HWND )).start()

    def eachImgList(self, img_list ):
        print('eachImgList')
        tasks = []
        i = 0
        for d in img_list:
            # print(d)
            file_name = d['id'] + '_' + d['alt_sizes'].split("_")[-1]
            file_path = osPath.join( self.target_folder, file_name )
            self.call('setImgId', d['id'], i )
            i+=1
            if not osPath.isfile(file_path):
                # print(file_path)
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
        Process(target = asyncImgList, args = ( self.imgDoneQ, tasks, self.Gui_HWND )).start()
        return

    def setImgBg(self, id, fpath):
        print('setImgBg')
        self.call('setImgBg', id, fpath )

    def setTumblrLi(self):
        html = ''
        limit = self.cfg['dashboard_param']['limit']
        i = 0
        while i < limit:
            html += '<li.loading imgid="' + str(i) + '"></li>'
            i += 1
        self.call('appendImgLoading', html )

