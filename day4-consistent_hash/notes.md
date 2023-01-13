<!--
 * @Author: Qile Liang
 * @Date: 2023-01-13 20:12:30
 * @LastEditTime: 2023-01-13 20:25:09
 * @LastEditors: Qile Liang
 * @Description: 
 * @FilePath: /distributed_cache_py/day4-consistent_hash/notes.md
 * @Email: liangqile@outlook.com
-->
# 一致性哈希
参考极客兔兔的博客
## why？
使用分布式缓存，若每次都是随机选取分布式节点获取数据则可能每次存入新缓存后下一次依然无法访问该节点。比方说有十个节点，则可能每次只有十分之一的几率找到上一次已经缓存的节点。因此我们需要尽量将同一个key存放在一个节点中。比方说我们将数据的某个编号mod10.
但是这样的话，当节点数量变化一次，算法找到的节点就会变化，因此我们引入了一致性hash，也就是一个hash环来解决这个问题。
## 原理：
### 步骤：
一致性哈希算法将 key 映射到 2^32 的空间中，将这个数字首尾相连，形成一个环。

计算节点/机器(通常使用节点的名称、编号和 IP 地址)的哈希值，放置在环上。
计算 key 的哈希值，放置在环上，顺时针寻找到的第一个节点，就是应选取的节点/机器。
### 数据倾斜问题：
如果服务器的节点过少，容易引起 key 的倾斜。例如上面例子中的 peer2，peer4，peer6 分布在环的上半部分，下半部分是空的。那么映射到环下半部分的 key 都会被分配给 peer2，key 过度向 peer2 倾斜，缓存节点间负载不均。

为了解决这个问题，引入了虚拟节点的概念，一个真实节点对应多个虚拟节点。

假设 1 个真实节点对应 3 个虚拟节点，那么 peer1 对应的虚拟节点是 peer1-1、 peer1-2、 peer1-3（通常以添加编号的方式实现），其余节点也以相同的方式操作。

第一步，计算虚拟节点的 Hash 值，放置在环上。
第二步，计算 key 的 Hash 值，在环上顺时针寻找到应选取的虚拟节点，例如是 peer2-1，那么就对应真实节点 peer2。
虚拟节点扩充了节点的数量，解决了节点较少的情况下数据容易倾斜的问题。而且代价非常小，只需要增加一个字典(map)维护真实节点与虚拟节点的映射关系即可。
## 具体实现：
定义了一致性hash类
```python
class map:
    def __init__(self,replicas,hash_func=hash) -> None:
        self.hash = hash_func
        self.replicas = replicas
        self.keys = []
        self.hash_map = {}
```
**hash**函数可以自定义，**replicas**为虚拟节点为真实节点的倍数，**key**为hash环，**hash_map**存放了虚拟节点与真实节点的映射。  
  
**add**方法：
```python
    def add(self,keys):
        for key in keys:
            for i in range(self.replicas):
                hash = self.hash(str(i)+key)
                self.keys.append(hash)
                self.hash_map[hash]=key
        self.keys.sort()
```
计算虚拟节点hash值并放入环中，然后重新对hash值排序。  
**get**方法：
```python

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
        return self.hash_map[self.keys[index%len(self.keys)]]
```
选择节点就非常简单了，第一步，计算 key 的哈希值。  
第二步，顺时针找到第一个匹配的虚拟节点的下标 idx，从 m.keys 中获取到对应的哈希值。如果 idx == len(m.keys)，说明应选择 m.keys[0]，这时next函数会抛出**StopIteration**异常，进行对应处理即可。  
第三步，通过 hashMap 映射得到真实的节点。