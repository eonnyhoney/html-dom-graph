
# 주어진 블록 구간의 데이터를 추출하는 기능 구현
class BlockScraper:

    domGraph = None
    compressedCalculus = None

    divide_block_list = []

    periodicConst = 2

    depth_block_data_list = []

    def __init__(self, domGraph, compressedCalculus, periodicConst=2):
        self.domGraph = domGraph
        self.compressedCalculus = compressedCalculus
        self.divide_block_list = compressedCalculus.divide_block_list
        self.periodicConst = periodicConst

    def searchBlockByDepthLevel(self, _depth):
        print('current depth level is ', _depth)
        block_data_list = []
        depthItem = self.divide_block_list[_depth]
        for block in depthItem:
            data_list = self.getDataFromBlock(block)
            block_data_list.append(data_list)

        return block_data_list

    def searchAllBlockDepthLevel(self):
        depth_block_data_list = []
        for depthLevel in range(0, len(self.divide_block_list)):
            block_data_list = self.searchBlockByDepthLevel(depthLevel)
            depth_block_data_list.append(block_data_list)

        self.depth_block_data_list = depth_block_data_list
        return depth_block_data_list

    # 주어진 블록에서 데이터 추출하여, 리스트로 반환
    def getDataFromBlock(self, block):

        startIdx = block['climbIdx'] * self.compressedCalculus.divideOffset
        endIdx = block['fallIdx'] * self.compressedCalculus.divideOffset

        sub_graph = self.domGraph.yAxis[startIdx:endIdx]

        # check periodical shape or not
        count = sub_graph.count(min(sub_graph))

        # 주기적인 형태를 띄지 않을 경우.

        # 주기적인 형태라 함은, 나타나는 len(minDepth) 개수로 구간을 나눠서
        if not self.isPeriodicalBlock(block):
            return

        selector = self.domGraph.currentSelector

        minIdx = sub_graph.index(min(sub_graph))
        # print('idx : ', minIdx, min(sub_graph))
        # print(sub_graph)
        parentElem = self.domGraph.tag_list[minIdx + startIdx]

        # print(block, parentElem)

        return None

    def isPeriodicalBlock(self, block):
        # print(block)
        startIdx = block['climbIdx'] * self.compressedCalculus.divideOffset
        endIdx = block['fallIdx'] * self.compressedCalculus.divideOffset

        sub_graph = self.domGraph.yAxis[startIdx:endIdx]

        min_depth_idx = sub_graph.index(min(sub_graph))
        min_depth = sub_graph[min_depth_idx]
        min_depth_count = sub_graph.count(min_depth)

        if min_depth_count < 3:
            return False

        graph_offset = int(len(sub_graph) / min_depth_count)
        # print(min_depth, ', ', min_depth_idx, ', ', graph_offset)
        flag = False
        for i in range(0, min_depth_count):
            start = (i * graph_offset)
            end = (i * graph_offset + graph_offset)
            count_result = sub_graph[start:end].count(min_depth)
            if count_result < 1:
                flag = True
            else:
                print(i, ' block count is ', count_result)

        if not flag:
            print('is periodical')
            return True
        else:
            print('min depth : ', min_depth, ', count : ', min_depth_count)
            print('Not periodical shape')
            return False