# This Appium sample uses the sample dotnet core winform's Basic app located in [root]\winforms\basic

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

driver = load_appium()

o = object_repository(".\\", driver)
print('* Finding DataGridView and wrapping with helper class...')
dg = data_grid_view(o.datagrid.grid, False, 20)

cols = dg.col_count()
rows = dg.row_count()
print('Grid has {0} cols and {1} rows'.format(cols, rows))

if cols != 3: raise ValueError('Expected 3 cols')
if rows <= 0: raise ValueError('Expected some rows')

last_row_index = rows - 1
#last_row = dg.datarow_get(last_row_index)
#print('got last row')
#dg.dump(last_row, "Last Row")
print(' move to row... 10 secs')
time.sleep(10)
selected_row = dg.selected_row()
dg.dump(selected_row, "Selected")
#dg.datarow_get(4).click()

#o.datagrid.dump_page()
#dg.scroll_to_row(20)
dg.scroll_to_row(last_row_index)
#dg._precise_click(dg.datarow_get(last_row_index))
#time.sleep(5)

#print('Scroll Position {0}'.format(dg.scroll_get_v_position()))

# Shutdown connection and close test app
driver.quit()
