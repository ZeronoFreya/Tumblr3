import asyncio
import random
async def wget(host):
    # for x in range(1,3):
    r = random.randint(0,9)
    await asyncio.sleep( r )
    print( r, host )

print('start')
loop = asyncio.get_event_loop()
tasks = [wget(host) for host in ['www.sina.com', 'www.sohu.com', 'www.163.com']]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
print('end')