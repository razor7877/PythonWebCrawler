# Simple class to represent the various websites encountered and store their data in an OOP friendly manner
class Website:
    lastId = 0
    urlToSite = {}
    
    def __init__(self, url: str, timesFound: int) -> None:
        self.url = url
        self.timesFound = timesFound
        
        self.id = Website.lastId
        Website.urlToSite[url] = self
        Website.lastId += 1
        self.explored = False
        # Each instance has an array containing the IDs of any other websites where it was obtained from
        self.linkedFrom = []
        # The number of URLs that have been found on the website, stays at 0 if not explored
        self.urlCount = 0
    
    def resetCounter(self) -> None:
        self.timesFound = 0
    
    # Increments the number of time the website was found
    def addToCounter(self, occurrences) -> None:
        self.timesFound += occurrences
    
    # Adds a new URL link from where the website was found unless it already exists
    def addLink(self, originUrl: str) -> None:
        correspondingId = Website.urlToSite[originUrl].id
        if correspondingId not in self.linkedFrom:
                self.linkedFrom.append(correspondingId)
        