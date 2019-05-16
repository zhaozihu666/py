import requests
from lxml import etree
from queue import Queue
import threading
import json

class thread_crawl(threading.Thread):
    """
    抓取线程类
    """
    def __init__(self, threadID, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.q = q


    def run(self):
        print("Starting"+self.threadID)
        self.qiushi_spider()
        print("Exxiting",self.threadID)


    def qiushi_spider(self):
        # page = 1
        while  True:
            if self.q.empty():
                break
            else:
                page = self.q.get()
                print("qiushi_spider=",self.threadID,'page=',str(page))
            url = 'http://www.qiushibaike.com/8hr/page/' + '/'
            headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
                'Accept-Language':'zh-CN,zh;q=0.8'
            }
            timeout = 4
            while timeout > 0:
                timeout -= 1
                try:
                    content = requests.get(url,headers=headers)
                    data_queue.put(content.text)
                    break
                except Exception as e :
                    print("qiushi-spider",e)
            if timeout < 0:
                print("timeout",url)

class Thread_Parser(threading.Thread):
    """
    页面解析类：
    """
    def __init__(self,threadID,queue, lock, f):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.queue = queue
        self.lock = lock
        self.f = f


    def run(self):
        print("starting",self.threadID)
        global total, exitFlag_Parser
        while not exitFlag_Parser:
            try:
                """
                调用队列对象的get()方法从对头删除并返回一个项目，可选参数为block，默认为True
                如果队列为空且block为true，get()就调用线程暂停，直到有项目可做
                如果队列为空且block为False,队列将引发Empty异常
                """
                item = self.queue.get(False)
                if not item:
                    pass
                self.parse_data(item)
                self.queue.task_done()
                print("thread_parser=", self.threadID,',total=',total)
            except:
                pass
        print('Exiting',self.threadID)


    def parse_data(self,item):
        """
        解析网页函数
        :param item: 网页内容
        :return:
        """
        global  total
        try:
            html = etree.HTML(item)
            result = html.xpath('//div[contains(@id,"qiushi_tag")]')
            for site in result:
                try:
                    imgUrl = site.xpath('.//img/@src')[0]
                    title = site.xpath('.//h2')[0].text
                    content = site.xpath('.//div/[@class="content"]/span')[0].text.strip()
                    vote = None
                    comments = None
                    try:
                        vote = site.xpath('.//i')[0].text
                        comments = site.xpath('.//i')[1].text
                    except:
                        pass
                    result ={
                        'imgUrl':imgUrl,
                        'title':title,
                        'content':content,
                        'vote':vote,
                        'comments':comments,
                    }

                    with self.lock:
                        # print ("write %s" % json.dumps(result))
                        self.f.write(json.dumps(result,ensure_ascii=False).encode('utf-8') + "\n")

                except Exception as e:
                    print('site in result',e)
        except Exception as e:
            print('parse-data',e)
            with self.lock:
                total += 1

data_queue = Queue()
exitFlag_Parser = False
lock = threading.Lock()
total = 0

def main():
    output = open('qiushibaike.json','a')

    pageQueue = Queue(50)
    for page in range(1,11):
        pageQueue.put(page)
    crawlthreads = []
    crawllist = ["craw-1","craw-2","craw-3"]

    for threadID in crawllist:
        thread = thread_crawl(threadID, pageQueue)
        thread.start()
        crawlthreads.append(thread)

    parserthreads = []
    parserlist = ["paser-1","paser-2","paser-3"]
    for threadID in parserlist:
        thread = Thread_Parser(threadID, data_queue,lock,output)
        thread.start()
        parserthreads.append(thread)

    while not pageQueue.empty():
        pass

    for t in crawlthreads:
        t.join()

    while not data_queue.empty():
        pass

    global exitFlag_Parser
    exitFlag_Parser = True

    for t in parserthreads:
        t.join()

    print("Exiting Main Thread")
    with lock:
        output.close()

if __name__ == '__main__':
    main()