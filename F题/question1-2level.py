import xlrd
import xlwt
import math
import time
# import necessary module
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
# 绘制结果图
def draw_picture(x,y,z):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    # set figure information
    ax.set_title("========result=========")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    # draw the figure, the color is r = read
    ax.plot(x,y,z, c='r')
    plt.show()
#  设置权重
def weight(x,y,a = 1,b = 1):
    return a*x+b*y
def main():
    path_1 = './static_file/dataset2.xlsx'
    exl_1 = xlrd.open_workbook(path_1)
    table_1 = exl_1.sheet_by_name('Sheet1')
    num_rows_1 = table_1.nrows
    num_cols_1 = table_1.ncols
    file_1 = xlwt.Workbook(encoding = 'utf-8')
    #print(num_rows_1)#统计的总行数
    # 1.xlsx
    x = [0.0]
    y = [0.0]
    z = [0.0]
    coordinates = []
    nodes = []  # 绘散点图使用
    for i in range(num_rows_1):
        node = []
        coordinate = list(table_1.row_values(i))
        node.append(table_1.row_values(i)[0])
        node.append(table_1.row_values(i)[1])
        node.append(table_1.row_values(i)[2])
        coordinate.append(0)
        coordinate.append(0)
        coordinates.append(coordinate)
        nodes.append(node)
    passed_coordinates = [coordinates[0]] # 记录走过的正确的点
    # print(coordinates)
    # print(nodes)
    j = 0
    min_value = math.inf
    mins = []
    min_i = 0
    min_index = []
    meet_coordinate = [] # 满足在球内部的点
    B = [100000,74860.5488999781,5499.61109489643]
    r = 0
    flag = 0
    temp_toB = 0
    min_toB = 0
    pre_toNow_dist = 0
    count_distance = 0
    start_time = time.clock()
    print("{0}【----当前从第{1}号点起飞----】{2}".format(0, 0, passed_coordinates[0]))
    while True:
        min_value = math.inf
        if j == 0:  # 如果是第一个数
            r = 20 / 0.001  # 球的半径条件
        elif j % 2 == 1:  # 奇数为垂直
            r = 20 / 0.001 if (20 / 0.001) < (25 - passed_coordinates[j][4] ) / 0.001 else (25 - passed_coordinates[j][
                4]) / 0.001
            flag = 1
        elif j % 2 == 0:  # 偶数为水平
            r = 15 / 0.001 if (15 / 0.001) < (25 - passed_coordinates[j][5] ) / 0.001 else (25 - passed_coordinates[j][
                5]) / 0.001
            flag = 0
        for i in range(1,len(coordinates)):
            # 计算当前点跟上一个走过的点之间的距离
            pre_dist = math.sqrt((coordinates[i][0] - passed_coordinates[j][0])**2 + (coordinates[i][1] - passed_coordinates[j][1])**2 + (coordinates[i][2] - passed_coordinates[j][2])**2)
            # 计算可选点到B点的距离
            if pre_dist <= r  and coordinates[i][3] == flag and coordinates[i] not in passed_coordinates: # 判断是否在球里面
                meet_coordinate.append(coordinates[i]) #找到在球内部的点就把它加进去
                # 再去判断选中的点是否是距离B点和之前路径和最小的点
                temp_toB = math.sqrt((B[0]- coordinates[i][0])**2 + (B[1] - coordinates[i][1])**2 + (B[2] - coordinates[i][2])**2)
                if min_value > weight(temp_toB,pre_dist):
                    pre_toNow_dist = pre_dist
                    min_value = weight(temp_toB,pre_dist)
                    min_i = i # 下表
                    min_toB = temp_toB
            else:
                pass
        min_index.append(min_i)
        mins.append(pre_toNow_dist)
        count_distance += pre_toNow_dist
        j += 1
        passed_coordinates.append (coordinates[min_i]) # 经过的点多一
        if j % 2 == 1:
            passed_coordinates[j][4] = pre_toNow_dist * 0.001
        elif j % 2 == 0:
            passed_coordinates[j][5] = pre_toNow_dist * 0.001
        print("{0}【----当前飞过第{1}号矫正点----】{2}".format(j, min_i, passed_coordinates[j]))
        # dist_b = math.sqrt((B[0] - passed_coordinates[j][0]) ** 2 + (B[1] - passed_coordinates[j][1]) ** 2 + (B[2] - passed_coordinates[j][2]) ** 2)
        if pre_toNow_dist * 0.001  + min_toB * 0.001< 30:
            break
    end_time = time.clock()
    print("{0}【----当前已到达第{1}号点----】{2}".format(j+1, 326, [100000,74860.5488999781,5499.61109489643,'B点',min_toB * 0.001,pre_toNow_dist * 0.001  + min_toB * 0.001]))
    print('经过：',min_index)
    print('路径长度：',sum(mins) + min_toB)
    print('用时：%s Seconds' % (end_time - start_time))
    # print(passed_coordinates)
    draw_nodes_1 = []
    draw_nodes_0 = []
    draw_nodes = [[0, 50000.0, 5000.0]]
    for i in range(len(passed_coordinates)):
        draw_node_1 = []
        draw_node_0 = []
        x.append(passed_coordinates[i][0])
        y.append(passed_coordinates[i][1])
        z.append(passed_coordinates[i][2])
        if passed_coordinates[i][3] == 1:
            draw_node_1.append(passed_coordinates[i][0])
            draw_node_1.append(passed_coordinates[i][1])
            draw_node_1.append(passed_coordinates[i][2])
            draw_nodes_1.append(draw_node_1)
            draw_nodes.append(draw_node_1)
        elif passed_coordinates[i][3] == 0:
            draw_node_0.append(passed_coordinates[i][0])
            draw_node_0.append(passed_coordinates[i][1])
            draw_node_0.append(passed_coordinates[i][2])
            draw_nodes_0.append(draw_node_0)
            draw_nodes.append(draw_node_0)
    draw_nodes.append(B)
    print('经过的所有的点', len(draw_nodes), draw_nodes)
    # draw_nodes.append([100000,59652.3433795158,5022.0011644816404])
    print('经过的垂直校正点：', len(draw_nodes_1), draw_nodes_1)
    print('经过的水平校正点：', len(draw_nodes_0), draw_nodes_0)
    nodes_1 = []  # 其它垂直校正点
    nodes_0 = []  # 其它水平校正点
    for i in range(num_rows_1):
        node_1 = []
        node_0 = []
        if i not in min_index and i != 0 and i != num_rows_1 - 1:
            if table_1.row_values(i)[3] == 1:
                node_1.append(table_1.row_values(i)[0])
                node_1.append(table_1.row_values(i)[1])
                node_1.append(table_1.row_values(i)[2])
                nodes_1.append(node_1)
            elif table_1.row_values(i)[3] == 0:
                node_0.append(table_1.row_values(i)[0])
                node_0.append(table_1.row_values(i)[1])
                node_0.append(table_1.row_values(i)[2])
                nodes_0.append(node_0)
    print('未经过垂直校正点：', nodes_1)
    print('未经过水平校正点：', nodes_0)
    # draw_picture(x,y,z)
if __name__ == '__main__':
    main()