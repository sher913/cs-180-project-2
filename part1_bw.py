import numpy as np
import cv2
import os
from scipy.signal import convolve2d
import matplotlib.pyplot as plt

def compute_gradient_orientation(img_dx, img_dy):
    """Computes the gradient orientation (angle) from dx and dy."""
    # np.arctan2 returns values in [-pi, pi]
    angle = np.arctan2(img_dy, img_dx)
    return angle

if __name__ == "__main__":
    img_path = 'data/cameraman.png'
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = img.astype(np.float32) / 255.0
    
    # Derivative of Gaussian (DoG) filters
    Dx = np.array([[1, -1]], dtype=np.float32)
    Dy = np.array([[1], [-1]], dtype=np.float32)
    
    ksize = 11
    sigma = 2.0
    gaussian_1d = cv2.getGaussianKernel(ksize, sigma)
    gaussian_2d = gaussian_1d @ gaussian_1d.T
    
    DoG_x = convolve2d(gaussian_2d, Dx, mode='full')
    DoG_y = convolve2d(gaussian_2d, Dy, mode='full')
    
    print("Computing gradients...")
    img_dog_dx = convolve2d(img, DoG_x, mode='same')
    img_dog_dy = convolve2d(img, DoG_y, mode='same')
    
    grad_mag = np.sqrt(img_dog_dx**2 + img_dog_dy**2)
    grad_angle = compute_gradient_orientation(img_dog_dx, img_dog_dy)
    
    # -------------------------------------------------------------
    # Bells & Whistles: Visualize Gradient Orientation using HSV
    # -------------------------------------------------------------
    print("Mapping to HSV...")
    # Map angle from [-pi, pi] to [0, 179] for OpenCV Hue
    hue = ((grad_angle + np.pi) / (2 * np.pi) * 179).astype(np.uint8)
    
    # Saturation is fully saturated (255)
    saturation = np.ones_like(hue) * 255
    
    # Value is the gradient magnitude, normalized to [0, 255]
    print("Calculating percentiles...")
    val_max = np.percentile(grad_mag, 99.5)
    value = (np.clip(grad_mag / val_max, 0, 1) * 255).astype(np.uint8)
    
    print("Merging HSV...")
    # Merge into an HSV image and convert to BGR for saving
    hsv_img = cv2.merge([hue, saturation, value])
    bgr_img = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)
    
    os.makedirs('output', exist_ok=True)
    cv2.imwrite('output/1_BW_gradient_orientation.jpg', bgr_img)
    
    print("Generating color legend...")
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    
    fig = plt.figure(figsize=(4, 4))
    ax = fig.add_subplot(111, projection='polar')
    theta = np.linspace(0, 2*np.pi, 100)
    r = np.linspace(0, 1, 100)
    T, R = np.meshgrid(theta, r)
    Z = T
    ax.pcolormesh(T, R, Z, cmap='hsv', shading='auto')
    ax.set_yticklabels([])
    plt.title('Color Legend for Gradient Direction')
    plt.savefig('output/1_BW_color_legend.jpg')
    plt.close()
    
    print("Success! Saved Bells & Whistles gradient orientation visualization.")
