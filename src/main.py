from graph.graphManager import GraphManager
from graph.densityManager import DensityManager
from graph.extractManager import ExtractManager
from graph.util.xpathParser import XpathParser
from graph.periodicityManager import PeriodicityManager

from pprint import pprint

import pandas as pd

# 코드 작업 중 계속해서, recursion error가 발생하여, setter, getter를 사용하지 않고 있는 중.

if __name__ == '__main__':
    url = 'http://browse.auction.co.kr/search?keyword=discovery&itemno=&nickname=&frm=hometab&dom=auction&isSuggestion=No&retry=&Fwk=discovery&acode=SRP_SU_0100&arraycategory=&encKeyword=discovery'
    c = 60

    graphManager = GraphManager(url, c) # 분석할 사이트 url, 구간 길이 상수 c

    domGraph = graphManager.domGraph
    depthHistogram = graphManager.depthHistogram
    # depthHistogram.removeItem(6) # <- 아직 구현되지 않은 메소드 (분석하지 않는 depth의 누적 카운트)
    depthHitCumulate = graphManager.depthHitCumulate
    compressedCalculus = graphManager.compressedCalculus

    # print(graphManager.htmlText)

    graphManager.setMinDepth(4)

    graphManager.setYMult(20) # _a, 구간별 bar chart 값 증폭
    compressedCalculus.multAvgSlopeA(0.5) # _a값 modify

    # graphManager.showDCgraph() # 모든 depth의 DC graph 한번에 출력
    graphManager.showSingleDCgraph(11) # depth 지정하여 DC graph 출력
    #
    # # graphManager.showPlot(domGraph) # domgraph 출력
    #
    # # search block to extract data
    # # graphManager.searchBlock(3)

    densityManager = DensityManager()
    densityManager.densityTest(len(domGraph.tag_list), compressedCalculus.divide_block_list, c, 6) # 밀도카운트
    absoluteBlockList = densityManager.getAbsolutBlockList() # 일정 밀도 이상인 idx 구간

    periodicityManager = PeriodicityManager(domGraph)
    periodicityManager.periodicityTest(absoluteBlockList)


    # print(absoluteBlockList)
    print()

    # for item in absoluteBlockList:
    #     min = 99
    #     for i in range(item[0],item[1]):
    #         depth = domGraph.depth_list[i]
    #         if depth <= min:
    #             min = depth
    #     print(item, '구간의 min(depth) = ', min)

    # daum news
    # input_pair = ['/html/body/div[2]/div[2]/div/div[1]/div[2]/ul/li[3]/div/div/span',
    #               '/html/body/div[2]/div[2]/div/div[1]/div[2]/ul/li[5]/div/div/span']

    # dc gallery
    input_pair = ['/html/body/div[2]/div[2]/main/section[1]/article[2]/div[2]/table/tbody/tr[1]/td[2]/a/b',
                  '/html/body/div[2]/div[2]/main/section[1]/article[2]/div[2]/table/tbody/tr[6]/td[2]/a']
    # dc vote
    # input_pair = ['/html/body/div[1]/div[3]/div[2]/ul/li[2]/div/a/p',
    #               '/html/body/div[1]/div[3]/div[2]/ul/li[6]/div/a/p']

    # extractManager = ExtractManager(graphManager)
    # extractManager.parseXpath(input_pair)

    xpathParser = XpathParser(domGraph)
    xpathParser.addParentKey(input_pair)

    # xpathParser.getDataFromBlocks(absoluteBlockList, 4)
    # dataList = xpathParser.getDataList()

    # graphManager.showPlot(domGraph)

    # df = pd.DataFrame(dataList)
    # df = df.T
    # df.to_csv('./dcgall.csv', index=False, encoding='euc-kr')


    # # csv test with jw

    # # html_list = []
    # # for item in domGraph.tag_list:
    # #     curXpath = item['xpath']
    # # test_xpath = '//*/div/a/div[2]/p'
    # #              # '//*[@id="thisClick_2852872206"]/div/a/div[2]/p'
    # #
    # # '//*[@id="search"]/div[1]/div[2]/div/span[3]/div[2]/div[2]/div/span/div/div/div[2]/h2/a/span'
    # # '/html/body/div[2]/div[5]/div[1]/div[10]/div[1]/div[2]/ul/li[2]/div/a/div[2]/p'
    # # html = domGraph.currentSelector.xpath(test_xpath + '/text()').extract()
    # # print(html)
    #
    # # html_list = []
    # # for item in domGraph.tag_list:
    # #     curXpath = item['xpath']
    # #     temp_list = domGraph.currentSelector.xpath(curXpath + '/text()').getall()
    # #
    # #     # flag = False
    # #     # for jtem in temp_list:
    # #     #     if len(jtem) == 0 or jtem is None:
    # #     #         flag = True
    # #     #         break
    # #     # if not flag:
    # #     #     html_list.append(temp_list)
    # #
    # #     if len(temp_list) != 0:
    # #         html_list.append(temp_list)
    # #
    # # df = pd.DataFrame(html_list)
    # # # df = df.T
    # #
    # # df.to_csv('./html_csv.csv', index=False, encoding='euc-kr')

