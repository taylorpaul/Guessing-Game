##Class Notes on Multi-Threading:

import queue
import threading
#import urllib2
import time
import sched

#Called by each thread
def get_url(i,lock,q,url):
    lock.acquire
    print("This is a new thread ", i, "\n")
    q.put(url)
    #q.put(urllib2.urlopen(url).read())
    lock.release()

def hello():
    print ("hello, world")

theurls = ["https://google.com", "http://yahoo.com", "http://www.nps.edu"]

q = queue.Queue()
lock = threading.Lock()

i = 0
for u in theurls:
    t=threading.Thread(target=get_url, args = (i, lock, q, u))
    #t.daemon = True
    i+=1
    t.start()

t=threading.Timer(30.0, hello)
t.start()

time.sleep(1)
s = q.qsize()

for i in range(0,s):
    c=q.get()
    print(c)