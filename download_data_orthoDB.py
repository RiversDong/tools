import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import json

def get_homo(driver, groupIndex):
    # --展开第一个group--#
    species2homo = {}
    g1_xpath = '//*[@id="group{0}"]/div[6]/div[2]/ul/li[1]/div/ul'.format(groupIndex)
    g1_content = driver.find_element("xpath",g1_xpath).text
    g1_content = g1_content.split("\n")
    g1_content_len = 0
    for item in g1_content:
        if "Drosophila" in item:
            g1_content_len = g1_content_len + 1
    for item in range(1, g1_content_len+1):
        g1_js = 'document.querySelector("#group{0} > div:nth-child(6) > div.orthologs > ul > li:nth-child(1) > div > ul > li:nth-child({1}) > span > span.fancytree-expander").click()'.format(groupIndex,item)
        driver.execute_script(g1_js)
    g1_gene_xpath = '//*[@id="group{0}"]/div[6]/div[2]/ul/li[1]/div/ul'.format(groupIndex)
    raw_gene = g1_content = driver.find_element("xpath",g1_gene_xpath).text
    raw_gene = raw_gene.split("Drosophila ")[1:]
    for item in raw_gene:
        item_list = item.split("\n")
        species = "Drosophila " + item_list[0].split(", ")[0]
        homogenes = item_list[1:]
        species2homo[species] = homogenes
    #print(species2homo)
    return species2homo
    # --展开第一个group--#

age_f = r"D:\GageTracker\result\GageTracker_r1_0.5.age.protein_coding"
outpath = r'D:\GageTracker\data\orthoDB_2'

age_data = pd.read_csv(age_f, sep="\t")
genes = list(age_data["Gene"])
option = webdriver.ChromeOptions()
option.add_argument('headless')
driver = webdriver.Chrome(chrome_options=option)
#genes = ["FBgn0002781", "FBgn0000055", "FBgn0031441"]
for i in genes:
    i = i.replace(".html", "")
    outpath_f = os.path.join(outpath, i + ".html")
    #outf = open(outpath_f,"w", encoding='utf-8')
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
            xpat_wait = '//*[@id="group0"]/div[6]/div[2]/ul/li[1]/span/span[2]/span[1]'
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpat_wait)))
            species2homo = get_homo(driver, 0)
            OUT = open(os.path.join(outpath, i), "w")
            json.dump(species2homo,OUT)
            OUT.close()

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
            species2homo_1 = get_homo(driver, 0) #展开第一个group
            
            OUT = open(os.path.join(outpath, i+"_g1"), "w")
            json.dump(species2homo_1,OUT)
            OUT.close()
            
            species2homo_2 = get_homo(driver, 1) #展开第二个group
            OUT = open(os.path.join(outpath, i+"_g2"), "w")
            json.dump(species2homo_2,OUT)
            OUT.close()
