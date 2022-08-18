from tkinter import Tk
from tkinter.filedialog import askopenfilename

def getYesNo(textHint: str) -> str:
    yesNoValue = ""
    while yesNoValue not in ("y", "n"):
        yesNoValue = input(textHint).lower()
    return yesNoValue

# This is a simple script to help the user configure
# the paths of their chrome driver & browser binaries

Tk().withdraw()

driverChoiceDone = False
while not driverChoiceDone:
    input("Choose your chromedriver.exe file in the next dialog window\nPress Enter to continue to the file dialog window")
    driverPath = askopenfilename(filetypes=[("Executables", "*.exe")])
    driverConfirmYesNo = getYesNo("Is this the correct chromedriver.exe path? (Y/N): " + driverPath + " ")
    if driverConfirmYesNo == "y":
        driverChoiceDone = True

browserChoiceDone = False
while not browserChoiceDone:
    input("Choose your Chrome or chromium-based (eg. Brave) binary file in the next dialog window\nPress Enter to continue to the file dialog window")
    browserPath = askopenfilename(filetype=[("Executables", "*.exe")])
    browserConfirmYesNo = getYesNo("Is this the correct browser binary path? (Y/N): " + browserPath + " ")
    if browserConfirmYesNo == "y":
        browserChoiceDone = True

fileName = "../settings.cfg"
fileContent = ""

try:
    file = open(fileName, "w")
    fileContent += "driverPath:" + driverPath + "\n"
    fileContent += "browserPath:" + browserPath
    file.write(fileContent)
    file.close()
    print("Settings successfully saved to", fileName)
except:
    print("There was an error while trying to save the settings")
