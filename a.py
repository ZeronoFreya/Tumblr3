import asyncio
from asyncio import Queue as asQ
import random
import time

async def work(q2):
    # print('work',d)
    # await asyncio.sleep(2)
    # await q.put( {'id':d['id'],'fpath':d['fpath']} )
    # tumblrCtrl.downloadImg(d['http'], d['fpath'])
    # postMessage(f_hwnd, loadImgMsg, 0, 0)
    # return
    # for i in range(q2.qsize()):
    while True:
        # print(i)
        # if not q2.empty():
        #     d = await q2.get()
        #     print(d)
        # else:
        #     q2.task_done()
        d = await q2.get()
        r = random.randint(1,5)
        await asyncio.sleep( r )
        try:
            print(r,d)
        finally:
            q2.task_done()


async def run( t ):
    q2 = asQ()
    # tasks = []
    await asyncio.wait([q2.put(i) for i in t])
    tasks = [asyncio.ensure_future(work(q2))]
    # for d in t:
        # tasks.append( asyncio.ensure_future(work(q, d)) )
    # asyncio.wait(tasks)
    print('wait join')
    await q2.join()
    # postMessage(f_hwnd, loadImgMsg, 0, 0)
    print('end join')
    for task in tasks:
        task.cancel()
if __name__ == '__main__':
    t=[{'id': '163313406078[1]', 'http': 'https://68.media.tumblr.com/8f64f8f7885f57b02b66d59695d21003/tumblr_otcacsCHN21qgdydto1_250.jpg', 'fpath': 'D:\\Project\\GitHub\\Tumblr3\\imgTemp\\163313406078[1]_250.jpg'}, {'id': '163313235630[1]', 'http': 'https://68.media.tumblr.com/c663f97b89bd8ce44cf8d1bc777ed580/tumblr_otfszhN3Qf1s3f5u5o1_250.jpg', 'fpath': 'D:\\Project\\GitHub\\Tumblr3\\imgTemp\\163313235630[1]_250.jpg'}, {'id': '163312030869[1]', 'http': 'https://68.media.tumblr.com/a2761ea359be62d2cdf4aab6547db9cc/tumblr_ot4b4vpkhD1qgdydto1_250.jpg', 'fpath': 'D:\\Project\\GitHub\\Tumblr3\\imgTemp\\163312030869[1]_250.jpg'}, {'id': '163311979203[1]', 'http': 'https://68.media.tumblr.com/a4696ec707a8e12f5be2850cffcfe1bf/tumblr_otfs0tb7yq1s3f5u5o1_250.jpg', 'fpath': 'D:\\Project\\GitHub\\Tumblr3\\imgTemp\\163311979203[1]_250.jpg'}, {'id': '163310726341[1]', 'http': 'https://68.media.tumblr.com/e22b9d2bb31d4c582d889b79b8001d2e/tumblr_ot2n98vTa91qz9aigo1_250.jpg', 'fpath': 'D:\\Project\\GitHub\\Tumblr3\\imgTemp\\163310726341[1]_250.jpg'}]
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(run())
    # loop.close()
    try:
        loop.run_until_complete(run(t))
    except Exception as e:
        # print(asyncio.Task.all_tasks())
        # print(asyncio.gather(*asyncio.Task.all_tasks()).cancel())
        loop.stop()
        loop.run_forever()
    finally:
        loop.close()
    print('ww')