import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import json
import time

def get_homo(driver, groupIndex):
    # --展开第一个group--#
    species2homo = {}
    g1_xpath = '//*[@id="group{0}"]/div[6]/div[2]/ul/li[1]/div/ul'.format(groupIndex)
    
    #{ 加上一个关于这个g1_xpath的时间等待
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, g1_xpath)))
    #}
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
    return species2homo
    
    
def get_homo_5(driver, groupIndex):
    species2homo = {}
    # -- 找不到g1_xpath时使用异常处理 -- #
    try:
        g1_xpath = '//*[@id="group{0}"]/div[5]/div[2]/ul/li[1]/div/ul'.format(groupIndex)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, g1_xpath)))
        g1_content = driver.find_element("xpath",g1_xpath).text
    except Exception:
        g1_xpath = '//*[@id="group{0}"]/div[6]/div[2]/ul/li[1]/div/ul'.format(groupIndex)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, g1_xpath)))
        g1_content = driver.find_element("xpath",g1_xpath).text
    # -- 找不到g1_xpath时使用异常处理 -- #
 
    g1_content = g1_content.split("\n")
    g1_content_len = 0
    for item in g1_content:
        if "Drosophila" in item:
            g1_content_len = g1_content_len + 1
    for item in range(1, g1_content_len+1):
        g1_js = 'document.querySelector("#group{0} > div:nth-child(5) > div.orthologs > ul > li:nth-child(1) > div > ul > li:nth-child({1}) > span > span.fancytree-expander").click()'.format(groupIndex,item)
        driver.execute_script(g1_js)
    g1_gene_xpath = '//*[@id="group{0}"]/div[5]/div[2]/ul/li[1]/div/ul'.format(groupIndex)
    raw_gene = g1_content = driver.find_element("xpath",g1_gene_xpath).text
    raw_gene = raw_gene.split("Drosophila ")[1:]
    for item in raw_gene:
        item_list = item.split("\n")
        species = "Drosophila " + item_list[0].split(", ")[0]
        homogenes = item_list[1:]
        species2homo[species] = homogenes
    return species2homo


age_f = r"D:\GageTracker\result\GageTracker_r1_0.5.age.protein_coding"
outpath = r'D:\GageTracker\data\orthoDB_2'
fails = open("no_found", "w")

age_data = pd.read_csv(age_f, sep="\t")
genes = list(age_data["Gene"])
option = webdriver.ChromeOptions()
option.add_argument('headless')
driver = webdriver.Chrome(chrome_options=option)

# -- 不包括的--
tmp_genes = os.listdir(r'D:\GageTracker\data\orthoDB_2')
remainings = set(genes).difference(set(tmp_genes))
genes = list(remainings)
print(len(genes))
# -- 不包括的 -- 

for i in genes:
    i = i.replace(".html", "")
    i_request = "https://www.orthodb.org/?query={0}&level=7214&species=7214".format(i)
    driver.get(i_request)
    print(i, i_request)
    # 计算一下找到几个同源簇
    xpath = '//*[@id="summary"]/div[1]'
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpath)))
    group_num = driver.find_element("xpath", xpath).text.split()[1]
    
    if group_num == "no":
        # 没有找到结果
        res_xpath = '//*[@id="summary"]/div[1]'
        res = driver.find_element("xpath", res_xpath).text
        fails.write("not found," +  i_request + "\n")
    else:
        # 找到一个group
        group_num = int(group_num)
        if group_num == 1:
            # {-- 搜不到xpat_wait以后的等待策略 #
            try:
                xpat_wait = '//*[@id="group0"]/div[6]/div[2]/ul/li[1]/span/span[2]/span[1]'
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpat_wait)))
                species2homo = get_homo(driver, 0)
                OUT = open(os.path.join(outpath, i), "w")
                json.dump(species2homo,OUT)
                OUT.close()
            except Exception:
                xpat_wait = '//*[@id="group0"]/div[5]/div[2]/ul/li[1]/span/span[2]/span[1]'
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpat_wait)))
                species2homo = get_homo_5(driver, 0)
                OUT = open(os.path.join(outpath, i), "w")
                json.dump(species2homo,OUT)
                OUT.close()
            #}

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
            species2homo_1 = get_homo(driver, 0)
            OUT = open(os.path.join(outpath, i+"_g1"), "w")
            json.dump(species2homo_1,OUT)
            OUT.close()

            # {-- 展开第二个group --#
            try:
                xpath_wait = '//*[@id="group1"]/div[6]/div[2]/ul/li/span/span[2]/span[1]'
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpat_wait)))
                species2homo_2 = get_homo(driver, 1) #展开第二个group
                OUT = open(os.path.join(outpath, i+"_g2"), "w")
                json.dump(species2homo_2,OUT)
                OUT.close()
            except Exception:
                xpath_wait = '//*[@id="group1"]/div[5]/div[2]/ul/li/span/span[2]/span[1]'
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpat_wait)))
                species2homo_2 = get_homo_5(driver, 1) #展开第二个group
                OUT = open(os.path.join(outpath, i+"_g2"), "w")
                json.dump(species2homo_2,OUT)
                OUT.close()
            # }
                
fails.close()
