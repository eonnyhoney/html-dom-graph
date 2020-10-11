from abc import ABC, abstractmethod

# interface of each graph
class Graph(ABC):

    DOM_GRAPH = 0
    DEPTH_HISTOGRAM = 1
    DEPTH_HIT_CUMULATE_GRAPH = 2
    COMPRESSED_CALCULUS_GRAPH = 3

    current_type = -1

    yAxis = []
    xAxis = []

    # def __init__(self):
        # self.xAxis = []
        # self.yAxis = []

    # 그래프를 그리기 위해, x and y 멤버 초기화
    @abstractmethod
    def setGraphMember(self):
        # in this case, do not need to add like this
        # this line is for note
        raise NotImplementedError

    # this method return current graph member.
    # for drawing graph
    def getGraphMember(self):
        return self.xAxis, self.yAxis

    # @property
    # def xAxis(self):
    #     return self._xAxis
    #
    # @xAxis.setter
    # def xAxis(self, xAxis):
    #     self._xAxis = xAxis
    #
    # @property
    # def yAxis(self):
    #     return self._yAxis
    #
    # @xAxis.setter
    # def yAxis(self, yAxis):
    #     self._yAxis = yAxis
