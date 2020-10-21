# coding: utf-8

import os
import shutil
import argparse
import time

'''
BDMV 格式的蓝光电影 nfo 不是以电影名命名 不会被emby识别
使用方法:
    python renamenfo.py -l 硬链接所有路径
例子
    python renamenfo.py -l /volume1/Movie/Movielink
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
        os.mkdir(path)

def mklink(src, desc):
    if not exists(desc):
        os.link(src, desc)


def copyfile(src, desc):
    '''
    存在先删除重新再拷贝
    '''
    if exists(desc):
        print("esxi")
        os.remove(desc)
    shutil.copyfile(src, desc)


def rename_nfo(src_path):
    abs_src_path = abspath(src_path)
    dir_or_file_list = os.listdir(src_path)
    for dir_or_file in dir_or_file_list:
        if dir_or_file == "@eaDir":
            continue
        dir_or_file_path = join(abs_src_path, dir_or_file)
        if is_file(dir_or_file_path):
            if dir_or_file == "movie.nfo" and "BDMV" in dir_or_file_list:
                # item_file_path = join(abs_src_path, src_path + ".nfo")
                item_file_path = abs_src_path + "/" + os.path.basename(src_path) + ".nfo"
                print(item_file_path)
                print(dir_or_file_path)
                copyfile(dir_or_file_path, item_file_path)
                
        elif is_dir(dir_or_file_path):
            rename_nfo(dir_or_file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='rename bdmv nfo')
    parser.add_argument('-l', help='link path')
    args = parser.parse_args()
    link = args.l
    print("请仔细核对以下内容，确认你所操作的对象是本次打印的内容。按1(继续)/0(退出)")
    print("重命名 {} 下的 BDMV nfo".format(link))
    confirm = input("请输入：1(继续)/0(退出)")
    if str(confirm) == "1":
        print("5秒钟后开始")
        time.sleep(5)
        rename_nfo(link)
        print("重命名完成")
    else:
        print("取消操作, 退出")

