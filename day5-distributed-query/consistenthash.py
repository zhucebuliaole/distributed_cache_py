'''
Author: Qile Liang
Date: 2023-01-13 15:53:51
LastEditTime: 2023-01-17 18:24:14
LastEditors: Qile Liang
Description: consistent hash class has get and add method
FilePath: \distributed_cache_py\day5-distributed-query\consistenthash.py
Email: liangqile@outlook.com
'''


class consistent_map:
    def __init__(self,replicas,hash_func=hash) -> None:
        self.hash = hash_func
        self.replicas = replicas
        self.keys = []
        self.hash_map = {}
    
    def add(self,keys):
        for key in keys:
            for i in range(self.replicas):
                hash = self.hash(str(i)+key)
                self.keys.append(hash)
                self.hash_map[hash]=key
        self.keys.sort()

    def get(self,key):
        if not self.keys:
            print("have no keys now")
            return ""
        
        hash =self.hash(key)
        index = None
        try:
            index = next(i for i,v in enumerate(self.keys) if v>=hash)
        except StopIteration:
            index = 0
        return self.hash_map[self.keys[index]]
