from graph.core.graph import Graph

class DepthHistogram(Graph):
    # store depth, set value at __init__
    # this value is quite temporary.
    # only using for counting depths
    depth_list = []
    # store max depth
    max_depth = -1

    # density of depth graph
    depthDensity_list = []

    # sorted depthDensity_list
    desc_depthDensity_list = []

    def __init__(self, domGraph):
        # set graph type
        self.current_type = self.DEPTH_HISTOGRAM

        self.depth_list = domGraph.yAxis
        self.max_depth = max(self.depth_list)

        self.initDensityList()
        self.sortDensityGraphByDesc()

        self.setGraphMember()

    # init density list
    def initDensityList(self):
        # fill 0 in array
        self.depthDensity_list = [0] * (self.max_depth + 1)

        for depth in self.depth_list:
            self.depthDensity_list[depth] += 1

    # not implemented yet
    def removeItem(self, cntTarget):
        # if item counts less than cntTarget
        # remove from list
        pass

    # sort by decrease
    def sortDensityGraphByDesc(self):
        # init value to list
        for depth, hits in enumerate(self.depthDensity_list):
            self.desc_depthDensity_list.append({
                'depth': depth,
                'hits': hits,
            })

        for item in self.desc_depthDensity_list:
            for jtem in self.desc_depthDensity_list:
                if item['hits'] > jtem['hits']:
                    temphits = {
                        'hits': item['hits'],
                        'depth': item['depth']
                    }
                    item['hits'] = jtem['hits']
                    item['depth'] = jtem['depth']
                    jtem['hits'] = temphits['hits']
                    jtem['depth'] = temphits['depth']

    # 그래프를 그리기 위해, x and y 멤버 초기화
    def setGraphMember(self):
        # x축 상승곡선과 y축 상승곡선이 서로 맞지 않아 그래프로 그리기 어렵다.
        # 이에, hits에 대한 정보는 폐기하고 depth에 대한 정보만 남기기로 한다.

        self.xAxis = [0] * len(self.desc_depthDensity_list)
        for item in self.desc_depthDensity_list:
            self.yAxis.append(item['depth'])
