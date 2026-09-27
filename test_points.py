import cv2
import numpy as np

img = cv2.imread('cs180_proj2_hybrid_starter_code/nutmeg.jpg')

# Points to test
p1 = (580, 290)
p2 = (740, 350)

cv2.circle(img, p1, 15, (0, 0, 255), -1)
cv2.putText(img, "p1", (p1[0]+20, p1[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

cv2.circle(img, p2, 15, (0, 255, 0), -1)
cv2.putText(img, "p2", (p2[0]+20, p2[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

cv2.imwrite('output/test_nutmeg_points.jpg', img)
