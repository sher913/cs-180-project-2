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
    
    Dx = np.array([[1, -1]], dtype=np.float32)
    Dy = np.array([[1], [-1]], dtype=np.float32)

    # -------------------------------------------------------------
    # PART 1.3: Derivative of Gaussian (DoG) Filter
    # -------------------------------------------------------------
    # Create 2D Gaussian kernel
    ksize = 11
    sigma = 2.0
    gaussian_1d = cv2.getGaussianKernel(ksize, sigma)
    gaussian_2d = gaussian_1d @ gaussian_1d.T
    
    # Approach A: Blur then difference
    img_blurred = convolve2d(img, gaussian_2d, mode='same')
    
    img_blurred_dx = convolve2d(img_blurred, Dx, mode='same')
    img_blurred_dy = convolve2d(img_blurred, Dy, mode='same')
    
    grad_mag_blur = compute_gradient_magnitude(img_blurred_dx, img_blurred_dy)
    
    # Binarize with a lower threshold since blurring reduces gradient magnitude
    threshold_1_3 = 0.08
    edge_img_blur = binarize_image(grad_mag_blur, threshold_1_3)
    
    cv2.imwrite('output/1_3_blurred_gradient_magnitude.jpg', (grad_mag_blur * 255).clip(0, 255).astype(np.uint8))
    cv2.imwrite('output/1_3_blurred_binarized_edges.jpg', edge_img_blur)
    
    # Approach B: Derivative of Gaussian (DoG) filters
    DoG_x = convolve2d(gaussian_2d, Dx, mode='full')
    DoG_y = convolve2d(gaussian_2d, Dy, mode='full')
    
    # Save DoG filters as images to visualize them
    cv2.imwrite('output/1_3_DoG_x_filter.jpg', ((DoG_x / np.max(np.abs(DoG_x)) * 0.5 + 0.5) * 255).clip(0, 255).astype(np.uint8))
    cv2.imwrite('output/1_3_DoG_y_filter.jpg', ((DoG_y / np.max(np.abs(DoG_y)) * 0.5 + 0.5) * 255).clip(0, 255).astype(np.uint8))
    
    img_dog_dx = convolve2d(img, DoG_x, mode='same')
    img_dog_dy = convolve2d(img, DoG_y, mode='same')
    
    grad_mag_dog = compute_gradient_magnitude(img_dog_dx, img_dog_dy)
    edge_img_dog = binarize_image(grad_mag_dog, threshold_1_3)
    
    cv2.imwrite('output/1_3_DoG_gradient_magnitude.jpg', (grad_mag_dog * 255).clip(0, 255).astype(np.uint8))
    cv2.imwrite('output/1_3_DoG_binarized_edges.jpg', edge_img_dog)
    
    # Verify they are the same
    # We ignore the outermost 15 pixels since border handling double-padding vs single-padding introduces edge differences
    diff = np.max(np.abs(grad_mag_blur[15:-15, 15:-15] - grad_mag_dog[15:-15, 15:-15]))
    print(f"Difference between (Blur -> Diff) and (DoG Filter) in image interior: {diff}")
    
    print("Success! Finished Part 1.3")
