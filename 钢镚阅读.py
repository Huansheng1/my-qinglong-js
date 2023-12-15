import datetime
import os
import random
import hashlib
import re
import time
import requests
import json
from concurrent.futures import ThreadPoolExecutor

# 活动地址: http://w.6mcyrj8t2qnq.cloud/?p=2918458
# 脚本更新时间: 2023-12-13
"""
抓包获取: Cookie，UserAgent。
key参数为PushPlus推送加的token用于接收通知，配置示例:["通知key1", "通知key2", "通知key3"]有几个写几个。
desc是这个账号的描述, count是这个账号每天跑多少篇最大180。
"""
# cron: */30 8-18 * * * nohup python3 /path/task.py >> /dev/null 2>&1 &
"""""" "只需要改下面的部分" """"""
accounts_list = [
    {
        "Cookie": "zzbb_info=%7B%22openid%22%3A%22oF1b14oJ4opUjWH9gvL41aS7CG9Y%22%2C%22pid%22%3A2920660%2C%22uid%22%3A2956396%7D; gfsessionid=o-0fIv-_HEjjSvRLtm52jWfPvQwg",
        "UA": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.44(0x18002c2b) NetType/WIFI Language/en",
        "keys": [
            "a97fdd804d3d4228a13451c2a5db948e",
        ],
        "desc": "halfroom",
        "count": 180,
    },
    # {
    #     "Cookie": "cookie",
    #     "UA": "ua",
    #     "keys": ["通知key"],
    #     "desc": "账号2",
    #     "count": 180,
    # },
    # 添加更多账号信息...
]
"""""" "只需要改上面的部分" """"""

check = [
    "MzkzMzI5NjQ3MA==",
    "MzkzMzI5Njc0Nw==",
    "MzkyMzI5NjgxMA==",
    "MzkzMzI5Njc0Nw==",
    "MzkyMzI5NjgxMA==",
    "Mzg4NjY5NzE4NQ==",
    "Mzg3NzY5Nzg0NQ==",
    "Mzg5NTU4MzEyNQ==",
    "MzI1ODcwNTgzNA==",
    "Mzg2NDY5NzU0Mw==",
    "MzkwODI5NzQ4MQ==",
    "MzU5OTgxNjg1Mg==",
]


def log(message):
    print(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]}] {message}')


def send_notification(title, content, keys):
    content += f', 事件ID：{datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]}'
    log(content)
    # 发送到pushplus
    send_pushplus_notification(title, content, keys)
    # 发送tg
    send_telegram_notification(title, content)
    # 发送到discord
    send_discord_notification(title, content)


def send_pushplus_notification(title, content, keys):
    pushplus_url = "http://www.pushplus.plus/send"

    for key in keys:
        pushplus_data = {
            "template": "txt",
            "token": key,
            "title": title,
            "content": content,
        }

        try:
            with requests.Session() as session:
                session.post(pushplus_url, data=pushplus_data, timeout=10)
        except requests.Timeout:
            pass
        except requests.RequestException as e:
            log("PushPlus推送时出错: {e}")


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


def read_articles(cookie, UA, keys, desc, count):
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
        send_notification("error", f"{response['message']}", keys)
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
            "退出",
            f"账号:{desc}\n超过设置最大阅读数!, 当前阅读 {res['data']['read']} 篇, 设置最大阅读数 {count} 篇",
            keys,
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
            # await send_notification("退出", f"账号:{desc}\n已退出！{response['message']}", key)
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
                    send_notification("检测文章", f"账号:{desc}\n发现检测文章, 标题:{nickname}", keys)
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
                    # print(f"第 {o + 1} 篇阅读成功--获得钢镚：{gain} 💰\n今日阅读：{read} 篇--今日获取：{gold} 💰\n可提现钢镚：{remain} 💰")
                    if read > count:
                        time.sleep(random.randint(1, 6))
                        send_notification(
                            "退出",
                            f"账号:{desc}\n超过设置最大阅读数!, 当前阅读 {read} 篇, 设置最大阅读数 {count} 篇",
                            keys,
                        )
                        return
                else:
                    break
            except KeyError:
                break
    # 任务执行完后发送总的阅读积分通知
    time.sleep(random.randint(1, 6))
    if total_gain == 0:
        send_notification("退出", f"账号:{desc}\n{message}", keys)
    else:
        send_notification(
            "阅读任务完成",
            f"账号:{desc}\n此次总获得阅读积分：{total_gain}，今日阅读：{total_read} 篇，今日获取：{total_gold}，可提现钢镚：{total_remain}\n{message}",
            keys,
        )


def execute_accounts(account):
    cookie = account.get("Cookie")
    ua = account.get("UA")
    desc = account.get("desc")
    keys = account.get("keys")
    count = account.get("count")
    read_articles(cookie=cookie, UA=ua, keys=keys, desc=desc, count=count)


# 使用线程池执行每个账号的任务
with ThreadPoolExecutor(max_workers=len(accounts_list)) as executor:
    for account_info in accounts_list:
        executor.submit(execute_accounts, account_info)
        time.sleep(random.randint(1, 6))  # 等待一秒钟再执行下一个任务,保证不会并发推送导致推送失败

# # 使用线程池执行每个账号的任务
# with ThreadPoolExecutor(max_workers=len(accounts_list)) as executor:
#     executor.map(execute_accounts, accounts_list)
