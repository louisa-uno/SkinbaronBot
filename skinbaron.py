from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains 
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
	options._binary_location = r'C:\Users\l2o0u\AppData\Local\Programs\Opera\73.0.3856.344\opera.exe'
	driver = webdriver.Opera(executable_path=r'operadriver.exe',options=options)
	# create action chain object 
	action = ActionChains(driver) 
	return driver, action

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

def get_items():
	return_items = []
	items = driver.find_elements_by_xpath('//*/sb-stackable-offer/div')
	for item in items:
		return_item = []
		return_item.append(item.find_element_by_xpath('.//div[2]/div[2]/div[1]').text)

		return_item.append(get_stock(item))

		prices = item.find_elements_by_xpath('.//div[2]/div[4]/div/div')
		return_item.append(get_price(prices[0]))
		prices.reverse()
		return_item.append(get_price(prices[0]))

		cart_buttons = item.find_elements_by_xpath('.//div[2]/div[4]/div[2]/sb-buy-button/div/div/div/button')
		return_item.append(cart_buttons[0])
		cart_buttons.reverse()
		return_item.append(cart_buttons[0])
		if return_item[4] == return_item[5]:
			return_item[5] = None
			return_item[3] = None


		return_items.append(return_item)
	return return_items


# Getting all items
def get_all_items():
	return_items = []
	# This while loop is going through all pages of items
	x = 4
	while True:
		return_items.append(get_items())


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

def bot_stop():
	driver.close()

# Starting the chromedriver
driver, action = start_driver()

# Loads the website
driver.get("https://skinbaron.de/")
time.sleep(3)

close_welcome_popup()
accept_cookies()
login()

def clear_cart():
	driver.get('https://skinbaron.de')
	time.sleep(2)
	driver.find_element_by_xpath('//*[@id="open-cart-button"]').click()
	try:
		while True:
			rm_button = driver.find_element_by_xpath('//*[@id="cart-container"]/div/div/div/div/div/div[1]/div[1]/div[3]')
			rm_button.click()#
			time.sleep(1)
	except:
		return

def checkout_cart(excepted_total):
	driver.get('https://skinbaron.de')
	time.sleep(2)

	driver.find_element_by_xpath('//*[@id="open-cart-button"]').click()
	time.sleep(0.5)

	try:
		cart_total = driver.find_element_by_xpath('//*[@id="cart-container"]/div/div/div/div/div/div[3]/div/div[1]/div[2]').text
		cart_total = float(cart_total.replace(' €','').replace(',','.'))
		if cart_total != excepted_total:
			return

		driver.find_element_by_xpath('//*[@id="cart-container"]/div/div/div/div/div/div[3]/div/div[2]/button').click()
		time.sleep(1)
		
		# Choose guthaben as payment method
		driver.find_element_by_xpath('//*[@id="cart-container"]/div/div/div/div[1]/div[2]/ul/li[1]/div').click()
		time.sleep(1)

		# Clicking Pay Now
		driver.find_element_by_xpath('//*[@id="cart-container"]/div/div/div/div[2]/div/div[2]/div/button[2]').click()
		time.sleep(1)

		# Clicking Store in Inventory
		driver.find_element_by_xpath('/html/body/modal-container/div/div/sb-buy-cart-trade-locked-modal/div[3]/div/button').click()
		time.sleep(5)
	except:
		return






simple_searches = [
	['https://skinbaron.de/?appId=730&v=2829&v=2832&sort=CF&language=de', 0.06],
	['https://skinbaron.de/?appId=730&v=2829&v=3076&sort=BP&language=de', 1.00],
	['https://skinbaron.de/?appId=730&v=2829&v=2904&sort=CF&language=de', 2.50],
	['https://skinbaron.de/?appId=730&v=2829&v=2833&sort=CF&language=de', 1.50]
]
# [[link, max_price]]

def main():
	total = 0
	clear_cart()
	for search in simple_searches:
		link = search[0]
		max_price = search[1]
		if max_price != None:
			link = link + '&pub=' + f'{max_price}'
		

		driver.get(link)
		time.sleep(3)

		items = get_items()
		print(items)

		for item in items:
			name = item[0]
			stock = item[1]
			price1 = item[2]
			price2 = item[3]
			cart_button1 = item[4]
			cart_button2 = item[5]

			if price1 <= max_price:
				print('Added ',name,' to cart')
				action.move_to_element(cart_button1).perform()
				time.sleep(0.2)
				cart_button1.click()
				total += price1
			if (price2 != None and price2 <= max_price):
				print('Added ',name,' to cart')
				action.move_to_element(cart_button2).perform()
				time.sleep(0.2)
				cart_button2.click()
				total += price2
	
	if total != 0:
		checkout_cart(total)

while True:
	main()
# bot_stop()