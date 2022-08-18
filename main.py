from selenium import webdriver
from src.WebsiteDatabase import WebsiteDatabase
from src.Crawler import Crawler
from src.GraphFactory import GraphFactory
from sys import argv
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def getYesNo(textHint: str) -> str:
    yesNoValue = ""
    while yesNoValue not in ("y", "n"):
        yesNoValue = input(textHint).lower()
    return yesNoValue
    
def main(siteDatabase = WebsiteDatabase()):
    # Parameters to determine what should be output and how the crawler should work
    
    if siteDatabase.isEmpty():
        url = input("Enter URL to crawl: ")
    else:
        url = ""
    
    saveDataYesNo = getYesNo("Should the database contents be saved to a file? This allows you to load and reuse the data later on. (Y/N): ")
    dumpFileYesNo = getYesNo("Should the gathered URLs be dumped into a .txt file? (Y/N): ")
    dumpConsoleYesNo = getYesNo("Should the gathered URLs be dumped into the console? (Keep in mind it can take a while to print everything)(Y/N): ")
    
    recursiveYesNo = getYesNo("Do you want to do a recursive crawling? (Y/N): ")
    
    if recursiveYesNo == "y":
        iterations = 0
        while iterations == 0:
            try:
                iterations = int(input("How many iterations should be done? (Keep in mind more than 1 can become exceedingly long to complete): "))
            except:
                print("Please enter a valid number")
        # Creates a new crawler object and starts recursive crawling with parameters given by the user
        webCrawler = Crawler()
        webCrawler.recursiveCrawler(url, iterations, siteDatabase)
    else:
        # Creates a new crawler object and starts non-recursive crawling with parameters given by the user
        webCrawler = Crawler()
        webCrawler.crawlOnce(url, siteDatabase)

    print("Finished crawling!")
    
    if saveDataYesNo == "y":
        siteDatabase.saveToFile()
    
    if dumpFileYesNo == "y":
        siteDatabase.dumpToFile()

    if dumpConsoleYesNo == "y":
        siteDatabase.dumpToConsole()
    
    print("Starting graph generation with", siteDatabase.getWebsitesCount(), "nodes")
    # Check GraphFactory class for more info if looking to play with the various parameters
    factory = GraphFactory()
    factory.graphMaker(siteDatabase, renderer="networkx")
    print("Graph generation finished!")
    
if __name__ == "__main__":
    # If a second argument is present (file path expected), then load it into a database
    if len(argv) > 1:
        siteDatabase = WebsiteDatabase()
        siteDatabase.loadFromFile(str(argv[1]))
        main(siteDatabase)
    # If no extra argument is passed, then simply proceed as usual
    else:
        main()
