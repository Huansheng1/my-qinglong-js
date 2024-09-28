# -*- coding: utf-8 -*-
'''
携趣 - 自动添加白名单

export xq_add_white="uid#ukey"
不支持多账号，因为携趣限制一个IP被添加到几个账号！
cron: * */2 * * *
new Env('携趣白名单');
'''
import requests
import os

# 从环境变量读取uid和ukeyValue
xq_add_white_str = os.getenv('xq_add_white')
if not xq_add_white_str:
    print("没有设置[xq_add_white]环境变量，退出")
    exit()

uid, ukeyValue = xq_add_white_str.split('#')

# 获取白名单
def get_whitelist():
    url = f"http://op.xiequ.cn/IpWhiteList.aspx?uid={uid}&ukey={ukeyValue}&act=get"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.split(',')
    else:
        print("获取白名单失败")
        return []

# 删除白名单IP
def delete_whitelist_ip(ip):
    url = f"http://op.xiequ.cn/IpWhiteList.aspx?uid={uid}&ukey={ukeyValue}&act=del&ip={ip}"
    response = requests.get(url)
    if response.status_code == 200:
        print(f"删除IP {ip} 成功")
    else:
        print(f"删除IP {ip} 失败")

# 添加白名单IP
def add_whitelist_ip(ip):
    url = f"http://op.xiequ.cn/IpWhiteList.aspx?uid={uid}&ukey={ukeyValue}&act=add&ip={ip}"
    response = requests.get(url)
    if response.status_code == 200:
        print(f"添加IP {ip} 成功")
    else:
        print(f"添加IP {ip} 失败")

def manage_whitelist(new_ip):
    whitelist = get_whitelist()
    if len(whitelist) >= 5:
        delete_whitelist_ip(whitelist[-1])
    add_whitelist_ip(new_ip)


def get_public_ip():
    print('开始获取当前服务器IP地址 >>> ')
    response = requests.get(
        'https://whois.pconline.com.cn/ipJson.jsp?ip=&json=true')
    if response.status_code == 200:
        data = response.json()
        return data.get('ip',None)
    return None

if __name__ == "__main__":
    ip = get_public_ip()
    if ip:
        print("当前服务器IP地址: ", ip)
    else:
        print("无法获取当前服务器IP地址")
        exit()
    manage_whitelist(ip)
