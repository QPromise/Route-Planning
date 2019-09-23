import xlrd
import xlwt
import math
import time
# import necessary module
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
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
# 求解两个圆的交点坐标
def intersection(p1, r1, p2, r2):
    x = p1[0]
    y = p1[1]
    R = r1
    a = p2[0]
    b = p2[1]
    S = r2
    d = math.sqrt((abs(a - x)) ** 2 + (abs(b - y)) ** 2)
    if d > (R + S) or d < (abs(R - S)):
        print("Two circles have no intersection")
        return [None]
    elif d == 0 and R == S:
        print("Two circles have same center!")
        return [None]
    else:
        A = (R ** 2 - S ** 2 + d ** 2) / (2 * d)
        h = math.sqrt(R ** 2 - A ** 2)
        x2 = x + A * (a - x) / d

        y2 = y + A * (b - y) / d
        x3 = round(x2 - h * (b - y) / d, 10)
        y3 = round(y2 + h * (a - x) / d, 10)
        x4 = round(x2 + h * (b - y) / d, 10)
        y4 = round(y2 - h * (a - x) / d, 10)
        # print(x3, y3)
        # print(x4, y4)
        c1 = [x3, y3]
        c2 = [x4, y4]
        return c1, c2

def distance(pre,rear,candidate): # 前俩是之前选过的点，最后是待选的点
    right_candidate = 1
    # 求直飞的夹角
    alpha = math.atan(abs((rear[1] - pre[1])/(rear[0] - pre[0])))
    # 求圆心坐标
    o = [rear[0]+((candidate[0] - rear[0]) / abs(candidate[0] - rear[0])) * 200 *
         math.sin(alpha),rear[1]+((candidate[1] - rear[1]) / abs(candidate[1] - rear[1])) *200 * math.cos(alpha)]
    # 圆心到到下一个待选点candidate的直线距离
    o_candidate_length = math.sqrt((candidate[0] - o[0]) ** 2 + (candidate[1] - o[1]) ** 2)
    # 以新的圆弧上的点到下一个待选点candidate的直线距离
    stright_length = math.sqrt(abs(o_candidate_length**2 - 200**2))
    # 求新的圆弧上的点坐标
    new_points = intersection(o,200,candidate,stright_length)
    new_point = []
    # 如果有两个交点
    if len(new_points)  == 2:
        if candidate[1] > rear[1]:
            new_point = new_points[0] if new_points[0][1] < new_points[1][1] else new_points[1]
        elif candidate[1] < rear[1]:
            new_point = new_points[1] if new_points[0][1] < new_points[1][1] else new_points[0]
        pass
    # 如果有一个或者没有，相切
    else:
        right_candidate = 0
    # print(new_points)
    # print(new_point)
    # 相交点到上一个走过的点的直线距离
    level_length = math.sqrt((new_point[0] - rear[0]) ** 2 + (new_point[1] - rear[1]) ** 2)
    theta =  math.acos((2 * 200 ** 2 - level_length) / (2 * 200 **2))
    min_length = math.sqrt((theta * 200  + stright_length) ** 2 + (rear[2] - candidate[2]) ** 2)
    # = math.sqrt(h ** 2 + level_length ** 2) + math.sqrt(h ** 2 + stright_length ** 2)
    # print(stright_length)
    # print(alpha)
    # print(o)
    return min_length,right_candidate

def weight(x,y,a = 1,b = 1):
    return a*x+b*y

def main():
    path_1 = './static_file/dataset1.xlsx'
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

    coordinates = [] # 表格中所有的点
    #nodes = []  # 绘散点图使用
    for i in range(num_rows_1):
        #node = []
        coordinate = list(table_1.row_values(i))
        #node.append(table_1.row_values(i)[0])
        #node.append(table_1.row_values(i)[1])
        #node.append(table_1.row_values(i)[2])
        coordinate.append(0)
        coordinate.append(0)
        coordinates.append(coordinate)
        #nodes.append(node)
    passed_coordinates = [coordinates[0]] # 记录走过的正确的点
    # print(distance(coordinates[0],coordinates[1],coordinates[2]))
    j = 0
    mins = [] # 走过的路径长度
    min_i = 0 # 记录要走点的下标
    min_index = [] # 记录所有走的下标
    meet_coordinate = [] # 满足在球内部的点
    B = [100000,59652.3433795158,5022.0011644816404]
    r = 0
    flag = 0
    count_distance = 0
    start_time = time.clock()
    print("{0}【----当前从第{1}号点起飞----】{2}".format(0, 0, passed_coordinates[0]))
    while True:
        pre_toNow_dist = 0
        min_toB = 0
        min_value = math.inf
        if j == 0:  # 如果是第一个数
            r = 20 / 0.001  # 球的半径条件
        elif j % 2 == 1:  # 奇数为垂直
            r = 20 / 0.001 if (20 / 0.001) < (25 - passed_coordinates[j][4] ) / 0.001 else (25 - passed_coordinates[j][
                4] ) / 0.001
            flag = 1
        elif j % 2 == 0:  # 偶数为水平
            r = 15 / 0.001 if (15 / 0.001) < (25 - passed_coordinates[j][5] ) / 0.001 else (25 - passed_coordinates[j][
                5] ) / 0.001
            flag = 0
        for i in range(1,len(coordinates)):
            # 计算当前点跟上一个走过的点之间的距离
            dist = math.sqrt((coordinates[i][0] - passed_coordinates[j][0])**2 + (coordinates[i][1] - passed_coordinates[j][1])**2 + (coordinates[i][2] - passed_coordinates[j][2])**2)
            # 计算可选点到B点的距离
            if len(passed_coordinates) == 1: # 刚从第一个点出发
                if dist <= r  and coordinates[i][3] == flag : # 判断是否在球里面 并 满足相应矫正点
                    meet_coordinate.append(coordinates[i]) #找到在球内部的点就把它加进去
                    # 再去判断选中的点是否是距离B点和之前路径和最小的点
                    temp_toB = math.sqrt((B[0]- coordinates[i][0])**2 + (B[1] - coordinates[i][1])**2 + (B[2] - coordinates[i][2])**2)
                    if min_value > temp_toB+ dist:
                        pre_toNow_dist = dist # 记录经过的点到现在点的距离
                        min_value = temp_toB + dist # 记录最小的距离和
                        min_i = i # 记录最小距离下的下标
                        min_toB = temp_toB
            else: # 走过点的个数>=1
                if dist <= r  and coordinates[i][3] == flag and coordinates[i] not in passed_coordinates:
                    meet_coordinate.append(coordinates[i])  # 找到在球内部的点就把它加进去
                    # 再去判断选中的点是否是距离B点和之前路径和最小的点
                    temp_toB = math.sqrt(
                        (B[0] - coordinates[i][0]) ** 2 + (B[1] - coordinates[i][1]) ** 2 + (B[2] - coordinates[i][2]) ** 2)
                    arc_distance,right_candidate = distance(passed_coordinates[j-1],passed_coordinates[j],coordinates[i])
                    # print(arc_distance,right_candidate)
                    if min_value > weight(temp_toB,arc_distance) and right_candidate == 1:# 满足距离最小 且 有两个交点
                        pre_toNow_dist = arc_distance
                        min_value = weight(temp_toB,arc_distance)
                        min_toB = temp_toB
                        min_i = i  # 下标
        min_index.append(min_i)
        # print(min_index)
        mins.append(pre_toNow_dist) # 走的总路径
        j += 1
        passed_coordinates.append (coordinates[min_i]) # 经过的点多一
        if j % 2 == 1:
            passed_coordinates[j][4] = pre_toNow_dist * 0.001
        elif j % 2 == 0:
            passed_coordinates[j][5] = pre_toNow_dist * 0.001
        print("{0}【----当前飞过第{1}号矫正点----】{2}".format(j,min_i, passed_coordinates[j]))
        # dist_b = math.sqrt((B[0] - passed_coordinates[j][0]) ** 2 + (B[1] - passed_coordinates[j][1]) ** 2 + (B[2] - passed_coordinates[j][2]) ** 2)
        if pre_toNow_dist * 0.001  + min_toB * 0.001 < 30:
            # print("{0} , {1}".format(pre_toNow_dist,min_toB))
            break
    end_time = time.clock()
    print("{0}【----当前已到达第{1}号点----】{2}".format(j+1, 612, [100000,59652.3433795158,5022.0011644816404,'B点',min_toB * 0.001,pre_toNow_dist * 0.001  + min_toB * 0.001]))
    print('经过的点：',min_index)
    print('路径长度：',sum(mins)+min_toB)
    print('用时：%s Seconds' % (end_time - start_time))
    # print(passed_coordinates)
    draw_nodes_1 = []
    draw_nodes_0 = []
    draw_nodes = [[0,50000.0,5000.0]]
    for i in range(len(passed_coordinates)):
        draw_node_1 = []
        draw_node_0 = []
        x.append(passed_coordinates[i][0] )
        y.append(passed_coordinates[i][1])
        z.append(passed_coordinates[i][2])
        if passed_coordinates[i][3] == 1:
            draw_node_1.append(passed_coordinates[i][0] )
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
    print('经过的所有的点',len(draw_nodes),draw_nodes)
    print('经过的垂直校正点：',len(draw_nodes_1),draw_nodes_1)
    print('经过的水平校正点：',len(draw_nodes_0),draw_nodes_0)
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
    print('未经过垂直校正点：',nodes_1)
    print('未经过水平校正点：', nodes_0)
    x.append(100000)
    y.append(59652.3433795158)
    z.append(5022.0011644816404)
    # draw_picture(x,y,z)
if __name__ == '__main__':
    main()