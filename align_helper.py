import cv2
import sys

def get_points(img_path, num_points=2):
    img = cv2.imread(img_path)
    if img is None:
        print(f"Could not read {img_path}")
        return []
    
    points = []
    
    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            points.append((x, y))
            cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
            cv2.imshow('Image', img)
            if len(points) == num_points:
                cv2.waitKey(500) # give a small delay to see the last dot
                cv2.destroyAllWindows()
                
    cv2.imshow('Image', img)
    cv2.setMouseCallback('Image', mouse_callback)
    
    print(f"Please click {num_points} points on {img_path}")
    cv2.waitKey(0)
    return points

if __name__ == "__main__":
    pts = get_points(sys.argv[1])
    print(f"Points for {sys.argv[1]}: {pts}")
