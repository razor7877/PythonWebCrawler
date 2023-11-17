from src.WebsiteDatabase import WebsiteDatabase
from src.GraphFactory import GraphFactory
from sys import argv
from tkinter import Tk
from tkinter.filedialog import askopenfilename

settingsDict = {}

# Gets settings.cfg file config
fileName = "settings.cfg"

with open(fileName, "r") as settings:
    for setting in settings:
        settingValuePair = setting.split(":", 1)
        # strip() removes the newline characters present in the file after each setting
        settingsDict[settingValuePair[0]] = settingValuePair[1].strip()

def getYesNo(textHint: str) -> str:
    yesNoValue = ""
    while yesNoValue not in ("y", "n"):
        yesNoValue = input(textHint).lower()
    return yesNoValue

# This file's only function is to load a graph from a saved .pickle database file
def main(siteDatabase = WebsiteDatabase()):
    if siteDatabase.isEmpty():
        databaseChoiceDone = False
        while not databaseChoiceDone:
            input("Choose your .pickle database file in the next dialog window\nPress Enter to continue to the file dialog window")
            databasePath = askopenfilename(filetypes=[("Database files", "*.pickle")])
            databaseConfirmYesNo = getYesNo("Is this the correct database path? (Y/N): " + databasePath + "\n")
            if databaseConfirmYesNo == "y":
                databaseChoiceDone = True
        siteDatabase.loadFromFile(databasePath)
    
    factory = GraphFactory()
    factory.graphMaker(siteDatabase, renderer=settingsDict["renderer"])

if __name__ == "__main__":
    # If a second argument is present (file path expected), then load it into a database
    if len(argv) > 1:
        siteDatabase = WebsiteDatabase()
        siteDatabase.loadFromFile(str(argv[1]))
        main(siteDatabase)
    # If no extra argument is passed, then simply proceed as usual
    else:
        main()
