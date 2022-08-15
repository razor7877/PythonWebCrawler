from selenium import webdriver
from re import findall
from Website import Website
from WebsiteDatabase import WebsiteDatabase
from Crawler import Crawler
from GraphFactory import GraphFactory

def main():
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
        webCrawler = Crawler()
        webCrawler.recursiveCrawler(url, iterations, siteDatabase)
    else:
        webCrawler = Crawler()
        siteDatabase.foundMultiple(webCrawler.crawlWebsite(url))
    webCrawler.endDriver()

    print("Finished crawling!")

    if dumpFileYesNo == "y":
        siteDatabase.dumpToFile()

    if dumpConsoleYesNo == "y":
        siteDatabase.dumpDatabase()

    factory = GraphFactory()
    factory.graphMaker(siteDatabase)
    
if __name__ == "__main__":
    main()
