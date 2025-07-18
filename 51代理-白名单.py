'''
51代理-白名单.py
变量名：FIVE_ONE_PROXY_APPKEY
变量值：秘钥
脚本功能：添加 IP 到白名单
作者：Huansheng
定时：0 0-23 * * *
'''
import os
import requests
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_appkey_from_env():
    """
    从环境变量中获取秘钥的值
    """
    appkey = os.getenv('FIVE_ONE_PROXY_APPKEY')
    if not appkey:
        logging.error("未找到环境变量 FIVE_ONE_PROXY_APPKEY")
        raise EnvironmentError("未找到环境变量 FIVE_ONE_PROXY_APPKEY")
    return appkey

def get_whitelist(appkey):
    """
    获取当前白名单列表
    """
    url = f"http://bapi.51daili.com/white-ip/list?appkey={appkey}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        logging.info("成功获取白名单列表")
        return response.json()
    except requests.RequestException as e:
        logging.error(f"获取白名单失败: {e}")
        return None

def add_to_whitelist(appkey, ips, isdel=1):
    """
    添加 IP 到白名单
    :param appkey: 秘钥
    :param ips: 要添加的 IP 地址，多个 IP 用逗号分隔
    :param isdel: 是否删除最早添加的 IP（0：不删除；1：删除）
    :return: 响应结果
    """
    url = f"http://bapi.51daili.com/white-ip/add?appkey={appkey}&isdel={isdel}&ips={ips}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        result = response.json()
        if result.get('code') == 1:
            logging.info(result.get('msg'))
        else:
            logging.error(result.get('msg'))
        return result
    except requests.RequestException as e:
        logging.error(f"添加白名单失败: {e}")
        return None

def main():
    try:
        # 从环境变量中获取秘钥
        appkey = get_appkey_from_env()

        # 获取当前白名单
        whitelist = get_whitelist(appkey)
        if whitelist and whitelist.get('code') == 200:
            ips = [entry['whiteip'] for entry in whitelist['rows']]
            logging.info(f"当前白名单共 {whitelist['total']} 个 IP：")
            for entry in whitelist['rows']:
                logging.info(f"IP: {entry['whiteip']} | 更新时间: {entry['updatetime']}")
        else:
            logging.warning("未能成功获取白名单数据")

        # 添加新的 IP 到白名单
        ips_to_add = "AUTO"
        result = add_to_whitelist(appkey, ips_to_add)

        if result and result.get('code') == 1:
            logging.info("IP 添加成功或已存在")
        else:
            logging.error("IP 添加失败")

    except Exception as e:
        logging.error(f"脚本执行过程中发生错误: {e}")

if __name__ == "__main__":
    main()
