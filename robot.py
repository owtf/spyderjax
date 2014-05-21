#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import sys
import time
import string
import re
from urlparse import urlparse
import getopt
from selenium.webdriver import *
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait


#***************************** BUILD your browser here************************************
# Comment out the webdriver which will not be used
'''
profile = FirefoxProfile()
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.http", "127.0.0.1")
profile.set_preference("network.proxy.http_port", "8008")
profile.update_preferences()

browser = Firefox(firefox_profile=profile)
#driver = Chromedriver(<pathtoexecutable>)

# OR could do this by defining it in a function

from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

def get_profile():
    # get the Firefox profile object
    firefoxProfile = FirefoxProfile()
    firefoxProfile.set_preference(<>)
    return firefoxProfile

driver = Firefox(firefox_profile=firefoxProfile)
'''
#******************************************************************************************

# Default take no screenshot
TakeScreenshots = False


def main():

    patterns = []                   # Holds RegExp for in-scope domains
    SitesToVisit = []               # URLs to visit
    sitesAdded = 0                  # pages has been added since last run
    numberOfSitesVisited = 0        # pages browsed

    previousNumberOfSitesVisited = numberOfSitesVisited

    #########################
    # Parse command options #
    #########################

    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvl:sb:d:", ["help","screenshots","browser","domain"])
    except getopt.error, msg:
        print(msg)
        print("for help use --help")
        sys.exit(2)

    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)

        if o in ("-b", "--browser"):
            if a == "firefox":
                browser = webdriver.Firefox() # Get local session of firefox
            elif a == "chrome":
                browser = webdriver.Chrome(executable_path="./chromedriver") # Get local session of chrome
        else:
            print("Please specify which browser you want to use")
            sys.exit(0)

        if o in ("-d", "--domain"):
            addDomainPatterns(patterns, a)
            print "Added %s to Domains in Scope" % a

        if o in ("-s", "--screenshots"):
            TakeScreenshots = True
            print "Taking screenshots"

    # process arguments
    for arg in args:
        if SitesToVisit.count(arg) < 1:
            SitesToVisit.append(arg)
            sitesAdded += 1

    ##############################
    # Go to each url in the list #
    ##############################

    for Site in SitesToVisit:
        leftToVisit = len(SitesToVisit) - numberOfSitesVisited

        print "=================================="
        print "Have %s items in the list" % len(SitesToVisit)
        print "Have visited %s sites" % numberOfSitesVisited
        print "Added %s sites since last interation" % sitesAdded
        print "Have %s sites left to visit" % leftToVisit
        print "=================================="

    #######################################
    # Print out all the pages in the list #
    #######################################
        page = 0
        for tmpSite in SitesToVisit:
            page += 1
            print "Page %d : %s" % (page, tmpSite)

        ###############
        # Go to a URL #
        ###############
        print "Surfing to  " + Site

        browser.get(Site) # Load page

        numberOfSitesVisited += 1
        sitesAdded = 0

        time.sleep(5) # Let the page load (wait 5 seconds)

        #############################
        # Get hold of all the links #
        #############################

        #links1 = browser.find_elements_by_xpath("//a[@href[contains(.,'http')]]")
        links1 = browser.find_elements_by_xpath("//a[contains(@href,'http')]")
        links2 = browser.find_elements_by_xpath("//div//a[contains(@href,'http')]")
        links = links1 + links2

        ##########################################
        # Add all the links to the list of links #
        ##########################################

        for link in links:
            try:
                if link.is_displayed() and link.is_enabled():
                # Add only links that are displayed and enabled
                    newURL = link.get_attribute("href") # Get the URL

                # Is the URL in scope?
                if urlInScope(patterns, getDomain(newURL)):
                    # Have we seen the URL before?
                    if SitesToVisit.count(newURL) < 1:
                    # Yes
                        print "Added       " + newURL
                        SitesToVisit.append(newURL)
                        sitesAdded += 1
                    else:
                        # No
                        print "Already had " + newURL

            except Exception, e:
                # Something went wrong (usually the DOM-tree is updated while we gather links)
                print "Error: %s" % e

        # Take a screenshot of the page
        takeScreenshot(browser, str(numberOfSitesVisited) + ".png")

        # No more links to visit, close and quit the browser
        browser.close()
        browser.quit()

        print "Crawl done!"


def addDomainPatterns(patterns, domain):
    """
    * Add regular expression patterns to a list of patterns
    """
    patterns.append(re.compile("^.*\." + domain + "$"))
    patterns.append(re.compile("^" + domain + "$"))


def urlInScope(patterns, url):
    """
    * Check if a given URL is in scope
    """
    for pattern in patterns:
        if pattern.match(url):
            print "In Scope:     " + url
            return True
        else:
            print "Out of Scope: " + url
            return False


def getDomain(url):
    """
    * Get the domain name from a URL
    """
    return urlparse(url)[1]


def takeScreenshot(browser, filename):
    """
    * Take a screenshot of the page
    """
    if TakeScreenshots:
        try:
            print "Taking screenshot: %s" % filename
            browser.save_screenshot(filename)
        except Exception, e:
            print "Error: %s" % e

#-----------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
