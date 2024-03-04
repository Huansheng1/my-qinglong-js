"""
* 仅供学习交流，请在下载后的24小时内完全删除 请勿将任何内容用于商业或非法目的，否则后果自负。
* 幻生魔改自用版 V1.61

* 活动入口,微信打开：
* 如果连接过期了运行一下就出来了最新的入口！
* https://u7ds.sy673.shop/yunonline/v1/auth/2639bb95daba1d99e5338a8c2e21e2f0?codeurl=u7ds.sy673.shop&codeuserid=2&time=1709021176
* 打开活动入口，抓包的任意接口cookies中的ysm_uid参数
* 
* 变量格式：
* 新建同名环境变量
* 变量名：xyyyd
* 变量值：
* # 3000 代表 3毛，后面两个推送参数可不填，那就必须配置全局推送！
* 账号备注#ysm_uid参数#unionId#提现金额如3000#wxpushApptoken#wxpushTopicId
* 
* 其他参数说明（脚本最下方填写参数）
* wxpusher全局参数：wxpusherAppToken、wxpusherTopicId
* 具体使用方法请看文档地址：https://wxpusher.zjiecode.com/docs/#/
* 
* 也可使用 微信机器人：wechatBussinessKey
* 
* 支持支付宝提现：账号备注#ysm_uid参数#unionId#提现金额如3000#wxpushApptoken#wxpushTopicId#支付宝姓名#支付宝账号
* 只想提现支付宝，不想填写其他参数，最少的参数就是：账号备注#ysm_uid参数#unionId####支付宝姓名#支付宝账号
*
* 增加 自定义检测文章等待时间：xyyydReadPostDelay，默认值是 15-20秒
* 定时运行每半小时一次
* 达到标准自动提现
* 达到标准，自动提现
"""

import hashlib
import json
import math
import os
import string
import time
import requests
import random
import re
from urllib.parse import quote, urlparse, parse_qs
import urllib3
from urllib.parse import parse_qs, urlsplit

urllib3.disable_warnings()

# 填wxpusher的appToken，配置在环境变量里这样没配置的账号会自动使用这个推送
wxpusherAppToken = os.getenv("wxpusherAppToken") or ""
wxpusherTopicId = os.getenv("wxpusherTopicId") or ""
wechatBussinessKey = os.getenv("wechatBussinessKey") or ""
readPostDelay = 0
if os.getenv("xyyydReadPostDelay") and os.getenv("xyyydReadPostDelay").isdecimal():
    readPostDelay = int(os.getenv("xyyydReadPostDelay"))


def safe_request(method, url, retries=3, **kwargs):
    for i in range(retries):
        try:
            if method.upper() == "GET":
                response = requests.get(url, **kwargs)
            elif method.upper() == "POST":
                response = requests.post(url, **kwargs)
            else:
                print(f"不支持的请求类型: {method}")
                return None
            return response
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            if i < retries - 1:  # 如果不是最后一次尝试，就等待一段时间再重试
                wait = random.randint(1, 5)  # 随机等待时间
                print(f"等待 {wait} 秒后重试...")
                time.sleep(wait)
            else:
                print("尝试请求失败，已达到最大尝试次数")
                return None  # 或者你可以返回一个特定的值或对象来表示请求失败


def push(appToken, topicIds, title, link, text):
    datapust = {
        "appToken": appToken,
        "content": f"""<body onload="window.location.href='{link}'">出现检测文章！！！\n<a style='padding:10px;color:red;font-size:20px;' href='{link}'>点击我打开待检测文章</a>\n请尽快点击链接完成阅读\n备注：{text}</body>""",
        "summary": title or "小阅阅阅读",
        "contentType": 2,
        "topicIds": [topicIds or "11686"],
        "url": link,
    }
    # print(datapust)
    urlpust = "http://wxpusher.zjiecode.com/api/send/message"
    try:
        p = safe_request("POST", url=urlpust, json=datapust, verify=False)
        # print(p)
        if p.json()["code"] == 1000:
            print("✅ 推送文章到微信成功，请尽快前往点击文章，不然就黑号啦！")
            return True
        else:
            print("❌ 推送文章到微信失败，完犊子，要黑号了！")
            return False
    except Exception as e:
        print("❌ 推送文章到微信失败，完犊子，要黑号了！")
        raise e
        return False


def pushWechatBussiness(robotKey, link):
    datapust = {"msgtype": "text", "text": {"content": link}}
    # print(datapust)
    urlpust = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=" + robotKey
    try:
        p = safe_request("POST", url=urlpust, json=datapust, verify=False)
        # print(p)
        if p.json()["errcode"] == 0:
            print("✅ 推送文章到企业微信成功！")
            return True
        else:
            print("❌ 推送文章到企业微信失败！")
            return False
    except:
        print("❌ 推送文章到企业微信失败！")
        return False


def getPostWechatInfo(link):
    try:
        r = safe_request("GET", link, verify=False)
        # print(link, r.text)
        html = re.sub("\s", "", r.text)
        biz = re.findall('varbiz="(.*?)"\|\|', html)
        if biz != []:
            biz = biz[0]
        if biz == "" or biz == []:
            if "__biz" in link:
                biz = re.findall("__biz=(.*?)&", link)
                if biz != []:
                    biz = biz[0]
        nickname = re.findall('varnickname=htmlDecode\("(.*?)"\);', html)
        if nickname != []:
            nickname = nickname[0]
        user_name = re.findall('varuser_name="(.*?)";', html)
        if user_name != []:
            user_name = user_name[0]
        msg_title = re.findall("varmsg_title='(.*?)'\.html\(", html)
        if msg_title != []:
            msg_title = msg_title[0]
        text = f"公众号唯一标识：{biz}|文章:{msg_title}|作者:{nickname}|账号:{user_name}"
        print(text)
        return nickname, user_name, msg_title, text, biz
    except Exception as e:
        # print(e)
        print("❌ 提取文章信息失败")
        return False


def ts():
    return str(int(time.time())) + "000"


checkDict = {
    "MzkxNTE3MzQ4MQ==": ["香姐爱旅行", "gh_54a65dc60039"],
    "Mzg5MjM0MDEwNw==": ["我本非凡", "gh_46b076903473"],
    "MzUzODY4NzE2OQ==": ["多肉葡萄2020", "gh_b3d79cd1e1b5"],
    "MzkyMjE3MzYxMg==": ["Youhful", "gh_b3d79cd1e1b5"],
    "MzkxNjMwNDIzOA==": ["少年没有乌托邦3", "gh_b3d79cd1e1b5"],
    "Mzg3NzUxMjc5Mg==": ["星星诺言", "gh_b3d79cd1e1b5"],
    "Mzg4NTcwODE1NA==": ["斑马还没睡123", "gh_b3d79cd1e1b5"],
    "Mzk0ODIxODE4OQ==": ["持家妙招宝典", "gh_b3d79cd1e1b5"],
    "Mzg2NjUyMjI1NA==": ["Lilinng", "gh_b3d79cd1e1b5"],
    "MzIzMDczODg4Mw==": ["有故事的同学Y", "gh_b3d79cd1e1b5"],
    "Mzg5ODUyMzYzMQ==": ["789也不行", "gh_b3d79cd1e1b5"],
    "MzU0NzI5Mjc4OQ==": ["皮蛋瘦肉猪", "gh_58d7ee593b86"],
    "Mzg5MDgxODAzMg==": ["北北小助手", "gh_58d7ee593b86"],
    "MzIzMDczODg4Mw==": ["有故事的同学Y", "gh_b8b92934da5f"],
    "MzkxNDU1NDEzNw==": ["小阅阅服务", "gh_e50cfefef9e5"],
    "MzkxNDYzOTEyMw==": ["蓝莓可乐", "gh_73ca238add97"],
}


class HHYD:
    def __init__(self, cg):
        self.balance = 0
        self.unionId = cg["unionId"]
        self.ysm_uid = cg["ysm_uid"]
        # print("cg", cg, self.unionId, self.ysm_uid)
        self.txbz = cg["txbz"]
        self.topicIds = cg["topicIds"]
        self.appToken = cg["appToken"]
        global wechatBussinessKey
        self.wechatBussinessKey = wechatBussinessKey or ""
        self.aliAccount = cg["aliAccount"] or ""
        self.aliName = cg["aliName"] or ""
        self.name = cg["name"]
        self.domnainHost = "1698855139.hxiong.top"
        self.exchangeParams = ""
        self.headers = {
            "Connection": "keep-alive",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090621) XWEB/8351 Flue",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": f"http://{self.domnainHost}/",
            "Origin": f"http://{self.domnainHost}",
            # "Host": f"{self.domnainHost}",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": f"ysm_uid={self.ysm_uid};",
        }

    def user_info(self):
        u = f"http://{self.domnainHost}/yunonline/v1/sign_info?time={ts()}&unionid={self.unionId}"
        r = ""
        try:
            r = safe_request("GET", u)
            rj = r.json()
            if rj.get("errcode") == 0:
                print(
                    f"账号[{self.name}]获取信息成功，当前阅读文章每篇奖励 {r.json()['data']['award']}个金币"
                )
                return True
            else:
                print(f"账号[{self.name}]获取用户信息失败，账号异常 或者 ysm_uid无效，请检测ysm_uid是否正确")
                return False
        except Exception as e:
            print(r.text)
            print(f"账号[{self.name}]获取用户信息失败,ysm_uid无效，请检测ysm_uid是否正确")
            return False

    def hasWechat(self):
        r = ""
        try:
            u = f"http://{self.domnainHost}/yunonline/v1/hasWechat?unionid={self.unionId}"
            r = safe_request("GET", u)
            print(f"账号[{self.name}]判断公众号任务数量：{r.json()['data']['has']}")
        except Exception as e:
            print(f"账号[{self.name}]判断是否有公众号任务失败：{r.text}")
            return False

    def gold(self):
        r = ""
        try:
            u = f"http://{self.domnainHost}/yunonline/v1/gold?unionid={self.unionId}&time={ts()}"
            r = safe_request("GET", u)
            # print(r.json())
            rj = r.json()
            self.remain = math.floor(int(rj.get("data").get("last_gold")))
            print(
                f'账号[{self.name}]今日已经阅读了{rj.get("data").get("day_read")}篇文章,剩余{rj.get("data").get("remain_read")}未阅读，今日获取金币{rj.get("data").get("day_gold")}，剩余{self.remain}'
            )
        except Exception as e:
            print(f"账号[{self.name}]获取金币失败：", e)
            # raise e
            return False

    def getKey(self):
        uk = ""
        ukRes = None
        for i in range(10):
            u = f"http://{self.domnainHost}/yunonline/v1/wtmpdomain"
            # print("提示 getKey：", u)
            p = f"unionid={self.unionId}"
            r = safe_request("POST", u, headers=self.headers, data=p, verify=False)
            # print("getKey：", r.text)
            rj = r.json()
            domain = rj.get("data").get("domain")
            # print("请求中转页：", r.text)
            pp = parse_qs(urlparse(domain).query)
            hn = urlparse(domain).netloc
            uk = pp.get("uk")[0]
            ukRes = r.text
            if uk:
                break
        if uk == "":
            print(f"账号[{self.name}]获取uk失败，返回错误：{ukRes}")
            return
        time.sleep(8)
        r = safe_request(
            "GET",
            domain,
            headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Connection": "keep-alive",
                "Host": f"{hn}",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
            },
            verify=False,
        )
        # print(f"账号[{self.name}] 阅读准备完成：{uk}，提取到的地址：{domain}")
        print(f"账号[{self.name}] 阅读准备成功 即将开始阅读 ✅ ，阅读参数为：{uk}")
        h = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Host": "nsr.zsf2023e458.cloud",
            "Origin": f"https://{hn}",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
        }
        return uk, h

    def read(self):
        info = self.getKey()
        if len(info) == 0:
            print(f"账号[{self.name}]获取阅读参数失败，停止往后阅读！⚠️ ")
            return
        # print(info)
        time.sleep(2)
        arctileTime = 1
        lastestArcticleId = ""
        while True:
            res = {"errcode": -1}
            refreshTime = 0
            while res["errcode"] != 0:
                timeStamp = str(ts())
                psgn = hashlib.md5(
                    (
                        info[1]["Origin"].replace("https://", "")[:11]
                        + info[0]
                        + timeStamp
                        + "A&I25LILIYDS$"
                    ).encode()
                ).hexdigest()
                self.params = {
                    "uk": info[0],
                    "time": timeStamp,
                    "psgn": psgn,
                    "v": "3.0",
                }
                u = f"https://nsr.zsf2023e458.cloud/yunonline/v1/do_read"
                r = safe_request(
                    "GET",
                    u,
                    headers=info[1],
                    params=self.params,
                    verify=False,
                    timeout=60,
                )
                print("-" * 50)
                # print(
                #     f"账号[{self.name}]第[{refreshTime+1}]次获取阅读文章[{info[0]}]目的页：{r.text}"
                # )
                # print("阅读文章参数查看：", u, self.params, r.text, info[1])
                if r.text and r.json()["errcode"] == 0:
                    res = r.json()
                    print(
                        f"账号[{self.name}]第[{refreshTime+1}]次获取第[{arctileTime}]篇阅读文章[{info[0]}]跳转链接成功"
                    )
                else:
                    decoded_str = json.loads(r.text)
                    if decoded_str["msg"]:
                        print(
                            f"账号[{self.name}]第[{refreshTime+1}]次获取第[{arctileTime}]篇阅读文章[{info[0]}]跳转链接失败：{decoded_str['msg']}"
                        )
                        return False
                    else:
                        print(
                            f"账号[{self.name}]第[{refreshTime+1}]次获取第[{arctileTime}]篇阅读文章[{info[0]}]跳转链接失败：{r.text}"
                        )
                time.sleep(1.5)
                refreshTime = refreshTime + 1
                if refreshTime >= 5:
                    print(f"⚠️ 账号[{self.name}]获取阅读第[{arctileTime}]篇文章[{info[0]}]超时……")
                    return
            wechatPostLink = ""
            if res.get("errcode") == 0:
                returnLink = ""
                try:
                    returnLink = res.get("data").get("link")
                except Exception as e:
                    print(
                        f"⚠️ 账号[{self.name}]获取阅读第[{arctileTime}]篇文章[{info[0]}]链接失败，疑似台子接口太垃圾，崩了，返回数据为：",
                        res.get("data"),
                    )
                    continue
                if "mp.weixin.qq.com" in returnLink:
                    print(f"账号[{self.name}] 阅读第[{arctileTime}]篇微信文章：{returnLink}")
                    wechatPostLink = returnLink
                else:
                    # print(f"账号[{self.name}] 阅读第[{arctileTime}]篇文章准备跳转：{link}")
                    wechatPostLink = self.jump(returnLink)
                    print(f"账号[{self.name}] 阅读第[{arctileTime}]篇文章：{wechatPostLink}")
                print(f"账号[{self.name}] 阅读第[{arctileTime}]篇文章：{wechatPostLink}")
                sleepTime = random.randint(7, 10)
                if "mp.weixin.qq.com" in wechatPostLink:
                    postWechatInfo = getPostWechatInfo(wechatPostLink)
                    if postWechatInfo == False:
                        print(
                            f"⚠️ 账号[{self.name}]因 获取公众号文章信息不成功，导致阅读第[{arctileTime}]篇文章[{info[0]}] 失败……"
                        )
                        return False
                    # 如果是检测特征到的文章 或者 后一篇文章与前一篇相似
                    if (
                        checkDict.get(postWechatInfo[4]) != None
                        or (res.get("data").get("a") == 2)
                        or ("&chksm=" in wechatPostLink)
                        or ("__biz" not in wechatPostLink)
                    ):
                        sleepTime = readPostDelay or random.randint(15, 20)
                        print(
                            f"⚠️ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}] 检测到疑似检测文章，正在推送，等待过检测，等待时间：{sleepTime}秒。。。"
                        )
                        if self.wechatBussinessKey:
                            pushWechatBussiness(self.wechatBussinessKey, wechatPostLink)
                        elif self.appToken:
                            push(
                                self.appToken,
                                self.topicIds,
                                "小阅阅阅读过检测",
                                wechatPostLink,
                                f"账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}] 正在等待过检测，等待时间：{sleepTime}秒\n幻生提示：快点，别耽搁时间了！",
                            )
                        else:
                            print(
                                f"⚠️ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}] 需要过检测，但是未配置推送token，为了避免黑号，停止阅读。。。"
                            )
                            return False
                    else:
                        print(
                            f"✅ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}] 非检测文章，模拟读{sleepTime}秒"
                        )
                else:
                    print(
                        f"✅ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}] 非检测文章，模拟读{sleepTime}秒"
                    )
                time.sleep(sleepTime)
                u1 = f"http://nsr.zsf2023e458.cloud/yunonline/v1/get_read_gold?uk={info[0]}&time={sleepTime}&timestamp={ts()}"
                r1 = safe_request("GET", u1, headers=info[1], verify=False)
                if r1.text and r1.json():
                    try:
                        print(
                            f"✅ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}]所得金币：{r1.json()['data']['gold']}个，账户当前金币：{r1.json()['data']['last_gold']}个，今日已读：{r1.json()['data']['day_read']}次，今日未读 {r1.json()['data']['remain_read']}篇文章"
                        )
                    except Exception as e:
                        print(
                            f"❌ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}]异常：{r1.json().get('msg')}"
                        )
                        if "本次阅读无效" in r1.json().get("msg"):
                            continue
                        else:
                            break
                else:
                    print(
                        f"❌ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}]失败：{r1.text}"
                    )
                    break
            elif res.get("errcode") == 405:
                print(f"⚠️ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}]阅读重复")
                time.sleep(1.5)
            elif res.get("errcode") == 407:
                print(f"⚠️ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}]阅读结束")
                return True
            else:
                print(f"⚠️ 账号[{self.name}]阅读第[{arctileTime}]篇文章[{info[0]}]未知情况")
                time.sleep(1.5)
            arctileTime = arctileTime + 1

    def jump(self, link):
        print(f"账号[{self.name}]开始本次阅读……")
        hn = urlparse(link).netloc
        h = {
            "Host": hn,
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090621) XWEB/8351 Flue",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh",
            "Cookie": f"ysm_uid={self.ysm_uid}",
        }
        r = safe_request("GET", link, headers=h, allow_redirects=False, verify=False)
        # print(r.status_code)
        Location = r.headers.get("Location")
        print(f"账号[{self.name}]开始阅读文章 - {Location}")
        return Location

    def withdrawPost(self, exchangeParams):
        u = f"http://{self.domnainHost}/yunonline/v1/withdraw"
        p = f"unionid={exchangeParams['unionid']}&signid={exchangeParams['request_id']}&ua=0&ptype=0&paccount=&pname="
        if self.aliAccount and self.aliName:
            p = f"unionid={exchangeParams['unionid']}&signid={exchangeParams['request_id']}&ua=2&ptype=1&paccount={quote(self.aliAccount)}&pname={quote(self.aliName)}"
        r = safe_request(
            "POST",
            u,
            headers={
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Cookie": f"ysmuid={self.ysm_uid}; ejectCode=1",
                "Host": f"{self.domnainHost}",
                "Origin": f"http://{self.domnainHost}",
                "Proxy-Connection": "keep-alive",
                "Referer": f"http://{self.domnainHost}/yunonline/v1/exchange?unionid={exchangeParams['unionid']}&request_id={exchangeParams['request_id']}&qrcode_number=16607864358145588",
                "X-Requested-With": "XMLHttpRequest",
            },
            data=p,
            verify=False,
        )
        print(f"✅ 账号[{self.name}] 提现结果：", r.json()["msg"])

    def withdraw(self):
        gold = int(int(self.remain) / 1000) * 1000
        print(f"账号[{self.name}] 本次提现金额 ", self.balance, "元 + ", gold, "金币")
        query = urlsplit(self.exchangeParams).query
        exchangeParams = parse_qs(query)
        # 将列表值转换为字符串
        for key, value in exchangeParams.items():
            exchangeParams[key] = value[0]
        withdrawBalance = round((int(self.txbz) / 1000), 3)
        if gold or (self.balance >= withdrawBalance):
            if gold:
                # 开始提现
                u1 = f"http://{self.domnainHost}/yunonline/v1/user_gold"
                p1 = f"unionid={exchangeParams['unionid']}&request_id={exchangeParams['request_id']}&gold={gold}"
                r = safe_request(
                    "POST",
                    u1,
                    data=p1,
                    headers={
                        "Accept": "application/json, text/javascript, */*; q=0.01",
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "zh-CN,zh;q=0.9",
                        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                        "Cookie": f"ysmuid={self.ysm_uid}; ejectCode=1",
                        "Host": f"{self.domnainHost}",
                        "Origin": f"http://{self.domnainHost}",
                        "Proxy-Connection": "keep-alive",
                        "Referer": f"http://{self.domnainHost}/yunonline/v1/exchange{self.exchangeParams}",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
                        "X-Requested-With": "XMLHttpRequest",
                    },
                    verify=False,
                )
                try:
                    res = r.json()
                    if res.get("errcode") == 0:
                        withdrawBalanceNum = self.balance + float(res["data"]["money"])
                        print(
                            f"✅ 账号[{self.name}] 金币兑换为现金成功，开始提现，预计到账 {withdrawBalanceNum} 元 >>> "
                        )
                        if withdrawBalanceNum < withdrawBalance:
                            print(f"账号[{self.name}]没有达到提现标准 {withdrawBalance} 元")
                            return False
                        self.withdrawPost(exchangeParams)
                        return
                    else:
                        print(
                            f"账号[{self.name}] 金币兑换为现金失败：",
                            r.text,
                            " 提现地址：",
                            u1,
                            " 提现参数：",
                            p1,
                        )
                except Exception as e:
                    # raise e
                    # 处理异常
                    print(f"账号[{self.name}] 提现失败：", e)
            self.withdrawPost(exchangeParams)

    def init(self):
        try:
            characters = string.ascii_letters + string.digits
            r = safe_request(
                "GET",
                f"https://nsr.zsf2023e458.cloud/yunonline/v1/getchatsite?t={time.time()}&cid={''.join(random.choices(characters, k=32))}&code=081ktRFa1TM60H0gr4Ga1U{''.join(random.choices(characters, k=10))}&state=1",
                verify=False,
            )
            self.domnainHost = r.json()["data"]["luodi"].split("/")[2]
            # print(r.text)
            print(f"账号[{self.name}]提取到的域名：{self.domnainHost}")
            self.headers = {
                "Connection": "keep-alive",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090621) XWEB/8351 Flue",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": f"http://{self.domnainHost}/",
                "Origin": f"http://{self.domnainHost}",
                # "Host": f"{self.domnainHost}",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Cookie": f"ysm_uid={self.ysm_uid};",
            }
            # 获取requestId
            self.signid = ""
            for i in range(3):
                r = safe_request(
                    "GET",
                    f"http://{self.domnainHost}/",
                    headers={
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "zh-CN,zh;q=0.9",
                        "Cookie": f"ysmuid={self.ysm_uid}",
                    },
                    verify=False,
                )
                htmltext = r.text
                if r.history:
                    for resp in r.history:
                        if "open.weixin.qq.com" in resp.headers["Location"]:
                            print(
                                f"账号[{self.name}] Cookie已过期，请重进一下网站，就会自动更新Cookie（目前不确定过期是因为自己手动进去过了还是什么其他原因）"
                            )
                            return False
                res1 = re.sub("\s", "", htmltext)
                signidl = re.findall('\)\|\|"(.*?)";', res1)
                # print(signidl, htmltext)
                if signidl == []:
                    time.sleep(1)
                    continue
                else:
                    self.signid = signidl[0]
                    break
            if self.signid == "":
                print(f"账号[{self.name}]初始化 requestId 失败,账号异常")
                return False
            # 获取提现页面地址
            r = safe_request(
                "GET",
                f"http://{self.domnainHost}/?cate=0",
                headers={
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Cookie": f"ysmuid={self.ysm_uid}",
                },
                verify=False,
            )
            htmltext = r.text
            res1 = re.sub("\s", "", htmltext)
            signidl = re.findall('/yunonline/v1/exchange(.*?)"', res1)
            # print("初始化 提现参数:", signidl[0])
            if signidl == []:
                print(f"账号[{self.name}]初始化 提现参数 失败,账号异常")
                return False
            else:
                self.exchangeParams = signidl[0]
            rewardNumResult = re.search(
                'div class="num number rewardNum">(.*?)</', htmltext
            )
            # print("初始化 提现参数:", signidl[0])
            if rewardNumResult == []:
                print(f"账号[{self.name}]初始化 提现参数 失败,账号异常")
                return False
            else:
                self.balance = float(rewardNumResult[1])
            return True
        except Exception as e:
            # raise e
            print(f"账号[{self.name}]初始化失败,请检查你的ck")
            return False

    def run(self):
        if self.init():
            self.user_info()
            self.hasWechat()
            self.gold()
            self.read()
            time.sleep(3)
            self.gold()
            time.sleep(3)
            self.withdraw()


def getNewInviteUrl():
    r = safe_request(
        "GET", "https://www.filesmej.cn/waidomain.php", verify=False
    ).json()
    if r.get("code") == 0:
        newEntryUrl = r.get("data").get("luodi")
        parsed_url = urlparse(newEntryUrl)
        host = parsed_url.hostname
        return f"https://u7ds.sy673.shop/yunonline/v1/auth/2639bb95daba1d99e5338a8c2e21e2f0?codeurl=u7ds.sy673.shop&codeuserid=2&time=1709021176".replace(
            "u7ds.sy673.shop", host or "u7ds.sy673.shop"
        )
    else:
        return "https://u7ds.sy673.shop/yunonline/v1/auth/2639bb95daba1d99e5338a8c2e21e2f0?codeurl=u7ds.sy673.shop&codeuserid=2&time=1709021176"


if __name__ == "__main__":
    # appToken：这个是填wxpusher的appToken
    # topicIds：这个是wxpusher的topicIds改成你自己的
    # 示例: 幻生#oZdBp04psgoN8dN1ET_uo81NTC31#3000#AT_UyIlbj2222nynESbM2vJyA7DrmUmUXD#11686
    accounts = os.getenv("xyyyd")
    inviteUrl = getNewInviteUrl()
    if accounts is None:
        print(f"你没有填入xyyyd，咋运行？\n走下邀请呗：{inviteUrl}")
    else:
        # 获取环境变量的值，并按指定字符串分割成多个账号的参数组合
        accounts_list = os.environ.get("xyyyd").split("&")

        # 输出有几个账号
        num_of_accounts = len(accounts_list)
        moreTip = ""
        if readPostDelay > 0:
            moreTip = f"已设置的推送文章等待点击时间为 {readPostDelay}秒 "
        print(
            f"当前脚本版本：幻生魔改自用版 V1.61 \n幻生提示：获取到 {num_of_accounts} 个账号 {moreTip}\n注册地址：{inviteUrl}"
        )

        # 遍历所有账号
        for i, account in enumerate(accounts_list, start=1):
            # print("\n")
            print("-" * 50)
            print(f"账号[{account.split('#')[0]}]开始执行任务 >>>")
            # print("\n")
            # 按@符号分割当前账号的不同参数
            values = account.split("#")
            # print(values)
            cg = {}
            try:
                if len(values) == 3:
                    cg = {
                        "name": values[0],
                        "ysm_uid": values[1],
                        "unionId": values[2],
                        "txbz": 3000,
                        "aliAccount": "",
                        "aliName": "",
                    }
                else:
                    cg = {
                        "name": values[0],
                        "ysm_uid": values[1],
                        "unionId": values[2],
                        "txbz": values[3] or 3000,
                        "aliAccount": "",
                        "aliName": "",
                    }
            except Exception as e:
                # 处理异常
                print("幻生逼逼叨:", "配置的啥玩意，缺参数了憨批，看清脚本说明！")
                continue
            cg["appToken"] = ""
            cg["topicIds"] = ""
            # print("手动：", len(values), values[4])
            if len(values) >= 5:
                if values[4]:
                    cg["appToken"] = values[4]
            else:
                cg["appToken"] = wxpusherAppToken
            if len(values) >= 6:
                if values[5]:
                    cg["topicIds"] = values[5]
            else:
                cg["topicIds"] = wxpusherTopicId
            if len(values) >= 7:
                if values[6]:
                    cg["aliName"] = values[6]
            if len(values) >= 8:
                if values[7]:
                    cg["aliAccount"] = values[7]
            try:
                if wechatBussinessKey == "":
                    if cg["appToken"].startswith("AT_") == False:
                        print(f"幻生提示，账号[{account.split('#')[0]}] wxpush 配置错误，快仔细看头部说明！")
                        continue
                    if (cg["appToken"].startswith("AT_") == False) or (
                        cg["topicIds"].isdigit() == False
                    ):
                        print(f"幻生提示，账号[{account.split('#')[0]}] wxpush 配置错误，快仔细看头部说明！")
                        continue
                api = HHYD(cg)
                if cg["aliName"] and cg["aliAccount"]:
                    print(
                        f"幻生提示，账号[{account.split('#')[0]}] 采用了 支付宝提现，姓名：{cg['aliName']}，账户：{cg['aliAccount']}"
                    )
                else:
                    print(f"幻生提示，账号[{account.split('#')[0]}] 采用了 微信提现")
                api.run()
            except Exception as e:
                if "Expecting value: line 1 column 1" in str(e):
                    print(f"幻生提示，账号[{account.split('#')[0]}] 疑似 unionId出错，换一个吧！")
                elif "link' is not defined" in str(e):
                    print(
                        f"幻生提示，账号[{account.split('#')[0]}] 疑似 新号的某种原因导致的无法阅读，请手动阅读两篇再试试吧！"
                    )
                else:
                    print(f"幻生提示，账号[{account.split('#')[0]}] 出错啦，请将下面报错截图发到tg交流群:")
                raise e
                continue
            # print("\n")
            print("-" * 50)
            print(f"账号[{account.split('#')[0]}]执行任务完毕！")
            # print("\n")
