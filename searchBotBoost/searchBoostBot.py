# -*- coding: utf-8 -*-

from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import threading
import random
import json
import traceback
import os
import time

STATUS = 1

def filePath():
    return os.path.dirname(os.path.abspath(__file__))

class boostBot:
    def __init__(self, site, request, sleep, click_sleep, stay_sleep, cycle_count, request_num):
        self.site = site
        self.request = request
        self.sleep = sleep
        self.click_sleep = click_sleep
        self.stay_sleep = stay_sleep
        self.cycle_count = cycle_count
        self.xpath = ['//p[.="Деятельность"]', '//p[.="О компании"]', '//p[.="Контакты"]']
        self.ids = ['comp-j7geey4o', 'comp-j7getfqo', 'comp-kjh4u1l9', 'comp-kjh555t4', 'comp-kjh52hc0', 'comp-j7getkms']
        self.request_num = request_num
          
    
    def main(self, search_engine):
        global STATUS
        try:
            self.driver = Firefox(executable_path=filePath() + '/geckodriver.exe')
            
            response = (self.google() if search_engine == 'https://google.com' else self.yandex())

            if response == 0:
                time.sleep(random.randint(self.stay_sleep[0], self.stay_sleep[1]))
            self.driver.quit()
            STATUS = (2 if response == 2 else 0)
        except:
            print(traceback.format_exc())
            self.driver.quit()
            STATUS = 2

    def proc_site(self):
        # Цикл по видам деятельности 
        cnt = random.randint(self.cycle_count[0], self.cycle_count[1])
        for ItrNum in range(0, cnt):
            self.driver.find_elements_by_xpath(self.xpath[0])[0].click() 
            time.sleep(random.randint(self.click_sleep[0], self.click_sleep[1]))
             # Выбор вида деятельности 
            ind = random.randint(0, 5)
            self.driver.find_elements_by_id(self.ids[ind])[0].click()
            time.sleep(random.randint(self.click_sleep[0], self.click_sleep[1]))
            hgt = self.driver.execute_script("return document.body.scrollHeight")
            hgt = hgt // 100
            for I in range(0, random.randint(hgt - 5, hgt)):
                S = "window.scrollTo(0," + str(I * 100) + ")"
                self.driver.execute_script(S)
                time.sleep(random.randint(0, 3) / 10)
            self.driver.find_element_by_tag_name('html').send_keys(Keys.HOME)
            time.sleep(random.randint(self.click_sleep[0], self.click_sleep[1]))         
            self.driver.find_element_by_tag_name('html').send_keys(Keys.END)
            time.sleep(self.sleep)         
            
        # Клик по Контактам или О Компании
        self.driver.find_elements_by_xpath(self.xpath[random.randint(1, 2)])[0].click()
        time.sleep(random.randint(self.click_sleep[0], self.click_sleep[1]))
        # Рандомное количество Page Down
        self.driver.find_element_by_tag_name('html').send_keys(Keys.HOME)
        time.sleep(self.sleep)         
        for I in range(0, random.randint(1, 2)):       
            self.driver.find_element_by_tag_name('html').send_keys(Keys.PAGE_DOWN)
            time.sleep(self.sleep)         

        return 0    

    def yandex(self):
        self.driver.get('https://yandex.ru')

        time.sleep(self.sleep)
        searchInput = self.driver.find_element_by_xpath('//input[@id="text"]')
        searchInput.click()
        searchInput.send_keys(self.request)
        time.sleep(self.sleep)

        searchButton = self.driver.find_element_by_xpath('//button[@type="submit"]')
        searchButton.click()
        time.sleep(self.sleep)

        main_cite = ''
        now_page = 1
        while True:
            time.sleep(self.sleep)
            cites = self.driver.find_elements_by_xpath('//a')
            for cite in cites:
                try:
                    if self.site in cite.get_attribute('href'): 
                        main_cite = cite
                        break
                except: pass
            if main_cite == '':
                now_page += 1
                try:
                    next_page = self.driver.find_element_by_xpath('//a[@aria-label="Следующая страница"]')
                    next_page.click()
                except: 
                    print('Сайт не найден по запросу: ' + self.request + ' Последняя страница: ' + str(now_page-1))
                    return 2
                time.sleep(self.sleep)
            else: break
        
        log_file = open(filePath() + "/request.txt", "a")
        try:
            log_file.write(str(self.request_num) + ' ' + time.strftime("%X", time.localtime()) + ' y "' + self.request + '" Страница: '  + str(now_page) + '\n')
        finally:    
            log_file.close()
        main_cite.click()
        
        self.driver.switch_to.window(self.driver.window_handles[1])
        
        try: WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.xpath[random.randint(0, len(self.xpath)-1)])))
        except: time.sleep(7)

        time.sleep(random.randint(self.click_sleep[0], self.click_sleep[1]))
 
        self.proc_site()

        return 0

    def google(self):
        self.driver.get('https://google.com')

        time.sleep(self.sleep)
        searchInput = self.driver.find_element_by_xpath('//input[@class="gLFyf gsfi"]')
        searchInput.click()
        searchInput.send_keys(self.request)

        time.sleep(self.sleep)
        actions = ActionChains(self.driver) 
        actions.send_keys(Keys.ENTER * 2)
        actions.perform()
        
        time.sleep(self.sleep)

        main_cite = ''
        now_page = 1
        while True:
            time.sleep(self.sleep)
            cites = self.driver.find_elements_by_xpath('//a')
            for cite in cites:
                try:
                    if self.site in cite.get_attribute('href'): 
                        main_cite = cite
                        break
                except: pass
            if main_cite == '':
                now_page += 1
                try:
                    next_page = self.driver.find_element_by_xpath('//a[@id="pnnext"]')
                    next_page.click()
                except: 
                    print('Сайт не найден по запросу: ' + self.request + ' Последняя страница: ' + str(now_page-1))
                    return 2
                time.sleep(self.sleep)
            else: break
        
        log_file = open(filePath() + "/request.txt", "a")        
        try:
            log_file.write(str(self.request_num) + ' ' + time.strftime("%X", time.localtime()) + ' g "' + self.request + '" Страница: '  + str(now_page) + '\n')
        finally:    
            log_file.close()
        main_cite.click()
        
        try: WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.xpath[random.randint(0, len(self.xpath)-1)])))
        except: time.sleep(7)

        time.sleep(random.randint(self.click_sleep[0], self.click_sleep[1]))
        self.proc_site()
        
        return 0
        
def start():
    with open(filePath() + "/config.json", "r", encoding='utf-8') as read_file:
        data = json.load(read_file)

    sleep = data["sleep"] # задержка после первого запуска (в секундах)
    site = data["site"] # исходный сайт
    request = data["request"] # запросы поиска
    sleep2 = data["sleep2"] # задержка между кликами (в секундах)
    click_sleep = data["click_sleep"] # задержка между кликами на сайте (нижняя и верхняя границы) (в секундах)
    stay_sleep = data["stay_sleep"] # задержка прибывания на сайте (нижняя и верхняя границы) (в секундах)
    cycle_count = data["cycle_count"] # количество кликов по видам деятельности (от и до) 
    search_sys = data["search_sys"] # Сейчас рандом. Если удалить одну будет работать, формат ссылок только такой
    request_num = 0
    log_file = open(filePath() + "/request.txt", "w")
    global STATUS
    while True:
        try:
            request_num = request_num + 1
            n = boostBot(site, request[random.randint(0, len(request)-1)], sleep2, click_sleep, stay_sleep, cycle_count, request_num)
            thread = threading.Thread(target=(n.main), args=(search_sys[random.randint(0, len(search_sys)-1)], ))
            STATUS = 1          
            thread.start()
            while STATUS == 1:
                time.sleep(1)

            if STATUS == 0:
                time.sleep(random.randint(sleep[0], sleep[1]))
        except: pass

if __name__ == '__main__':
    start()