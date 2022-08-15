from Website import Website
from os.path import exists

# The class that serves as interface between the Crawler and Website classes
# Manages creation of new entries, incrementation of existing ones ...
class WebsiteDatabase:
    
    def __init__(self) -> None:
        self.websites = []
    
    # Main method to call externally, automatically manages creation or update of site entries
    def foundSite(self, url: str, timesFound: int, originUrl = "") -> None:
        siteExists = self.findByUrl(url)
        if siteExists != None:
            siteExists.addToCounter(timesFound)
        else:
            self.addEntry(url, timesFound)
            siteExists = self.websites[-1]
        if originUrl != "":
            siteExists.addLink(originUrl)
    
    # Can be used to pass multiple URLs scraped from a website
    def foundMultiple(self, urls: list, originUrl = "") -> None:
        for url in urls:
            self.foundSite(url, 1, originUrl)

    # Iterates over it's own websites list and returns the first whose url attribute equals passed parameter
    # If none found, None is returned
    def findByUrl(self, url: str) -> Website:
        for site in self.websites:
            if site.url == url:
                return site
        return None
    
    # Creates a new Website using the constructor and adds it to it's own websites list
    def addEntry(self, url: str, timesFound: int) -> None:
        self.websites.append(Website(url, timesFound))

    # Delete an entry by it's url
    def deleteEntry(self, url) -> None:
        self.websites.remove(self.findByUrl(url))
    
    # Clears the database
    def clearDatabase(self) -> None:
        self.websites.clear()

    # Returns how many websites are stored in the database object
    def getWebsitesCount(self) -> int:
        return len(self.websites)

    # Gets how many times each website was found and returns the sum
    def getFoundCounts(self) -> int:
        counter = 0
        for site in self.websites:
            counter += site.timesFound
        return counter
    
    # Dumps the content of the URLs that have been gathered to the console
    def dumpDatabase(self) -> None:
        print("Website count: ", self.getWebsitesCount())
        print("Found count: ", self.getFoundCounts())
        for i in range(len(self.websites)):
            site = self.websites[i]
            
            #print("\n*-----* Entry #",i, "*-----*")
            #print("ID:", site.id)
            #print("URL:", site.url)
            #print("Times found:", site.timesFound)
            #print("Linked from:", site.linkedFrom)
            
            # Optimized way that aims to reduce the number of print() calls, same as the commented out print() calls above
            print("\n*-----* Entry #",i, "*-----\nID:", site.id,"\nURL:", site.url,"\nTimes found:", site.timesFound,"\nLinked from:", site.linkedFrom)
    
    # Attempts dumping the URLs that have been gathered to a text file
    def dumpToFile(self) -> None:
        print("Starting file dump")
        fileContent = ""
        fileName = "crawlerDump.txt"
        try:
            if exists(fileName):
                continueYesNo = input("File crawlerDump.txt already exists. Overwrite it? (Y/N): ").lower()
                if continueYesNo != "y":
                    return
            file = open(fileName, "w")
            for site in self.websites:
                fileContent += site.url + "\n"
            file.write(fileContent)
            file.close()
            print("Content successfully dumped to", fileName)
        except:
            print("There was an error while trying to dump to file")
