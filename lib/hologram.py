import cv2
import numpy as np

class hologram:
    def makeHologram(original,scale=0.5,scaleR=4,distance=0):
        '''
           Create 3D hologram from image (must have equal dimensions)
        '''
    
        height = int((scale*original.shape[0]))
        width = int((scale*original.shape[1]))
    
        image = cv2.resize(original, (width, height), interpolation = cv2.INTER_CUBIC)
    
        up = image.copy()
        down =  hologram.rotate_bound(image.copy(),180)
        right = hologram.rotate_bound(image.copy(), 90)
        left = hologram.rotate_bound(image.copy(), 270)
    
        holo = np.zeros([max(image.shape)*scaleR+distance,max(image.shape)*scaleR+distance,3], image.dtype)
    
        center_x = (holo.shape[0])//2
        center_y = (holo.shape[1])//2
    
        vert_x = (up.shape[0])//2
        vert_y = (up.shape[1])//2
        holo[0:up.shape[0], center_x-vert_x+distance:center_x+vert_x+distance] = up
        holo[ holo.shape[1]-down.shape[1]:holo.shape[1] , center_x-vert_x+distance:center_x+vert_x+distance] = down
        hori_x = (right.shape[0])//2
        hori_y = (right.shape[1])//2
        holo[ center_x-hori_x : center_x-hori_x+right.shape[0] , holo.shape[1]-right.shape[0]+distance : holo.shape[1]+distance] = right
        holo[ center_x-hori_x : center_x-hori_x+left.shape[0] , 0+distance : left.shape[0]+distance ] = left
    
        return holo

    def rotate_bound(image, angle):
        # grab the dimensions of the image and then determine the
        # center
        (h, w) = image.shape[:2]
        (cX, cY) = (w // 2, h // 2)
 
        # grab the rotation matrix (applying the negative of the
        # angle to rotate clockwise), then grab the sine and cosine
        # (i.e., the rotation components of the matrix)
        M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])
 
        # compute the new bounding dimensions of the image
        nW = int((h * sin) + (w * cos))
        nH = int((h * cos) + (w * sin))
 
        # adjust the rotation matrix to take into account translation
        M[0, 2] += (nW / 2) - cX
        M[1, 2] += (nH / 2) - cY
 
        # perform the actual rotation and return the image
        return cv2.warpAffine(image, M, (nW, nH))
    def crop_img(origin):
        w = min(origin.shape[0],origin.shape[1]) 
        if(w % 2 != 0):
           w = w - 1
        crop_img = origin[0:w, 0:w]
        return crop_img
    def pad_img(img):
        #Getting the bigger side of the image
        s = max(img.shape[0:2])

        #Creating a dark square with NUMPY  
        f = np.zeros((s,s,3),np.uint8)

        #Getting the centering position
        ax,ay = (s - img.shape[1])//2,(s - img.shape[0])//2

        #Pasting the 'image' in a centering position
        f[ay:img.shape[0]+ay,ax:ax+img.shape[1]] = img
        return f
    def process_video(video,target_name):
        cap = cv2.VideoCapture(video)

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        holo = None
        ret = False
        while(not ret):
            ret, frame = cap.read()
            if ret:
                frame = hologram.pad_img(frame)
                frame = cv2.resize(frame, (640, 640), interpolation = cv2.INTER_CUBIC)
                holo = hologram.makeHologram(frame)
        out = cv2.VideoWriter(target_name,fourcc, 30.0, (holo.shape[0],holo.shape[1]))
        total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        count = 0
        print("Processing %d frames"%(total_frames))
        while(True):
            # Capture frame-by-frame
            ret, frame = cap.read()
            if ret:
                frame = hologram.pad_img(frame)
                frame = cv2.resize(frame, (640, 640), interpolation = cv2.INTER_CUBIC)
                holo = hologram.makeHologram(frame)
                out.write(holo)
                count += 1
                print("Total:%d of %d"%(count,total_frames))
            if(count>=total_frames-1):
               break
    
        # Release everything if job is finished
        cap.release()
        out.release()
        return