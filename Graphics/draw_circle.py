import numpy as np
from matplotlib import pyplot as plt
color,style='blue','.'
def draw_one_point(cx,cy,x,y):
    true_x=cx+x
    true_y=cy+y
    plt.plot(true_x,true_y,color=color,marker='.')
def draw_all_point_in_circle(cx,cy,x,y):
    # 在img上绘制point和它的七个对称点
    draw_one_point(cx,cy,x,y)
    draw_one_point(cx,cy,y,x)
    draw_one_point(cx,cy,y,-x)
    draw_one_point(cx,cy,x,-y)
    draw_one_point(cx,cy,-x,-y)
    draw_one_point(cx,cy,-y,-x)
    draw_one_point(cx,cy,-y,x)
    draw_one_point(cx,cy,-x,y)
    # plt.show()
def draw_circle(cx,cy,cr):
    plt.plot(cx,cy,color='red',marker='.')
    x,y=0,cr
    d=float(1-cr)
    draw_all_point_in_circle(cx,cy,x,y)
    while x<y:
        if d<0:
            d+=2*x+3
        else:
            d+=2*(x-y)+5
            y-=1
        x+=1
        draw_all_point_in_circle(cx,cy,x,y)
    plt.show()
# draw_circle(5,5,100)
# 半径要足够大不然画不成圆形