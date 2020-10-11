from graph.util.xpathParser import XpathParser
from graph.util.blockScraper import BlockScraper

class ExtractManager:

    xpathParser = None
    blockScraper = None

    graphManager = None

    domGraph = None
    depthHistogram = None
    depthHitCumulate = None
    compressedCalculus = None

    def __init__(self, graphManager):
        self.graphManager = graphManager

        self.domGraph = graphManager.domGraph
        self.depthHistogram = graphManager.depthHistogram
        self.depthHitCumulate = graphManager.depthHitCumulate
        self.compressedCalculus = graphManager.compressedCalculus

        self.xpathParser = XpathParser(self.domGraph)

    def parseXpath(self, xpath_pair):
        # result = self.xpathParser.xpath(xpath)

        # input_pair = ['/html/body/div[2]/div[2]/div/div[1]/div[2]/ul/li[3]/div/div/span',
        #               '/html/body/div[2]/div[2]/div/div[1]/div[2]/ul/li[5]/div/div/span']
        self.xpathParser.addParentKey(xpath_pair)

        pass

    def parseBlocks(self, blocks):
        self.xpathParser.getDataFromBlocks(blocks)