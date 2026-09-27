import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
from scipy.signal import convolve2d

def conv2d_4loops(image, kernel, mode='same'):
    """2D Convolution using 4 nested for-loops."""
    kernel = np.flipud(np.fliplr(kernel))
    i_h, i_w = image.shape
    k_h, k_w = kernel.shape
    pad_h = k_h // 2
    pad_w = k_w // 2
    padded_img = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)
    out_h = i_h if mode == 'same' else i_h + k_h - 1
    out_w = i_w if mode == 'same' else i_w + k_w - 1
    output = np.zeros((out_h, out_w), dtype=np.float32)
    for y in range(out_h):
        for x in range(out_w):
            for i in range(k_h):
                for j in range(k_w):
                    output[y, x] += padded_img[y + i, x + j] * kernel[i, j]
    return output

def conv2d_2loops(image, kernel, mode='same'):
    """2D Convolution using 2 nested for-loops (vectorized over the kernel)."""
    kernel = np.flipud(np.fliplr(kernel))
    i_h, i_w = image.shape
    k_h, k_w = kernel.shape
    pad_h = k_h // 2
    pad_w = k_w // 2
    padded_img = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)
    out_h = i_h if mode == 'same' else i_h + k_h - 1
    out_w = i_w if mode == 'same' else i_w + k_w - 1
    output = np.zeros((out_h, out_w), dtype=np.float32)
    for y in range(out_h):
        for x in range(out_w):
            output[y, x] = np.sum(padded_img[y:y+k_h, x:x+k_w] * kernel)
    return output

if __name__ == "__main__":
    selfie_path = 'data/selfie.jpg'
    
    if os.path.exists(selfie_path):
        print("Found selfie.jpg! Running convolutions...")
        img_path = selfie_path
    else:
        print("Could not find selfie.jpg. Falling back to cameraman.png for testing...")
        img_path = 'data/cameraman.png'
        
    # Read as grayscale and normalize
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = img.astype(np.float32) / 255.0
    
    # 1. 9x9 Box Filter
    box_filter = np.ones((9, 9), dtype=np.float32) / 81.0
    img_box = conv2d_2loops(img, box_filter)
    
    # 2. Finite Difference Operators
    Dx = np.array([[1, -1]], dtype=np.float32)
    Dy = np.array([[1], [-1]], dtype=np.float32)
    
    img_dx = conv2d_2loops(img, Dx)
    img_dy = conv2d_2loops(img, Dy)
    
    # Save results
    os.makedirs('output', exist_ok=True)
    cv2.imwrite('output/box_blur.jpg', (img_box * 255).clip(0, 255).astype(np.uint8))
    
    # Shift and scale gradients for visualization so negative values become visible (gray background)
    dx_vis = ((img_dx + 0.5) * 255).clip(0, 255).astype(np.uint8)
    dy_vis = ((img_dy + 0.5) * 255).clip(0, 255).astype(np.uint8)
    
    cv2.imwrite('output/dx_edge.jpg', dx_vis)
    cv2.imwrite('output/dy_edge.jpg', dy_vis)
    
    print("Success! Saved box_blur.jpg, dx_edge.jpg, and dy_edge.jpg to the 'output' folder.")
