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
option = webdriver.ChromeOptions()
option.add_argument('headless')
driver = webdriver.Chrome(chrome_options=option)
error = open("error", "w")
for i in genes:
    i_request = "https://www.orthodb.org/?query={0}&level=7214&species=7214".format(i)
    driver.get(i_request)
    try:
        # 使用try处理异常，可以下载全部的基因
        outpath_f = os.path.join(outpath, i + ".html")
        f = open(outpath_f,"w", encoding='utf-8')
        # 根据对应的xpath是否存在，设置等待浏览器加载的时间，只有这个xpath存在
        # 程序才能获取到对应的tree_count的数量，以便在循环中使用
        xpath_cmd = '//*[@id="group0"]/div[6]/div[2]/ul/li[1]/span/span[2]/span[1]/span'
        species_xpath = '//*[@id="group0"]/div[5]/div[1]/ul/li[1]'
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath_cmd)))

        # 使用xpath产看在多少个果蝇里面有直系同源，xpath的路劲可以通过chrome浏览器的开发者模式获取
        # 按下F12进入开发者模式，在想要获取的元素上右击-->检查
        # 这个时候定位到元素对应的html上
        # 然后在对应的html上右击-->复制xpath就得到了全部的xpath路径
        #time.sleep(5)
        tmp_tree_count = driver.find_element("xpath",species_xpath).text
        tree_count = int(tmp_tree_count.split()[3])
        print(i_request, tree_count)
        for j in range(1, tree_count):
            js_command = 'document.querySelector("#group0 > div:nth-child(6) > div.orthologs > ul > li:nth-child(1) > div > ul > li:nth-child({0}) > span > span.fancytree-expander").click()'.format(j)
            #print(js_command)
            driver.execute_script(js_command)
        html = driver.page_source
        f.write(html)
        f.close()
    except Exception as res:
        error.write(i + "\t" + str(res))
error.close()