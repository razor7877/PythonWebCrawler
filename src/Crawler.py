from selenium import webdriver
from re import findall, fullmatch
from src.WebsiteDatabase import WebsiteDatabase
from src.Website import Website
from datetime import datetime
from datetime import timedelta

# The class responsible for doing the actual crawling
# Not directly linked to the two other classes, but returns data usable by them
class Crawler:
    # Declares the regex for URL parsing and driver and browser binaries locations for selenium
    def __init__(self) -> None:
        self.urlRegex = r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"
        
        # Values that will be parsed in settings.cfg file are initialized beforehand to be able to create
        # the settingsDict dictionary in parseConfig()
        self.settingsDict = {}
        self.parseConfig()
        
        # Sets up driver with required options and starts it
        option = webdriver.ChromeOptions()
        option.binary_location = self.settingsDict["browserPath"]
        option.page_load_strategy = "eager"
        self.driver = webdriver.Chrome(executable_path=self.settingsDict["driverPath"], options=option)
        self.driver.set_page_load_timeout(10)
    
    # Dumps the HTML content from the given URL and adds them to the database passed in parameter
    def crawlWebsite(self, url: str, dataBase: WebsiteDatabase) -> list:
        if fullmatch(self.urlRegex, url):
            self.driver.get(url)
            pageContent = self.driver.page_source
            
            parsedUrls = self.parseUrls(pageContent)
            dataBase.foundMultiple(parsedUrls, url)
            return parsedUrls
        return []
    
    # Wrapper for the crawlWebsite() function
    def crawlOnce(self, url: str, dataBase: WebsiteDatabase) -> list:
        # If on new database, simply explore the given URL
        print("dataBase.isEmpty():",str(dataBase.isEmpty()))
        if dataBase.isEmpty():
            dataBase.addEntry(url, 1)
            self.crawlWebsite(url, dataBase)
        # If on an existing database, get the list of unexplored websites, and explore each once only
        else:
            toExplore = dataBase.getUnexplored()
            for site in toExplore:
                self.crawlWebsite(site.url, dataBase)
        
        self.endDriver()
    
    # Recursively crawls webpages with a given number of iterations and adds any new URLs to a given WebsiteDatabase
    def crawlRecursive(self, startUrl: str, repeats: int, dataBase: WebsiteDatabase) -> None:
        if repeats >= 0:
            print("Exploring", startUrl)
            lastContent = self.crawlWebsite(startUrl, dataBase)
            for i in lastContent:
                try:
                    site = Website.urlToSite[i]
                    if site.explored == False:
                        self.crawlRecursive(i, repeats-1, dataBase)
                except:
                    pass
    
    # Wrapper for the crawlRecursive() function that displays some extra information in the console
    def recursiveCrawler(self, startUrl: str, repeats: int, dataBase: WebsiteDatabase) -> None:
        print("Starting recursive crawling from URL:", startUrl, "with", repeats, "iterations")
        startTime = datetime.now()
        
        # If on a new database, starts crawling recursively from the given URL with n repeats
        if dataBase.isEmpty():
            dataBase.addEntry(startUrl, 1)
            self.crawlRecursive(startUrl, repeats, dataBase)
        # If on an existing database, for each unexplored URL, starts crawling recursively with n repeats
        else:
            toExplore = dataBase.getUnexplored()
            for site in toExplore:
                self.crawlRecursive(site.url, repeats, dataBase)
        self.endDriver()
        
        endTime = datetime.now()
        runTime = (endTime - startTime).total_seconds()
        print("Recursive crawling finished in", runTime, "seconds")
    
    # Parse the scraped HTML content and searches for URLs using a regex match
    def parseUrls(self, pageContent: str) -> list:
        # Parses any URLs in the passed content, then uses a concise for-if loop to only return those that also
        # contain the "http" substring
        return  [url for url in findall(self.urlRegex, pageContent) if "http" in url]
    
    # Self explanatory, closes the browser & driver
    def endDriver(self) -> None:
        self.driver.quit()
    
    # Gets executables paths from settings.cfg file
    def parseConfig(self) -> None:
        fileName = "settings.cfg"
        
        with open(fileName, "r") as settings:
            for setting in settings:
                settingValuePair = setting.split(":", 1)
                # strip() removes the newline characters present in the file after each setting
                self.settingsDict[settingValuePair[0]] = settingValuePair[1].strip()
                