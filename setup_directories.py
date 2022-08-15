from tkinter import Tk
from tkinter.filedialog import askopenfilename

# This is a simple script to help the user configure
# the paths of their chrome driver & browser binaries

Tk().withdraw()

yesNoTuple = ("y", "n")

driverChoiceDone = False
while not driverChoiceDone:
    print("Choose your chromedriver.exe file in the next dialog window")
    input("Press Enter to continue to the file dialog window")
    driverPath = askopenfilename(filetypes=[("Executables", "*.exe")])
    driverConfirmYesNo = ""
    while driverConfirmYesNo not in yesNoTuple:
        driverConfirmYesNo = input("Is this the correct chromedriver.exe path? (Y/N): " + driverPath + " ").lower()
    if driverConfirmYesNo == "y":
        driverChoiceDone = True

browserChoiceDone = False
while not browserChoiceDone:
    print("Choose your chrome or chromium-based (eg. Brave) binary file in the next dialog window")
    print("Press Enter to continue to the file dialog window")
    browserPath = askopenfilename(filetype=[("Executables", "*.exe")])
    browserConfirmYesNo = ""
    while browserConfirmYesNo not in yesNoTuple:
        browserConfirmYesNo = input("Is this the correct browser binary path? (Y/N): " + browserPath + " ").lower()
    if browserConfirmYesNo == "y":
        browserChoiceDone = True

fileName = "settings.cfg"
fileContent = ""

try:
    file = open(fileName, "w")
    fileContent += "driverPath:" + driverPath + "\n"
    fileContent += "browserPath:" + browserPath + "\n"
    file.write(fileContent)
    file.close()
    print("Settings successfully saved to", fileName)
except:
    print("There was an error while trying to save the settings")
