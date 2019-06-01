from selenium import webdriver
from os import sys

# Settings (Don't touch unless you know what you do!).
chromedriver = "./chromedriver.exe"
game_url = "https://orteil.dashnet.org/cookieclicker/"

cookie_xpath = "//*[@id='bigCookie']"
upgrades_xpath = "//*[@class='crate upgrade enabled']"
buildings_xpath = "//*[@class='product unlocked enabled']"
close_advancements_xpath = "//*[@class='close']"

# Interprete args.
if '--show-advancements' in sys.argv:
	close_advancements_xpath = ''

# Initialize chrome and load game from url.
driver = webdriver.Chrome(chromedriver)
driver.get(game_url)

# Get cookie object.
cookie = driver.find_element_by_xpath(cookie_xpath)

# Infinitely click and buy more stuff.
running = True
while running:
	try:
		# Click cookie.
		cookie.click()
		# Find buyable upgrades and buy them.
		upgrades = driver.find_elements_by_xpath(upgrades_xpath)
		for upgrade in upgrades:
			upgrade.click()
		
		# Same for buildings.
		buildings = driver.find_elements_by_xpath(buildings_xpath)
		for building in buildings:
			building.click()
		
		# Close advancement messages.
		closes = driver.find_elements_by_xpath(close_advancements_xpath)
		for close in closes:
			close.click()
	except:
		pass

# Close website.
driver.close()