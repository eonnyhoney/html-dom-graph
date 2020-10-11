from graph.core.domGraph import DomGraph
from graph.graphManager import GraphRenderer

import pandas as pd
import re
from pprint import pprint

class XpathParser:

    domGraph = None

    # parent key list
    # [{
    #   'xpath_key': ..., 'element': ...,
    #   'child_key_list': [...]
    # }, ...]
    parent_list = []

    data_list = []


    def __init__(self, domGraph):
        self.domGraph = domGraph
        pass

    # parent key를 찾고, 리스트에 추가한다.
    # 찾은 key를 반환한다.
    # xpath_pair는 반드시, full xpath로 된 pair여야 한다.
    def addParentKey(self, xpath_pair):
        if len(xpath_pair) > 2:
            print('(warning) 이 메소드는 2 이상의 인덱스로 참조된 멤버들은 무시합니다. 현재 멤버 수는 ', len(xpath_pair), ' 입니다.')

        length = 0
        if len(xpath_pair[0]) > len(xpath_pair[1]):
            length = len(xpath_pair[0])
        else:
            length = len(xpath_pair[1])

        for i in range(0, length):
            if xpath_pair[0][i] != xpath_pair[1][i]:
                break

        # parsing 내용은, 형제 노드가 있다는 것을 전제로 한다.
        temp = xpath_pair[0][0:i]
        key_str = temp[::-1].split('/', 1)[1][::-1]
        target_child_tag = temp[::-1].split('/', 1)[0][::-1].replace('[', '')

        parent_item = {
            'xpath_key': key_str,
            'selector': self.domGraph.currentSelector.xpath(key_str),
            'target_child_name': target_child_tag
        }

        self.parent_list.append(parent_item)
        # print(self.parent_list)
        parent_index = self.domGraph.getIndexFromTable(key_str)

        if parent_index < 0:
            print('(Error) there is no index match to given xpath : ', key_str)
            return None

        parent_depth = self.domGraph.yAxis[parent_index]
        end_idx = parent_index # initialize

        dom_block_to_end = self.domGraph.yAxis[parent_index+1:]
        for idx, depth in enumerate(dom_block_to_end):
            if parent_depth >= depth:
                end_idx = idx
                break

        # print(parent_index, parent_item['selector'])
        # print('end depth : ', depth, ', end_idx:', end_idx)
        # print(self.domGraph.tag_list[end_idx+1])

        child_depth = parent_depth + 1
        # dom_block is part of yAxis, has depths
        dom_block = dom_block_to_end[0:end_idx]

        # print(len(dom_block), end_idx - parent_index, len(dom_block_to_end))

        unit_index_list = []
        unit_list = []
        start_idx = parent_index + 1 # original
        # start_idx = 0
        # make unit index pair

        # list up all of possible xpath to set column name
        # for implement full join
        parent_key = parent_item['xpath_key'] + '/' + parent_item['target_child_name']
        parent_key = parent_key.replace('[1]', '')
        tag_list = self.domGraph.tag_list
        xpath_column_name_list = []
        # print(parent_key)

        # result data list
        data_list = []

        print(dom_block)
        for idx, depth in enumerate(dom_block):
            dom_graph_index = start_idx + idx

            # make unit pair
            # 동시에, 태그명도 함께 보기.
            if child_depth == depth:
                # actual dom graph's index
                if len(unit_index_list) > 0:
                    unit_index_list[len(unit_index_list) - 1].append(dom_graph_index)
                    # end if
                unit_index_list.append([dom_graph_index])
                unit_list.append(self.domGraph.tag_list[dom_graph_index])

            # collect column name
            current_xpath = tag_list[dom_graph_index]['xpath']
            xpath_key_split = current_xpath.replace(parent_key, '').split('/', 1)
            if len(xpath_key_split) == 2:
                if not xpath_key_split[1] in xpath_column_name_list:
                    # 추후에, None data를 가지는 키 값은 추가하지 않도록 하기.
                    # temp_data = self.domGraph.currentSelector.xpath(current_xpath + '/text()').get()
                    # if temp_data != None:
                    xpath_column_name_list.append(xpath_key_split[1])

                current_key_xpath = xpath_key_split[1]
                # 필요시, 예외처리 추가바람.
                # if len(unit_index_list) > 0:
                current_row_num = len(unit_index_list) - 1
                # find column index
                column_idx = xpath_column_name_list.index(current_key_xpath)
                # data extraction
                current_data = self.domGraph.currentSelector.xpath(current_xpath + '/text()').get()

                if len(data_list) <= current_row_num:
                    data_list.append([])
                if len(data_list[current_row_num]) <= column_idx:
                    _offset = column_idx - len(data_list[current_row_num]) + 1
                    data_list[current_row_num].extend([0] * _offset)
                # try:
                data_list[current_row_num][column_idx] = current_data
                # except:
                #     print('============')
                #     print(data_list[current_row_num])
                #     print(len(data_list), len(data_list[current_row_num]))
                #     print(current_row_num, column_idx, _offset)
        unit_index_list[len(unit_index_list) - 1].append(idx + start_idx)

        self.data_list = data_list

        # print current extracted data
        # pprint(data_list)
        # print(self.domGraph.tag_list[unit_index_list[-1][1]])

        # print(unit_index_list)
        # print(unit_list)

        # xpath 처리하면서, 리스트에 정렬된 키 값 리스트 업
        # 리스트 업 되어있는 리스트를 탐색하여, 컬럼 지정해서 값 넣기
        # 하나의 루프 내에서 정리 가능할 듯.

        # pprint(xpath_column_name)
        # set up data frame
        df = pd.DataFrame(data_list, columns=xpath_column_name_list)
        df.to_csv('./extract_data.csv', encoding='euc-kr')

        # for index_pair in unit_index_list:
        #     for i in range(index_pair[0], index_pair[1]):
        #         pass


        # set child key list
        # self.setChildKey(parent_item)

        return parent_item

    # get data from assumption blocks
    def getDataFromBlocks(self, blocks, minDepth_const):
        # 블록은 [40, 60]으로, 전 구간 모든 요소를 포함한다.

        parent_list = []

        for block_index, block in enumerate(blocks):
            # print(block)
            # find min depth
            min_depth = 99
            min_depth_idx = 0
            for i in range(block[0], block[1]+1):
                depth = self.domGraph.yAxis[i]
                if depth < min_depth:
                    min_depth = depth
                    min_depth_idx = i
            # 현재는 임시로 해당 상수보다 낮은 뎁스의 블럭은
            # 블럭을 버린다.
            # => periodical test로 변경
            if min_depth < minDepth_const:
                continue

            child_depth = min_depth
            child_xpath = self.domGraph.tag_list[min_depth_idx]['xpath']
            parent_xpath = child_xpath[::-1].split('/', 1)[1][::-1]
            child_tagName = child_xpath[::-1].split('/', 1)[0][::-1].split('[')[0]
            parent_index = self.domGraph.getIndexFromTable(parent_xpath)
            parent_depth = child_depth - 1

            for idx, depth in enumerate(self.domGraph.yAxis[parent_index+1:]):
                if parent_depth >= depth:
                    end_idx = idx + parent_index
                    break

            print(parent_index, end_idx)

            dom_block = self.domGraph.yAxis[parent_index:end_idx]
            parent_item = {
                'xpath_key': parent_xpath,
                'selector': self.domGraph.currentSelector.xpath(parent_xpath),
                'target_child_name': child_tagName
            }

            print('block searching..::::::::::::::::::::::')
            unit_index_list = []
            unit_list = []
            start_idx = parent_index + 1  # original
            # start_idx = 0
            # make unit index pair

            # list up all of possible xpath to set column name
            # for implement full join
            parent_key = parent_item['xpath_key'] + '/' + parent_item['target_child_name']
            parent_key = parent_key.replace('[1]', '')
            tag_list = self.domGraph.tag_list
            xpath_column_name_list = []
            # print(parent_key)
            child_depth = min_depth

            # result data list
            data_list = []
            #
            for idx, depth in enumerate(dom_block):
                dom_graph_index = start_idx + idx
                # make unit pair
                # 동시에, 태그명도 함께 보기.
                if child_depth == depth:
                    # actual dom graph's index
                    if len(unit_index_list) > 0:
                        unit_index_list[len(unit_index_list) - 1].append(dom_graph_index)
                        # end if
                    unit_index_list.append([dom_graph_index])
                    unit_list.append(self.domGraph.tag_list[dom_graph_index])

                # collect column name
                current_xpath = tag_list[dom_graph_index]['xpath']
                xpath_key_split = current_xpath.replace(parent_key, '').split('/', 1)
                # 차일드 태그에는 데이터가 없을 것으로 추정하여, 제외했다.
                # 필요시, 차일드 태그의 데이터도 수집하는 기능을 추가해야한다.
                if len(xpath_key_split) == 2:
                    if not xpath_key_split[1] in xpath_column_name_list:
                        # 추후에, None data를 가지는 키 값은 추가하지 않도록 하기.
                        # temp_data = self.domGraph.currentSelector.xpath(current_xpath + '/text()').get()
                        # if temp_data != None:
                        xpath_column_name_list.append(xpath_key_split[1])

                    current_key_xpath = xpath_key_split[1]
                    # 필요시, 예외처리 추가바람.
                    # if len(unit_index_list) > 0:
                    current_row_num = len(unit_index_list) - 1
                    # find column index
                    column_idx = xpath_column_name_list.index(current_key_xpath)
                    # data extraction
                    current_data = self.domGraph.currentSelector.xpath(current_xpath + '/text()').get()

                    # print(len(unit_index_list), current_key_xpath, len(data_list), current_row_num)

                    if len(data_list) <= current_row_num:
                        data_list.append([])
                    # try:
                    if len(data_list[current_row_num]) <= column_idx:
                        _offset = column_idx - len(data_list[current_row_num]) + 1
                        data_list[current_row_num].extend([0] * _offset)
                    # except:
                    #     print(current_row_num, len(data_list), current_key_xpath)
                    #     print('data : ', data_list)
                    #     print(unit_index_list)
                    # try:
                    data_list[current_row_num][column_idx] = current_data
                    # except:
                    #     print('============')
                    #     print(data_list[current_row_num])
                    #     print(len(data_list), len(data_list[current_row_num]))
                    #     print(current_row_num, column_idx, _offset)
            if len(unit_index_list) > 0:
                unit_index_list[len(unit_index_list) - 1].append(idx + start_idx)
            self.data_list = data_list

            # print current extracted data
            # pprint(data_list)
            # print(self.domGraph.tag_list[unit_index_list[-1][1]])

            # print(unit_index_list)
            # print(unit_list)

            # xpath 처리하면서, 리스트에 정렬된 키 값 리스트 업
            # 리스트 업 되어있는 리스트를 탐색하여, 컬럼 지정해서 값 넣기
            # 하나의 루프 내에서 정리 가능할 듯.

            # pprint(xpath_column_name)
            # set up data frame
            df = pd.DataFrame(data_list, columns=xpath_column_name_list)
            df.to_csv('./' + str(block_index) + '_extract_data.csv', encoding='utf-8')

            # for index_pair in unit_index_list:
            #     for i in range(index_pair[0], index_pair[1]):
            #         pass

            # set child key list
            # self.setChildKey(parent_item)

        pass


    # current not used
    def setChildKey(self, parent_item):

        children = parent_item['selector'].xpath('child::*')
        children_list = []
        # count target tag sibling
        for child in children:
            child_tag_name = child.xpath('name()').get()
            if child_tag_name == parent_item['target_child_name']:
                children_list.append(child)

        # children_list에 타겟 태그 차일드만 있기 때문에
        # 이제 children_list의 모든 자식 노드를 탐색한다.

        for child in children_list:
            # xpath를 key로 사용하기 때문에, full xpath를 저장하지 않는다.
            key_list = self.getChild(child)

        pass

    def getChild(self, _child):
        # children = _child.xpah('child::*')
        # for child in children:

        print('-----------')
        sub_html_text = ''
        for txt in _child.getall():
            sub_html_text += txt
        sub_dom = DomGraph(sub_html_text)
        pprint(sub_dom.tag_list)

        # renderer = GraphRenderer()
        # renderer.showPlot(sub_dom)

        pass

    # deprecated method
    def depricatedXpath(self, xpath):

        # parse xpath
        extract_xpath = '//*/' + xpath.split('/', 3)[-1]
        parse_path_list = extract_xpath.split('/')

        # has sibling list, insert index
        has_sibling_list = []
        regex = re.compile(r'[\d]')
        for idx, tag in enumerate(parse_path_list):
            match_obj = regex.search(tag)
            if not match_obj:
                continue
            has_sibling_list.append(idx)

        print(has_sibling_list)
        print(parse_path_list)


        # get sibling with index from graph

        # sibling_list = []
        # for start_idx in has_sibling_list:
        #     path = '//*/'
        #
        #     for i in range(start_idx, len(parse_path_list)):
        #         path += parse_path_list[i] + '/'
        #     sibling_list.append(path)
        #
        # print(sibling_list)



        # find elem
        selector = self.domGraph.currentSelector

        current_elem = selector.xpath(extract_xpath)
        print(current_elem)

        return None


    def getDataList(self):
        return self.data_list