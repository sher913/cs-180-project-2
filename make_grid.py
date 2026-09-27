import cv2
import sys

def draw_grid(img_path, out_path):
    img = cv2.imread(img_path)
    if img is None:
        return
        
    h, w = img.shape[:2]
    
    # Draw vertical lines
    for x in range(0, w, 50):
        cv2.line(img, (x, 0), (x, h), (255, 255, 255), 1)
        if x % 100 == 0:
            cv2.putText(img, str(x), (x+5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            cv2.putText(img, str(x), (x+5, h-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            
    # Draw horizontal lines
    for y in range(0, h, 50):
        cv2.line(img, (0, y), (w, y), (255, 255, 255), 1)
        if y % 100 == 0:
            cv2.putText(img, str(y), (5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            cv2.putText(img, str(y), (w-40, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
    cv2.imwrite(out_path, img)

if __name__ == "__main__":
    draw_grid('data/su ying.webp', 'output/grid_suying.jpg')
    draw_grid('data/lord farquaad.webp', 'output/grid_farquaad.jpg')
