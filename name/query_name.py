# -*- codec: utf-8 -*-
import re
import time
from selenium import webdriver

# 網頁每天同IP查詢次數有限制, 需搭配定時換IP執行

word_db = [
	['','','','','一'], #1
	['人','','卜','二','又'], #2
	['千','工','子','女','山'], #3
	['心','月','文','日','允'], #4
	['仙','可','北','令','由'], #5
	['妁','朵','妃','光','安'], #6
	['秀','君','妤','巫','岑'], #7
	['金','宜','雨','妮','夜'], #8
	['星','科','香','貞','音'], #9
	['倩','家','紋','夏','恩'], #10
	['晨','梅','習','甜','婉'], #11
	['絢','雁','扉','智','嵐'], #12
	['新','睛','微','暖','愛'], #13
	['嫦','輕','蜜','綾','嫣'], #14
	['趣','嬌','緲','蝶','影'], #15
	['靜','橙','霏','糖','嬡'], #16
	['鍾','簇','霜','瞳','優'], #17
	['雙','顏','馥','繚','璧'], #18
	['鏡','簽','靡','麗','韻'], #19
	['馨','繼','繽','朧','罌'], #20
]

def query(stroke1, stroke2, elmnt1, elmnt2):
	global driver
	global word_db
	driver.get('http://www.dearmoney.idv.tw/name')
	driver.find_element_by_id('first_name').send_keys('周')
	driver.find_element_by_id('last_name').send_keys(word_db[stroke1][elmnt1] + word_db[stroke2][elmnt2])
	driver.find_elements_by_css_selector("input[type='radio'][value='F']")[0].click()
	e = driver.find_element_by_id('_Year')
	e.send_keys('西西西西西西西西西西西西西西西西西西西西西西西西西西西西西西西西西西西')
	e = driver.find_element_by_id('_Month')
	e.send_keys("5")
	e = driver.find_element_by_id('_Day')
	e.send_keys("23")
	e = driver.find_element_by_id('_Hour')
	e.send_keys("111")
	driver.find_element_by_id('btnok').click()
	time.sleep(1)
	result = ''
	s = re.search('1982年5月23日11時', driver.page_source)
	result = s.group(0) + '\t'
	s = re.search('維基百科.+<b>(.+)</b>.+<b>(.+)</b>.+[康熙筆劃].+<b>(.+)</b>.+<b>(.+)</b>.+[康熙筆劃].+20px; ">(.+)</span>.+此造命名五行', driver.page_source)
	result += str(stroke1+1) + '\t' + str(stroke2+1) + '\t' + s.group(2) + '\t' + s.group(4) + '\t' + s.group(1) + '\t' + s.group(3) + '\t' + s.group(5)

	s = re.search('主運.+前運', driver.page_source)
	p = re.search('主運.+center">(\d+)<p>【(.)】.+【<.+>(.+)</font>】.+前運', s.group(0))
	result += ('\t' + p.group(1) + '\t' + p.group(2) + '\t' + p.group(3))
	s = re.search('前運.+副運', driver.page_source)
	p = re.search('前運.+center">(\d+)<p>【(.)】.+【<.+>(.+)</font>】.+副運', s.group(0))
	result += ('\t' + p.group(1) + '\t' + p.group(2) + '\t' + p.group(3))
	s = re.search('副運.+後運', driver.page_source)
	p = re.search('副運.+center">(\d+)<p>【(.)】.+【<.+>(.+)</font>】.+後運', s.group(0))
	result += ('\t' + p.group(1) + '\t' + p.group(2) + '\t' + p.group(3))
	s = re.search('後運.+三才配置', driver.page_source)
	p = re.search('後運.+center">(\d+)<p>【(.)】.+【<.+>(.+)</font>】.+三才配置', s.group(0))
	result += ('\t' + p.group(1) + '\t' + p.group(2) + '\t' + p.group(3))

	s = re.search('相生相剋.+三才五行順生/逆生', driver.page_source)
	p = re.search('相生相剋.+【.+>(.+)</font>】.+三才五行順生/逆生', s.group(0))
	result += ('\t' + p.group(1))

	s = re.search('人格/地格.+【.+>(.+)</font>】.+人格/天格.+【.+>(.+)</font>】.+人格/外格.+【.+>(.+)</font>】.+namesec3', driver.page_source)
	result += ('\t' + s.group(1) + '\t' + s.group(2) + '\t' + s.group(3))

	s = re.search('取字說明.+【.+>(.+)</font>】.+【.+>(.+)</font>】.+namesec4', driver.page_source)
	result += ('\t' + s.group(1) + '\t' + s.group(2))
	print(result)

driver = webdriver.Safari()
driver.get('http://www.google.com')
driver.maximize_window()
print('生日\t筆畫(第一字)\t筆畫(第二字)\t五行(第一字)\t五行(第二字)\t第一字\t第二字\t八字姓名學\t人格筆畫\t人格五行\t人格\t地格筆畫\t地格五行\t地格\t外格筆畫\t外格五行\t外格\t總格筆畫\t總格五行\t總格\t三才配置\t人格/地格\t人格/天格\t人格/外格\t生肖取字(第一字)\t生肖取字(第二字)')
for a in range(0,20):
	for c in range(0,5):
		for b in range(0,20):
			for d in range(0,5):
				if (word_db[a][c] != '' and word_db[b][d] != ''):
					success = 0
					while (success == 0):
						try:
							query(a, b, c, d)
							success = 1
						except KeyboardInterrupt:
							raise
						except:
							continue
time.sleep(1)
driver.close()
