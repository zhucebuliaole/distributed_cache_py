'''
Author: Qile Liang
Date: 2023-01-09 17:29:02
LastEditTime: 2023-01-10 15:30:55
LastEditors: Qile Liang
Description: 
FilePath: /distributed-cache/python-cache/day2-single-node/cache.py
Email: liangqile@outlook.com
'''

from lru.lru import Cache
import multiprocessing 
class cache:
    def __init__(self,maxsize) -> None:
        self.mu = multiprocessing.Lock()
        self.lru = None
        self.cacheBytes = maxsize
    
    def add(self,key,value):
        with self.mu:
            if not self.lru:
                self.lru = Cache(self.cacheBytes)
            self.lru.add(key,value)
    
    def get(self,key):
        with self.mu:
            if not self.lru:
                return
            return self.lru.get(key)