import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os

age_f = r"D:\GageTracker\result\GageTracker_r1_0.5.age.protein_coding"
outpath = r"D:\GageTracker\data\orthoDB"
age_data = pd.read_csv(age_f, sep="\t")
genes = list(age_data["Gene"])
genes = os.listdir(r'D:\GageTracker\data\problems')

option = webdriver.ChromeOptions()
option.add_argument('headless')
driver = webdriver.Chrome(chrome_options=option)
for i in genes:
    i = i.replace(".html", "")
    outpath_f = os.path.join(outpath, i + ".html")
    f = open(outpath_f,"w", encoding='utf-8')
    i_request = "https://www.orthodb.org/?query={0}&level=7214&species=7214".format(i)
    
    try:
        driver.get(i_request)
        outpath_f = os.path.join(outpath, i + ".html")
        xpath_cmd = '//*[@id="group0"]/div[6]/div[2]/ul/li[1]/span/span[2]/span[1]/span'
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath_cmd)))
        html = driver.page_source
        f.write(html)
        f.close()
        print("OK!", i_request)

    except Exception as res:
        #print("fail", i_request, res)
        res_xpath = '//*[@id="summary"]/div[1]'
        res = driver.find_element("xpath", res_xpath).text
        print("fail,", res + ",", i_request)
