"""
活动地址: http://2956396.w.u5re46414.3l0mqnkypptv.cloud/?p=2956396
脚本更新时间: 2023-12-17
抓包获取: Cookie，UserAgent。
key参数为PushPlus推送加的token用于接收通知，配置示例:["通知key1", "通知key2", "通知key3"]有几个写几个。
青龙脚本配置：请在环境变量配置GBYD_COOKIE，变量值为你抓取到的cookie与pushplus的token拼接，例如："cookie&pushplus=xxxxxx&desc=大号"，
如果多个账号请用'&&&'隔开，例如："cookie1&pushplus=11111&desc=大号&&&cookie2&pushplus=22222&desc=小号1"
desc是这个账号的描述, count是这个账号每天跑多少篇最大180。
如果要推送discord请在配置文件里配置变量DISCORD_WEBHOOK_URL，例如
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/idxxx/xxxxxxxxx"
如果要推送telegram，也请在配置文件里配置好，与qinglong共用变量
cron: */45 8-23 * * * 钢镚阅读.py
"""
import datetime
import os
import random
import hashlib
import re
import sys
import time
import traceback
import requests
import json
import emoji
from concurrent.futures import ThreadPoolExecutor

# gbyd_cookie = os.environ.get("GBYD_COOKIE")
gbyd_cookie = "zzbb_info=%7B%22openid%22%3A%22oF1b14oJ4opUjWH9gvL41aS7CG9Y%22%2C%22pid%22%3A2920660%2C%22uid%22%3A2956396%7D; gfsessionid=o-0fIv-_HEjjSvRLtm52jWfPvQwg&pushplus=a97fdd804d3d4228a13451c2a5db948&desc=大号&&&zzbb_info=%7B%22openid%22%3A%22oF1b14uS_ZsXU2e_MfONor5QfLTU%22%2C%22pid%22%3A2956396%2C%22uid%22%3A2992011%7D; gfsessionid=o-0fIv_ZFL9yiUKmWVqSPzROyywc&pushplus=7a30cef08741413bbb4917e21d59b50a&desc=小尾巴&&&zzbb_info=%7B%22openid%22%3A%22oF1b14oosg-qpZHuVm5zKO8FH82o%22%2C%22pid%22%3A2956396%2C%22uid%22%3A2958186%7D; gfsessionid=o-0fIv3fe-9wsH9QYy7_d6iY_T_E&pushplus=54316a3958d64490813b390a99ea218e&desc=新新&&&zzbb_info=%7B%22openid%22%3A%22oF1b14pE_71bcj-3ZbUxGFha0L6o%22%2C%22pid%22%3A2956396%2C%22uid%22%3A2992378%7D; gfsessionid=o-0fIv4t7mYaU2Nl7wC9TxaMpfKg&pushplus=4f7bda4d77a245a2b7b56b1eb1552862&desc=申屠&&&zzbb_info=%7B%22openid%22%3A%22oF1b14tbV9COTosZko47q-Z3D2qQ%22%2C%22pid%22%3A2956396%2C%22uid%22%3A2993372%7D; gfsessionid=o-0fIv5alQLzLUEFYIoDgUaJp0Vo&pushplus=fae32cbbadf74c81a963ef7e9e6010a7&desc=小尾巴mom&&&zzbb_info=%7B%22openid%22%3A%22oF1b14kCdfFWRt5u4CpnVFPzg6tI%22%2C%22pid%22%3A2956396%2C%22uid%22%3A2993274%7D; gfsessionid=o-0fIv0alYj2-BeGFwig2FN6qokQ&pushplus=fae32cbbadf74c81a963ef7e9e6010a7&desc=Nemo"

# 按 "&&&" 分割成多个账号信息
if type(gbyd_cookie) != str:
    gbyd_cookie = ""
account_infos = gbyd_cookie.split("&&&")

# 初始化账号列表
accounts_list = []

# 遍历每个账号信息
for account_info in account_infos:
    # 按 "&" 分割成多个字段
    fields = account_info.split("&")
    # 检查是否有足够的字段
    if len(fields) >= 3:
        # 创建账号字典
        account_dict = {
            "Cookie": fields[0],
            "key": fields[1].split("=")[-1],  # 获取key字段的值
            "desc": fields[2].split("=")[-1],  # 获取desc字段的值
            "UA": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.44(0x18002c2b) NetType/WIFI Language/en",
            "count": 180,
        }
        # 将账号字典添加到列表中
        accounts_list.append(account_dict)

check = [
    "MzkyMzI5NjgxMA==",
    "MzkzMzI5NjQ3MA==",
    "Mzg5NTU4MzEyNQ==",
    "Mzg3NzY5Nzg0NQ==",
    "MzU5OTgxNjg1Mg==",
    "Mzg4OTY5Njg4Mw==",
    "MzI1ODcwNTgzNA==",
    "Mzg2NDY5NzU0Mw==",
    "MzA4OTI3ODY4Mg=",
    "MzAwNTIzNjYzNA==",
    "Mzg4NjY5NzE4NQ==",
    "MzkwODI5NzQ4MQ==",
    "MzkzMzI5Njc0Nw==",
    "Mzg5NDg5MDY3Ng==",
    "MzA3MjMwMTYwOA==",
    "MzkyNTM5OTc3OQ==",
    "MjM5OTQ0NzI3Ng==",
    "MzkwOTU3MDI1OA==",
    "MzAwOTc2NDExMA==",
    "MzA3OTI4MDMxMA==",
    "MzkxNzI2ODcwMQ==",
    "MzA3MDMxNzMzOA==",
    "Mzg3NjAwODMwMg==",
    "MzI3NDE2ODk1Nw==",
    "MzIyMDMyNTMwMw==",
    "MzIzMjY2NTMwNQ==",
    "MzkxNzMwMjY5Mg==",
    "MzA5Njg3MDk2Ng==",
    "MzA5MzM1OTY2OQ==",
    "MzA4NTQwNjc3OQ==",
    "MjM5NTY5OTU0MQ==",
    "MzU1NTc4OTg2Mw==",
    "MzkwMzI0NjQ4Mw==",
    "MzI3OTA2NDk0Nw==",
    "MjM5MDU4ODgwMw==",
    "Mzg4NzUyMjQxMw==",
]


def log(message):
    print(
        emoji.emojize(
            f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]}] {message}'
        )
    )


def send_notification(title, content, key):
    log(content)
    # 发送到pushplus
    send_pushplus_notification(title, content, key)
    # 发送tg
    send_telegram_notification(title, content)
    # 发送到discord
    send_discord_notification(title, content)


def send_pushplus_notification(title, content, key):
    pushplus_url = "http://www.pushplus.plus/send"
    content += f', 事件ID：{datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]}'
    pushplus_data = {
        "template": "txt",
        "token": key,
        "title": title,
        "content": content,
    }

    try:
        requests.post(pushplus_url, data=pushplus_data, timeout=10)
    except requests.Timeout:
        log("推送pushplus消息超时，重试")
        requests.post(pushplus_url, data=pushplus_data, timeout=10)
    except requests.RequestException as e:
        log(f"推送pushplus异常")
        traceback.print_exc()


def send_telegram_notification(title, content):
    telegram_bot_token = os.environ.get("TG_BOT_TOKEN")
    telegram_chat_id = os.environ.get("TG_USER_ID")

    if not telegram_bot_token or not telegram_chat_id:
        log("Telegram bot_token或chat_id缺失。跳过发送Telegram通知。")
        return

    telegram_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    telegram_params = {
        "chat_id": telegram_chat_id,
        "text": content,
        "parse_mode": "Markdown",
    }

    try:
        response = requests.post(telegram_url, params=telegram_params, timeout=10)
        response.raise_for_status()
    except requests.Timeout:
        pass
    except requests.RequestException as e:
        log("发送Telegram通知时出错: {e}")


def send_discord_notification(title, content):
    discord_webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")

    if not discord_webhook_url:
        log("Discord Webhook URL缺失。跳过发送Discord通知。")
        return

    discord_data = {"content": content, "username": title}

    try:
        response = requests.post(discord_webhook_url, json=discord_data, timeout=10)
        response.raise_for_status()
    except requests.Timeout:
        pass
    except requests.RequestException as e:
        log("发送Discord通知时出错: {e}")


# 示例用法：
# send_notification("通知标题", "通知内容", ["PUSH_PLUS_KEY"])


def calculate_sign():
    current_time = str(int(time.time()))
    sign_str = f"key=4fck9x4dqa6linkman3ho9b1quarto49x0yp706qi5185o&time={current_time}"
    sha256_hash = hashlib.sha256(sign_str.encode())
    return sha256_hash.hexdigest(), current_time


def read_articles(cookie, UA, key, desc, count, acct_idx):
    if not cookie:
        log(f"账号[{desc}]未获取到cookie")
        return
    time.sleep(random.randint(1, 6))
    url = "http://2903155.mwierdnx2hd0.ntryvuir104.fnpz9xy95zkel.cloud/share"
    headers = {"User-Agent": UA, "Cookie": cookie}
    sign, current_time = calculate_sign()
    data = {"time": current_time, "sign": sign}
    response = requests.get(url, headers=headers, json=data).json()
    if response["code"] == 0:
        share_links = response["data"]["share_link"]
        p_value = share_links[0].split("=")[1].split("&")[0]
        headers = {"User-Agent": UA}
        response = requests.get(share_links[0], headers=headers, allow_redirects=False)
        url1 = response.headers["Location"]
        pattern = r"http://([^/]+)"
        match = re.search(pattern, url1)
        host = match.group(1)
    else:
        time.sleep(random.randint(1, 6))
        send_notification("error", f"{response['message']}", key)
        return
    total_gain = 0  # 记录总的阅读积分
    total_read = 0
    total_gold = 0
    total_remain = 0
    message = ""
    # 获取这个账号跑了多少篇
    sign, current_time = calculate_sign()
    url = f"http://{host}/read/info?time={current_time}&sign={sign}"
    headers = {"User-Agent": UA, "Cookie": cookie}
    try:
        res = requests.get(url, headers=headers, timeout=7).json()
    except requests.Timeout:
        res = requests.get(url, headers=headers, timeout=7).json()
    if res["data"]["read"] > count:
        time.sleep(random.randint(1, 6))
        send_notification(
            "今日阅读已完成",
            f"账号[{desc}]今日阅读任务已达上限 {count} 篇",
            key,
        )
        return
    for o in range(30):
        sign, current_time = calculate_sign()
        url = f"http://{host}/read/task"
        headers = {"User-Agent": UA, "Cookie": cookie}
        data = {"time": current_time, "sign": sign}
        time.sleep(2)
        try:
            response = requests.get(url, headers=headers, json=data, timeout=7).json()
        except requests.Timeout:
            response = requests.get(url, headers=headers, json=data, timeout=7).json()
        if response["code"] == 1:
            message = response["message"]
            # await send_notification("退出", f"账号[{desc}]已退出！{response['message']}", key)
            break
        else:
            try:
                link = response["data"]["link"]
                response = requests.get(link, headers=headers, allow_redirects=False)
                link1 = response.headers["Location"]
                response = requests.get(url=link1, headers=headers).text
                pattern = r'<meta\s+property="og:url"\s+content="([^"]+)"\s*/>'
                pattern1 = r'nickname">(.*?)<'
                matches1 = re.search(pattern1, response)
                biz = link1.split("__biz=")[1].split("&")[0]
                nickname = matches1.group(1) if matches1 else None
                if biz in check:
                    time.sleep(random.randint(1, 6))
                    send_notification(
                        "请处理检测文章", f"账号[{desc}]发现检测文章, 请手动阅读一篇，标题:{nickname}", key
                    )
                    break  # 如果检测到文章，跳出循环
                sleep = random.randint(23, 38)
                time.sleep(sleep)
                sign, current_time = calculate_sign()
                url = f"http://{host}/read/finish"
                headers = {"User-Agent": UA, "Cookie": cookie}
                data = {"time": current_time, "sign": sign}
                try:
                    try:
                        response = requests.get(
                            url, headers=headers, data=data, timeout=7
                        ).json()
                    except json.decoder.JSONDecodeError:
                        break
                    except Exception:
                        log("阅读异常，随机几秒延后重试")
                        time.sleep(random.randint(1, 10))
                        try:
                            response = requests.get(
                                url, headers=headers, data=data, timeout=7
                            ).json()
                        except json.decoder.JSONDecodeError:
                            break
                except requests.Timeout:
                    try:
                        response = requests.get(
                            url, headers=headers, data=data, timeout=7
                        ).json()
                    except json.decoder.JSONDecodeError:
                        break
                if response["code"] == 0:
                    gain = response["data"]["gain"]
                    total_gain += gain  # 记录阅读积分
                    read = response["data"]["read"]
                    total_read = read
                    gold = response["data"]["gold"]
                    total_gold = gold
                    remain = response["data"]["remain"]
                    total_remain = remain
                    log(
                        f"账号[{desc}]第 {o + 1} 篇阅读成功--获得钢镚：{gain} :money_bag: ,今日阅读：{read} 篇--今日获取：{gold} :money_bag:,可提{remain} :money_bag:"
                    )
                    if read > count:
                        time.sleep(random.randint(1, 6))
                        send_notification(
                            "退出",
                            f"账号[{desc}]超过设置最大阅读数!, 当前阅读 {read} 篇, 设置最大阅读数 {count} 篇",
                            key,
                        )
                        return
                else:
                    break
            except KeyError:
                break
    # 任务执行完后发送总的阅读积分通知
    time.sleep(random.randint(1, 6))
    if total_gain == 0:
        # send_notification("退出", f"账号[{desc}]{message}", key)
        log(f"账号[{desc}]退出：{message}")
    else:
        send_notification(
            "本次阅读任务完成",
            f"账号[{desc}]此次总获得阅读积分：{total_gain}，今日阅读：{total_read} 篇，今日获取：{total_gold} :money_bag:，可提现钢镚：{total_remain} :money_bag: \n{message}",
            key,
        )


def execute_accounts(account, index):
    try:
        cookie = account.get("Cookie")
        ua = account.get("UA")
        desc = account.get("desc")
        key = account.get("key")
        count = account.get("count")
        read_articles(
            cookie=cookie, UA=ua, key=key, desc=desc, count=count, acct_idx=index
        )
    except Exception as e:
        log(f"账号阅读[{desc}]发生运行时异常")
        traceback.print_exc()  # 打印异常栈信息


if len(accounts_list) < 1:
    log("没有读取到账号")
    sys.exit(0)
# 使用线程池执行每个账号的任务
with ThreadPoolExecutor(max_workers=len(accounts_list)) as executor:
    for index, account_info in enumerate(accounts_list, start=1):
        executor.submit(execute_accounts, account_info, index)
        time.sleep(random.randint(1, 30))
