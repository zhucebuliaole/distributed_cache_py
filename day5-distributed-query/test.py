'''
Author: Qile Liang
Date: 2023-01-18 15:04:23
LastEditTime: 2023-01-18 17:31:30
LastEditors: Qile Liang
Description: 
FilePath: \distributed_cache_py\day5-distributed-query\test.py
Email: liangqile@outlook.com
'''

from tokenize import PseudoExtras
from typing import List
from cache_manager import Group
from http_server import http_server,Handler,API_Handler


db = {	"Tom":  "630",
	"Jack": "589",
	"Sam":  "567",}

def createGroup():
    def getter(key):
        print("search key {}".format(key))
        if key in db.keys:
            return db[key]
        else:
            print("{} not exist".format(key))
            return None
    return Group("scores",3,getter)
    

def startCacheServer(addr:str,addrs:List[str],pycache:Group):
    peers = http_server(addr)
    peers.Set(addrs)
    pycache.register_peers(peers)
    print("cache run in {}".format(addr))
    from http.server import HTTPServer
    server = HTTPServer(('localhost', int(addrs[-4:])), Handler)
    print('Starting cache server, use <Ctrl-C> to stop')
    server.serve_forever()

def startAPIServer(apiAddr: str, pycache : Group):
    from http.server import HTTPServer
    server = HTTPServer(('localhost', 8080), API_Handler)
    print('Starting api server, use <Ctrl-C> to stop')



if __name__ == '__main__':
    pass