'''
Author: Qile Liang
Date: 2023-01-09 17:42:00
LastEditTime: 2023-01-10 15:58:44
LastEditors: Qile Liang
Description: 
FilePath: /distributed-cache/python-cache/day2-single-node/byteview.py
Email: liangqile@outlook.com
'''

class byte_view:
    def __init__(self,b) -> None:
        
        self.b = b

    def Len(self):
        return len(self.b)
    
    def cloneBytes(self):
        c = self.b.deepcopy()
        return c

    def string(self):
        return str(self.b)
    