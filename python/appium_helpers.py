import json
import os, glob
from appium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from appium.webdriver.common.mobileby import By

class object_loader:
	def __init__(self, jsonConfig, driver):
		self.jsonConfig = jsonConfig
		self.parent = None
		self.dict = {}
		self.cached_items = {}
		self.driver = driver
		
		# The JSON format we use is essentially a dictionary of UI elements, containing sub dictionaries (children) UI elements
		with open(jsonConfig) as json_file:
			data = json.load(json_file)
			self.dict = data
			
	def __getattr__(self, name):
		# Have we already created the accessor object for this name? if so, save time and memory and return same instance
		if name in self.cached_items:
			return self.cached_items[name]
		
		if name in self.dict:
			item = self.dict[name]
			cached_item = objec_instance(self, name, item, self.driver)
			self.cached_items[name] = cached_item
			return cached_item
			
		raise AttributeError(name + ' not found - validate Object Store Definition')
		
	def dump_page(self):
		xml = self.driver.page_source
		with open("window_dump.xml", "w") as dump:
			dump.write(xml)

class object_repository:
	""" 
		Finds all json files in given path and creates an object_loader for each one found. 
		sample usage (with a myapp.json file in current dir):
			o = object_repository(".\\")
			o.myapp.<someelelement>.get()
	"""
	def __init__(self, objectRepositoryLocation, driver):
		self.dict = {}

		search = os.path.join(objectRepositoryLocation, "*.json")
		for file in glob.glob(search):
			name = os.path.basename(file)
			name = os.path.splitext(name)[0].lower()
			self.dict[name] = object_loader(file, driver)

	def __getattr__(self, name) -> object_loader:
		lookupName = name.lower()
		if lookupName in self.dict:
			return self.dict[lookupName]

		raise AttributeError(name + ' not found - validate Object Store Definition')

class objec_instance:
	def __init__(self, parent, name, dict, driver):
		self.parent = parent
		self.name = name
		self.dict = dict
		self.cached_items = {}
		self.driver = driver
		  
	def __getattr__(self, name):
		# Have we already created the accessor object for this name? if so, save time and memory and return same instance
		if name in self.cached_items:
			return self.cached_items[name]
			
		if "children" in self.dict:
			children = self.dict["children"]
			if name in children:
				cached_item = objec_instance(self, name, children[name], self.driver)
				self.cached_items[name] = cached_item
				return cached_item

		raise AttributeError(name + ' not found - validate Object Store Definition')
		
	def _getCallChain(self):
		chain = [self.parent, self]
		
		# Build an ordered temporary call chain starting from root O(N)
		# Could cache this, but would likely than lead to definite memory leaks - would then need weakref's
		p = self.parent.parent
		while p != None:
			chain.insert(0, p)
			p = p.parent
			
		# Selector...
		selector_chain = []
		for i in chain:
			if i.dict == None: continue
			self._appendCallChainSelector(i.dict, selector_chain)

		return selector_chain

	def _appendCallChainSelector(self, dict, selector_chain):	
		# Type of selector: id (accessible), xpath, select (multiple calls)
		if 'id' in dict:
			selector_chain.append(selector_accessibility(dict['id']))
		elif 'xpath' in dict:
			selector_chain.append(selector_xpath(dict['xpath']))
		elif 'name' in dict:
			selector_chain.append(selector_name(dict['name']))
		elif 'select' in dict:
			select = dict['select']
			for i in select:
				# Nested select is just sub dictionaries in a certain order
				self._appendCallChainSelector(i, selector_chain)

	def get(self) -> webdriver.WebElement:
		"""Get web driver callable object: no wait - throws error if not"""
		
		chain = self._getCallChain()
		root = self.driver
		for c in chain:
			root = c.get(root)

		# Root should not be driver
		if root == self.driver:
			raise Exception("Couldn't find UI element '{0}'".format(self.name))

		return root

	def get_wait(self, seconds) -> webdriver.WebElement:
		""" Get web driver callable object: wait max secs """
		# We need to do a wait for for each item up the chain...
		chain = self._getCallChain()
		root = self.driver
		for c in chain:
			wait = WebDriverWait(root, seconds)
			root = c.get_wait(wait)

		if root == self.driver: raise Exception("Couldn't find UI element '{0}'".format(self.name))
		return root

class selector_base:
	def __init__(self):
		"""Constructor"""
	
	def get(self, driver):
		raise NotImplementedError()

	def get_wait(self, delay):
		raise NotImplementedError()

class selector_xpath(selector_base):
	def __init__(self, xpath):
		selector_base.__init__(self)
		self.xpath = xpath

	def get(self, driver):
		#print('get_by_xpath {0}'.format(self.xpath))
		return driver.find_element_by_xpath(self.xpath)

	def get_wait(self, wait):
		#print('get_wait_by_xpath {0}'.format(self.xpath))
		return wait.until(ec.presence_of_element_located((By.XPATH, self.xpath)))

class selector_accessibility(selector_base):
	def __init__(self, id):
		selector_base.__init__(self)
		self.id = id

	def get(self, driver):
		#print('get_by_id {0}'.format(self.id))
		return driver.find_element_by_accessibility_id(self.id)

	def get_wait(self, wait):
		#print('get_wait_by_id {0}'.format(self.id))
		return wait.until(ec.visibility_of_element_located((By.ACCESSIBILITY_ID, self.id)))

class selector_name(selector_base):
	def __init__(self, name):
		selector_base.__init__(self)
		self.name = name

	def get(self, driver):
		#print('get_by_name {0}'.format(self.name))
		return driver.find_element_by_name(self.name)

	def get_wait(self, wait):
		#print('get_wait_by_name {0}'.format(self.name))
		return wait.until(ec.visibility_of_element_located((By.NAME, self.name)))


