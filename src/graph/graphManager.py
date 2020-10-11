from requestManager import RequestManager
from graph.core.domGraph import DomGraph
from graph.core.depthHistogram import DepthHistogram
from graph.core.depthHitCumulateGraph import DepthHitCumulateGraph
from graph.core.compressedCalculusGraph import CompressedCalculusGraph

from graph.graphRenderer import GraphRenderer
from graph.core.graph import Graph as GRAPH

from graph.util.blockScraper import BlockScraper

# init each graph and draw
# depth=0 수준의 값은 무시하고 사용한다.

# 그래프를 매개변수로 받지말고, 각각 그래프 출력해주는 함수를 만드는게 더 나은 방식인 것 같다.
class GraphManager():

    htmlText = ''

    domGraph = None
    depthHistogram = None
    depthHitCumulate = None
    compressedCalculus = None

    renderer = None

    minDepth = 1

    def __init__(self, url, dividerOffset):
        # request
        reqManager = RequestManager(url)
        res = reqManager.requests()
        self.htmlText = res.text

        # init every graph
        self.initGraphs(dividerOffset)

        self.renderer = GraphRenderer()
        # print(dividerOffset)
        # self.dividerOffset = dividerOffset

    def setMinDepth(self, minDepth):
        self.minDepth = minDepth

    def setYMult(self, _mult):
        self.renderer.yMult = _mult

    # @property
    # def domGraph(self):
    #     if self.domGraph == None:
    #         print('(Error) current dom graph instance is None')
    #     return self.domGraph

    # init every graph
    def initGraphs(self, dividerOffset):
        # dom
        self.domGraph = DomGraph(self.htmlText)
        # depth histogram
        self.depthHistogram = DepthHistogram(self.domGraph)
        # depth hit cumulate
        self.depthHitCumulate = DepthHitCumulateGraph(self.domGraph, self.depthHistogram)
        self.compressedCalculus = CompressedCalculusGraph(self.depthHitCumulate, dividerOffset)

    # :::::::::::::::::::::::::::: show method :::::::::::::::::::::::::::::::::: #

    def showScatter(self, graph):
        if graph.current_type == GRAPH.DOM_GRAPH:
            print('DOM graph')
            self.renderer.showScatter(graph)
        elif graph.current_type == GRAPH.DEPTH_HISTOGRAM:
            print('Depth Histogram')
            self.renderer.showScatter(graph)

        # 모든 그래프를 다 작성한다.
        elif graph.current_type == GRAPH.DEPTH_HIT_CUMULATE_GRAPH:
            print('Depth hits cumulate graph')

            for idx in range(0, len(graph.depthHit_cumulate_list) - 1):
                graph.setGraphMemberByDepth(idx)
                self.renderer.showScatter(graph)
        # 구간별로 나누어 그리는 기울기 그래프
        elif graph.current_type == GRAPH.COMPRESSED_CALCULUS_GRAPH:
            self.showCompressedCalculus(graph)

    def showCompressedCalculus(self, graph):
        print('Compressed Calculus graph')
        for idx in range(0, len(graph.depthHit_cumulate_list)):
            # graph.setGraphMemberByDepth(idx)
            self.renderer.showCompressedCalculus(graph, idx)
        # graph.setGraphMemberByDepth(8)
        # self.renderer.showCompressedCalculus(graph, 8)

    def showDCgraph(self):
        print('DOM Calculus graphs ', len(self.compressedCalculus.depthHit_cumulate_list))

        for idx in range(self.minDepth, len(self.compressedCalculus.depthHit_cumulate_list)):
            try:
                self.renderer.showDCgraph(self.domGraph, self.compressedCalculus, idx)
            except:
                print(idx)

    def showSingleDCgraph(self, _depth):
        print('DOM Calculus graph')
        self.renderer.showDCgraph(self.domGraph, self.compressedCalculus, _depth)

    def showPlot(self, graph):

        if graph.current_type == GRAPH.DOM_GRAPH:
            print('DOM graph')
            self.renderer.showPlot(graph)
        elif graph.current_type == GRAPH.DEPTH_HISTOGRAM:
            print('Depth Histogram')
            self.renderer.showPlot(graph)

        # 모든 그래프를 다 작성한다.
        elif graph.current_type == GRAPH.DEPTH_HIT_CUMULATE_GRAPH:
            print('Depth hits cumulate graph')

            for idx in range(self.minDepth, len(graph.depthHit_cumulate_list)):
                graph.setGraphMemberByDepth(idx)
                self.renderer.showPlot(graph)

    def showSingleHitCumulate(self, _depth):
        print('Depth hits cumulate graph')

        self.depthHitCumulate.setGraphMemberByDepth(_depth)
        self.renderer.showPlot(self.depthHitCumulate)

    # :::::::::::::::::::::::::::: util method :::::::::::::::::::::::::::::::::: #

    def searchBlock(self, periodicalConst):
        blockScraper = BlockScraper(self.domGraph, self.compressedCalculus, periodicalConst)
        depth_block_data_list = blockScraper.searchAllBlockDepthLevel()

        pass
