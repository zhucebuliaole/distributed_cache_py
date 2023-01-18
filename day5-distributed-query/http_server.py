'''
Author: Qile Liang
Date: 2023-01-11 16:08:59
LastEditTime: 2023-01-18 17:33:58
LastEditors: Qile Liang
Description: 
FilePath: \distributed_cache_py\day5-distributed-query\http_server.py
Email: liangqile@outlook.com
'''

from http.server import BaseHTTPRequestHandler
import multiprocessing
from urllib import parse,request
from urllib.request import Request, urlopen
from urllib.error import URLError
import cache_manager
from consistenthash import consistent_map

class http_getter:
    def __init__(self,baseURL) -> None:
        self.baseURL = baseURL
    
    def Get(self,group:str,key:str):
        url = self.baseURL+"/"+group+"/"+key
        req = Request(url)
        try:
            response = urlopen(req)
        except URLError as e:
            if hasattr(e, 'reason'):
                print('We failed to reach a server.')
                print('Reason: ', e.reason)
            elif hasattr(e, 'code'):
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
        else:
            return response.read()

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        # parsed_path = parse.urlparse(self.path)
        # message_parts = [
        #     'CLIENT VALUES:',
        #     'client_address={} ({})'.format(
        #         self.client_address,
        #         self.address_string()),
        #     'command={}'.format(self.command),
        #     'path={}'.format(self.path),
        #     'real path={}'.format(parsed_path.path),
        #     'query={}'.format(parsed_path.query),
        #     'request_version={}'.format(self.request_version),
        #     '',
        #     'SERVER VALUES:',
        #     'server_version={}'.format(self.server_version),
        #     'sys_version={}'.format(self.sys_version),
        #     'protocol_version={}'.format(self.protocol_version),
        #     '',
        #     'HEADERS RECEIVED:',
        # ]
        # for name, value in sorted(self.headers.items()):
        #     message_parts.append(
        #         '{}={}'.format(name, value.rstrip())
        #     )
        # message_parts.append('')
        # message = '\r\n'.join(message_parts)
        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()
        # path must be \basepath\group\key
        parts = self.path.split('/')
        parts = parts[1:]
        if len(parts) != 3:
            print("path must have basepath group and key") 
        elif parts[0]!="cache":
            print("error of basepath")
        print("cache run at {}".format(self.address_string()))
        group_name = parts[1]
        key = parts[2]
        group = cache_manager.get_group(group_name)
        if not group:
            print("group isn't exist")
            self.wfile.write("group isn't exist".encode('utf-8'))
            return
        data = group.get(key)
        self.wfile.write(data.string().encode('utf-8'))
        
        # self.wfile.write(message.encode('utf-8'))

class http_server:
    def __init__(self,address,basepath="/cache",port=8080,replicas=10) -> None:
        self.address = address
        self.defaultBasePath = basepath
        self.mu =  multiprocessing.Lock()
        self.peers = None 
        self.httpGetters = {}
        self.replicas = replicas
        from http.server import HTTPServer
        self.server = HTTPServer((address, port), Handler)
        self.server.serve_forever()
        print("server start. Address{} port{}".format(self.address,port))

    def Set(self,peers):
        with self.mu:
            self.peers = consistent_map(self.replicas)
            self.peers.add(peers)
            for peer in peers:
                self.httpGetters[peer] = http_getter(peer+self.defaultBasePath)
    
    def PickPeer(self,key:str):
        with self.mu:
            peer = self.peers.get(key)
            if peer!= None or peer!=self:
                print("Pick peer {}".format(peer))
                return self.httpGetters[peer]
            return 

class API_Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        # parsed_path = parse.urlparse(self.path)
        # message_parts = [
        #     'CLIENT VALUES:',
        #     'client_address={} ({})'.format(
        #         self.client_address,
        #         self.address_string()),
        #     'command={}'.format(self.command),
        #     'path={}'.format(self.path),
        #     'real path={}'.format(parsed_path.path),
        #     'query={}'.format(parsed_path.query),
        #     'request_version={}'.format(self.request_version),
        #     '',
        #     'SERVER VALUES:',
        #     'server_version={}'.format(self.server_version),
        #     'sys_version={}'.format(self.sys_version),
        #     'protocol_version={}'.format(self.protocol_version),
        #     '',
        #     'HEADERS RECEIVED:',
        # ]
        # for name, value in sorted(self.headers.items()):
        #     message_parts.append(
        #         '{}={}'.format(name, value.rstrip())
        #     )
        # message_parts.append('')
        # message = '\r\n'.join(message_parts)
        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()
        # path must be \basepath\group\key
        parts = self.path.split('/')
        parts = parts[1:]
        if parts[0]!="api":
            print("error of basepath")
        print("cache run at {}".format(self.address_string()))

        parameters = dict(qc.split("=") for qc in self.path.split("&"))
        key = parameters["key"]
        data = None
        self.wfile.write(data.string().encode('utf-8'))

if __name__ == '__main__':
    from http.server import HTTPServer

    server = HTTPServer(('localhost', 8080), Handler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
    