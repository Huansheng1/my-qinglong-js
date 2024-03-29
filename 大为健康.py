"""
 * 大为健康 V1.40

 * 外面嘎嘎代挂的一天8R项目

 * 微信打开：https://hb2.hbdtxt.com/#/pages/index/video?huodong_id=1648345948&tid=1352505&store_id=131

 * 一个微信一天八块，先改 像老年人的头像和昵称，过十分钟再点链接 +客服 要进群，年龄装作五十岁以上的老年人
 * 然后抓两个参数如下配置，全自动奔放，每天运行一次即可，抓完不用管，自动判断自动领
 * 【注意】请将 大为健康-店铺ID.json 这个文件放在脚本同一目录！

 * export dwjkAccounts='uid#Authorization'

 * 多账号换行

 * 原作者：Tan90

 * Update by Huansheng

 * 定制、偷撸、投稿 联系 QQ：1047827439

"""
import json
import os
from urllib import parse
import requests
import time
import random
from datetime import datetime
import urllib3

urllib3.disable_warnings()

# 如果是三群请修改变量！比如 hb3，自己抓包看自己的请求接口是什么开头！
groupName = "hb2"


def remove_duplicates(arr):
    return list(set(arr))


def save_array_to_json(array, file_name):
    with open(file_name, "w") as f:
        json.dump(array, f)


def load_array_from_json(file_name):
    if not os.path.exists(file_name):
        with open(file_name, "w") as f:
            json.dump([], f)
    with open(file_name, "r") as f:
        return json.load(f)


def count_today_members(datalist):
    today = datetime.now().strftime("%Y-%m-%d")
    count = 0
    for data in datalist:
        if data["adddate"].startswith(today):
            count += 1
    return count


activeIdList = remove_duplicates(load_array_from_json("大为健康-店铺ID.json")) or []


def send_request(pageIndex):
    url = f"https://{groupName}.hbdtxt.com/api/index/huodong"
    headers = {
        "Authorization": "e2ccf7f8a24dca1464cec8d964e15019",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; NX629J_V1S Build/PQ3A.190705.09211555; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36 MMWEBID/2157 MicroMessenger/8.0.42.2460(0x28002A54) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "content-type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "X-Requested-With": "com.tencent.mm",
        "Referer": f"https://{groupName}.hbdtxt.com/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "s342b0066=tu7bbcn9brab7rhosb27jomff2",
    }
    data = {
        "keyword": "",
        "limit": 10,
        "number": (pageIndex - 1) * 10,
        "page": pageIndex,
        "api_type": "h5",
        "uid": "1350591",
    }
    try:
        global activeIdList
        response = requests.post(url, headers=headers, data=data, verify=False)
        response_text = response.text
        print("结果：", response_text)
        if response.json()["code"] == 1:
            activeIdList.extend([item["id"] for item in response.json()["list"]])
            # activeIdList.append(huodong_id)
            activeIdList = remove_duplicates(activeIdList)
            save_array_to_json(activeIdList, "大为健康-店铺ID.json")
            print(f"请求成功 - 当前活动数：{len(activeIdList)}")
        else:
            print(f"请求失败 - 当前页数: {pageIndex}，返回：{response_text}")
    except Exception as e:
        # raise e
        print(f"请求失败，延迟10s")
        time.sleep(10)  # 延迟60s避免报错


# 答题领红包
def recieveRebBag(uid, Authorization, huodong_id="1648773920"):
    url = f"https://{groupName}.hbdtxt.com/api/index/index"
    headers = {
        "Authorization": Authorization,
        "User-Agent": "/5.0 (Linux; Android 9; NX629J_V1S Build/PQ3A.190705.09211555; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36 MMWEBID/2157 MicroMessenger/8.0.42.2460(0x28002A54) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": f"https://{groupName}.hbdtxt.com/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "s342b0066=tu7bbcn9brab7rhosb27jomff2",
    }

    # Define the data for the POST request
    data = {"huodong_id": huodong_id, "ids": "", "api_type": "h5", "uid": uid}

    # Make the POST request
    response = requests.post(url, headers=headers, data=data)

    # Decode the response content to utf-8
    response_content = response.content.decode("utf-8")

    # Parse the JSON response
    response_data = json.loads(response_content)

    if response_data["code"] == 1:
        # Extract the required information
        # code = response_data["code"]
        # msg = response_data["msg"]
        # canyu_status = response_data["canyu_status"]
        # is_can = response_data["is_can"]
        # huodong = response_data["huodong"]
        wentilist = response_data["wentilist"]

        # Create a new list for the modified questions
        modified_wentilist = []

        for question in wentilist:
            daan = json.loads(question["daan"])[
                0
            ]  # Extract the first element from daan
            for option in question["xuanxiang"]:
                if option["xuhao"] == daan:
                    option["xuanzhong"] = 1
                else:
                    option["xuanzhong"] = 0
            modified_wentilist.append(question)

        # Print the modified list
        # print(f"问题列表={json.dumps(modified_wentilist, ensure_ascii=False)}")
        # 修改了data的内容
        data = json.dumps(modified_wentilist, ensure_ascii=False)

        # 编码data为URL编码形式
        encoded_data = parse.quote(data)

        # 打印结果
        a = f"wentilist={encoded_data}&huodong_id={huodong_id}&ids=&api_type=h5&uid={uid}"
        # print("答题提交数据：", a)
        url1 = f"https://{groupName}.hbdtxt.com/api/index/dati"
        response = requests.post(url1, headers=headers, data=a)
        response_data = response.json()
        if "上限" in response.text:
            return True
        # print("答题结果：", response.text)
        if response.json()["code"] == 1:
            print("答题成功：获得现金", response_data["money"])
            return True
        else:
            print("答题异常：", response_data["msg"])
            return False
    else:
        if "上限" in response.text:
            return True
        # print(response_data)
        if response_data["code"] == 777:
            print("答题失败，需要参加上一期活动：", response_data["msg"])
            if response_data["prev_huodong_id"]:
                return recieveRebBag(
                    uid, Authorization, response_data["prev_huodong_id"]
                )
            else:
                return False
        else:
            print("答题异常：", response_data["msg"])


def getUserTotalNumber(uid, token):
    url = f"https://{groupName}.hbdtxt.com/api/index/index"
    response = requests.post(
        url,
        headers={
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Authorization": token,
            "Connection": "keep-alive",
            "Host": f"{groupName}.hbdtxt.com",
            "Origin": f"https://{groupName}.hbdtxt.com",
            "Referer": f"https://{groupName}.hbdtxt.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
            "content-type": "application/x-www-form-urlencoded",
        },
        data={
            "huodong_id": "1648345948",
            "store_id": "131",
            "noneedlogin": "0",
            "api_type": "h5",
            "uid": uid,
        },
        verify=False,
    )
    result = response.json()
    # print(response.text)
    # print(response)
    if result["code"] == 1:
        print(f"查询成功 - 已领红包总数：{result['user']['count_money_num']}个")
        return int(result["user"]["count_money_num"])
    else:
        print(
            f"查询失败 - 返回：{response.json()['msg']}，请确认自己是哪个群的，2群 和 3群的接口是不一样的，自己看脚本说明，实在不行给我打钱咩"
        )
        return -1


def checkRecieveNumber(uid, token):
    url = f"https://{groupName}.hbdtxt.com/api/index/datilog"
    response = requests.post(
        url,
        headers={
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Authorization": token,
            "Connection": "keep-alive",
            "Host": f"{groupName}.hbdtxt.com",
            "Origin": f"https://{groupName}.hbdtxt.com",
            "Referer": f"https://{groupName}.hbdtxt.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
            "content-type": "application/x-www-form-urlencoded",
        },
        data={
            "api_type": "h5",
            "uid": uid,
        },
        verify=False,
    )
    result = response.json()
    # print(response.text)
    # print(response)
    if result["code"] == 1:
        todayNumber = count_today_members(result["datilist"]) or 0
        print(f"查询成功 - 今日已领红包数：{todayNumber}个")
        return int(todayNumber)
    else:
        print(
            f"查询失败 - 返回：{response.json()['msg']}，请确认自己是哪个群的，2群 和 3群的接口是不一样的，自己看脚本说明修改下配置即可，实在不行给我打钱咩"
        )
        return -1


if __name__ == "__main__":
    print(
        f"当前版本：大为健康 V1.11，Update by Huansheng \n更新地址：https://github.com/Huansheng1/my-qinglong-js\n自己看脚本说明，还不会的话给我打钱，包教包会！"
    )
    # print("开始遍历店铺")

    # # 创建多个线程并发发送请求
    # threads = []  # 下面是开始遍历的id
    # for pageIndex in range(1, 30):
    #     send_request(pageIndex)

    # # 等待所有线程完成
    # for t in threads:
    #     t.join()

    # print("遍历店铺已完成：", activeIdList)
    accountAnswerTime = 10
    activeIdList = sorted(activeIdList)
    accounts_list = os.environ.get("dwjkAccounts").split("&")
    # 输出有几个账号
    num_of_accounts = len(accounts_list)
    print(f"幻生提示：获取到 {num_of_accounts} 个账号")

    for accountToken in accounts_list:
        accountConfig = accountToken.split("#")
        print("-" * 50)
        print(f"\n账号[{accountConfig[0]}]答题操作开始")
        answerSuccess = 0
        queryNumber = checkRecieveNumber(accountConfig[0], accountConfig[1])
        if queryNumber >= 0:
            answerSuccess = queryNumber
            if answerSuccess == 10:
                print(f"账号[{accountConfig[0]}]都答题完10期了，还玩个屁！")
                continue
        else:
            print(f"账号[{accountConfig[0]}]获取今日答题数失败，怕封号，还玩个屁！")
            continue
        for activeId in activeIdList:
            if answerSuccess >= accountAnswerTime:
                print(f"账号[{accountConfig[0]}]都答题完10期了，还玩个屁！")
                break
            if recieveRebBag(accountConfig[0], accountConfig[1], activeId):
                answerSuccess = answerSuccess + 1
                print(f"账号[{accountConfig[0]}]延迟一会，进行下一次答题")
                time.sleep(random.randint(18, 46))
        print(f"账号[{accountConfig[0]}]答题操作 已完成")
