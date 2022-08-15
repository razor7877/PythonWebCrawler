import networkx
import matplotlib.pyplot as plt
from WebsiteDatabase import WebsiteDatabase

class GraphFactory:

    def graphMaker(self, database: WebsiteDatabase):
        G = networkx.Graph()
        websites = database.websites
        labelDict = {}
        
        for website in websites:
            G.add_node(website.id)
            labelDict[website.id] = website.url
        for website in websites:
            for link in website.linkedFrom:
                G.add_edge(website.id, link)
        pos = networkx.spring_layout(G, scale=5)
        networkx.draw(G, pos, labels=labelDict, with_labels=True)
        plt.show()
