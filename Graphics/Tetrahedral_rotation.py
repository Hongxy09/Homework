"""
作业题目：四面体的旋转
1）点绕坐标轴旋转（设X轴）
2）四面体的可见性
"""
import numpy as np
import matplotlib as mpl
from matplotlib import cm
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def get_point():
    # 输入ABCD四个点坐标got ABCD分别在xoy，yoz，xoz和x轴上
    pointA = [6, 0, 0]
    pointB = [3, 6, 0]
    pointC = [0, 0, 0]
    pointD = [3, 0, 3]
    point_list = [pointA, pointB, pointC, pointD]
    point_list = np.array(point_list)
    # if rotate==True:
    #     point_list=
    return point_list


def get_data(point_list):
    data_list = np.array(point_list).T
    # data_list=data_list.tolist()# 转回list
    return data_list


def get_inner_point(point_list):
    data_list = get_data(point_list)
    sum = (np.array([0, 0, 0]))
    inner_point = (np.array([0, 0, 0]))
    for i in range(3):
        sum[i] = np.sum(data_list[i], axis=0)
        inner_point = np.true_divide(sum, np.array([4]))
    return inner_point


def get_center_point(point_list, num):
    if num <= 0 or num >= 5:
        print("Wrong num!")
        return None
    data_list = get_data(point_list)
    index = num - 1
    data_list = np.delete(data_list, index, axis=1)
    center = (np.array([0, 0, 0]))
    sum = (np.array([0, 0, 0]))
    for i in range(3):
        sum[i] = np.sum(data_list[i], axis=0)
        center = np.true_divide(sum, np.array([3]))
    return center


def get_true_n(center, n):
    # 获得真正的法向量（朝外）
    a, b, c = n[0], n[1], n[2]
    x1, y1, z1 = center[0], center[1], center[2]
    d = (-a)*(x1)+(-b)*(y1)+(-c)*(z1)
    flag = np.dot(center, n)+d
    if flag >= 0:
        print("is not outside n!")
    #     n_new = np.negative(n)
    # print("n changed from",n," to ",n_new)
    # return n_new


def get_each_panner_point_list(point_list, num):
    if num <= 0 or num >= 5:
        print("Wrong num!")
        return None
    index = num - 1
    # 每个面由三个顶点，去掉多的那个，以ABC为例,point删除行，data删除列
    point_list = np.delete(point_list, index, axis=0)
    return point_list


def get_true_n2(point_list, inner_point, n):
    # 带入平面方程获得真正的法向量（朝外）这里传入的point_list应当只有三个点
    if point_list.shape[0] != 3:
        print("more point in get true n!")
        return None
    point = point_list[0]
    compare_vec = inner_point-point
    flag = np.dot(compare_vec, n)
    n_new = n
    if flag >= 0:
        n_new = np.negative(n)
        print(n, "is not outside n!So changed to ", n_new)
    return n_new


def get_vector(num, point_list):
    # 默认的面顺序为ABC，ADC，ABD，BCD，输出当前面法向量
    # 内部点用于计算法向量朝向
    inner_point = get_inner_point(point_list)
    point_list = get_each_panner_point_list(point_list, num)
    vec1 = point_list[1]-point_list[0]
    vec2 = point_list[2]-point_list[0]
    # print("In panner ", num, "The point_list is:", point_list)
    # print("In panner ", num, "The vec1 is:", vec1, "The vec2 is:", vec2)
    n = np.cross(vec1, vec2)
    n = get_true_n2(point_list, inner_point, n)
    print("In panner ", num, "The n is:", n)
    return n


def get_view_vector(view_point, num, point_list):
    # 第num个面的视点向量
    this_type_str = type(view_point)
    if this_type_str is not np.ndarray:
        view_point = np.array(view_point)
    center = get_center_point(point_list, num)
    view_vector = center-view_point
    print("In panner ", num, "The center is:",
          center, "The view_v is:", view_vector)
    return view_vector


def get_panner_flag(view_point, point_list):
    # 返回所有面的可见性组
    eye_flag = []
    n_list, view_vector_list, = [], []
    this_type_str = type(view_point)
    if this_type_str is not np.ndarray:
        view_point = np.array(view_point)
    for i in range(1, 5):
        # 遍历四个面获得一下他们的view_vec和n
        n = get_vector(i, point_list)
        v = get_view_vector(view_point, i, point_list)
        n_list.append(n)
        view_vector_list.append(v)
    n_list, view_vector_list = np.array(n_list), np.array(view_vector_list)
    for i in range(4):
        flag = np.dot(n_list[i], view_vector_list[i])
        eye_flag.append(flag)
    eye_flag = np.array(eye_flag)
    eye_flag[eye_flag <= 0] = 1  # 小于等于零的面可见，置为1
    eye_flag[eye_flag != 1] = 0  # 没有置为1的是不可见的面，置为0
    print("eye_flag is:", eye_flag)
    return eye_flag


def line_in_each_paner(num, point_list) -> list:
    # 返回第num个面的边矩阵
    if num <= 0 or num >= 5:
        print("Wrong num!")
        return None
    index = num-1
    line_list = []
    for i in range(4):
        for j in range(i+1, 4):
            if i != index and j != index:
                line = (point_list[j]-point_list[i]).tolist()
                line_list.append([(num), (i+1, j+1), line, 2])
    # 返回的信息是：线所在的面（1-4）线的端点序号（1-4）线的向量
    # line_list=np.array(line_list)
    return line_list


def new_all_line_list(all_line_list):
    true_line_list = []
    for panner_index in range(4):
        for line_index in range(3):
            line = all_line_list[panner_index][line_index][2]
            true_line_list.append(line)

    res_line_list = []
    for item in true_line_list:
        item_reverse = [-l for l in item]
        if not item in res_line_list and not item_reverse in res_line_list:
            res_line_list.append(item)

    # 记录边的顶点信息
    res_line_list_num = []
    for i in range(len(res_line_list)):
        item = res_line_list[i]
        for panner_index in range(4):
            for line_index in range(3):
                line_with_num = all_line_list[panner_index][line_index]
                point_num = line_with_num[1]
                line = line_with_num[2]
                if line == item and point_num not in res_line_list_num:
                    print("With the point ", point_num,
                          "the line vector is:", item)
                    res_line_list_num.append(point_num)
    # 返回真正的六条边的顶点信息
    return res_line_list_num


def deduct_one_panner_in_point_list(index, all_line_list, real_point_list_with_eyeflag):
    # 输入面的序列，可以删除对应真边的值-1
    if index < 0 or index > 3:
        print("Wrong index of panner!")
        return None
    for complex_line in all_line_list[index]:
        point = complex_line[1]
        point_reverse = reversed(point)
        for complex_point in real_point_list_with_eyeflag:
            real_point = complex_point[0]
            if point == real_point or point_reverse == real_point:
                complex_point[1] -= 1
    return real_point_list_with_eyeflag


def line_can_see(eye_flag, point_list):
    # 输入四个面的可见性，输出真边表的可见性
    all_line_list = []
    for index in range(1, 5):
        all_line_list.append(line_in_each_paner(
            index, point_list))  # 记录了顶点和边向量
    real_point_list = new_all_line_list(all_line_list)  # 仅记录了顶点信息
    real_point_list_with_eyeflag = []  # 记录顶点和eyeflag
    for i in range(len(real_point_list)):
        real_point_list_with_eyeflag.append([real_point_list[i], 2])
        # real_point_list_with_eyeflag[1][0]—>Out[39]: (2, 4)
    # 根据eye删除对应的面上的边flag，然后统计非0的边
    for panner_index, panner_eye_flag in enumerate(eye_flag):
        if panner_eye_flag == 0:  # eye_flag中为0的是不可见的面，其对应的边要-1
            deduct_one_panner_in_point_list(
                panner_index, all_line_list, real_point_list_with_eyeflag)
    # print("We can see line is real_point_list_with_eyeflag:",real_point_list_with_eyeflag)
    return real_point_list_with_eyeflag


def draw_point(point_list, inner, view_point, ax):
    data_list = get_data(point_list).tolist()
    # 画四个点和视点
    ax.scatter(data_list[0], data_list[1], data_list[2],
               zdir='z', c='k', label='point')
    ax.scatter(view_point[0], view_point[1], view_point[2],
               c='r', marker='^', label='view_point')
    # ax.scatter(inner[0], inner[1], inner[2],c='b', label='inner_point')
    ax.legend(loc='best')
    # 给点标号
    for i in range(len(data_list[0])):
        ax.text(data_list[0][i], data_list[1][i], data_list[2][i], i+1)
    plt.show()


def divide_line(line_list):
    # 输入的是带顶点信息和可见性的边表
    notsee_line_list = []
    see_line_list = []
    # 遍历每个边，将可见性为0的放到虚线表中，可见性为1的不动
    for i in range(len(line_list)):
        line_point = line_list[i][0]
        if line_list[i][1] == 0 and line_point not in notsee_line_list:
            notsee_line_list.append(line_point)
        elif line_point not in see_line_list:
            see_line_list.append(line_point)
    return see_line_list, notsee_line_list


def draw_line_between_two_point(point_a, point_b, point_list, ax, linecolor='k', linestyle='-'):
    draw_point_list = []
    # 两点连线
    draw_point_list.append(point_list[point_a-1])
    draw_point_list.append(point_list[point_b-1])
    draw_point_list.append(point_list[point_a-1])
    # 获得datalist
    draw_data_list = get_data(draw_point_list)
    # 画线
    ax.plot3D(draw_data_list[0], draw_data_list[1],
              draw_data_list[2], c=linecolor, linestyle=linestyle)


def draw_all_line(point_list, eye_flag, ax, linecolor='g', linestyle='--'):
    line_list = line_can_see(eye_flag, point_list)
    see_line_list, notsee_line_list = divide_line(line_list)
    for i in range(len(see_line_list)):
        # print(see_line_list[i][0],"and",see_line_list[i][1])
        draw_line_between_two_point(
            see_line_list[i][0], see_line_list[i][1], point_list, ax)  # 实线用默认的绘图风格
    for j in range(len(notsee_line_list)):
        # 虚线用指定的绘图风格
        draw_line_between_two_point(
            notsee_line_list[j][0], notsee_line_list[j][1], point_list, ax, linecolor, linestyle)


def draw_tetrahedral(view_point, inner, point_list, linecolor):
    # 四面体的绘制 view_point=[0,0,0]
    # 画布与坐标轴的绘制
    this_type_str = type(view_point)
    if this_type_str is not np.ndarray:
        view_point = np.array(view_point)
    fig = plt.figure(figsize=(12, 8), facecolor='lightyellow')
    ax = fig.gca(fc='whitesmoke', projection='3d')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    eye_flag = get_panner_flag(view_point, point_list)
    # 画点
    draw_point(point_list, inner, view_point, ax)
    # 根据面的可见性画出对应的实现边和虚线边
    draw_all_line(point_list, eye_flag, ax, linecolor)
    ax.view_init(azim=49, elev=7)
    plt.show()


def check_of_n():
    view_point = [9, 3, 1]
    n_list = []
    for i in range(1, 5):
        n = get_vector(i, point_list)
        n_list.append(n)
    return n_list


def rotate(point_list, theta):
    # 输入旋转角度和原始顶点信息，输出旋转后的顶点信息
    if theta > 360:
        theta -= 360
    rotate_matrix = np.zeros((3, 3))
    cos_value = np.cos(theta*np.pi/180)
    sin_value = np.sin(theta*np.pi/180)
    rotate_matrix[0][0] = cos_value
    rotate_matrix[0][1] = -sin_value
    rotate_matrix[1][0] = sin_value
    rotate_matrix[1][1] = cos_value
    rotate_matrix[2][2] = 1
    new_point_list = np.dot(point_list, rotate_matrix)
    return new_point_list


def fun():
    # 设置旋转角度，虚线颜色，视点坐标
    theta = 120
    linecolor = 'r'
    view_point = [5,5,5]
    point_list = get_point()
    inner = get_inner_point(point_list)
    # 绘制旋转前的图形
    draw_tetrahedral(view_point, inner, point_list, linecolor)
    # 绘制旋转后的图形
    rotated_point_list = rotate(point_list, theta)
    rotated_inner = get_inner_point(rotated_point_list)
    draw_tetrahedral(view_point, rotated_inner, rotated_point_list, linecolor)
