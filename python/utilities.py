import os
import sys
from appium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def send_key_repeated(ui, key, repeat_count):
	for i in range(repeat_count):
		ui.send_keys(key)
		
def load_appium() -> webdriver.Remote:
	path = "app/Test/Test/bin/Debug/netcoreapp3.1/Test.exe"
	desired_caps = {}
	desired_caps["app"] = path
	desired_caps["ms:experimental-webdriver"] = True
	#desired_caps["platformName"] = "Windows"
	#desired_caps["deviceName"] = "WindowsPC"
		
	driver = webdriver.Remote(command_executor='http://127.0.0.1:4723', desired_capabilities=desired_caps)
	return driver
