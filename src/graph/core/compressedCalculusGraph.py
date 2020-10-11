from graph.core.graph import Graph
import copy

class CompressedCalculusGraph(Graph):

    # set from depthHitCumulate graph
    # 이 리스트는 각각의 뎁스 수준에 따른 누적 뎁스히트 상승곡선에 대해
    # 각 뎁스 레벨에 따라 보유하고 있습니다.
    # 각 인덱스는 뎁스 수준을 나타냅니다.
    depthHit_cumulate_list = []

    # min, max
    # 각 기울기
    # 분할된 각 뎁스 리스트의 기울기 값 리스트
    # [{'list': [],
    # 'min': ..,
    # 'max': ..,
    # 'divide_list': [{'climbIdx': ..., 'fallIdx': ...}]}]
    calculus_list = []

    # 각 뎁스 별, 구분된 블록의 리스트
    # divide_block_list[depth] = [{'', ''}, {} ...]
    divide_block_list = []

    # 범위를 나눌 상수
    divideOffset = 1

    # 현재 시점의 평균 기울기
    currentA = 0

    def __init__(self, depthHitCumulateGraph, divideOffset=10):
        self.current_type = self.COMPRESSED_CALCULUS_GRAPH
        self.depthHit_cumulate_list = depthHitCumulateGraph.depthHit_cumulate_list
        self.divideOffset = divideOffset

        self.initGraphMember()

    def initGraphMember(self):
        # depth level
        for idx, list in enumerate(self.depthHit_cumulate_list):
            # 각 뎁스에서 min, max 얻기
            _min = min(list)
            _max = max(list)

            # 상수(c)로 나누어, 각 범위 별로 기울기 구하기
            # 나눠진 범위에 대해 각각 min, max 구하기
            additional_index = 2
            destRange = int(len(list)/self.divideOffset) + additional_index
            temp_list = []
            for offset in range(0, destRange):
                # get min from list
                idx = offset * self.divideOffset
                if idx > len(list):
                    idx = len(list) - 1
                try:
                    listMin = list[idx]
                except:
                    print('what is this')

                # get max from list
                maxIdx = idx+self.divideOffset
                if idx+self.divideOffset >= len(list):
                    maxIdx = len(list) - 1
                listMax = list[maxIdx]
                # print(listMin, ' and ', listMax)
                if listMax - listMin == 0:
                    listA = 0
                else:
                    listA = (listMax - listMin) / self.divideOffset

                # depthItem = {
                #     'min': listMin,
                #     'max': listMax,
                #     'a': listA
                # }
                # temp_list.append(depthItem)
                temp_list.append(listA)
            # end divide for loop

            # global slope value
            _a = (list[len(list)-1] - list[0]) / len(list)
            tempItem = {
                'list': temp_list,
                # 'min': _min,
                # 'max': _max,
                'a': _a
            }
            self.calculus_list.append(tempItem)
        # end for loop


    def multAvgSlopeA(self, _mult):
        for item in self.calculus_list:
            item['a'] *= _mult

        self.setDivdieIndex()

    def setDivdieIndex(self):
        for depth, depthItem in enumerate(self.calculus_list):
            _a = depthItem['a']
            flag = False
            divide_list = []

            # 기준 기울기 값을 넘은 값과 내려온 값의 페어가 존재한다.
            # 페어가 존재해야 해당 값을 리스트에 넣는다.
            # 각 climbIdx, fallIdx는 해당 변화(기준 선은 넘거나 내려가거나)가 일어나는 인덱스를 의미한다.
            for idx, slope in enumerate(depthItem['list']):
                # const line (기준 기울기 값)을 넘은 값(각 구간의 기울기 값)이 등장했을 때
                if not flag and slope > _a:
                    climbIdx = idx + 1
                    flag = True
                # const line (기준 기울기 값)을 내려온 값(각 구간의 기울기 값)이 등장했을 때.
                elif flag and slope < _a:
                    fallIdx = idx - 1
                    # 추후에 인덱스 0, 1로 변경바람.
                    if fallIdx - climbIdx >= 1:
                        divide_list.append({
                            'climbIdx': climbIdx,
                            'fallIdx': fallIdx
                        })
                    flag = False

                    # reset value
                    climbIdx = -1
                    fallIdx = -1


            # end for loop

            # 만약 페어가 생성되지 못했다면
            if flag:
                # 마지막 인덱스를 하강점으로 잡는다.
                fallIdx = len(depthItem['list']) - 1
                divide_list.append({
                        'climbIdx': climbIdx,
                        'fallIdx': fallIdx
                    })


            # print(divide_list)
            # add divide list to depth_list
            depthItem['divide_list'] = divide_list
            self.divide_block_list.append(copy.deepcopy(divide_list))

        # end for loop

    def setGraphMember(self):
        pass

    # this method return xAxis and yAxis
    def setGraphMemberByDepth(self, _depth):
        self.yAxis = self.calculus_list[_depth]['list']
        # for yValue in self.calculus_list[_depth]['list']:
        #     self.yAxis.append(yValue['a'])
        self.xAxis = range(0, len(self.calculus_list[_depth]['list']))

        self.currentA = self.calculus_list[_depth]['a']

