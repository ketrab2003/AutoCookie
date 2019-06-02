from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.command import Command
from selenium.common.exceptions import WebDriverException
import argparse

# Settings (Don't touch unless you know what you do!).
chromedriver = "./chromedriver.exe"
game_url = "https://orteil.dashnet.org/cookieclicker/"
load_wait_time = 60
default_save_file = "save.txt"

cookie_xpath = "//*[@id='bigCookie']"
upgrades_xpath = "//*[@class='crate upgrade enabled']"
buildings_xpath = "//*[@class='product unlocked enabled']"
shimmer_xpath = "//*[@class='shimmer']"
close_advancements_xpath = "//*[@class='close']"
options_xpath = "//*[@id='prefsButton']"
close_options_xpath = "//*[@class='close menuClose']"
option_button_xpath = "//*[@class='option']"
export_button_text = "Export save"
import_button_text = "Import save"
text_area_xpath = "//*[@id='textareaPrompt']"
ok_xpath = "//*[@id='promptOption0']"
active_stats_xpath = "//*[contains(@id,'statsButton') and contains(@class,'button selected')]"
active_info_xpath = "//*[contains(@id,'logButton') and contains(@class,'button selected')]"
active_settings_xpath = "//*[contains(@id,'prefsButton') and contains(@class,'button selected')]"
prompt_xpath = "//*[@id='promptContent']"

# Interprete args.
ap = argparse.ArgumentParser()
ap.add_argument("-l", "--load", required=False, help="load file with game save data", nargs='?', const=default_save_file)
ap.add_argument("-d", "--chrome-driver", required=False, help="set chrome driver location", default=chromedriver)
ap.add_argument("--show-advancements", required=False, help="use if you want advancements to not be closed", action='store_true')

args = vars(ap.parse_args())

chromedriver = args["chrome_driver"]

if args["show_advancements"]:
	close_advancements_xpath = ''


# Functions.
def click_all(xpath):
	# Click all elements found by xpath.
	buttons = driver.find_elements_by_xpath(xpath)
	for button in buttons:
		button.click()

def save_file(data):
	with open(default_save_file, 'w') as save:
		save.write(data)

# Initialize chrome and load game from url.
driver = webdriver.Chrome(chromedriver)
driver.get(game_url)
WebDriverWait(driver, load_wait_time).until(EC.presence_of_element_located((By.XPATH, options_xpath)))
WebDriverWait(driver, 1)

# Load game (if possible).
try:
	with open(args["load"]) as save:
		print('loading...')
		data = save.readline()

		driver.find_element_by_xpath(options_xpath).click()

		options = driver.find_elements_by_xpath(option_button_xpath)
		for option in options:
			if option.text == import_button_text:
				option.click()
				break

		driver.find_element_by_xpath(text_area_xpath).send_keys(data)
		driver.find_element_by_xpath(ok_xpath).click()
		driver.find_element_by_xpath(close_options_xpath).click()
		print('loaded')
except:
	pass

# Get cookie object.
cookie = driver.find_element_by_xpath(cookie_xpath)

# Infinitely click and buy more stuff.
running = True
errors = 0
while running:
	try:
		# Save if user clicked export button.
		if len(driver.find_elements_by_xpath(prompt_xpath)) > 0:
			prompt = driver.find_element_by_xpath(prompt_xpath)
			if "Export save" in prompt.text:
				save_file(driver.find_element_by_xpath(text_area_xpath).text)
				# Auto close window.
				driver.find_element_by_xpath(ok_xpath).click()
		errors = 0
		# Not click if stats is active.
		if len(driver.find_elements_by_xpath(active_stats_xpath)) > 0:
			continue
		# Not click if settings is active.
		if len(driver.find_elements_by_xpath(active_settings_xpath)) > 0:
			continue
		# Exit if info is active.
		if len(driver.find_elements_by_xpath(active_info_xpath)) > 0:
			break
		
		# Click shimmers.
		click_all(shimmer_xpath)
		# Click cookie.
		cookie.click()
		# Find buyable upgrades and buy them.
		click_all(upgrades_xpath)
		# Same for buildings.
		click_all(buildings_xpath)
		# Close advancement messages.
		click_all(close_advancements_xpath)
	except:
		errors += 1
		if errors > 500:
			break

# Close website.
driver.close()
print("Closed website.")