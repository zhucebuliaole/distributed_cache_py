'''
Author: Qile Liang
Date: 2023-01-08 20:19:43
LastEditTime: 2023-01-08 21:04:27
LastEditors: Qile Liang
Description: 
FilePath: /distributed-cache/python-cache/day1-lru/lru_test.py
Email: liangqile@outlook.com
'''
import sys
from lru import Cache

a = Cache(2)
print(a.add("one",1))
print(a.add("two",2))
print(a.get("one"))
print(a.add("three",3))
print(a.get("one"))
print(a.get("two"))