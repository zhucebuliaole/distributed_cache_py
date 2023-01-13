<!--
 * @Author: Qile Liang
 * @Date: 2023-01-08 21:31:07
 * @LastEditTime: 2023-01-08 21:57:05
 * @LastEditors: Qile Liang
 * @Description: 
 * @FilePath: /distributed-cache/python-cache/day1-lru/notes.md
 * @Email: liangqile@outlook.com
-->
# LRU  原理
![avatar](images/lru.jpeg)
这张图很好地表示了 LRU 算法最核心的 2 个数据结构

蓝色的是字典(map)，存储键和值的映射关系。这样根据某个键(key)查找对应的值(value)的复杂是O(1)，在字典中插入一条记录的复杂度也是O(1)。  
红色的是双向链表(double linked list)实现的队列。将所有的值放到双向链表中，这样，当访问到某个值时，将其移动到队尾的复杂度是O(1)，在队尾新增一条记录以及删除一条记录的复杂度均为O(1)。
# 代码实现
## 定义cache类
```python
class Cache:
    def __init__(self,maxsize) -> None:
        self.max_size = maxsize
        self.cur_size = 0
        self.d_link = Dlink.DLinkList()
        self.cache_map = dict() 
```        
期中Dlinke为自己实现的双向链表。
当达到最大size后需要进行置换算法。cachemap存储了指向每个节点的指针，这样可以让操作的时间复杂度下降到O（1）。  

## 查找
```python
def get(self,key):
    if key in self.cache_map:
        node = self.cache_map[key]
        value = self._update_node(node)
        del node
        self.d_link.append(value,key)
        self.cache_map[key] = self.d_link.get_tail()
    else:
        value = None
    return value
``` 
如若已经在缓存中则击中，返回value值并置换到队列末尾。其中用到了缓存击中时的更新函数如下。需要特别处理当击中的节点为head或者为tail。
```python
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
```
## 删除
当新增时大于缓存大小时需要进行替换，将双向队列中的head进行替换掉。
```python
    def cache_disuse(self):
        # disuse the first cache item
        key = self.d_link._head.key
        self.d_link.remove_head()
        del self.cache_map[key]
        self.cur_size-=1
``` 
## 新增or修改
若命中缓存则更新，若大于缓存大小则进行置换。
```python
    def add(self,key,value):
        if key in self.cache_map:
            node = self.cache_map[key]
            value = self._update_node(node)
        
        self.d_link.append(value,key)
        self.cache_map[key] = self.d_link.get_tail()
        self.cur_size+=1
        if self.cur_size>self.max_size:
            self.cache_disuse()
            self.cur_size-=1
``` 
## 双向链表
``` python
class Node(object):
    # 双向链表节点
    def __init__(self, item,key):
        # variable "key" used for the cache_map delete node
        self.item = item
        self.key  = key
        self.next = None
        self.prev = None

class DLinkList(object):
    # 双向链表
    def __init__(self):
        self._head = None
        self._tail = None

    def is_empty(self):
        # 判断链表是否为空
        return self._head == None

    def get_length(self):
        # 返回链表的长度
        cur = self._head
        count = 0
        while cur != None:
            count = count+1
            cur = cur.next
        return count

    def print_list(self):
        # 遍历链表
        items_list = []
        cur = self._head
        while cur != None:
            items_list.append(cur.item)
            # print(cur.item)
            cur = cur.next

        print(items_list)
        # print("")

    def add(self, item,key):
        # 头部插入元素
        node = Node(item,key)
        if self.is_empty():
            # 如果是空链表，将 node 赋值给 _head
            self._head = node
            self._tail = node
        elif self._head == self._tail:
            self._head = node
            self._tail.prev = self._head
            self._head.next = self._tail
        else:
            # 将 node 的 next 属性指向头节点 _head
            node.next = self._head
            # 将头节点 _head 的 prev 属性指向 node
            self._head.prev = node
            # 将 node 赋值给 _head
            self._head = node

    def append(self, item,key):
        # 尾部插入元素
        node = Node(item,key)
        if self.is_empty():
            # 如果是空链表，将 node 赋值给 _head
            self._head = node
            self._tail = node
        elif self._head == self._tail:
            self._tail = node
            self._tail.prev = self._head
            self._head.next = self._tail
        else:
            # 将 node 的 next 属性指向头节点 _head
            node.prev = self._tail
            # 将头节点 _head 的 prev 属性指向 node
            self._tail.next = node
            # 将 node 赋值给 _head
            self._tail = node

    def search(self, item):
        # 查找元素是否存在
        cur = self._head
        while cur != None:
            if cur.item == item:
                return True
            cur = cur.next
        return False

    def insert(self, pos, item,key):
        # 在指定位置添加节点
        if pos <= 0:
            self.add(item)
        elif pos > (self.get_length()-1):
            self.append(item)
        else:
            node = Node(item,key)
            cur = self._head
            count = 0
            # 移动到指定位置的前一个位置
            while count < (pos-1):
                count += 1
                cur = cur.next
            # 将 node 的 prev 属性指向 cur
            node.prev = cur
            # 将 node 的 next 属性指向 cur 的下一个节点
            node.next = cur.next
            # 将 cur 的下一个节点的 prev 属性指向 node
            cur.next.prev = node
            # 将 cur 的 next 指向 node
            cur.next = node

    def remove(self, item):
        # 删除元素
        if self.is_empty():
            return
        else:
            cur = self._head
            if cur.item == item:
                # 如果首节点的元素即是要删除的元素
                if cur.next == None:
                    # 如果链表只有这一个节点
                    self._head = None
                else:
                    # 将第二个节点的 prev 属性设置为 None
                    cur.next.prev = None
                    # 将 _head 指向第二个节点
                    self._head = cur.next
                return
            while cur != None:
                if cur.item == item:
                    # 将 cur 的前一个节点的 next 指向 cur 的后一个节点
                    cur.prev.next = cur.next
                    # 将 cur 的后一个节点的 prev 指向 cur 的前一个节点
                    cur.next.prev = cur.prev
                    break
                cur = cur.next

    def reverse(self):
        """
        将链表头尾反转
        :return:
        """
        prev = None
        current = self._head # 将头节点保存在current中

        # 当链表为非空的时候，需要执行相应反转的操作
        # 分别将相邻的两个节点的前驱后继关系进行反转
        while current:
            next_node = current.next    # 将下一个节点保存在next_node中
            current.next = prev     # 由于反转链表，因此头节点反转后，成为尾节点，应该指向None
            current.prev = next_node    # 尾节点的前驱应指向原本的后继

            prev = current      # 更新prev，向后移动
            current = next_node # 更新current，向后移动

        # 到达链表尾部时，需要特殊处理
        self._head = prev

    def init_list(self, list):
        for item in list:
            self.append(item)

    def remove_head(self):
        self._head = self._head.next
        self._head.prev.next = None
        self._head.prev = None
    
    def get_tail(self):
        return self._tail
```