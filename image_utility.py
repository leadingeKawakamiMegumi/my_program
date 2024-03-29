import cv2
import numpy as np

def jyuusin(img):
    mu = cv2.moments(img, False)
    xc,yc= mu["m10"]/mu["m00"], mu["m01"]/mu["m00"]
    return(xc,yc)

def sobelxy(img):
    img2 = img.copy()
    sobelx = cv2.Sobel(img2,cv2.CV_64F,1,0,ksize=5)
    sobely = cv2.Sobel(img2,cv2.CV_64F,0,1,ksize=5)
    grad2 = np.sqrt(sobelx  ** 2 + sobely ** 2) 
    hosei = np.max(grad2)
    grad2 = grad2/hosei * 255
    imgs = grad2.astype(np.uint8)
    return(imgs)

def rotation_im(im,angle,scale):
    '''
    Parameters
    -----------
    im: image
        8-bit single-channel image.
    
    angle: 左周り角度(見た目）[degree]
    scale: 倍率
    
    Returns
    ---------
    np.uint8
    '''
    h,w = im.shape
    center = ((w-1)/2,(h-1)/2)
    
    trans = cv2.getRotationMatrix2D(center, angle , scale) 
    
    image2 = cv2.warpAffine(im, trans, (w,h))
    return(image2)
    
def image_translation(im,shift_x,shift_y):
    '''
    input
    -------------------------------
    im:np.uint8
    shiftx : #右（x方向）に移動したい量
    shifty : #下（y方向）に移動したい量
    '''
    h,w = im.shape
    shiftx = shift_x 
    shifty = shift_y
    mat = np.array([[1, 0, shiftx], [0, 1, shifty]], dtype=np.float32)
    return(cv2.warpAffine(im, mat, (h,w)))


def min_max_norm(image):
    a = np.min(image)
    b = np.max(image)
    im_out = (image - a) / (b-a) *255
    im_out = im_out.astype(np.uint8)
    return(im_out)

def make_cirkle_mask(im_size):
    '''
    input
    -------------------------------
    image: height(h) = width(w)
    '''
    im_size_half = int(im_size/2) 
    print("circle_r",im_size_half) 
    im_mask = np.zeros((im_size,im_size),np.uint8)
    return(cv2.circle(im_mask,(im_size_half,im_size_half),im_size_half,255,-1))
