# -*- coding: utf-8 -*-
'''
根据tracker自动分类 使用tracker地址的host做分类名
脚本依赖 python-qbittorrent 0.4.2
安装 依赖
pip install python-qbittorrent==0.4.2 -i https://pypi.tuna.tsinghua.edu.cn/simple some-package

'''


from qbittorrent import Client
try:
    from urllib.parse import urlparse
except:
    from urlparse import urlparse

# qbittorrent 地址
server = "http://host:port"
# 用户
user = "admin"
# 密码
password = "adminadmin"

# 是否覆盖原分类 如更换了 tracker地址
cover = True


client = Client(server)
login_result = client.login(user, password)
if login_result is not None:
    print(u"登录失败 请检查配置")

categories = set()
torrents = client.torrents()

maindata = client.sync_main_data()
categories = maindata['categories'].keys()
print("已有分类: {}".format(categories))

# 设置分类

print(categories)

for torrent in torrents:
    category = torrent['category']
    tracker = torrent['tracker']
    _hash = torrent['hash']
    name = torrent['name']
    if not category:
        category = urlparse(tracker).hostname
        if category not in categories:
            categories.add(category)
            client.create_category(category)
        client.set_category(_hash, category)
        print(u"添加 {} 到分类 {}".format(name, category))
    else:
        if cover:
            new_category = urlparse(tracker).hostname
            if new_category != category:
                print(u"需要转移{} 到 {}".format(name, new_category))
                if new_category not in categories:
                    categories.add(category)
                    client.create_category(category)
                client.set_category(_hash, new_category)
                print(u"添加 {} 到分类 {}".format(name, new_category))

