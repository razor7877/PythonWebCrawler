from networkx import Graph, spring_layout, draw_networkx_edges, draw_networkx_nodes, draw_networkx_labels
import matplotlib.pyplot as plt
from datetime import datetime
from pyvis.network import Network
from src.WebsiteDatabase import WebsiteDatabase

class GraphFactory:
    
    # The settings here tend to greatly reduce the information that can be shown but might be helpful to improve readability on large graphs
    def __init__(self, labelsYesNo = True, trimYesNo = True, labelsSmallYesNo = False, scaleNodesYesNo = True, allowLoopsYesNo = False) -> None:
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
    
    def graphMaker(self, dataBase: WebsiteDatabase, renderer: str) -> None:
        if renderer == "networkx":
            self.nxRenderer(dataBase)
        elif renderer == "pyvis":
            self.pyVisRenderer(dataBase)
    
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
        maxNodeSize = 30
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
        
        for node in net.nodes:
            node["label"] = labelDict[node["id"]]
            node["value"] = nodeSizes[int(node["id"])]
            node["opacity"] = 0.70
            if node["value"] > 10:
                node["color"] = "#162347"
            else:
                node["color"] = "#4b5980"
        
        for edge in net.edges:
            edge
        
        net.show_buttons()
        net.save_graph(fileName)
        