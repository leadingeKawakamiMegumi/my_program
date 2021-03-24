import cv2

def rotation_im(im,angle,scale):
    '''
    Parameters
    -----------
    im: image
        8-bit single-channel image.
    
    angle: 左周り角度(見た目）
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
