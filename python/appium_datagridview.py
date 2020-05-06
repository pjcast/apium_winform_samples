import os, sys, time
from appium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class data_grid_view:
	"""This class provides helper methods for DataGridView"""

	def __init__(self, object, verbose, wait):
		self.object = object
		self.verbose = verbose
		self.name = self.object.name
		
		if verbose:
			print("data_grid_view getting: {0}".format(self.name))

		self.ui = self.object.get_wait(wait)

		if self.ui.text != "DataGridView":
			raise Exception("Not a DataGridView!")

		if self.ui.tag_name != "ControlType.Table":
			raise Exception("Not a ControlType.Table!")

		self.auto_dump(self.ui, "Grid")

	def datarow_get(self, row_index):
		""" Returns the element at index """
		# Xpath here, but finding by name seems pretty decent
		row = self.ui.find_element_by_name("Row {0}".format(row_index))
		self.auto_dump(row, "Row:{0}".format(row_index))
		return row
		
	def datarow_get_column(self, row_index, row_column):
		"""Get Column located in Row"""
		row = self.datarow_get(row_index)
		search = "//DataItem[{0}]".format(row_column)
		col = row.find_element_by_xpath(search)
		self.auto_dump(col, "Row{0}:Col{1}".format(row_index, row_column))
		return col
		
	def datarow_click(self, row_index):
		""" Clicks the element at index """
		print("TODO implement datarow_click for {0}... ".format(self.name))
	
	def datarow_right_click(self, row_index):
		""" Right Clicks the element at index """
		print("implement datarow_right_click for {0}... ".format(self.name))
		row = self.datarow_get(row_index)
		action = ActionChains(self.object.driver)
		action.context_click(row).perform()

	def datarow_double_click(self, row_index):
		""" Double Clicks the element at index """
		row = self.datarow_get(row_index)
		action = ActionChains(self.object.driver)
		action.double_click(row).perform()
			
	def row_count(self):
		return self._getAttributeInt("Grid.RowCount", 0)
		
	def col_count(self):
		return self._getAttributeInt("Grid.ColumnCount", 0)
		
	def selected_row(self):
		# Ensure we have focus - so we can find selected row by currently active item
		self.ui.send_keys(Keys.SHIFT)
		
		cur_focus = self.object.driver.switch_to.active_element
		# Figure out what we are in - could be a cell, edit, or row depending on row select/readonly modes
		if self._isDataRow(cur_focus) == False:
			xpath = '//*[@RuntimeId="{0}"]/parent::*'.format(cur_focus.id)
			if self.verbose: print('Print Looking for parent item: {0}'.format(xpath))
			cur_focus = self.object.driver.find_element_by_xpath(xpath)
			if self._isDataRow(cur_focus) == False:
				raise ValueError("Could not find selected row")
		
		self.auto_dump(cur_focus, 'Selected Row')
		return cur_focus
		
	def visible_rows(self):
		elements = self.ui.find_elements_by_xpath("./Custom") # Want to use contains or starts-with, but does not seem to work
		elements += self.ui.find_elements_by_xpath("./DataItem")
		visible = []
		for e in elements:
			name = e.get_attribute("Name")
			if name.startswith('Row') and int(e.location['y']) >= 0: visible.append(e)
		
		return visible
	
	def _isDataRow(self, item):
		if item == None: raise ValueError("Unexpected Null Element while looking for selected")
		
		tag = item.tag_name
		if tag == "DataItem": return True
		elif tag == "ControlType.Custom" and item.get_attribute("Name").startswith("Row "): return True
		return False
		
	def _areRowsEqual(self, row1, row2):
		return row1.get_attribute("RuntimeId") == row2.get_attribute("RuntimeId")
		
	def _getRowIndexFromName(self, row):
		index = row.text[3:].strip()
		return int(index)		
		
	def _send_key_repeated(self, element, key, repeat_count):
		for i in range(repeat_count):
			element.send_keys(key)
			
	def _precise_click(self, element):
		actions = ActionChains(self.object.driver)
		actions.move_to_element(element)
		actions.click()
		actions.perform()
		#action.double_click(row).perform()
		#self.ui.move_to_element(element)
		
	def scroll_to_row(self, row_index):
		visible_rows = self.visible_rows()
		visible_rows_count = len(visible_rows)
		if visible_rows_count == 0: raise ValueError('Expected row(s) to be visible')

		start = self._getRowIndexFromName(visible_rows[0])
		if visible_rows_count > 1:
			end = self._getRowIndexFromName(visible_rows[visible_rows_count - 1])
		else:
			end = start
			
		if row_index >= start and row_index <= end:
			print('Row {0} already contained in visible area (rows {1}-{2})'.format(row_index, start, end))
		
		print('dst row {0}, start {1}, end {2} (visible range {3})'.format(row_index, start, end, len(visible_rows)))
		time.sleep(10)
		
		# Need to go up or down?
		if row_index < start:
			offset = start - row_index
			key = Keys.UP
			print('Clicking row {0}, offset {1}, up'.format(start, offset))
			time.sleep(2)
			visible_rows[0].click()
			time.sleep(5)
			#self.datarow_get(start).click()
		else:
			offset = row_index - end
			key = Keys.DOWN
			print('Clicking row {0}, offset {1}, down'.format(end, offset))
			time.sleep(1)
			self.dump(visible_rows[visible_rows_count - 2], "row-2")
			self.dump(visible_rows[visible_rows_count - 1], "row-1")
			visible_rows[visible_rows_count - 2].click()
			time.sleep(5)
			#self.datarow_get(end).click()
			
		self._send_key_repeated(self.ui, key, offset)
		
	def scroll_get_v_position(self):
		''' Returns scroll position 1 to 100 '''
		vs = self._getVScrollBar()
		#self.dump(vs, "hsb")
		#Value.Value: "31"
		return 0

	def scroll_get_h_position(self):
		''' Returns scroll position 1 to 100 '''
		return 0
		
	def _getVScrollBar(self):
		#Name: "Vertical", ScrollBar
		# TODO: Support no scroll bar! return -1?
		return self.ui.find_element_by_name("Vertical")
		
	def _getHScrollBar(self):
		#Name: "Horizontal", ScrollBar
		# TODO: Support no scroll bar! return -1?
		return self.ui.find_element_by_name("Horizontal")

	def _getAttributeInt(self, attr, default):
		val = self.ui.get_attribute(attr)
		if val == None:
			return default
		try:
			return int(val)
		except ValueError:
			return default
			
	def auto_dump(self, element, name):
		if self.verbose == None or self.verbose == False:
			return
		self.dump(element, name)
	
	def dump(self, element, name):
		print("")
		print("")
		print("-----------------------------------------------------")
		print("Object Friendly name: {0}".format(name))
		print("Text: {0}".format(element.text))
		print('RuntimeId {0}'.format(element.id))
		print("Tag: {0}".format(element.tag_name))
		self.dump_attribute(element, "Name")
		self.dump_attribute(element, "LegacyName")
		self.dump_attribute(element, "AutomationId")
		self.dump_attribute(element, "FrameworkId")
		self.dump_attribute(element, "ClassName")
		self.dump_attribute(element, "IsEnabled")
		self.dump_attribute(element, "IsKeyboardFocusable")
		self.dump_attribute(element, "IsControlElement")
		#self.dump_attribute(element, "ProcessId")
		self.dump_attribute(element, "RuntimeId")
		self.dump_attribute(element, "ClickablePoint")
		self.dump_attribute(element, "SelectionItem.IsSelected")
		self.dump_attribute(element, "IsSelectionItemPatternAvailable")
		self.dump_attribute(element, "IsSelectionPatternAvailable")
		self.dump_attribute(element, "LastChild")
		self.dump_attribute(element, "Children")
		self.dump_attribute(element, "NativeWindowHandle")
		#self.dump_attribute(element, "ProviderDescription")
		self.dump_attribute(element, "HasKeyboardFocus")
		
		self.dump_attribute(element, "Grid.ColumnCount")    # Property of Grid
		self.dump_attribute(element, "Grid.RowCount")       # Property of Grid
		self.dump_attribute(element, "Selection.Selection") # Property of Grid
		self.dump_attribute(element, "Value.Value")      # Property of ScrollBar
	
		print('Appium Exposed Properties:')
		print("Enabled: {0}".format(element.is_enabled()))
		print("Displayed: {0}".format(element.is_displayed()))
		print("Location: {0}".format(element.location))
		print("Size: {0}".format(element.size))
		print("Rect: {0}".format(element.rect))
		print("Location in view: {0}".format(element.location_in_view))
		print("-----------------------------------------------------")
		sys.stdout.flush()

	def dump_attribute(self, element, attribute):
		print("Attribute: '{0}': '{1}'".format(attribute, element.get_attribute(attribute)))
	