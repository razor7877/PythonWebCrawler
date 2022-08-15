# Simple class to represent the various websites encountered and store their data in an OOP friendly manner
class Website:
    lastId = 0

    def __init__(self, url: str, timesFound: int) -> None:
        self.id = Website.lastId
        Website.lastId += 1
        self.url = url
        self.timesFound = timesFound
        self.explored = False
        self.linkedFrom = []
    
    def resetCounter(self) -> None:
        self.timesFound = 0
    
    # Increments the number of time the website was found
    def addToCounter(self, occurrences) -> None:
        self.timesFound += occurrences
    
    # Adds a new URL link from where the website was found
    def addOriginLinked(self, originUrl: str) -> None:
        self.linkedFrom.append(originUrl)