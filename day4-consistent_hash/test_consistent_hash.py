'''
Author: Qile Liang
Date: 2023-01-13 19:52:39
LastEditTime: 2023-01-13 20:11:31
LastEditors: Qile Liang
Description: 
FilePath: /distributed_cache_py/day4-consistent_hash/test_consistent_hash.py
Email: liangqile@outlook.com
'''
from consistenthash import map
def toString(key):
    return int(key)
hash_func = toString
a = map(3,toString)
a.add(["6","4","2"])
test_case = {"2":"2","11":"2","23":"4","27":"2"}
for k,v in test_case.items():
    if a.get(k)!=v:
        print("Asking for {}, should have yielded {}".format( k, v))

a.add("8")

test_case["27"]="8"

for k,v in test_case.items():
    if a.get(k)!=v:
        print("Asking for {}, should have yielded {}".format( k, v))
