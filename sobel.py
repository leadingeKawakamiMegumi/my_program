import numpy as np
import cv2

def sobelxy(img):

    img2 = img.copy()
    
    sobelx = cv2.Sobel(img2,cv2.CV_64F,1,0,ksize=5)
    sobely = cv2.Sobel(img2,cv2.CV_64F,0,1,ksize=5)
    grad2 = np.sqrt(sobelx  ** 2 + sobely ** 2) 
    hosei = np.max(grad2)
    grad2 = grad2/hosei * 255
    imgs = grad2.astype(np.uint8)
    return(imgs)
