import numpy as np
from matplotlib import pyplot as plt

def get_top_point(x,y):
    # 取出顶点
    point_list=[]
    for index, item in enumerate(zip(x,y), 1):
        point = (item[0], item[1])
        point_list.append(point)
    return point_list
