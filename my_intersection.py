def my_intersection(aa1,bb1,aa2,bb2):
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
