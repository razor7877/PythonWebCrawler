# Python Web Crawler

A very basic web crawler made in Python as a weekend project. It can simply scrapes URLs from a webpage or recursively scrape the URLs that it finds. It also generates graphs to visualize the data.

![A graph generated by the crawler with PyVis](img/webcrawler_pyvis.png "A graph generated by the crawler")

## Features

 - Scrape any website once or recursively with a given number of iterations
 - Save scraped URLs and resume scraping later
 - Dump URLs into a text file
 - Dump scraping data into the console
 - Generate graphs to visualize the URLs found and how they are connected using either the PyVis or NetworkX renderers

## How to use?

### Setup

Before using it, the crawler requires a little configuration to work properly. You will have to:

1. Download the required python libraries if they are not already installed on your machine. You can do it by executing the "install_dependencies.bat" batch file, or manually by installing the following libraries:
		- Selenium (for manipulating web drivers)
		- NetworkX (for the generation of network graphs)
		- Matplotlib (used by NetworkX for displaying generated graphs)
		- Scipy (used by NetworkX for generating graphs)
2. If you don't already have it, download the chromedriver.exe file that corresponds to your Chrome or chromium-based browser version here: [https://chromedriver.chromium.org/](https://chromedriver.chromium.org/)
3. Execute the "setup_directories.py" script file to configure the paths of your executables. Simply follow the instructions and the locations of your chromedriver.exe and browser binary will be saved in a "settings.cfg" file in the main directory
4. You can now run the "main.py" script file and follow the instructions to run the web crawler

You can change the renderer used in the settings.cfg file, the two valid options are either "pyvis" (default) or "networkx"

### Crawling a website

Once setup is done, simply run the "main.py" script file and follow the instructions

### Creating/loading a graph

You can drag and drop a .pickle database file on the "load_graph.py" script file, or directly open the file and follow the instructions. The renderer used is the one defined in the config file

## Pictures

![A graph generated by the crawler with PyVis](img/webcrawler_pyvis.png "A graph generated by the crawler with PyVis")
![A graph generated by the crawler with NetworkX](img/webcrawler_networkx.png "A graph generated by the crawler with NetworkX")