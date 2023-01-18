'''
Author: Qile Liang
Date: 2023-01-09 18:19:43
LastEditTime: 2023-01-18 16:11:41
LastEditors: Qile Liang
Description: 
FilePath: \distributed_cache_py\day5-distributed-query\cache_manager.py
Email: liangqile@outlook.com
'''
from abc import ABC, abstractmethod
import multiprocessing
from cache import cache
from byteview import byte_view
from http_server import http_getter
# class Getter(ABC):
#     @abstractmethod
#     def Get(self,key):
#         pass 

mu = multiprocessing.Lock()
groups = dict()
multiprocessing.RLock
class Group():
    def __init__(self,name,cache_size,httpgetter:callable) -> None:
        with mu:
            self.name = name 
            self.mainCache = cache(cache_size)
            self.getter = httpgetter
            self.peers = None
            groups[name]=self

    def register_peers(self,peers):
        # 将 实现了 PeerPicker 接口的 HTTPPool 注入到 Group 中。
        if self.peers:
            print("RegisterPeerPicker called more than once")
        self.peers = peers
    
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
        # return self.getLocally(key)
        if self.peers:
            peer = self.peers.PickPeer(key)
            if peer:
                value = self.get_from_peer(peer,key)
                print("load data from peer:{} by key:{}".format(peer,key))
                return value
        return self.getLocally(key)
    
    def getLocally(self,key):
        data = self.getter(key)
        value = byte_view(data)
        self.populate_cache(key,value)
        return value
    
    def populate_cache(self,key,value):
        self.mainCache.add(key,value)
    
    def get_from_peer(self,peer : http_getter,key):
        # get data from other nodes by peerGetter
        data = peer.Get(self.name,key)
        return data


def get_group(name):
    with mu:
        if name not in groups.keys():
            return None
        g = groups[name]
        return g
        