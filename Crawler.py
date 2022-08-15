from selenium import webdriver
from re import findall, fullmatch
from WebsiteDatabase import WebsiteDatabase
from datetime import datetime
from datetime import timedelta

# The class responsible for doing the actual crawling
# Not directly linked to the two other classes, but returns data usable by them
class Crawler:
    # Declares the regex for URL parsing and driver and browser binaries locations for selenium
    def __init__(self) -> None:
        self.urlRegex = r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"
        
        self.parseConfig()
        
        option = webdriver.ChromeOptions()
        option.binary_location = self.browserPath
        option.page_load_strategy = "eager"
        self.driver = webdriver.Chrome(executable_path=self.driverPath, options=option)
        self.driver.set_page_load_timeout(5)
    
    # Dumps the HTML content from the given URL and returns a list of the URLs found
    def crawlWebsite(self, url: str) -> list:
        if fullmatch(self.urlRegex, url):
            self.driver.get(url)
            pageContent = self.driver.page_source
            
            return self.parseUrls(pageContent)
        return []
    
    # Recursively crawls webpages with a given number of iterations and adds any new URLs to a given WebsiteDatabase
    def crawlRecursive(self, startUrl: str, repeats: int, dataBase: WebsiteDatabase) -> None:
        if repeats >= 0:
            print("Exploring ", startUrl)
            lastContent = self.crawlWebsite(startUrl)
            dataBase.foundMultiple(lastContent, startUrl)
            for i in lastContent:
                try:
                    site = dataBase.findByUrl(i)
                    if site.explored == False:
                        site.explored = True
                        self.crawlRecursive(i, repeats-1, dataBase)
                except:
                    pass
    
    # This is just a wrapper for the crawlRecursive function that displays some extra information in the console
    def recursiveCrawler(self, startUrl: str, repeats: int, dataBase: WebsiteDatabase) -> None:
        print("Starting recursive crawling from URL:", startUrl, "with", repeats, "iterations")
        startTime = datetime.now()
        self.crawlRecursive(startUrl, repeats, dataBase)
        endTime = datetime.now()
        runTime = (endTime - startTime).total_seconds()
        print("Recursive crawling finished in", runTime, "seconds")
    
    # Parse the scraped HTML content and searches for URLs using a regex match
    def parseUrls(self, pageContent: str) -> list:
        urlList = findall(self.urlRegex, pageContent)
        newList = []
        for url in urlList:
            if "http" in url:
                newList.append(url)
        return newList
    
    # Self explanatory, closes the browser & driver
    def endDriver(self) -> None:
        self.driver.quit()
    
    # Gets executables paths from settings.cfg file
    def parseConfig(self) -> None:
        fileName = "settings.cfg"
        file = open("settings.cfg", "r")
        content = file.read()
        settings = content.split("\n")
        for setting in settings:
            keyValue = setting.split(":", 1)
            if keyValue[0] == "driverPath":
                self.driverPath = keyValue[1]
            elif keyValue[0] == "browserPath":
                self.browserPath = keyValue[1]