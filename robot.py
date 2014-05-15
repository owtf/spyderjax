# Build browser to be used in the main module
#

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

######******* BUILD your browser here************
# Comment out the webdriver which will not be used
profile = webdriver.FirefoxProfile()
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.http", "127.0.0.1")
profile.set_preference("network.proxy.http_port", "8008")
profile.update_preferences()

driver = webdriver.Firefox(firefox_profile=profile)
#driver = webdriver.Chromedriver

#*************************************************

class Robot():
	"""
	A robot which clicks the clickable elements in DOM, and captures page snapshots for each
	state change until there are no more available.
	"""

	def initialize():
