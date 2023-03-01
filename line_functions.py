#上から
# 2点を通る直線の傾きと切片を求める
# 2つの直線の2等分線を求める　(2本あることに注意）
# 2つの直線の交点を求める
#　点と直線の距離を求める

def line_2poit(px1,py1,px2,py2):
    '''
    input
    ----------------------------------
    (px1,py1),(px2,py2):座標情報
    
    output
    ----------------------------------
    aa:2点を通る直線の傾き
    bb:2点を通る直線の切片
    '''
    if px1==px2:
        aa = 0
        bb = py1
    else:    
        aa = (py2 - py1)/(px2 - px1)
        bb = (px2 * py1 - px1 * py2)/(px2 - px1)
   
    return  aa,bb


def bisector_line(a1,b1,a2,b2):
    '''
    input
    ----------------------------------
    l1 = a1・x + b1
    l2 = a2・x + b2
    (a1!=a2)
    
    output
    ----------------------------------
    bisector_a1・x +  bisector_b1:傾き>=0の方の2等分線
    bisector_a2・x +  bisector_b2:傾きマイナスの方の2等分線
    '''
    aa1 = (a1**2 + 1)**0.5
    aa2 = (a2**2 + 1)**0.5
        
    bisector_a1 = (aa1 * a2 - aa2 * a1)/(aa1 - aa2)
    bisector_b1 = (aa1 * b2 - aa2 * b1)/(aa1 - aa2)
    bisector_a2 = (aa1 * a2 + aa2 * a1)/(aa1 + aa2)
    bisector_b2 = (aa1 * b2 + aa2 * b1)/(aa1 + aa2)
        
    return (bisector_a1,bisector_b1,bisector_a2,bisector_b2)


def intersection_line(a1,b1,a2,b2):
    '''
    input
    ----------------------------------
    l1 = a1・x + b1
    l2 = a2・x + b2
    (a1!=a2)
    
    output
    ----------------------------------
    intersection_x
    intersection_y
    '''
    if a1==a2:
        print("error:Straight lines are parallel. So output=(0,0)")
        intersection_x = 0
        intersection_y = 0
    else:    
        intersection_x = (b2-b1)/(a1-a2)
        intersection_y = (a1*b2-b1*a2)/(a1-a2)
        
    return (intersection_x,intersection_y)


def intersection_line2(aa1,bb1,aa2,bb2):
    '''
    input----------------------
    aa1:slope of line1
    bb1:intercept of line1
    aa2:slope of line2
    bb2:intercept of line2
    output--------------------
    x_inter:intersection x
    y_inter:intersection y
    if 
    '''
    error_code = 0
    if aa1 == aa2: #平行（同じ直線含む）
        print("直線が平行（一致を含む）")
        x_inter = 100000
        y_inter = 100000
        error_code = 1
    else:    
        aa = aa2 -aa1
        bb = aa2 * bb1 -aa1 * bb2
        x_inter = (bb1-bb2)/aa
        y_inter = bb/aa
        
    return(x_inter,y_inter,error_code)


def distance_point_line(xp,yp,ka,kb):
    '''
    distance between point and line ｙ＝ka*x + kb
    input----------------------
    point:(xp,yp)
    ka:slope 
    kb:intercept 
    output--------------------
    kyori (float64)
    '''
    kyori = (ka*xp -yp + kb)/np.sqrt(ka*ka + 1)　#?
    return kyori
