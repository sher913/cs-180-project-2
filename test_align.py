import cv2
import numpy as np

img = cv2.imread('data/nutmeg rotated.jpg')

p1 = (250, 200)
p2 = (400, 200)

cv2.circle(img, p1, 15, (0, 0, 255), -1)
cv2.putText(img, "p1", (p1[0]+20, p1[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

cv2.circle(img, p2, 15, (0, 255, 0), -1)
cv2.putText(img, "p2", (p2[0]+20, p2[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

cv2.imwrite('output/test_farquaad_points.jpg', img)
pts3 = (p1, p2, p3, p4)

suying_a, farquaad_a = align_image_centers(suying, farquaad, pts3)
suying_a, farquaad_a = rescale_images(suying_a, farquaad_a, pts3)
suying_a, angle = rotate_im1(suying_a, pts3)
suying_a, farquaad_a = match_img_size(suying_a, farquaad_a)

# Draw red cross at center of suying_a
h, w = suying_a.shape[:2]
cx, cy = w // 2, h // 2
suying_out = suying_a.copy()
cv2.line(suying_out, (cx-20, cy), (cx+20, cy), (1, 0, 0), 2)
cv2.line(suying_out, (cx, cy-20), (cx, cy+20), (1, 0, 0), 2)

# Draw red cross at center of farquaad_a
farquaad_out = farquaad_a.copy()
cv2.line(farquaad_out, (cx-20, cy), (cx+20, cy), (1, 0, 0), 2)
cv2.line(farquaad_out, (cx, cy-20), (cx, cy+20), (1, 0, 0), 2)

cv2.imwrite('output/debug_suying.jpg', (suying_out[:, :, ::-1] * 255).astype(np.uint8))
cv2.imwrite('output/debug_farquaad.jpg', (farquaad_out[:, :, ::-1] * 255).astype(np.uint8))
