# coding: UTF-8
import os
from time import sleep
import re

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def save_img(img_url, name):
    # すでに存在していたら何もしない
    if os.path.isfile(name):
        return

    re = requests.get(img_url)
    with open(name, 'wb') as f:
        f.write(re.content)

def main():

    DOMAIN_URL = 'https://umamusume.jp'
    URL = '/character/'
    save_path = 'img/'

    # chromedriverはhttps://sites.google.com/a/chromium.org/chromedriver/downloadsでダウンロードできる
    driver_path = 'C:\chromedriver\chromedriver'

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(driver_path, options=options)

    driver.get(DOMAIN_URL + URL)
    # 読み込むために遅延
    sleep(5)
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")
    characters_li = soup.select("section.main-container li > a")
    
    # 保存用のフォルダ作成
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    for character_li in characters_li:
        character_url = DOMAIN_URL + character_li.get('href')
        print(character_url)

        driver.get(character_url)
        # 読み込むために遅延
        sleep(2.5)
        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html, "html.parser")
        imgs = soup.select("div.character-detail__image > img")

        for img in imgs:
            img_url = img.get('src')
            img_alt = img.get('alt')
            # 空白の置き換え
            img_alt = re.sub(' ', '_', img_alt)
            # タグの置き換え　(STARTING FUTURE用)
            img_alt = re.sub("""<("[^"]*"|'[^']*'|[^'">])*>""", '', img_alt)
            print({img_alt: img_url})
            save_img(img_url, save_path + img_alt + '.png')

    driver.close()

if __name__ =='__main__':
    main()