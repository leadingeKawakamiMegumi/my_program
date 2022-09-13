import numpy as np
import time
import cv2
import matplotlib.pyplot as plt
import matplotlib.cm as cm

kernel = np.ones(shape=(3,3),dtype=np.float32)/9

#y = a*x + b
#a = -cos(theta)/sin(theta)
#b = ro/sin(theta)

def my_round0(a):
    '''
    Round to an integer (not bank rounding)
    '''
    from decimal import Decimal, ROUND_HALF_UP
    a = Decimal(str(a)).quantize(Decimal('0'), rounding=ROUND_HALF_UP)
    a = int(a)
    return(a)

def line_ab(x1,y1,x2,y2):
    '''
    input
    ------------------------
    (x1,y1),(x2,y2)
    
    output
    ------------------------------------------------
    (a,b) :y=ax+b
    Find a straight line and intercept that pass through two points
    '''
    xx = x2 - x1
    error = 0
    if xx == 0:
        a = x1
        b = 0
        error = 1
    else:    
        a = (y2-y1)/xx
        b = (x2*y1 - x1*y2)/xx   
    return(a,b,error)

def line_intersection(a1,b1,a2,b2):
    '''
    inout
    ----------------------------
    y=a1x+b1,y=a2x+b2
    
    output
    -----------------------
    Intersection of two straight lines
    '''
    inter_x = -(b1-b2)/(a1-a2)
    inter_y = (a1*b2-a2*b1)/(a1-a2)
    inter_x = my_round0(inter_x)
    inter_y = my_round0(inter_y)
    return(inter_x,inter_y)

def return_coordinates(x,y,w2,h2):
    '''
    input
    -----------------------
    (x,y):coordinate
    w2:image width
    h2:image height
   
    output
    -------------------------
　　Coordinate transformation
    1.center of the image ---> (0.0)
    2.Invert y
    '''
    x = x  + w2
    y = h2-y
    return(x,y)

#inter_x =inter_x + w2
#inter_y = h2- inter_y

def linehough_space360degree(im):
    '''hough space output
    input
    ------------------
    im:image
    
    output
    -------------------
    datahough
    height_min:0
    height_max:image_size/2 * Diagonal length 
    width_min :0[degree]
    width_max :360[degree](1pixel=1degree)
    '''
    
    h,w = im.shape
    h2  = int(h/2) #center of image
    w2  = int(w/2) #center of image
    ro_max = (h2**2 + w2**2)**0.5
    print("size",h,w,h2,w2,ro_max)

    #imgrs_ro = int(h) #Diagonal length
    datahough = np.zeros((int(ro_max)+1,360),float)
    for iy in range(0,h):
        iy2 = h2 - iy
        for ix in range(0,w):
            ix2 = ix - w2
            if im[iy,ix] > 0:
                for theta_h in range(0,360):  #0~360degree
                    theta_h2 = theta_h*np.pi/180  
                    ro = ix2 * np.cos(theta_h2) + iy2 * np.sin(theta_h2)
                    ro = my_round0(ro)
                    if 0 <= ro <=ro_max:
                        datahough[ro,theta_h] = datahough[ro,theta_h]  + im[iy,ix]
                        #datahough[ro,theta_h] = datahough[ro,theta_h]  + 1
    #print("datahough.T-space")                    
    plt.imshow(datahough)
    plt.show()
    
    return datahough

def my_lines_360degree(im,lines,nstart=0,nlast=1):
    #nlast = lines.shape[0]
    imdbg = im.copy()
    h,w  = imdbg.shape
    h2 = int(h/2)
    w2 = int(w/2)
    print("lines",lines)
    list_ab = []
    for i in lines[nstart:nlast]:
        rho = i[0][0]
        theta = i[0][1]
        a = np.cos(theta)
        b = np.sin(theta)
        #print("rho,theta:",rho,round(theta*180/np.pi,2))
        x0 = rho * a
        y0 = rho * b
        x1 = x0 + 100 * (-b)
        x1 = x1+w2
        x1 = my_round0(x1)
        y1 = y0 + 100 * (a)
        y1 = h2 -y1
        y1 = my_round0(y1)
        x2 = x0 - 100 * (-b)
        x2 = x2+w2
        x2 = my_round0(x2)
        y2 = y0 - 100 * (a)
        y2 = h2-y2
        y2 = my_round0(y2)
        print( "(x1, y1), (x2, y2):", (x1, y1), (x2, y2))
        print("(x1, y1), (x2, y2):", (x0 + 100 * (-b), y0 + 100 * (a)), (x0 - 100 * (-b), y0 - 100 * (a)))
        cv2.line(imdbg, (x1, y1), (x2, y2), (150,150,150), 1)
        a ,b, error= line_ab(x1,y1,x2,y2)
        if error==1:
            list_ab.append([a,"False"])
        else:
            list_ab.append([a,b])
    #fig = plt.figure(figsize=(6,6))
    #plt.imshow(imdbg) 
    #plt.show()
    return(imdbg,list_ab)

def my_lines_180degree(im,lines,nstart=0,nlast=1):
    #nlast = lines.shape[0]
    imdbg = im.copy()
    h,w  = imdbg.shape
    h2 = int(h/2)
    w2 = int(w/2)
    for i in lines[nstart:nlast]:
        rho = i[0][0]
        theta = i[0][1]
        a = np.cos(theta)
        b = np.sin(theta)
        #print("rho,theta:",rho,round(theta*180/np.pi,2))
        x0 = (rho-w2) * a
        y0 = (rho-h2) * b
        x1 = int(x0 + 1000 * (-b)) + w2
        y1 = int(y0 + 1000 * (a))  +h2
        x2 = int(x0 - 1000 * (-b)) + w2 
        y2 = int(y0 - 1000 * (a)) +h2
        cv2.line(imdbg, (x1, y1), (x2, y2), (150,150,150), 1)
    #fig = plt.figure(figsize=(6,6))
    #plt.imshow(imdbg) 
    #plt.show()
    return(imdbg)
    
#my_line_hough_space
def linehough_space180degree(im):
    '''hough space output
    input
    ------------------
    im:image
    
    output
    -------------------
    datahough
    heigh_min:-image_size/2 * Diagonal length 
    heigh_max:+image_size/2 * Diagonal length 
    width_min :0[degree]
    width_max :180[degree](1pixel=1degree)
    '''
    
    h,w = im.shape
    h2  = int(h/2) #center of image
    w2  = int(w/2) #center of image
    imgrs_ro = int(h) #Diagonal length
    datahough = np.zeros((imgrs_ro,180),float)
    for iy in range(0,h):
        iy2 = iy - h2
        for ix in range(0,w):
            ix2 = ix - w2
            if im[iy,ix] > 0:
                for theta_h in range(0,180):  #0~180degree
                    theta_h2 = theta_h*np.pi/180  
                    ro = int(ix2 * np.cos(theta_h2) + iy2 * np.sin(theta_h2))
                    if -h2 < ro < h2:
                        #datahouh[ro,theta_h] = datahouh[ro,theta_h]  + im[iy,ix]
                        datahough[ro+h2,theta_h] = datahough[ro+h2,theta_h]  + 1
    #print("datahough.T-space")                    
    #plt.imshow(datahough.T)
    #plt.show()
    return datahough

from skimage.feature import peak_local_max
def local_max_points(image,top_n, min_dist = 30):
    #https://sabopy.com/py/scikit-image-51/
    #min_dist = 30

    # image_max is the dilation of im with a 30*30 structuring element
    # It is used within peak_local_max function
    #image_max = ndi.maximum_filter(im, size=30, mode='constant')

    # Comparison between image_max and im to find the coordinates of local maxima
    coordinates = peak_local_max(image, min_distance = min_dist)

    #plt.imshow(image_max,interpolation='none')

    coordinates2 = []
    for i in range(0,len(coordinates)):
        score_y = coordinates[i,0]
        score_x = coordinates[i,1]
        coordinates2.append([score_y,score_x,image[score_y,score_x]])
        #print(i,score_y,score_x,image[score_y,score_x])
        
    coordinates3 = sorted(coordinates2, key = lambda x:x[2])[::-1]
    
    if len(coordinates3)>top_n:
        coordinate_t = np.array(coordinates3[0:top_n])
    else:
        coordinate_t = np.array(coordinates3)
        
    #plt.imshow(image)
    #plt.plot(coordinate_t[:,1],coordinate_t[:,0],'r.') 
    im_out = image.copy()
    for i in range(0,len(coordinate_t)):
        #print(int(coordinate_t[i,0]),int(coordinate_t[i,1]))
        cv2.drawMarker(im_out, (int(coordinate_t[i,1]),int(coordinate_t[i,0])), (255, 255,255), markerType=cv2.MARKER_STAR, markerSize=10) #cv2 (x,y)
        
    return(coordinate_t,im_out)   
  
def main(im_input,top_n):
    fig = plt.figure(figsize=(10,10))
    start = time.time()
    houghdbg = linehough_space180degree(im_input)
    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
    img = cv2.resize(houghdbg,(512,512))
    plt.subplot(131),plt.imshow(im_input,cmap=cm.pink)
    plt.subplot(132),plt.imshow(img,cmap=cm.pink)

    houghdbg_sm  = cv2.filter2D(houghdbg,-1,kernel)
    coordinate_t,imdbg2 = local_max_points(houghdbg_sm,top_n= top_n, min_dist = 10)
    #print(coordinate_t)
    #center_h = int(houghdbg.shape[0]/2)
    #print("center_h",center_h)
    h,w = imdbg2.shape
    #for i in range(len(coordinate_t)):
        #print(int(coordinate_t[i][0]),int(coordinate_t[i][1]))

    lines2 = np.zeros((top_n,1,2),float)
    for i in range(0,top_n):
        lines2[i][0][0] = int(coordinate_t[i][0])
        lines2[i][0][1] = coordinate_t[i][1]/180*np.pi
    imdbg = my_lines_180degree(im_input,lines2,0,6) 
    plt.subplot(133),plt.imshow(imdbg)
    plt.show()
    plt.imshow(imdbg2,cmap=cm.pink)
    plt.show()
