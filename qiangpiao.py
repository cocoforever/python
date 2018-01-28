#!/usr/bin/env python
#coding:utf-8
"""
  Author:  cocoforever --<>
  Purpose: 
  Created: 2018/1/24
"""

from splinter.browser import Browser
from time import sleep
import json
import traceback
import time,sys
import os

#处理地址
def get_12306addr(addr):
    all_addr = {'台州':'TZH','上海':'SHH'}
    
    #1.将中文转unicode
    ascii_addr = json.dumps(addr,ensure_ascii=True).replace("\"","").replace("\\","%")
    return ascii_addr + '%2C' + all_addr[addr]

class huoche(object):
    '''docstring for huoche'''
    driver_name = ''
    executable_path = ''
    
    #用户名和密码
    username = u'419936222@qq.com'
    passwd   = u'chengyong120522'
    start_addr = get_12306addr('台州')
    end_addr   = get_12306addr('上海')
    
    #时间
    dtime = u'2018-01-30'
    
    #车次，选择第几趟，0则从上到下一次点击
    order = 0
    
    #乘客名字
    passengers = [u'程勇']
    
    #席位座次
    seating = u'二等座'
    adult   = u'成人票'
    
    #座位
    seats = ['A']
    
    #网址
    ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init"
    login_url  = "https://kyfw.12306.cn/otn/login/init"
    initmy_url = "https://kyfw.12306.cn/otn/index/initMy12306"
    buy        = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"
    
    def __init__(self):
        self.driver_name = 'chrome'
        self.executable_path = 'chromedriver'
        
    def login(self):
        self.driver.visit(self.login_url)
        self.driver.fill('loginUserDTO.user_name',self.username)
        sleep(1)
        self.driver.fill('userDTO.password',self.passwd)
        sleep(1)
        print('等待验证码，自行输入***')
        while True:
            if self.driver.url != self.initmy_url:
                sleep(1)
            else:
                break
    
    def start(self):
        self.driver = Browser(driver_name=self.driver_name)
        self.driver.driver.set_window_size(1480,1096)
        self.login()
        sleep(1)
        
        self.driver.visit(self.ticket_url)
        try:
            print('购票页面开始...')
            ##sleep(1)
            
            #加载查询信息
            self.driver.cookies.add({"_jc_save_fromStation":self.start_addr})
            self.driver.cookies.add({'_jc_save_toStation':self.end_addr})
            self.driver.cookies.add({'_jc_save_fromDate':self.dtime})
            self.driver.reload()
            
            count = 0
            if self.order != 0:
                while self.driver.url == self.ticket_url:
                    self.driver.find_by_text('查询').click()
                    count += 1
                    print('循环点击查询...第{}次'.format(count))
                    #sleep(1)
                    
                    try:
                        self.driver.find_by_text('预订').click()
                    except Exception as e:
                        print(e)
                        print('还没开始预定')
                        continue
            else:
                while self.driver.url == self.ticket_url:
                    self.driver.find_by_text('查询').click()
                    count += 1
                    print('循环点击查询...第{}次'.format(count))
                    sleep(1)
                    
                    try:
                        for i in self.driver.find_by_text('预订'):
                            i.click()
                            #sleep(1)
                    except Exception as e:
                        print(e)
                        print('还没开始预订 {}'.format(count))
                        continue
            
            print('开始预订')
            sleep(1)
            
            print('开始选择用户')
            for user in self.passengers:
                self.driver.find_by_text(user).last.click()
            
            print('提交订单')
            #sleep(1)
            self.driver.find_by_id('submitOrder_id').click()
            
            #sleep(1.5)
            print('开始选座')
            for i in range(len(self.passengers)):
                self.driver.find_by_id(str(i+1)+self.seats[i]).last.click()
            self.driver.find_by_id('qr_submit_id').click()
        
        except Exception as e:
            print(e)

if __name__ == '__main__':
    huoche = huoche()
    huoche.start()