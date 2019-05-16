import socket
import sys
from multiprocessing import Process
import re

class WSGIServer(object):

    addressFamily = socket.AF_INET
    socketType = socket.SOCK_STREAM
    requestQueueSize = 5

    def __init__(self, serverAddress):
        #create a socket
        self.listenSocket = socket.socket(self.addressFamily,self.sockerType)
        #allow wo repeat use the socket with port
        self.listenSocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR)

        #bind
        self.listenSocket.bind(serverAddress)
        #turn to the object and to get the queue length
        self.listenSocket.listen(self.requestQueueSize)
        self.servrName = "localhost"
        self.servrPort = serverAddress[1]

    def serveForever(self):
        #crycle to run the program serveclient and wait for the browserclient resquest
        while True:
            self.clientSocket, client_address = self.listenSocket.accept()
            newClinetProcess = Process(target= self.handleRequest)
            newClinetProcess.start()
            self.clientSocket.close()

    def setApp(self,application):
        #设置此WSGI服务器调用的应用程序入口函数
        self.application = application

    def handleRequest(self):
        self.recvData = self.clientSocket.recv(2014)
        requestHeaderLines = self.recvData.splitlines()
        for line in requestHeaderLines:
            print(line)

        httpRequestMethodLine = requestHeaderLines[0]
        getFileName = re.match("[^/]+(/[^ ]*)",httpRequestMethodLine).group(1)
        print("file name is ===>%s"%getFileName)

        if getFileName[-3:] != ".py":

            if getFileName == '/':
                getFileName = documentRoot + "/index.html"
            else:
                getFileName = documentRoot + getFileName
            print("file name is ==2>%s"%getFileName)

            try:
                f = open(getFileName)
            except IOError:
                responseHeaderLines = "HTTP/1.1 404 not found \r\n)"
                responseHeaderLines = "====sorry ,file not found===="
            else:
                responseHeaderLines = "http/1.1 200 OK\r\n"
                responseHeaderLines +="\r\n"
                responseBody = f.read()
                f.close()
            finally:
                response = responseHeaderLines +responseBody
                self.clientSocket.send(response)
                self.clientSocket.close()
        else:
            self.parseRequest()
            env = self.getEnviron()
            bodyContent = self.application(env, self.startResponse)
            self.finishResponse(bodyContent)

    def parseRequest(self):
        requestLine = self.recvData.splitlines()[0]
        requestLine = requestLine.rstrip('\r\n')
        self.requestMethod, self.path, self.requestVersion = requestLine.split(" ")
    def getEnviron(self):
        env = {}
        env['wsgi.version'] =(1,0)
        env['wsgi.input'] = self.recvData
        env['REQUEST_METHOD'] = self.requestMethod
        env['PATH_INFO'] =self.path
        return env


    def startResponse(self, status, response_headers, exc_info=None):
        serverHeaders = [
            ('Data', 'Tue, 31 Mar 2016 10:11:12 GMT'),
            ('Server', 'WSGIServer 0.2'),
        ]
        self.headers_set = [status, response_headers + serverHeaders]

    def finishResponse(self, bodyContent):
        try:
            status, response_headers = self.headers_set
            response = 'HTTP/1.1 {status}\r\n'.format(status=status)
            for header in response_headers:
                response += '{0}:{1}\r\n'.format(*header)
            response +='\r\n'
            for data in bodyContent:
                response += data

            self.clientSocket.send(response)
        finally:
            self.clientSocket.close()

#build serveclient port
serverAddr = (HOST, PORT) = '',8888
documentRoot = './html'
pythonRoot = './wsgipy'

def makeServer(serverAddr, application):
    server = WSGIServer(serverAddr)
    server.setApp(application)
    return server

def main():

    if len(sys.argv)< 2:
        sys.exit('请按照要求，制定模块名称：应用名称，例如 module:callable')
        appPath = sys.argv[1]
        module, appliaction = appPath.split(':')
        sys.path.insert(0, pythonRoot)
        module = __import__(module)
        appliaction = getattr(module, appliaction)
        httpd = makeServer(serverAddr,appliaction)
        print('WSGIServer: Serving HTTP on port %d ...\n'%PORT)
        httpd.serveForever()

if __name__ == '__main__':
    main()

