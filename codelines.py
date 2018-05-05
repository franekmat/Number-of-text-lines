import cv2
import numpy as np

path = raw_input()
image = cv2.imread(path)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bitwise_not(gray)

thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

coords = np.column_stack(np.where(thresh > 0))
angle = cv2.minAreaRect(coords)[-1]

if angle < -45:
	angle = -(90 + angle)

else:
	angle = -angle

(h, w) = image.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
image = cv2.warpAffine(image, M, (w, h),
	flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
_,thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY_INV)
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
dilated = cv2.dilate(thresh,kernel,iterations = 3)
_, contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

last = 1000700000
count = 0

for contour in contours:
    [x,y,w,h] = cv2.boundingRect(contour)
    if h < 20:
        continue
    if (last - y) > 15:
        count = count + 1
    last = y

print count
