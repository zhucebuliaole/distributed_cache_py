'''
Author: Qile Liang
Date: 2023-01-09 17:28:41
LastEditTime: 2023-01-09 17:28:41
LastEditors: Qile Liang
Description: 
FilePath: /distributed-cache/python-cache/day2-single-node/lru/lru.py
Email: liangqile@outlook.com
'''
'''
Author: Qile Liang
Date: 2023-01-08 17:26:10
LastEditTime: 2023-01-09 16:41:43
LastEditors: Qile Liang
Description: 
FilePath: /distributed-cache/python-cache/day1-lru/lru.py
Email: liangqile@outlook.com
'''
import sys 
sys.path.append("..")
import utils.Dlink as Dlink

class Cache:
    def __init__(self,maxsize,callback=None) -> None:
        self.max_size = maxsize
        self.cur_size = 0
        self.d_link = Dlink.DLinkList()
        self.cache_map = dict()
        self.callback = callback

    def get(self,key):
        if key in self.cache_map:
            # node = self.cache_map[key]
            # value = node.item
            # if node.next:
            #     node.next.prev = node.prev
            # if node.prev:
            #     node.prev.next = node.next
            node = self.cache_map[key]
            value = self._update_node(node)
            del node
            self.d_link.append(value,key)
            self.cache_map[key] = self.d_link.get_tail()
        else:
            value = None
        return value
    
    def cache_disuse(self):
        # disuse the first cache item
        key = self.d_link._head.key
        value = self.d_link._head.item
        self.d_link.remove_head()
        del self.cache_map[key]
        self.cur_size-=1
        if self.callback:
            self.callback(key,value)

    def add(self,key,value):
        if key in self.cache_map:
            node = self.cache_map[key]
            value = self._update_node(node)
            # value = node.item
            # if node.next:
            #     node.next.prev = node.prev
            # if node.prev:
            #     node.prev.next = node.next
            # del node
        
        self.d_link.append(value,key)
        self.cache_map[key] = self.d_link.get_tail()
        self.cur_size+=1
        if self.cur_size>self.max_size:
            self.cache_disuse()
            self.cur_size-=1
    
    def _update_node(self,node):
            value = node.item
            if node==self.d_link._head:
                self.d_link._head=self.d_link._head.next
            if node==self.d_link._tail:
                self.d_link._tail=self.d_link._tail.prev
                
            if node.next:
                node.next.prev = node.prev
            if node.prev:
                node.prev.next = node.next
            del node
            return value

        

        
