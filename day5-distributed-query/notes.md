<!--
 * @Author: Qile Liang
 * @Date: 2023-01-18 21:01:32
 * @LastEditTime: 2023-01-24 16:13:44
 * @LastEditors: Qile Liang
 * @Description: 
 * @FilePath: \distributed_cache_py\day5-distributed-query\notes.md
 * @Email: liangqile@outlook.com
-->
# 分布式节点
## 实现peerpicker
在这里，抽象出 2 个接口，PeerPicker 的 PickPeer() 方法用于根据传入的 key 选择相应节点 PeerGetter。
接口 PeerGetter 的 Get() 方法用于从对应 group 查找缓存值。PeerGetter 也就是之前流程中的 HTTP 客户端，在http客户端中可以调用group得到值。

## HTTP客户端重构 
### step1 提供客户端功能
每个节点的http客户端除了当服务器，也会进行请求，因此添加了请求功能。实现peergetter。
```python
class http_getter:
    def __init__(self,baseURL) -> None:
        self.baseURL = baseURL
    
    def Get(self,group:str,key:str):
        url = self.baseURL+"/"+group+"/"+key
        req = Request(url)
        try:
            response = urlopen(req)
        except URLError as e:
            if hasattr(e, 'reason'):
                print('We failed to reach a server.')
                print('Reason: ', e.reason)
            elif hasattr(e, 'code'):
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
        else:
            return response.read()
```
### step2 重写http服务，提供选择节点功能
```python
class http_server:
    def __init__(self,address,basepath="/cache",port=8080,replicas=10) -> None:
        self.address = address
        self.defaultBasePath = basepath
        self.mu =  multiprocessing.Lock()
        self.peers = None 
        self.httpGetters = {}
        self.replicas = replicas
        from http.server import HTTPServer
        self.server = HTTPServer((address, port), Handler)
        self.server.serve_forever()
        print("server start. Address{} port{}".format(self.address,port))

    def Set(self,peers):
        with self.mu:
            self.peers = consistent_map(self.replicas)
            self.peers.add(peers)
            for peer in peers:
                self.httpGetters[peer] = http_getter(peer+self.defaultBasePath)
    
    def PickPeer(self,key:str):
        with self.mu:
            peer = self.peers.get(key)
            if peer!= None or peer!=self:
                print("Pick peer {}".format(peer))
                return self.httpGetters[peer]
            return 
```
新增成员变量 **peers**，类型是一致性哈希算法的 Map，用来根据具体的 key 选择节点。  
新增成员变量 **httpGetters**，映射远程节点与对应的 httpGetter。每一个远程节点对应一个 httpGetter，因为 httpGetter 与远程节点的地址 baseURL 有关。
**Set()**方法将传入的peers（节点）放入一致性哈希环中，并建立每一个peer对应的getter的映射。  
**Pickpeer**方法根据传入的key，使用一致性hash的get方法得到节点，再通过httpgetters找到对应的getter（也就是对应的http客户端）。
## 修改主流程
```python
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

    def load(self,key):
        # return self.getLocally(key)
        if self.peers:
            peer = self.peers.PickPeer(key)
            if peer:
                value = self.get_from_peer(peer,key)
                print("load data from peer:{} by key:{}".format(peer,key))
                return value
        return self.getLocally(key)

    def get_from_peer(self,peer : http_getter,key):
        # get data from other nodes by peerGetter
        data = peer.Get(self.name,key)
        return data
```   
   
新增RegisterPeers()方法，将实现了PeerPicker 接口的 HTTPPool 注入到 Group 中。也就是说每一个新的节点的httpserver会被同一个group统一管理。  
修改 load 方法，使用 PickPeer() 方法选择节点，若非本机节点，则调用 getFromPeer() 从远程获取。若是本机节点或失败，则回退到 getLocally()。
新增 getFromPeer() 方法，使用实现了 PeerGetter 接口的 httpGetter 从访问远程节点，获取缓存值。  
需要注意的是：每个节点有自己的无数个group，当group重名是，就意味着是**一类资源**，当同一类资源本地不存在时，则去请求peer看peer的同名group下是否有hit的资源。计算出该key应该存在哪一个节点（使用一致性hash算法算出），去该节点尝试获取。