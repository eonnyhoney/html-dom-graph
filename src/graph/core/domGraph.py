from graph.core.graph import Graph
from pprint import pprint
from parsel import Selector

### 상언

# html dom-tree를 이용하여, 그래프를 생성하는 클래스
# getChild는 생성자를 통해 호출되며, 루트 노드인 html 태그부터 탐색을 시작한다.
# getChild는 각 자식 노드를 탐색하며, 깊이 우선 순회를 한다.
# 순회 순서에 따라 각 태그와 태그의 깊이(depth)를 리스트에 추가한다.
# 해당 리스트를 통해 그래프를 그린다.
# 그래프의 x축은 리스트의 index가 되고, y축은 depth가 된다.
class DomGraph(Graph):
    # store depth of each elements
    tag_list = []
    # depth list of DOM
    depth_list = []

    # constant, every depth must start by depth=zer0
    INITIAL_DEPTH = 0

    # maximum depth in the tag_list
    max_depth = 0

    # temporary stack for count tags in each of depth
    # 각 부모에 따른 리스트 수를 카운팅
    # count = depthStack[depth][tagName]
    # |==> count = depthStack[depth][xpath-parent][tagName]
    # |==> count = depthStack[xpath-parent][tagName]
    depthStack = []
    # temporary index count
    indexCount = 0

    # store current selector to search dom-tree
    # this set location to html tag
    currentSelector = None

    # search must start with html tag
    HTML_TAG = '/html'

    # xpath delimiter
    DELIMITER = '/'

    # init tag_list
    # DFS start with 'html' tag
    def __init__(self, htmlText):
        # set graph type
        self.current_type = self.DOM_GRAPH
        # html tag로 Selector(탐색 객체)를 위치한다.
        self.currentSelector = Selector(htmlText)
        parent = self.currentSelector.xpath(self.HTML_TAG)

        # parse Dom tree
        self.tag_list = self.getChild(parent, self.HTML_TAG, self.INITIAL_DEPTH)
        # set graph members
        self.setGraphMember()

        # print("set graph's x and y members...")
        # print('total x count is ', len(self.xAxis))

    # get tag data from selector object
    def getTagData(self, tagItem, depth, xpath):
        # 각 태그 객체에서 정보를 얻는다.
        tagName = tagItem.xpath('name()').get()
        # 같은 계층의 형제 중에서 몇번째 태그 아이템인지
        count = self.getSiblingTagIndexInDepthStack(depth, xpath, tagName)

        indexChar = ''
        if count > 1:
            indexChar = '[' + str(count) + ']'

        return {
            'tagName': tagName,
            'depth': depth,
            'xpath': xpath + '/' + tagName + indexChar
        }

    # current not used
    # 부모에 무관하게, depth가 같은 태그를 카운트하기 때문에 full xpath로 접근할 때 이용할 수 없다.
    # 각 뎁스에 따른 카운트를 증가시키면서, 현재 태그가 몇번째 카운트인지 알려준다.
    # def getTagIndexInDepthStack(self, depth, tagName):
    #     depthIdx = depth - 1
    #     if len(self.depthStack) < depth:
    #         self.depthStack.append({tagName: 1})
    #     else:
    #         if not tagName in self.depthStack[depthIdx].keys():
    #             self.depthStack[depthIdx][tagName] = 1
    #         else:
    #             # print(depthIdx, tagName, ', ', self.depthStack[depthIdx][tagName])
    #             self.depthStack[depthIdx][tagName] += 1
    #     return self.depthStack[depthIdx][tagName]

    # 동일한 뎁스에 동일한 부모를 가진 태그의 카운트만 증가
    # 이를 xpath 히스토리를 이용한다.
    # count = depthStack[depth][xpath-parent][tagName]
    def getSiblingTagIndexInDepthStack(self, depth, xpathHistory, tagName):
        depthIdx = depth - 1

        # 해당 depth가 존재하지 않으면, depth를 추가한다.
        if len(self.depthStack) < depth:
            self.depthStack.append({xpathHistory: {tagName: 1}})
        # depth가 존재하는  경우.
        else:
            # no xpathHistory or no tagName
            if not xpathHistory in self.depthStack[depthIdx].keys():
                self.depthStack[depthIdx][xpathHistory] = {tagName: 1}
            elif not tagName in self.depthStack[depthIdx][xpathHistory].keys():
                self.depthStack[depthIdx][xpathHistory][tagName] = 1
            else:
                self.depthStack[depthIdx][xpathHistory][tagName] += 1
        # return current target count
        return self.depthStack[depthIdx][xpathHistory][tagName]

    # recursive method
    def getChild(self, parent, xpath, depth):
        depth += 1

        if self.max_depth < depth:
            self.max_depth = depth

        children = parent.xpath('child::*')
        # has children
        tag_list = []
        for child in children:
            # print(depth, 'mid node', len(child.xpath('child::*')))
            if len(child.xpath('child::*')) > 0:
                tagData = self.getTagData(child, depth, xpath)
                tag_list.append(tagData)

                # recursive to find children
                currentXpath = tagData['xpath']
                grandChildren = self.getChild(child, currentXpath, depth)
                # return value is always object list
                for grandChild in grandChildren:
                    tag_list.append(grandChild)
            # catch leaf node
            else:
                tag_list.append(self.getTagData(child, depth, xpath))

        return tag_list

    # 그래프를 그리기 위해, x and y 멤버 초기화
    def setGraphMember(self):
        depth_list = []
        index_list = []
        for idx, depth in enumerate(self.tag_list):
            depth_list.append(depth['depth'])
            index_list.append(idx)

        self.depth_list = depth_list

        self.yAxis = depth_list
        self.xAxis = index_list

    # (minor issue) '/html' -> return -1
    # return index from tag graph
    # using string compare
    # when target can not found in table, return -1
    # @_targetXpath, which one we want to find from dom graph
    def getIndexFromTable(self, _targetXpath):
        # *** at the tag table, do not use [1], only [1]
        # eg) /html/div[1]/span[2]/p --> /html/div/span[2]/p
        # so we replace it.
        targetXpath = _targetXpath.replace('[1]', '')

        for idx, tagItem in enumerate(self.tag_list):
            if targetXpath == tagItem['xpath']:
                return idx
        # can not find target
        return -1

    # search same like getChild and return dest-index
    # works recursive
    # this method not working now...
    # def getIndex(self, fulXpath):
    #
    #     return None
    #     # init detph stack
    #     if len(self.depthStack) > 0:
    #         self.depthStack = []
    #     if self.indexCount != 0:
    #         self.indexCount = 0
    #
    #     # search must start with 'html' tag
    #     # compare every xpath
    #     return self.getXpathChild(destPath=fulXpath, curXpath=self.HTML_TAG, parent=self.currentSelector)
    #
    # # search dest full xpath with counting index number
    # # 목표 full xpath를 탐색하며, 각 단계의 tag명을 비교하면서 트리를 탐색한다.
    # # 마찬가지로 깊이 우선 순회이다.
    # #
    # # 대상이 되는 full xpath를 찾았을 경우, 해당 인덱스를 반환한다.
    # # 만약 대상을 찾지 못한 경우, -1을 반환한다.
    # # coding...
    # def getXpathChild(self, destPath, curXpath, parent):
    #     self.indexCount += 1
    #
    #     # not match to xpath
    #     # keep searching.
    #     if destPath != curXpath:
    #         index = -1
    #         print('flag -1')
    #         # 매치가 되지 않는다면, 계속 찾는다.
    #         children = parent.xpath('child::*')
    #         for child in children:
    #             print(child.xpath('name()').get(), child)
    #             xpath = curXpath + self.DELIMITER + child.xpath('name()').get()
    #             index = self.getXpathChild(destPath=destPath, curXpath=xpath, parent=child)
    #             print('index ', index)
    #             if index >= 0:
    #                 break
    #
    #         print('flag -2')
    #         if index >= 0:
    #             print('flag 0')
    #             return self.indexCount
    #     # if this element is last node of dom-tree
    #     # return -1, means can not find dest target.
    #     elif len(self.tag_list) >= self.indexCount:
    #         print('flag 1')
    #         return -1
    #
    #     # match to xpath
    #     # stop search and return count
    #     else:
    #         print('flag 2')
    #         return self.indexCount







