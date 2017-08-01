from multiprocessing import Process,Queue
import ctypes
# import random
# import requests
import aiohttp
import asyncio
from common import gets
from os import path as osPath
from json import load as JLoad
from win32con import WM_USER
from tumblpy import Tumblpy

postMessage = ctypes.windll.user32.PostMessageW
loadImgListMsg = WM_USER+10
loadImgMsg = WM_USER+20
loadtest = WM_USER+30



def asyncImgList(imgDoneQ, t, f_hwnd, proxies):
    '''协程下载列表中图片'''
    async def stream_download( client, imgDoneQ, d, f_hwnd, prox ):
        async with client.get( d['http'], proxy='http://127.0.0.1:61274', timeout=10 ) as response:
            if response.status != 200:
                print('error')
                return
            with open(d['fpath'], 'ab') as file:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    file.write(chunk)
        imgDoneQ.put( {'id':d['id'],'fpath':d['fpath']} )
        postMessage(f_hwnd, loadImgMsg, 0, 0)

    print('asyncImgList')
    client = aiohttp.ClientSession()
    loop = asyncio.get_event_loop()
    tasks = [stream_download(client, imgDoneQ, d, f_hwnd, proxies) for d in t]
    try:
        loop.run_until_complete( asyncio.wait(tasks) )
    except Exception as e:
        print('0',asyncio.Task.all_tasks())
        print('1',asyncio.gather(*asyncio.Task.all_tasks()).cancel())
    finally:
        loop.stop()
        loop.run_forever()
        loop.close()
    print('end')
    # postMessage(f_hwnd, loadtest, 0, 0)
    return

def mkMainDict( d, preview_size, alt_sizes ):
    data = []
    for v in d["posts"]:
        t = {
            'link_url'        : gets(v, 'link_url', ''),
            'source_url'        : gets(v, 'source_url', '')
        }
        index = 1
        for i in v['photos']:
            t['id'] = str(v['id']) + '[' + str(index) + ']'
            t['original_size'] = gets(i, 'original_size.url', '')
            t['preview_size'] = gets(i, 'alt_sizes.' + str(preview_size) + '.url', '')
            t['alt_sizes'] = gets(i, 'alt_sizes.' + str(alt_sizes) + '.url', '')
            data.append(t.copy())
            index += 1
    return data

def asyncLoadTumblr(imgListQ, f_hwnd, tumblr, param):
    '''获取图片列表'''
    print("asyncLoadTumblr")
    p = param['posts_param'].copy()
    p['limit'] *= 5
    print(p)
    # dashboard = tumblr.dashboard( param['dashboard_param'] )
    dashboard = tumblr.posts('kuvshinov-ilya.tumblr.com', None, p)
    if not dashboard:
        return
    param['dashboard_param']['offset'] += p['limit']
    imgList = mkMainDict( dashboard, param['preview_size'], param['alt_sizes'] )
    # imgList = [{
    #     'link_url': 'xx',
    #     'source_url': '',
    #     'id': str( random.randint(1,999999) ),
    #     'original_size': 'xx',
    #     'preview_size': 'x',
    #     'alt_sizes': 'x'
    # }]
    for d in imgList:
        imgListQ.put( d )
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
        self.imgListQ = Queue()
        self.imgDoneQ = Queue(50)
        self.imglist = {
            'dashboard' : 0
        }
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
        if self.imgListQ.qsize() < self.cfg['dashboard_param']['limit']:
            print('getList')
            Process(target = asyncLoadTumblr, args = ( self.imgListQ, self.Gui_HWND, self.tumblr, self.cfg )).start()
        else:
            postMessage(self.Gui_HWND, loadImgListMsg, 0, 0)
            pass
        # Process(target = self.asyncLoadTumblr, args = (self.imgListQ,)).start()

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
                self.setImgBg(d['id'], file_path)
                pass
        if tasks:
            Process(target = asyncImgList, args = ( self.imgDoneQ, tasks, self.Gui_HWND, self.proxies )).start()
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


