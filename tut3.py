import cv2 as cv 

img = cv.imread("Photos/cat1.jpg")

#-------------------------- RESIZING
def resize_image(image,scale= 0.75):
    width = int(image.shape[1]*scale)
    height = int(image.shape[0]*scale)
    dimension = (width,height)

    return cv.resize(image,dimension,interpolation=cv.INTER_AREA)
 
#--------------------- 1-CONVERTING INTO GRAYSCALE 
gray_image = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
resized_image = resize_image(gray_image,0.5)
cv.imshow("Gray,Image",resized_image)
# the image is too big so we resize it 

#--------------------- 2 - BLURRING AN IMAGE(The Gaussian BLur)
blurred_image = cv.GaussianBlur(img,(15,15),cv.BORDER_DEFAULT)
resized_blurred_image = resize_image(blurred_image,0.5)
cv.imshow("Blurred image",blurred_image)
cv.waitKey(0)
cv.destroyAllWindows()