import numpy as np
import cv2
import os
from scipy.signal import convolve2d

def compute_gradient_magnitude(img_dx, img_dy):
    """Computes the gradient magnitude from dx and dy derivatives."""
    return np.sqrt(img_dx**2 + img_dy**2)

def binarize_image(img, threshold):
    """Binarizes an image based on a threshold."""
    return (img > threshold).astype(np.uint8) * 255

if __name__ == "__main__":
    img_path = 'data/cameraman.png'
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = img.astype(np.float32) / 255.0
    
    os.makedirs('output', exist_ok=True)
    
    # -------------------------------------------------------------
    # PART 1.2: Finite Difference Operator
    # -------------------------------------------------------------
    Dx = np.array([[1, -1]], dtype=np.float32)
    Dy = np.array([[1], [-1]], dtype=np.float32)
    
    img_dx = convolve2d(img, Dx, mode='same')
    img_dy = convolve2d(img, Dy, mode='same')
    
    grad_mag = compute_gradient_magnitude(img_dx, img_dy)
    
    # Save partial derivatives (shift by 0.5 to show negative values as dark, positive as bright)
    cv2.imwrite('output/1_2_cameraman_dx.jpg', ((img_dx + 0.5) * 255).clip(0, 255).astype(np.uint8))
    cv2.imwrite('output/1_2_cameraman_dy.jpg', ((img_dy + 0.5) * 255).clip(0, 255).astype(np.uint8))
    
    # Save gradient magnitude
    grad_mag_vis = (grad_mag * 255).clip(0, 255).astype(np.uint8)
    cv2.imwrite('output/1_2_gradient_magnitude.jpg', grad_mag_vis)
    
    # Binarize to find edges (threshold chosen qualitatively, usually around 0.15 to 0.3)
    threshold_1_2 = 0.25
    edge_img = binarize_image(grad_mag, threshold_1_2)
    cv2.imwrite('output/1_2_binarized_edges.jpg', edge_img)
    print("Success! Finished Part 1.2")
