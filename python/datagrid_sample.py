# This Appium sample uses the sample dotnet core winform's DataGrid app located in [root]\winforms\datagrid

import os
import sys
import time
from appium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from appium_helpers import object_repository
from appium_datagridview import data_grid_view
	
def load_appium() -> webdriver.Remote:
	path = os.path.join(os.getcwd(), "..\\winforms\\datagrid\\DataGrid\\bin\\Debug\\netcoreapp3.1\\DataGrid.exe")
	desired_caps = {}
	desired_caps["app"] = path
	desired_caps["ms:experimental-webdriver"] = True
		
	driver = webdriver.Remote(command_executor='http://127.0.0.1:4723', desired_capabilities=desired_caps)
	return driver
	
def assert_value(name, expected, actual):
	if expected != actual:
		msg = "Expected {0} to equal {1}. Actual: {2}".format(name, expected, actual)
		raise ValueError(msg)
		
def assert_true(name, actual):
	if actual == False:
		msg = "Expected {0} to be true, actual: {1}".format(name, actual)
		raise ValueError(msg)

driver = load_appium()

o = object_repository(".\\", driver)
print('* Finding DataGridView and wrapping with helper class...')
dg = data_grid_view(o.datagrid.grid, False, 20)

row_count = dg.row_count()
assert_value('Column Count', 3, dg.col_count())
assert_true('Row Count > 0', row_count > 0)

selected_row = dg.selected_row()
assert_value('Selected Row', 'Row 0', selected_row.text)

dg.send_key_repeated(Keys.DOWN, 2)
selected_row = dg.selected_row()
assert_value('Selected Row', 'Row 2', selected_row.text)

print("Moving to last row")
dg.move_to_row(row_count - 1)

# Shutdown connection and close test app
driver.quit()
