from graph.core.domGraph import DomGraph

class PeriodicityManager():

    domGraph = None

    def __init__(self, domGraph):
        self.domGraph = domGraph
        pass

    def periodicityTest(self, absolute_block_list):
        for block in absolute_block_list:
            start_point = block[0]
            end_point = block[1]
            block_length = end_point - start_point

            index_list_by_each_depth = {}
            for i in range(start_point, end_point+1):
                depth = self.domGraph.depth_list[i]
                if depth not in index_list_by_each_depth:
                    index_list_by_each_depth[depth] = [i]
                else:
                    index_list_by_each_depth[depth].append(i)

            for depth, index_list in index_list_by_each_depth.items():
                n = len(index_list)
                if n > 2:
                    first = index_list[0]
                    last = index_list[-1]
                    mean = (int(last) - int(first) + 1) / (n - 1)

                    interval_list = []
                    for x in range(len(index_list)):
                        if x == 0:
                            continue
                        else:
                            interval_list.append(index_list[x] - index_list[x-1])

                    deviation_list = []
                    for interval in interval_list:
                        deviation = ((interval - mean)**2 / n)**(1/2)
                        deviation_list.append(deviation)
                    print(deviation_list)
