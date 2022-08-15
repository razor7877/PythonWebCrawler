# Simple class to represent the various websites encountered and store their data in an OOP friendly manner
class Website:
    lastId = 0
    urlToIds = {}
    
    def __init__(self, url: str, timesFound: int) -> None:
        self.url = url
        self.timesFound = timesFound
        
        self.id = Website.lastId
        Website.urlToIds[url] = self.id
        Website.lastId += 1
        self.explored = False
        self.linkedFrom = []
    
    def resetCounter(self) -> None:
        self.timesFound = 0
    
    # Increments the number of time the website was found
    def addToCounter(self, occurrences) -> None:
        self.timesFound += occurrences
    
    # Adds a new URL link from where the website was found
    def addLink(self, originUrl: str) -> None:
        # Needs to be made better so that errors cannot occur (thus removing the need for try/except)
        try:
            correspondingId = Website.urlToIds[originUrl]
            if correspondingId not in self.linkedFrom:
                self.linkedFrom.append(correspondingId)
        except:
            pass
        