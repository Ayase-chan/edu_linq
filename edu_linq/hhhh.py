# from selenium import webdriver
# import time
#
# while 1:
#     driver = webdriver.Chrome(r'C:\Users\lin\Desktop\day13\chromedriver.exe')
#     driver.get('https://reserve-prime.apple.com/CN/zh_CN/reserve/G/availability?&iUP=N')
#     time.sleep(3)
#     res = driver.find_elements_by_xpath('//*[@id="main"]/div')
#     # 打印数据内容
#     x = res[0].text
#     print(x)
#     driver.close()
#     s = '''我们目前不接受 iPhone 的预约购买。
# iPhone 预约购买情况每天可能有所不同，你可稍后实时查看今天的预约情况，也可以立即在线选购并选择其他购买方式。 如果你参加了 iPhone 年年焕新计划，请查询升级换购资格，然后预约到
# Apple Store 零售店购买新 iPhone。
# 查询升级换购资格'''
#     if x != s:
#         break

import requests
r = requests.get('https://reserve-prime.apple.com/CN/zh_CN/reserve/G/availability?&iUP=N')
print(r.text)
