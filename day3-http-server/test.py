'''
Author: Qile Liang
Date: 2023-01-11 18:12:01
LastEditTime: 2023-01-11 18:39:04
LastEditors: Qile Liang
Description: 
FilePath: /distributed-cache/python-cache/day3-http-server/test.py
Email: liangqile@outlook.com
'''

import cache_manager

def getter(key):
    return key+"res"

a = getter
group = cache_manager.Group("test",3,a)
group.get("1")

from http.server import HTTPServer
import http_server


server = HTTPServer(('localhost', 8080), http_server.Handler)
server.serve_forever()