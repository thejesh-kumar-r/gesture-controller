import cv2 as cv

#-----------------------------------RESIZING 
def frameresize(frame,scale=0.75):
    width = int(frame.shape[1]*scale)
    height = int(frame.shape[0]*scale)
    dimension = (width,height)

    return cv.resize(frame,dimension,interpolation = cv.INTER_AREA)

#------------------------------ IMAGE CAPTURING 
img = cv.imread('Photos\cat1.jpg')
cv.imshow('cat',img)
cv.waitKey(0) 

#--------------------------------VIDEO CAPTURE 
capture = cv.VideoCapture('Videos\IMG_2139.mov')

while True :
    isTrue,frame = capture.read()
    frame_resized = frameresize(frame,0.25)
    cv.imshow('video_resized',frame_resized)

    if cv.waitKey(20) & 0xFF == ord('d'):
        break

capture.release()
cv.destroyAllWindows()