#!/usr/bin/env python

from selenium import webdriver
import time, sys, os
from selenium.webdriver.chrome.options import Options  


time.sleep(2)
chrome_options = Options()  
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
PASSWORD = os.environ.get('PASSWORD', '6fjvyW7pLjU2&062@N0d@M%T*')
DOMAIN = 'http://' + '128.199.157.172:21721' + '/'
while(1):
	try:
		browser = webdriver.Chrome(options=chrome_options)
		browser.get(DOMAIN + 'login')
		time.sleep(3);
		username = browser.find_element_by_id("inputUsername")
		password = browser.find_element_by_id("inputPassword")
		username.send_keys("abcdef")
		password.send_keys(PASSWORD)
		browser.find_element_by_tag_name("button").click()
		time.sleep(3);
		print(browser.current_url)

		browser.quit()
	except Exception as e:
		print(e)
