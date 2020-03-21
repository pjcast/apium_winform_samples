# This Appium sample uses the sample dotnet core winform's Basic app located in [root]\winforms\basic

import os
import sys
from appium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from appium_helpers import object_repository

def send_key_repeated(ui, key, repeat_count):
	for i in range(repeat_count):
		ui.send_keys(key)

def tab_through_controls(tab_count):
	for i in range(tab_count):
		# Since we are tabbing, active element will likely be changing
		element = driver.switch_to.active_element
		element.send_keys(Keys.TAB)
		
	return driver.switch_to.active_element
	
def get_automation_id(element):
	return element.get_attribute("AutomationId")
		
def load_appium() -> webdriver.Remote:
	path = os.path.join(os.getcwd(), "..\\winforms\\basic\\Basic\\bin\\Debug\\netcoreapp3.1\\Basic.exe")
	desired_caps = {}
	desired_caps["app"] = path
	desired_caps["ms:experimental-webdriver"] = True
		
	driver = webdriver.Remote(command_executor='http://127.0.0.1:4723', desired_capabilities=desired_caps)
	return driver

driver = load_appium()

# Find all json files, and dynamically build a list of object repositories - useful in a large program to group objects by window/tabs/locations
# this object is dynamic, and has attributes that get added based on what is in the JSON
# The returned objects provide an appium wrapper to reduce duplicate code with lookups/gets/waits
o = object_repository(".\\", driver)

# Give a little time for UI to be available. This method actually returns the webelement instance - or, raises an error if it cannot
cb = o.basic.checkbox.get_wait(20)
selected = cb.get_attribute("Toggle.ToggleState")
print('Checkstate = {0}'.format(selected))

# Toggle Checkbox's state
cb.click()
selected = cb.get_attribute("Toggle.ToggleState")
print('Checkstate = {0}'.format(selected))

# We expect to now be on textbox1 after a tab - send tab, and get the element selected
element = tab_through_controls(1)
if get_automation_id(element) != "textBox1":
	raise Exception("Incorrect element != textBox1")

send_key_repeated(element, "abc", 3)

# Tab back around, expect to be back on button
element = tab_through_controls(4)
if get_automation_id(element) != "button1":
	raise Exception("Incorrect element != button1")
element.click()

# Example accessing nested objects... sometimes, you do not have an AutomationId/Name'ed winforms object. And xpath is your only recourse,
# and if your UI is complicated, WinAppDriver's xpath lookup at the root level can take some time... best to get an Id as close as possible in your UI graph,
# and then go down the xpath route. In this example, panel is parent of this textbox
tb2 = o.basic.panel.textbox2.get()
tb2.send_keys("This is textbox2")

# Simple interaction with combobox and keyboard
o.basic.panel.combobox.get().send_keys(Keys.DOWN)

# Shutdown connection and close test app
driver.quit()
