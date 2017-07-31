"""Minimalistic PySciter sample for Windows."""
# import json
import sciter
import ctypes

# import time
# import win32con
# import os
from json import load as JLoad
from win32con import WM_USER

from os import path as osPath, getcwd, mkdir as osMkdir
# from multiprocessing import Process,Queue
# from threading import Thread

# import asyncio
# from asyncio import Queue as asQ

from tumblrctrl import TumblrCtrl

ctypes.windll.user32.SetProcessDPIAware(2)
postMessage = ctypes.windll.user32.PostMessageW
loadImgListMsg = WM_USER+10
loadImgMsg = WM_USER+20
loadtest = WM_USER+30

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
        self.cfg = {"tumblr":{"alt_sizes":-3,"preview_size":-4,"dashboard_param":{"limit":5,"offset":0},"posts_param":{"limit":5,"offset":0}},"proxies":{}}
        with open('data.json', 'r') as f:
            self.cfg.update( JLoad(f) )
        self.current_folder = getcwd()
        self.target_folder = osPath.join(self.current_folder, 'imgTemp')
        if not osPath.isdir(self.target_folder):
            osMkdir(self.target_folder)
        self.download_folder = osPath.join(self.current_folder, 'download')
        if not osPath.isdir(self.download_folder):
            osMkdir(self.download_folder)
        # print(self.cfg)

    def _document_ready(self, target):
        return
        self.tumblrCtrl = TumblrCtrl({
            'call'          : self.call_function,
            'cfg'           : self.cfg,
            'Gui_HWND'      : self.hwnd,
            'target_folder' : self.target_folder
        })
        self.tumblrCtrl.getDashboards()

    def on_message(self, hwnd, msg, wparam, lparam):
        if msg == loadImgListMsg:
            print("loadImgListMsg")
            try:
                d = self.tumblrCtrl.imgListQ.get()
                return self.tumblrCtrl.eachImgList( d )
            except Exception as e:
                raise e
        elif msg == loadImgMsg:
            print('loadImgMsg')
            try:
                d = self.tumblrCtrl.imgDoneQ.get()
                self.tumblrCtrl.setImgBg( d['id'], d['fpath'] )
            except Exception as e:
                raise e
        elif msg == loadtest:
            print("loadtest")

    def document_close(self):
        print("close")
        return True




    def loadTumblr(self):
        print('loadTumblr')
        if not self.tumblrCtrl:
            self.tumblrCtrl = TumblrCtrl({
                'call'          : self.call_function,
                'cfg'           : self.cfg,
                'Gui_HWND'      : self.hwnd,
                'target_folder' : self.target_folder
            })
        self.tumblrCtrl.getDashboards()
        pass

if __name__ == '__main__':
    frame = Frame()
    frame.load_file("Gui/main.html")
    frame.run_app()
