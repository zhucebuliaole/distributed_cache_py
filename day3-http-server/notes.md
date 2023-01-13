<!--
 * @Author: Qile Liang
 * @Date: 2023-01-11 19:43:38
 * @LastEditTime: 2023-01-11 19:53:10
 * @LastEditors: Qile Liang
 * @Description: 
 * @FilePath: /distributed-cache/python-cache/day3-http-server/notes.md
 * @Email: liangqile@outlook.com
-->
# HTTP 服务端
这部分使用python自带的http库实现简单的HTTP服务端，通过服务端的接口调用LRU缓存。
## 接口
使用BaseHTTPRequestHandler，自定义继承后的handler，在其中有处理逻辑。需要注意的是，继承的该方法不支持重写。
```python

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):

        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()
        # path must be \basepath\group\key
        parts = self.path.split('/')
        parts = parts[1:]
        if len(parts) != 3:
            print("path must have basepath group and key") 
        elif parts[0]!="cache":
            print("error of basepath")
        print("cache run at {}".format(self.address_string()))
        group_name = parts[1]
        key = parts[2]
        group = cache_manager.get_group(group_name)
        if not group:
            print("group isn't exist")
            self.wfile.write("group isn't exist".encode('utf-8'))
            return
        data = group.get(key)
        self.wfile.write(data.string().encode('utf-8'))
```
其中因为python import的性质，当import cache_manager之后，其管理的全局变量便在该命名空间之下了，便可以根据groupname找到对应的group，并调用该group对缓存进行操作。