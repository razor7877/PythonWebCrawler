from networkx import Graph, spring_layout, draw_networkx_edges, draw_networkx_nodes, draw_networkx_labels
import matplotlib.pyplot as plt
from datetime import datetime
from pyvis.network import Network
from src.WebsiteDatabase import WebsiteDatabase
from urllib.parse import urlparse

class GraphFactory:
    
    # The settings here tend to greatly reduce the information that can be shown but might be helpful to improve readability on large graphs
    def __init__(self, labelsYesNo = True, trimYesNo = True, labelsSmallYesNo = False, scaleNodesYesNo = True, allowLoopsYesNo = False, distinguishDomains = False, distinguishSubDomains = False) -> None:
        # Whether labels should be displayed at all or not (overrides others)
        self.labelsYesNo = labelsYesNo
        # Whether labels should only show the domain name (eg. www.domain.com)
        self.trimYesNo = trimYesNo
        # Whether labels should be shown for nodes that have not been explored (only linked to their origin node)
        self.labelSmallYesNo = labelsSmallYesNo
        # Whether nodes should scale in size depending on how many other nodes they are linked to
        self.scaleNodesYesNo = scaleNodesYesNo
        # Whether edges that link nodes to themselves should be displayed or not
        self.allowLoopsYesNo = allowLoopsYesNo
        
        # Whether URLs with the same domain name should be distinguished or shown as a single node
        # (eg. example.com/path1/image.png & example.com/video.mp4)
        self.distinguishDomains = distinguishDomains
        # Whether URLs with the same subdomain name should be distinguished or shown as a single node
        # (eg. drive.google.com & images.google.com)
        # This parameter is overriden by the first one
        self.distinguishSubDomains = distinguishSubDomains
    
    def graphMaker(self, dataBase: WebsiteDatabase, renderer: str) -> None:
        print("Starting graph generation with", dataBase.getWebsitesCount(), "nodes")
        
        if renderer == "networkx":
            self.nxRenderer(self.distinguisher(dataBase))
        elif renderer == "pyvis":
            self.pyVisRenderer(self.distinguisher(dataBase))
        
        print("Graph generation finished!")
        
    # The function that generates NetworkX graphs. Not responsible for the visualization, only outputs
    # data relevant to visualization for further use
    def nxMaker(self, dataBase: WebsiteDatabase) -> list:
        # Creates a new nx graph object, gets the passed database websites list in a local object
        # and initalizes a dictionary to match the nodes IDs with their corresponding URLs
        G = Graph()
        websites = dataBase.websites

        labelDict = {}
        nodeSizes = []
        
        maxUrlCount = 0
        
        # Creates all nodes first, identified by their IDs, then attributes them a label (their url)
        for website in websites:
            G.add_node(website.id)
            if not self.labelSmallYesNo or website.urlCount > 0:
                # website.url : gets the url of the website the loop is currently iterating over
                # split("://")[1] : splits the URL and retrieves the part after the http(s) protocol
                # split("/")[0] : splits on slashes and retrieves only the first part (the domain name)
                labelDict[website.id] = website.url.split("://")[1].split("/")[0]
            if website.urlCount > maxUrlCount:
                maxUrlCount = website.urlCount
        
        # The ratio between these two determines the size differences between the largest and smallest nodes
        # 30:1 means the biggest node(s) will be 30x the size of the smallest one(s)
        maxNodeSize = 300
        minNodeSize = 1

        # Once all nodes exists, all the links are created between the nodes
        for website in websites:
            # Creating all edges based on linking data
            for link in website.linkedFrom:
                if website.id != link or self.allowLoopsYesNo:
                    G.add_edge(website.id, link)
            
            # Creating the node sizes list
            if self.scaleNodesYesNo and website.urlCount != 0:
                # Calculates the ratio between the website's URL count 
                nodeSizes.append(maxNodeSize * (website.urlCount / maxUrlCount) * 10)
            else:
                nodeSizes.append(minNodeSize * 10)
        
        graphData = [G, labelDict, nodeSizes]
        return graphData
    
    # Used to render a graph using NetworkX and matplotlib directly
    def nxRenderer(self, dataBase: WebsiteDatabase) -> None:
        # Unpacks the values from the graph maker
        G, labelDict, nodeSizes = self.nxMaker(dataBase)
        
        pos = spring_layout(G, scale=1)
        draw_networkx_edges(G, pos, edge_color="m", alpha=0.5)
        draw_networkx_nodes(G, pos, node_size=nodeSizes, node_color="#210070", alpha=0.9)
        label_options = {"ec": "k", "fc": "white", "alpha": 0.2}
        draw_networkx_labels(G, pos, font_size=6, bbox=label_options, labels=labelDict)
        
        plt.show()
    
    # Used to render a graph using pyVis instead
    def pyVisRenderer(self, dataBase: WebsiteDatabase) -> None:
        G, labelDict, nodeSizes = self.nxMaker(dataBase)
        fileTime = datetime.now().strftime("%Y%m%d%H%M%S")
        fileName = "graphs/graph_" + fileTime + ".html"
        
        net = Network(height="600px",width="1000px")
        net.from_nx(G)
        
        # A counter has eventually been added since the distinguisher() builds a WebsiteDatabase on top of an existing one,
        # and therefore the ID attribution starts at higher than 0 because Website.lastId is a static variable
        counter = 0
        for node in net.nodes:
            node["label"] = labelDict[node["id"]]
            node["value"] = nodeSizes[counter]
            node["opacity"] = 0.70
            if node["value"] > 10:
                node["color"] = "#162347"
            else:
                node["color"] = "#4b5980"
            
            counter += 1
        
        net.show_buttons()
        net.save_graph(fileName)
    
    # Function used for applying the parameters related to whether subdomains and domains/paths should be distinguished
    # It essentially completely rebuilds a new database
    
    # Each URls from the old database that obtain the same new URLs when applying the parameters are merged into single Website entries
    # This implies that new entries are made for each of those, with different IDs, so each of the linkedFrom list has to be rebuilt completely as well
    # One or multiple old IDs become a single new ID in the new database
    # Each of those old IDs contains their own linkedFrom list
    
    # Multiple dictionaries are made to handle the process, existingUrls associates an url that has already been added with it's corresponding entry (it's Website object)
    # Dictionaries are made to allow easy access from oldId > newId and newId > oldId, and a third one "oldIdsToLinks" allows to associate the linkedFrom lists of every
    # old entries with their respective old ID
    def distinguisher(self, dataBase: WebsiteDatabase) -> WebsiteDatabase:
        # Get the old database
        displayDataBase = WebsiteDatabase()
        
        existingUrls = {}
        oldIdsToLinks = {}
        idsNewToOld = {}
        idsOldToNew = {}
        
        corruptedIds = []
        
        for site in dataBase.websites:
            try:
                urlComponents = urlparse(site.url)
                
                # Not distinguishing between domains
                if not self.distinguishDomains:
                    # Distinguishing neither domains or subdomains (www.example.com/path/image.png == sub.example.com/video.mp4 : becomes http://example.com)
                    if not self.distinguishSubDomains:
                        splitNetloc = urlComponents[1].split(".")
                        # If netloc has form domain.tld
                        if len(splitNetloc) == 2:
                            url = urlComponents[0] + "://" + urlComponents[1]
                        # If netloc has form subdomain.domain.tld
                        else:
                            url = urlComponents[0] + "://" + splitNetloc[1] + "." + splitNetloc[2]
                    
                    # Distinguishing subdomains but not domains (www.example.com != sub.example.com ; sub.example.com/image.png == sub.example.com/ftp/files/)
                    else:
                        url = urlComponents[0] + "://" + urlComponents[1]
                
                # Distinguishing both domains and subdomains (www.example.com != sub.example.com ; sub.example.com/image.png != sub.example.com/ftp/files/)
                else:
                    url = site.url
                
                if url not in existingUrls:
                    # Create entry in the new database
                    displayDataBase.addEntry(url, site.timesFound)
                    # Set it's url count, and sets it explored if url count is not 0
                    displayDataBase.websites[-1].urlCount = site.urlCount
                    if site.urlCount > 0:
                        displayDataBase.websites[-1].explored = True;
                    # Gets the id of the last website in the new database, and gets the id of the current website in the old database and assigns to dictionary
                    idsNewToOld[displayDataBase.websites[-1].id] = [site.id]
                else:
                    # If url already exists in the new database, get the corresponding website with the existingUrls dictionary, and adds the old site id to it
                    idsNewToOld[existingUrls[url].id].append(site.id)
                
                idsOldToNew[site.id] = displayDataBase.websites[-1].id
                # Associates the old database id with it's list of (old) id links
                oldIdsToLinks[site.id] = site.linkedFrom
                # Associates the current url with the latest website created in the new database
                existingUrls[url] = displayDataBase.websites[-1]
            # There can sometimes be issue with weird specific URLs (eg http.js, a.http, www.website.com/https ...)
            # We skip those when generating the graph if an error occurs
            except:
                print("Error with website", site.id, "at url:", site.url)

        # For each new site in the new database
        for site in displayDataBase.websites:
            # For each new site, get it's associated old IDs, and iterate over them
            for oldId in idsNewToOld[site.id]:
                # For each old ID, gets it's associated linkFrom list (of old IDs themselves), and iterates over the list
                for link in oldIdsToLinks[oldId]:
                    # For each link value in the list, get the corresponding new ID from the old ID
                    correspondingId = idsOldToNew[link]
                    # If this new ID is not already in the linkedFrom list of the new object, append it
                    if correspondingId not in site.linkedFrom:
                        site.linkedFrom.append(correspondingId)
        
        return displayDataBase