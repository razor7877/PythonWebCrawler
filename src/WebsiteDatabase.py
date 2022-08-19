from src.Website import Website
from os.path import exists
from datetime import datetime
from pickle import dump, load

# The class that serves as interface between the Crawler and Website classes
# Manages creation of new entries, incrementation of existing ones ...
class WebsiteDatabase:
    
    def __init__(self) -> None:
        self.websites = []
    
    def isEmpty(self) -> bool:
        if len(self.websites) == 0:
            return True
        return False
    
    # Returns a list of websites in the database that haven't been explored (used for exploring existing databases)
    def getUnexplored(self) -> list:
        unexploredSites = []
        for site in self.websites:
            if not site.explored:
                unexploredSites.append(site)
        return unexploredSites
    
    # Main method to call externally, automatically manages creation or update of site entries
    def foundSite(self, url: str, timesFound: int, originUrl) -> None:
        if url in Website.urlToSite:
            Website.urlToSite[url].addToCounter(timesFound)
        else:
            self.addEntry(url, timesFound)
        Website.urlToSite[url].addLink(originUrl)
    
    # Can be used to pass multiple URLs scraped from a website
    def foundMultiple(self, urls: list, originUrl) -> None:
        [self.foundSite(url, 1, originUrl) for url in urls]
        originWebsite = Website.urlToSite[originUrl]
        originWebsite.urlCount = len(urls)
        originWebsite.explored = True
    
    # Creates a new Website using the constructor and adds it to it's own websites list
    def addEntry(self, url: str, timesFound: int) -> None:
        self.websites.append(Website(url, timesFound))
    
    # Clears the database
    def clearDatabase(self) -> None:
        self.websites.clear()

    # Returns how many websites are stored in the database object
    def getWebsitesCount(self) -> int:
        return len(self.websites)

    # Gets how many times each website was found and returns the sum
    def getFoundCount(self) -> int:
        counter = 0
        for site in self.websites:
            counter += site.timesFound
        return counter
    
    # Dumps the content of the URLs that have been gathered to the console
    def dumpToConsole(self) -> None:
        print("Website count: ", self.getWebsitesCount())
        print("Found count: ", self.getFoundCount())
        for i in range(len(self.websites)):
            site = self.websites[i]
            
            #print("\n*-----* Entry #",i, "*-----*")
            #print("ID:", site.id)
            #print("URL:", site.url)
            #print("Times found:", site.timesFound)
            #print("Linked from:", site.linkedFrom)
            #print("URL count:", site.urlCount)
            #print("Explored:", site.explored)
            
            # Optimized way that aims to reduce the number of print() calls, same as the commented out print() calls above
            print("\n*-----* Entry #",i, "*-----*\nID:", site.id,"\nURL:", site.url,"\nTimes found:", site.timesFound,"\nLinked from:", site.linkedFrom,"\nURL count:", site.urlCount,"\nExplored:", site.explored)
    
    # Attempts dumping the URLs that have been gathered to a text file
    def dumpToFile(self) -> None:
        print("Starting file dump")
        fileContent = ""
        fileTime = datetime.now().strftime("%Y%m%d%H%M%S")
        fileName = "dumps/dump_" + fileTime + ".txt"
        try:
            # Gets the urls of every websites found, and writes them all to a file separated by newlines \n
            file = open(fileName, "w")
            for site in self.websites:
                fileContent += site.url + "\n"
            file.write(fileContent)
            file.close()
            print("Content successfully dumped to", fileName)
        except Exception as ex:
            print(ex)
            print("There was an error while trying to dump to file")
    
    # Used to serialize and save an instance's data to a file for later reuse
    def saveToFile(self):
        print("Starting file save")
        fileTime = datetime.now().strftime("%Y%m%d%H%M%S")
        fileName = "data/database_" + fileTime + ".webdb"
        try:
            with open(fileName, "wb") as file:
                dump(self.websites, file)
                file.close()
            print("Database successfully saved to", fileName)
        except:
            print("There was an error while trying to serialize the file")
    
    # Unserialize given file and loads it back into the instance
    def loadFromFile(self, fileName):
        print("Loading from file",fileName)
        try:
            with open(fileName, "rb") as file:
                self.websites = load(file)
            Website.lastId = len(self.websites) - 1
            for site in self.websites:
                Website.urlToSite[site.url] = site
            print("Database successfully loaded from", fileName)
        except Exception as ex:
            print(ex)
            print("There was an error while trying to unserialize the file")    
