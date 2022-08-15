from selenium import webdriver
from re import findall
from Website import Website
from WebsiteDatabase import WebsiteDatabase
from Crawler import Crawler

from datetime import datetime
from datetime import timedelta


def main():
    driverPath = "C:/Users/Sandra/Desktop/Python/chromedriver.exe"
    browserPath = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
    
    url = input("Enter URL to crawl: ")

    yesNoTuple = ("y", "n")
    dumpFileYesNo = ""
    while dumpFileYesNo not in yesNoTuple:
        dumpFileYesNo = input("Should the gathered URLs be dumped into a .txt file? (Y/N): ").lower()
        print(dumpFileYesNo)

    dumpConsoleYesNo = ""
    while dumpConsoleYesNo not in yesNoTuple:
        dumpConsoleYesNo = input("Should the gathered URLs be dumped into the console? (Keep in mind it can take a while to print everything)(Y/N): ")
    
    recursiveYesNo = ""
    while recursiveYesNo not in yesNoTuple:
        recursiveYesNo = input("Do you want to do a recursive crawling? (Y/N): ").lower()

    siteDatabase = WebsiteDatabase()
    siteDatabase.clearDatabase()
    
    if recursiveYesNo == "y":
        iterations = 0
        while iterations == 0:
            try:
                iterations = int(input("How many iterations should be done? (Keep in mind more than 1 can become exceedingly long to complete): "))
            except:
                print("Please enter a valid number")
        webCrawler = Crawler(driverPath, browserPath)
        webCrawler.recursiveCrawler(url, iterations, siteDatabase)
    else:
        webCrawler = Crawler(driverPath, browserPath)
        siteDatabase.foundMultiple(webCrawler.crawlWebsite(url), url)
    webCrawler.endDriver()

    print("Finished crawling!")
    
    if dumpFileYesNo == "y":
        siteDatabase.dumpToFile()

    if dumpConsoleYesNo == "y":
        startTime = datetime.now()
        siteDatabase.dumpDatabase()
        endTime = datetime.now()
        runTime = (endTime - startTime).total_seconds()
        print("Console dump run time: ",runTime," seconds")
    
if __name__ == "__main__":
    main()
