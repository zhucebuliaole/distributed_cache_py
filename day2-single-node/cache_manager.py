'''
Author: Qile Liang
Date: 2023-01-09 18:19:43
LastEditTime: 2023-01-11 17:59:53
LastEditors: Qile Liang
Description: 
FilePath: /distributed-cache/python-cache/day2-single-node/cache_manager.py
Email: liangqile@outlook.com
'''
from abc import ABC, abstractmethod
import multiprocessing
from cache import cache
from byteview import byte_view
# class Getter(ABC):
#     @abstractmethod
#     def Get(self,key):
#         pass 

mu = multiprocessing.Lock()
groups = {}
multiprocessing.RLock
class Group():
    def __init__(self,name,cache_size,getter) -> None:
        with mu:
            self.name = name 
            self.mainCache = cache(cache_size)
            self.getter = getter
            groups[name]=self
    
    def get(self,key):
        if key == "":
            print("need a key")
        v = self.mainCache.get(key)
        if v:
            print("cache hit")
            return v
        else:
            print("data dont exist")
            
        return self.load(key)
    
    def load(self,key):
        return self.getLocally(key)
    
    def getLocally(self,key):
        data = self.getter(key)
        value = byte_view(data)
        self.populate_cache(key,value)
        return value
    
    def populate_cache(self,key,value):
        self.mainCache.add(key,value)
    
def get_group(self,name):
    with mu:
        g = groups[name]
        return g
