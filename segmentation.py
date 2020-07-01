import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(0)
cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('min_Hue','image',0,255,nothing)
cv2.createTrackbar('max_Hue','image',0,255,nothing)
cv2.createTrackbar('min_Saturation','image',0,255,nothing)
cv2.createTrackbar('max_Saturation','image',0,255,nothing)
cv2.createTrackbar('min_Value','image',0,255,nothing)
cv2.createTrackbar('max_Value','image',0,255,nothing)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    # get current positions of four trackbars
    min_h = cv2.getTrackbarPos('min_Hue','image')
    max_h = cv2.getTrackbarPos('max_Hue','image')
    min_s = cv2.getTrackbarPos('min_Saturation','image')
    max_s = cv2.getTrackbarPos('max_Saturation','image')
    min_v = cv2.getTrackbarPos('min_Value','image')
    max_v = cv2.getTrackbarPos('max_Value','image')

    # Segment image based on the color limits
    min_limit = (min_h, min_s, min_v)
    max_limit = (max_h, max_s, max_v)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, min_limit, max_limit)

    # Overlay obtained mask on original image
    mask_final = np.zeros((hsv.shape))
    mask_final[:,:,1] = mask
    mask_final = np.uint8(mask_final)
    added_image = cv2.addWeighted(frame,0.7,mask_final,0.3,0)

    # Calculate centroid
    # calculate moments of binary image
    M = cv2.moments(mask)
    # calculate x,y coordinate of center
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX = 0
        cY = 0
    cv2.circle(added_image, (cX, cY), 5, (255, 255, 255), -1)
    cv2.putText(added_image, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Display the resulting frame
    cv2.imshow('image',cv2.hconcat([frame,cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR), added_image]))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()