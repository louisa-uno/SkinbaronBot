from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
import os
import time
import pathlib
import pyautogui
import shutil

def start_driver():
	options = webdriver.ChromeOptions()
	# options.add_argument("--start-maximized")
	opera_profile = r"C:\Users\l2o0u\AppData\Roaming\Opera Software\Opera Stable"
	options.add_argument('user-data-dir=' + opera_profile)
	options._binary_location = r'C:\Users\l2o0u\AppData\Local\Programs\Opera\73.0.3856.344\\opera.exe'
	driver = webdriver.Opera(executable_path=r'operadriver.exe',options=options)
	return driver

def check_exists_by_xpath(xpath, driver):
	try:
		driver.find_element_by_xpath(xpath)
	except NoSuchElementException:
		return False
	return True

def check_exists_by_xpath(xpath):
	try:
		driver.find_element_by_xpath(xpath)
	except NoSuchElementException:
		return False
	return True

def click_if_exists_by_xpath(xpath):
	if check_exists_by_xpath(xpath) == True:
		driver.find_element_by_xpath(xpath).click()

# Accepts Cookies
def accept_cookies():
	click_if_exists_by_xpath('/html/body/div[2]/div[3]/div/div/div[2]/div/button[2]')

# Close the welcome popup
def close_welcome_popup():
	click_if_exists_by_xpath('/html/body/modal-container/div/div/sb-landing-page-modal/div[1]/button')

# Logging in with the loaded Steam Cookies
def login():
	# Clicking on the Steam Redirect
	driver.find_element_by_xpath('/html/body/sb-root/div/sb-layout-header/sb-layout-header-default/div/header/nav/ul/li[1]/div').click()
	time.sleep(1)
	# Clicking on the Sign In button in Steam and redirecting to Skinbaron
	driver.find_element_by_xpath('//*[@id="imageLogin"]').click()
	time.sleep(1)

def get_price(price):
	price = price.text
	price = price.split('\n')
	price.reverse()
	price = price[0]
	price = price.replace(' €','')
	price = float(price)
	return price

def get_stock(item):
	stock = item.find_element_by_xpath('.//div[2]/div[4]/div[3]/p').text
	stock = stock[:-10]
	stock = int(stock)
	return stock


# Getting all items
def get_items():
	return_items = []
	# This while loop is going through all pages of items
	x = 4
	while True:
		items = driver.find_elements_by_xpath('//*/sb-stackable-offer/div')
		
		for item in items:
			return_item = []
			return_item.append(item.find_element_by_xpath('.//div[2]/div[2]/div[1]').text)

			return_item.append(get_stock(item))

			prices = item.find_elements_by_xpath('.//div[2]/div[4]/div/div')
			return_item.append(get_price(prices[0]))

			prices.reverse()
			return_item.append(get_price(prices[0]))


			return_items.append(return_item)


		if check_exists_by_xpath(f'//*[@id="offer-container"]/div/sb-one-sided-pagination/ul/li[{x}]/button') == True:
			try:
				driver.find_element_by_xpath(f'//*[@id="offer-container"]/div/sb-one-sided-pagination/ul/li[{x}]/button').click()
			except StaleElementReferenceException:
				break
			except ElementClickInterceptedException:
				break
			time.sleep(1)
		else:
			break
		if x != 11:
			x += 1

	return return_items


# Starting the chromedriver
driver = start_driver()

# Loads the website
driver.get("https://skinbaron.de/")
time.sleep(1)

accept_cookies()
close_welcome_popup()
# login()

driver.get('https://skinbaron.de/?appId=730&v=2829&v=2832&sort=CF&language=de&pub=1')
time.sleep(3)

items = get_items()

# for item in items:
# 	name = item[0]
# 	stock = item[1]
# 	price1 = item[2]
# 	price2 = item[3]
	
# 	factor = round(price1 / price2, 2)
# 	if factor > 3:
# 		if stock > 10:
# 			print(f'Factor: {factor} | Prices: {price1}:{price2} | Stock: {stock} | {name}')



for item in items:
	name = item[0]
	stock = item[1]
	price1 = item[2]
	price2 = item[3]
	
	factor = round(price1 / price2, 2)
	if factor > 3:
		if stock > 10:
			print(f'Factor: {factor} | Prices: {price1}:{price2} | Stock: {stock} | {name}')

driver.close()