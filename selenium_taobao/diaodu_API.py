import time
from multiprocessing import Process
from cookiespool.api import app
from cookiespool.config import *
from cookiespool.generator import *
from cookiespool.tester import *

class Scheduler(object):
    @staticmethod
    #----------------------------------------------------------------------
    def valid_cookie(cycle=CYCLE):
        while Ture:
            print('Cookies 检测到进程开始运行')
            try:
                for website,cls in TESTER_MAP.items():
                    tester = eval(cls + '(website="' + website + '")')
                    tester.run()
                    print("Cookies检测完成")
                    del tester
                    time.sleep(cycle)
            except Exception as e:
                print(e.args)
    @staticmethod
    #----------------------------------------------------------------------
    def gengerate_cookie(cycle=CYCLE):
        while Ture:
            print('Cookies 生成进程开始运行')
            try:
                for website,cls in GENERATOR_MAP.items():
                    generator = eval(cls + '(website="' + website + '")')
                    generator.run()
                    print("Cookies生成完成")
                    generator.close()
                    time.sleep(cycle)
            except Exception as e:
                print(e.args)
    
    @staticmethod
    #----------------------------------------------------------------------
    def api():
        print('Cookies 检测到进程开始运行')
        app.run(host=API_HOST,port=API_PORT)
    def run(self):
        if API_PROCESS:
            api_process = Process(target = Scheduler.api)
            api_process.start()
        if GENERATOR_PROCESS:
            generator_process = Process(target = Scheduler.generator_cookie)
            generator_process.start()
        if VALID_PROCESS:
            valid_process = Process(target = Scheduler.valid_cookie)
            valid_process.start()        
GENERATOR_MAP = {
    'weibo':'WeiboCookiesGenerator'
}
TESTER_MAP = {
    'weibo':'WeiboValidTester'
}

GENERATOR_PROCESS = True
VALID_PROCESS = False
API_PROCESS = True
                
            
        
        