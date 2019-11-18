
# coding : utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import time
import pymysql

browser = webdriver.Chrome()
# 显示等待，指定最长等待时间
wait = WebDriverWait(browser, 10)
# 搜索关键字
KEYWORD = 'IPAD'
conn = pymysql.connect(
    host="localhost",
    database="test",
    user="root",
    password="root",
    port=3306,
    charset='utf8'
)
cursor = conn.cursor()

def login():
    logon_url = "https://login.taobao.com/"
    browser.get(logon_url)

    try:
        print("请扫码登录")
        time.sleep(10)
        # until（）方法传入等待条件，presence_of_element_located()代表节点出现，其参数为节点的定位元祖。
        input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="q"]')))
        submit = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="btn-search tb-bg"]')))
        input.clear()
        input.send_keys(KEYWORD)
        submit.click()
        time.sleep(2)
        print("登录成功")
    except Exception as e :
        print("登录失败",e)

def index_page():
    # 循环页数
    for i in range(2,11):
        html = browser.page_source
        get_products(html)

        print("正在翻页-------------")
        # 获取数字框，往里面写入数字，然后点击确定
        input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mainsrp-pager"]/div/div/div/div[2]/input')))
        input.clear()
        input.send_keys(i)
        # 确定按钮
        next = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@class="btn J_Submit"]')))
        next.click()
        print("翻页完成")
        time.sleep(3)

    print("请求完成！")

def get_products(html):
    """
    抓取商品信息
    :return:
    """
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('data-src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        write(product)

def write(info):
    sql = "insert into taobao_ipad (image,price,deal,title,shop,location)values (%s,%s,%s,%s,%s,%s);"
    cursor.execute(sql,(info["image"],info["price"],info["deal"],info["title"],info["shop"],info["location"]))

def main():

    login()
    index_page()

if __name__ == "__main__":
    main()
    conn.commit()
