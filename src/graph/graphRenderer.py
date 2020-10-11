import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import  make_interp_spline, BSpline

import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import pandas as pd

from plotly.graph_objects import layout

from pprint import pprint

class GraphRenderer():

    graph_type = 0

    yMult = 1

    def __init__(self):
        pass

    def show(self):
        pass

    # init graph by each type
    def setGraphByType(self, type):

        if self.graph_type == self.DOM_GRAPH:
            self.setDomGraphMember()

    def setDomGraphMember(self):
        pass

    # compressed calculus 내역을 세팅하고 fig를 반환하는 함수
    def setCompressedCalculus(self, graph, depth):
        graph.setGraphMemberByDepth(depth)

        xAxis = np.array(graph.xAxis)
        yAxis = np.array(graph.yAxis)

        # local graph in calculus list
        current_graph = graph.calculus_list[depth]

        temp_line = [graph.currentA] * len(graph.xAxis)
        aLine = np.array(temp_line)

        # Create traces
        fig = go.Figure()
        # print(fig['layout'])
        # fig['layout'] = {
        #     'hovermode': 'closest',
        #     'xaxis': {'showspikes': True}
        # }
        fig.add_trace(go.Scatter(x=xAxis, y=yAxis,
                                 mode='markers',
                                 name='분기별 기울기',
                                 fillcolor='#0d47a1'))
        # 평균 (기준) 기울기 값
        fig.add_trace(go.Scatter(x=xAxis, y=aLine,
                                 mode='lines',
                                 name='평균(기준) 기울기', fillcolor='#ef5350'))

        verticalLineHeight = max(current_graph['list'])
        for item in current_graph['divide_list']:
            climb_x = item['climbIdx']
            fall_x = item['fallIdx']

            fig.add_shape(
                # Line Vertical
                dict(
                    type="line",
                    x0=climb_x,
                    y0=0,
                    x1=climb_x,
                    y1=verticalLineHeight,
                    line=dict(
                        color='#8bc34a',
                        width=1
                    )
                ), name='divide-line')

            fig.add_shape(
                # Line Vertical
                dict(
                    type="line",
                    x0=fall_x,
                    y0=0,
                    x1=fall_x,
                    y1=verticalLineHeight,
                    line=dict(
                        color='#8bc34a',
                        width=1
                    )
                ), name='divide-line')

        title = 'compressed calculus :: ' + str(depth) + ' level'
        fig.update_layout(
            title=title,
            xaxis_title="DOM graph index",
            yaxis_title="a (slope)",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#263238"
            )
        )

        return fig

    # compressedCalculus를 그리기 위한 함수
    def showCompressedCalculus(self, graph, depth):
        if graph.current_type != graph.COMPRESSED_CALCULUS_GRAPH:
            print('(warning) this graph is not proper type. this method work for compressedCalculus graph...')
            return

        fig = self.setCompressedCalculus(graph, depth)
        fig.show()


    def showDCgraph(self, domGraph, ccGraph, depth):
        if ccGraph.current_type != ccGraph.COMPRESSED_CALCULUS_GRAPH:
            print('(warning) this graph is not proper type. this method work for compressedCalculus graph...')
            return

        ccGraph.setGraphMemberByDepth(depth)

        cc_xAxis = np.array(ccGraph.xAxis) * ccGraph.divideOffset
        cc_yAxis = np.array(ccGraph.yAxis) * self.yMult

        # local graph in calculus list
        current_graph = ccGraph.calculus_list[depth]

        # hard coded
        additionalLine = 2
        lineLength = len(ccGraph.xAxis) + additionalLine
        temp_line = [ccGraph.currentA] * (lineLength)
        aLineY = np.array(temp_line) * self.yMult
        aLineX = np.array(range(0, lineLength)) * ccGraph.divideOffset

        # Create traces
        fig = go.Figure()
        # print(fig['layout'])
        # fig['layout'] = {
        #     'hovermode': 'closest',
        #     'xaxis': {'showspikes': True}
        # }
        fig.add_trace(go.Scatter(x=cc_xAxis, y=cc_yAxis,
                                 mode='markers',
                                 name='분기별 기울기',
                                 fillcolor='#0d47a1'))

        # fig.add_histogram(x=cc_xAxis, y=cc_yAxis,
        #                   name='divide-alpha',
        #                   opacity=0.5)

        fig.add_bar(x=cc_xAxis, y=cc_yAxis,
                          name='divide-alpha', width=ccGraph.divideOffset, offset=(ccGraph.divideOffset/128))

        # 평균 (기준) 기울기 값
        fig.add_trace(go.Scatter(x=aLineX, y=aLineY,
                                 mode='lines',
                                 name='평균(기준) 기울기', fillcolor='#ef5350'))

        # match to DOM graph

        # set vertical divider line
        vertical_color = '#00bfa5'
        vertical_width = 1
        verticalLineHeight = domGraph.max_depth
        for item in current_graph['divide_list']:
            climb_x = item['climbIdx'] * ccGraph.divideOffset
            fall_x = item['fallIdx'] * ccGraph.divideOffset

            # climb vertical line
            fig.add_shape(
                dict(
                    type="rect",
                    x0=climb_x,
                    y0=0,
                    x1=fall_x,
                    y1=verticalLineHeight,
                    line=dict(
                        color=vertical_color,
                        width=vertical_width
                    ),
                    fillcolor="#bdbdbd",
                    opacity=0.5,
                ), name='divide-start-line')

            # # fall vertical line
            # fig.add_shape(
            #     dict(
            #         type="line",
            #         x0=fall_x,
            #         y0=0,
            #         x1=fall_x,
            #         y1=verticalLineHeight,
            #         line=dict(
            #             color=vertical_color,
            #             width=vertical_width
            #         )
            #     ), name='divide-end-line')

        title = 'DOM Calculus :: depth ' + str(depth) + ' level, divide offset=' + str(ccGraph.divideOffset)
        fig.update_layout(
            title=title,
            xaxis_title="DOM graph index",
            yaxis_title="depth (DOM graph), alpha(분기별 기울기, multiplied)",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#263238"
            )
        )

        dom_xAxis = np.array(domGraph.xAxis)
        dom_yAxis = np.array(domGraph.yAxis)
        fig.add_trace(go.Scatter(x=dom_xAxis, y=dom_yAxis,
                                 mode='lines+markers',
                                 name='DOM graph value',
                                 fillcolor='#ffb74d'))


        fig.show()


    # 꺽은선 그래프
    def showScatter(self, graph):

        np.random.seed(1)

        N = 100
        random_x = np.linspace(0, 1, N)
        random_y0 = np.random.randn(N) + 5
        random_y1 = np.random.randn(N)
        random_y2 = np.random.randn(N) - 5

        xAxis = np.array(graph.xAxis)

        # Create traces
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=xAxis, y=random_y0,
                                 mode='lines',
                                 name='lines'))
        # fig.add_trace(go.Scatter(x=random_x, y=random_y1,
        #                          mode='lines+markers',
        #                          name='lines+markers'))
        # fig.add_trace(go.Scatter(x=random_x, y=random_y2,
        #                          mode='markers', name='markers'))

        fig.show()


        # # if x, y are not initialized. raise error
        # if len(graph.xAxis) == 0:
        #     print('error::there is no value in the xAxis...')
        #     raise ValueError
        #
        # xAxis = np.array(graph.xAxis)
        # yAxis = np.array(graph.yAxis)
        #
        # plt.scatter(xAxis, yAxis)
        # plt.show()

        # 꺽은선 그래프

    def showPlot(self, graph):
        # if x, y are not initialized. raise error
        if len(graph.xAxis) == 0:
            print('error::there is no value in the xAxis...')
            raise ValueError

        xAxis = np.array(graph.xAxis)
        yAxis = np.array(graph.yAxis)

        plt.plot(xAxis, yAxis)
        plt.show()

    # 곡선 그래프
    def showSplineGraph(self):
        return None

        # if x, y are not initialized. raise error
        if len(self.xAxis) == 0:
            print('error::there is no value in the xAxis...')
            raise ValueError

        # 300 represents number of points to make between T.min and T.max
        xnew = np.linspace(self.xAxis.min(), self.xAxis.max(), 300)

        spl = make_interp_spline(self.xAxis, self.yAxis, k=3)  # type: BSpline
        power_smooth = spl(xnew)

        plt.plot(xnew, power_smooth)
        plt.show()

    # show graph of depthDensity
    def showDensityGraph(self):
        if len(self.depthDensity_list) == 0:
            self.initDensityList()

        if len(self.desc_depthDensity_list) == 0:
            self.sortDensityGraphByDesc()

        depth_list = []
        hits_list = []
        for item in self.desc_depthDensity_list:
            depth_list.append(item['depth'])
            hits_list.append(item['hits'])

        yAxis = np.array(hits_list)
        xAxis = np.array(depth_list)

        plt.plot(xAxis, yAxis)
        plt.show()