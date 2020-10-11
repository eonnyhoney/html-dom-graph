from graph.core.graph import Graph
import copy

# 각 뎁스에 따른 누적 상승 곡선을 작성한다.
# 이를 통해, DOM graph에서 블록을 특정할 것 이다.
class DepthHitCumulateGraph(Graph):

    # store each depth level
    # high to low, sorting by desc
    # {
    #   'depth': ..., 'hits': ...
    # },
    # {}, {} ...
    desc_depth_list = []

    # depth list of actual dom graph
    dom_depth_list = []
    # maximum depth level
    max_depth = -1

    # 이 리스트는 각각의 뎁스 수준에 따른 누적 뎁스히트 상승곡선에 대해
    # 각 뎁스 레벨에 따라 보유하고 있습니다.
    # 각 인덱스는 뎁스 수준을 나타냅니다.
    depthHit_cumulate_list = []

    def __init__(self, domGraph, depthHistogram):
        # set graph type
        self.current_type = self.DEPTH_HIT_CUMULATE_GRAPH
        self.dom_depth_list = domGraph.depth_list
        self.desc_depth_list = depthHistogram.desc_depthDensity_list

        self.max_depth = depthHistogram.max_depth

        self.setEachGraphByDepth()
        self.setGraphMember()

    def setEachGraphByDepth(self):
        for currentFocusDepth in range(0, self.max_depth+1):
            tempDepth_list = []
            count = 0
            for depth in self.dom_depth_list:
                if currentFocusDepth == depth:
                    count += 1
                tempDepth_list.append(count)
            self.depthHit_cumulate_list.append(copy.deepcopy(tempDepth_list))

    # 누적 뎁스가 가장 많은 뎁스를 초기화
    def setGraphMember(self):
        maxDepthAccumulateIndex = self.desc_depth_list[0]['depth']
        self.yAxis = self.depthHit_cumulate_list[maxDepthAccumulateIndex]
        self.xAxis = range(0, len(self.dom_depth_list))

    # this method return xAxis and yAxis
    def setGraphMemberByDepth(self, _depth):
        self.yAxis = self.depthHit_cumulate_list[_depth]
        self.xAxis = range(0, len(self.dom_depth_list))

        # return self.xAxis, self.yAxis
