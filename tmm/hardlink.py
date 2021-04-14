# coding: utf-8

import os
import argparse
import time
'''
创建硬链接

不能跨盘创建硬链接

请认真确认信息
请认真确认信息
请认真确认信息


使用方法:
    python hardlink.py -s 源路径 -d 目标路径
例子
    python hardlink.py -s /volume1/tv -d /volume1/tv_link

'''

is_dir = os.path.isdir
is_file = os.path.isfile
is_link = os.path.islink
join = os.path.join
abspath = os.path.abspath
exists = os.path.exists
splitext = os.path.splitext


def mkdir(path):
    if not exists(path):
        print("创建目录: {}".format(path))
        os.mkdir(path)


def mklink(src, desc):
    if not exists(desc):
        print("创建硬链接: {} to {}".format(src, desc))
        os.link(src, desc)


def hardlink(src_path, desc_path):
    abs_src_path = abspath(src_path)
    abs_desc_path = abspath(desc_path)
    if is_file(abs_src_path):
        os.link(abs_src_path, abs_desc_path)
    mkdir(abs_desc_path)
    dir_or_file_list = os.listdir(src_path)
    for dir_or_file in dir_or_file_list:
        if dir_or_file == "@eaDir":
            continue
        dir_or_file_path = join(abs_src_path, dir_or_file)
        desc_dir_or_file_path = join(abs_desc_path, dir_or_file)
        if is_file(dir_or_file_path):
            suffix = splitext(dir_or_file_path)[-1]
            # 不链接 nfo 文件及图片文件 可根据需求自行需改过滤
            if suffix in [".nfo", ".jpg", ".png", ".jepg"]:
                continue
            # 更上一行操作重叠部分
            if os.path.basename(dir_or_file_path) in [
                    "banner.jpg", "clearart.png", "clearlogo.png", "disc.png",
                    "fanart.jpg", "keyart.jpg", "logo.png", "poster.jpg",
                    "thumb.jpg"
            ]:
                continue
            mklink(dir_or_file_path, desc_dir_or_file_path)
        elif is_dir(dir_or_file_path):
            mkdir(desc_dir_or_file_path)
            hardlink(dir_or_file_path, desc_dir_or_file_path)


if __name__ == "__main__":
    '''
    如果不需要提示
    将下边的代码删除替换成如下代码
    src = ""  # 配置需要硬链接的路径 如 /volume1/movie
    desc = ""   # 硬链接到的路径  如 /vomume1/movie_link
    hardlink(src, desc)
    '''

    parser = argparse.ArgumentParser(description='hard link')
    parser.add_argument('-s', help='src path')
    parser.add_argument('-d', help='desc path')
    args = parser.parse_args()

    src = args.s
    desc = args.d
    if src and desc:
        print("请仔细核对以下内容，确认你所操作的对象是本次打印的内容。按1(继续)/0(退出)")
        print("硬链接 {} 到 {}".format(src, desc))
        confirm = str(input("请输入：1(继续)/0(退出)"))
        if confirm == "1":
            print("5秒钟后开始")
            time.sleep(5)
            hardlink(src, desc)
            print("硬链接完成")
        else:
            print("取消操作, 退出")
    else:
        print("缺少参数 -s 或 -d")
