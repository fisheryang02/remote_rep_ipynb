import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
def main(filepath,id,total,pagenum):
    if (not os.path.exists(filepath)):  # 若不存在，则创建文件夹好保存每种鸟类的文件
        os.makedirs(filepath)
    os.chdir(filepath)  # 切换至文件夹
    chrom_opt = webdriver.ChromeOptions()
    # prefs = { "profile.managed_default_content_settings.images": 2 }       #不加载图片提高速度
    # chrom_opt.add_experimental_option("prefs", prefs)
    # chrom_opt.add_argument('--blink-settings=imagesEnabled=false')#禁用图像加载
    chrom_opt.add_argument("headless")#不显示浏览器页面
    chrom_opt.add_argument('--no-sandbox')#取消沙盒不然会报错，不允许进入
    # chrom_opt.add_argument('--disable-gpu')
    # chrom_opt.add_argument('--disable-dev-shm-usage')
    path = Service('chromedriver.exe')
    driver = webdriver.Chrome(service=path, options=chrom_opt)
    driver.implicitly_wait(10)#设置隐式等待
    driver.maximize_window()

    url = f'http://www.birdreport.cn/home/member/chart.html?taxon_id={id}&taxon_id={id}'
    driver.get(url)
    time.sleep(2)
    '''
    for i in range(12):
        if i<=pagenum-1:
            driver.find_element(By.CLASS_NAME,"layui-laypage-next").click()
            time.sleep(1)
            continue
        time.sleep(10)
        #driver.refresh()
        picture=driver.find_elements(By.XPATH,"//img[contains(@src,'https://bird-buckets.oss-cn-hangzhou.aliyuncs.com')]")
        time.sleep(5)
        for j in range(len(picture)):
            img=picture[j].get_attribute("src")
            img=requests.get(img)#得到对应的访问图片网址
            total += 1
            f = open(filepath+"/%s_%s.jpg" % (id,total), 'wb')  # 以二进制格式写入img文件夹中
            f.write(img.content)
            f.close()
            print("第%s张图片下载完毕" % total)
            time.sleep(5)
        driver.find_element(By.CLASS_NAME,"layui-laypage-next").click()
        #driver.refresh()
    '''
    for i in range(13):
        if i<=pagenum-1:
            driver.find_element(By.CLASS_NAME,"layui-laypage-next").click()
            time.sleep(1)
            continue
        time.sleep(2)
        picture=driver.find_elements(By.XPATH,"//img[contains(@src,'https://bird-buckets.oss-cn-hangzhou.aliyuncs.com')]")
        for j in range(len(picture)):
            picture[j].click()
            driver.switch_to.window(driver.window_handles[-1])
            img=driver.find_element(By.XPATH,"//img[contains(@src,'https://bird-buckets.oss-cn-hangzhou.aliyuncs.com')]").get_attribute("src")
            img=requests.get(img)#得到对应的访问图片网址
            total += 1
            f = open(filepath+"/%s_%s.jpg" % (id,total), 'wb')  # 以二进制格式写入img文件夹中
            f.write(img.content)
            f.close()
            print("第%s张图片下载完毕" % total)
            time.sleep(2)
            # 关闭当前标签页
            driver.close()
            # 切换回原来的标签页
            driver.switch_to.window(driver.window_handles[0])
    # 选择文件
        driver.find_element(By.CLASS_NAME, "layui-laypage-next").click()
    driver.quit()
#

if __name__ == "__main__":
    #for id in [920,141,844,713,1427,1088,986,1000,98,1417,821,82,763,615,1344,596,795,1325,846,1204,674,248,391,726,710,350,768,731,355]:
    for id in[615]:
    #for id in [183,738,655,286,689,1200]:
        #filepath=r'D:\pythoncode\crawler\second'+f"/{id}"#每种鸟类建立一个文件夹储存图片
        filepath=r'D:\pythoncode\crawler\short'+f"/{id}"#每种鸟类建立一个文件夹储存图片
        pagenum=0#已经爬取的页数
        total=0#已经爬取的图片数目
        main(filepath,id,total,pagenum)
