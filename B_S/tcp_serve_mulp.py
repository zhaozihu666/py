from socket import *
from multiprocessing import *
from time import sleep

def dealWithClient(newSocket,destAddr):
    while True:
        recvData = newSocket.recv(1024)
        if len(recvData) > 0:
            print('recv[%s]:%s' % (str(destAddr), recvData))
        else:
            print('[%s]客户端已经关闭' % str(destAddr))
            break
    newSocket.close()

def main():
    serSocket = socket(AF_INET,SOCK_STREAM)
    serSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    localAddr = ('',7788)
    serSocket.bind(localAddr)
    serSocket.listen(5)

    try:
        while True:

            print('-----主进程，等待新客户端的到来-----')
            newSocket, destAddr = serSocket.accept()
            print('----主进程，接下来负责数据处理[%s]----' % str(destAddr))
            client = Process(target=dealWithClient,args=(newSocket,destAddr))
            client.start()

            newSocket.close()
    finally:
        serSocket.close()

if __name__ == '__main__':
    main()

