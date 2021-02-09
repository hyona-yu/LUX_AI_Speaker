from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
import urllib.parse
from urllib.request import Request, urlopen
from time import sleep
import pandas as pd
import time
from hanspell import spell_checker
import re
driver = webdriver.Chrome('chromedriver.exe')
driver.get('http://www.instargram.com')
time.sleep(3)

# 인스타그램 접속하기
######## 인스타 계정 로그인이 필요합니다 #########

email = 'rgtmxm'
input_id = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[0]
input_id.clear()
input_id.send_keys(email)

password = 'hg10311031'
input_pw = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[1]
input_pw.clear()
input_pw.send_keys(password)
input_pw.submit()
time.sleep(3)





def go_crowl(search, eng_sub):
    search = urllib.parse.quote(search)
    url = 'https://www.instagram.com/explore/tags/'+ str(search)

    pause_time = 1.2
    driver.get(url)
    sleep(3)

    reallink = []
    while True:
        page_str = driver.page_source
        bs = BeautifulSoup(page_str, 'lxml')

        for link in bs.find_all(name = 'div', attrs={'class':'Nnq7C weEfm'}):
            real = link.select('a')[0].attrs['href']
            if real not in reallink:
                reallink.append(real)

        last_height = driver.execute_script('return document.body.scrollHeight')
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(pause_time)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(pause_time)
            new_height =driver.execute_script('return document.body.scrollHeight')
            if new_height == last_height:
                break
            else:
                last_height = new_height
                continue
        if len(reallink) >=250:
            break

    reallink_len = len(reallink)
    print(reallink_len , ' datas')
    data = []
    try:
        for rlink in reallink:
            req = 'https://www.instagram.com/p' + rlink
            driver.get(req)
            webpage = driver.page_source
            soup = BeautifulSoup(webpage, 'html.parser')
            try:
                content = soup.select('div.C4VMK > span')[0].text
                content = re.compile('[^가-힣]+').sub("",content)
                content = spell_checker.check(content)
                content = content.checked

            except:
                content =''
            data.append(content)
            if len(data) %10 ==0:
                result = {}
                result['id'] = list(range(0, len(data)))
                result['senten'] = data
                pd.DataFrame(result).to_csv(eng_sub + '.csv')
    except:
        print('error!')

#go_crowl('행복해💕', 'insta_happy5') #행복해💕, 기분좋은날😊, 최우수상
#go_crowl('화가난다😡', 'insta_anger3')#화가난다😡
go_crowl('아프다😭', 'insta_sadness4')#에흎, 지친다
#go_crowl('꿀꿀', 'insta_meh')
