# coding-utf-8
import time
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Login(object):
    def __init__(self):
        self.headers = {
            "Origin":"https://github.com",
            "Host":"github.com",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"
        }
        self.login_url = "https://github.com/login"
        self.post_url = "https://github.com/session"
        self.session = requests.Session()

        self.lresponse = self.session.get(self.login_url, headers=self.headers)
        self.html = etree.HTML(self.lresponse.text)


    def token(self):
        token = self.html.xpath('//input[@name="authenticity_token"]/@value')[0]
        return token

    def ga_id(self):
        broser = webdriver.Chrome()
        broser.get(self.login_url)
        time.sleep(5)
        html = broser.page_source
        html = etree.HTML(html)
        ga_id = html.xpath('//div//input[@name="ga_id"]/@value')[0]
        return ga_id

    def timestamp(self):
        tiemstamp = self.html.xpath('//input[@name="timestamp"]/@value')[0]
        return tiemstamp

    def timestamp_secret(self):
        tiemstamp_secret = self.html.xpath('//input[@name="timestamp_secret"]/@value')[0]
        return tiemstamp_secret


    def login(self):
        formdata = {
            'commit':'Sign in',
            'utf8':'√',
            'authenticity_token':self.token(),
            'ga_id':self.ga_id(),
            'login':username,
            'password':password,
            'webauthn-support':'',
            'webauthn-iuvpaa-support':'',
            'timestamp':self.timestamp(),
            'timestamp_secret':self.timestamp_secret()

        }
        response = self.session.post(self.post_url,data=formdata,headers=self.headers)


        zhuye = self.session.get('https://github.com/settings/keys',headers =self.headers)
        print(zhuye.text)

if __name__ =="__main__":
    github = Login()
    github.login()
