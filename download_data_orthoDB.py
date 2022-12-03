import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os

genes = []
f = r'D:\GageTracker\bin\problem_info'
outpath = r'D:\GageTracker\data\orthoDB_1'

f = open(f).read().split("\n")
for i in f:
    if "groups" in i:
        gene = i.split(",")[2].split("&")[0].split("=")[1]
        genes.append(gene)

option = webdriver.ChromeOptions()
option.add_argument('headless')
driver = webdriver.Chrome(chrome_options=option)
for i in genes:
    i = i.replace(".html", "")
    outpath_f = os.path.join(outpath, i + ".html")
    outf = open(outpath_f,"w", encoding='utf-8')
    i_request = "https://www.orthodb.org/?query={0}&level=7214&species=7214".format(i)
    driver.get(i_request)
    
    # 计算一下找到几个同源簇
    xpath = '//*[@id="summary"]/div[1]'
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpath)))
    group_num = driver.find_element("xpath", xpath).text.split()[1]
    
    if group_num == "no":
        # 没有找到结果
        res_xpath = '//*[@id="summary"]/div[1]'
        res = driver.find_element("xpath", res_xpath).text
        print("fail,", res + ",", i_request)
    else:
        group_num = int(group_num)
        if group_num == 1:
            # 找到一个group
            outpath_f = os.path.join(outpath, i + ".html")
            xpath_cmd = '//*[@id="group0"]/div[5]/div[2]/ul/li/span/span[2]/span[1]'
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath_cmd)))
            html = driver.page_source
            outf.write(html)
            outf.close()
            print("OK!", i_request)
        else:
            # 找到两个group
            js = 'document.querySelector("#group0 > div > div.s-group-header-arrow.s-group-header-arrow-right > a").click()'
            driver.execute_script(js)
            js = 'document.querySelector("#group1 > div > div.s-group-header-arrow.s-group-header-arrow-right > a").click()'
            driver.execute_script(js)
            xpat_wait = '//*[@id="group0"]/div[6]/div[2]/ul/li[1]/span/span[2]/span[1]'
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpat_wait)))
            xpath_wait = '//*[@id="group1"]/div[6]/div[2]/ul/li/span/span[2]/span[1]'
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpat_wait)))
            html = driver.page_source
            outf.write(html)
    outf.close()
            
