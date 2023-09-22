import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

def main(filepath,total,keyword):
    chrom_opt = webdriver.ChromeOptions()
    # prefs = { "profile.managed_default_content_settings.images": 2 }       #不加载图片提高速度
    # chrom_opt.add_experimental_option("prefs", prefs)
    # chrom_opt.add_argument('--blink-settings=imagesEnabled=false')#禁用图像加载
    # chrom_opt.add_argument("headless")#不显示浏览器页面
    chrom_opt.add_argument('--no-sandbox')#取消沙盒不然会报错，不允许进入
    # chrom_opt.add_argument('--disable-gpu')
    # chrom_opt.add_argument('--disable-dev-shm-usage')
    path = Service('chromedriver.exe')
    driver = webdriver.Chrome(service=path,options=chrom_opt)
    driver.implicitly_wait(10)#设置隐式等待
    driver.maximize_window()

    url = f'https://media.ebird.org/catalog?sort=rating_rank_desc&mediaType=photo'
    driver.get(url)
    driver.find_element(By.XPATH, "//input[contains(@type,'text')]").send_keys(keyword)
    driver.find_element(By.XPATH, "//span[contains(@class,'Suggestion-text')]").click()
    time.sleep(10)

    sum=0
    order = 261
    while True:
        imglist = driver.find_elements(By.XPATH, "//a[contains(@class,'ResultsGallery-link')]")
        for i in range(len(imglist)):
            if i<sum:
                continue

            driver.execute_script("window.open('{}', '_blank');".format(imglist[i].get_attribute('href')))
            # 切换到新标签页
            driver.switch_to.window(driver.window_handles[-1])
            # 切换到新标签页
            img=driver.find_element(By.XPATH,"//img[contains(@src,'https://cdn.download.ams.birds.cornell.edu/')]").get_attribute("src")

            img=requests.get(img)#得到对应的访问图片网址
            total += 1

            dic={"Picus canus":615,"Dendrocopos canicapillus":596,"Cecropis daurica":795,"Phylloscopus inornatus":846,"Dicrurus macrocercus":674,"Buteo japonicus":248,"Corvus corone":710,"Tringa ochropus":350}
            f = open(f"{filepath}/{dic[keyword]}_{keyword}_{order}.jpg", 'wb')  # 以二进制格式写入img文件夹中
            f.write(img.content)
            f.close()
            print("第%s张图片下载完毕,%s" % (total,f"{filepath}/{dic[keyword]}_{keyword}_{order}.jpg"))
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            order+=1
            if total==210:
                driver.quit()
                return
        driver.find_element(By.XPATH,"//button[@class='Button u-margin-none']").click()
        length = len(imglist)
        sum=length
        time.sleep(10)

if __name__ == "__main__":
    totals=[135,128,186,114,184]
    keywords=["Phylloscopus inornatus","Dicrurus macrocercus","Buteo japonicus","Corvus corone","Tringa ochropus"]
    filepaths=[r"D:\pythoncode\crawler\second\846_Phylloscopus inornatus",r"D:\pythoncode\crawler\second\674_Dicrurus macrocercus",r"D:\pythoncode\crawler\second\248_Buteo japonicus",r"D:\pythoncode\crawler\second\710_Corvus corone",r"D:\pythoncode\crawler\second\350_Tringa ochropus"]
    for filepath,total,keyword in zip(filepaths,totals,keywords):
        main(filepath,total,keyword)
