import cv2 as cv 
import numpy as np 

# -------------------  DRAWING ON IMAGES 
blank = np.zeros((500,500,3),dtype = 'uint8') # creates a blank screen 
#   Rectangle function 
cv.rectangle(blank,(0,0),(250,250),(0,255,0),thickness=2)
#   Writing the text 
cv.putText(blank,"otha ommala",(250,250),cv.FONT_HERSHEY_TRIPLEX,1.0,(255,0,0),2)
cv.imshow("blank",blank)
cv.waitKey(0)
cv.destroyAllWindows()

