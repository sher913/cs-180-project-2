import numpy as np
import cv2
import os
from scipy.signal import convolve2d

def get_gaussian_kernel(ksize, sigma):
    g1d = cv2.getGaussianKernel(ksize, sigma)
    return g1d @ g1d.T

def unsharp_mask_filter(ksize, sigma, alpha):
    """Creates a single unsharp masking 2D filter."""
    gaussian = get_gaussian_kernel(ksize, sigma)
    impulse = np.zeros_like(gaussian)
    impulse[ksize//2, ksize//2] = 1.0
    
    return (1 + alpha) * impulse - alpha * gaussian

def sharpen_image(img_path, alpha=1.5, ksize=11, sigma=2.0, out_prefix=''):
    img = cv2.imread(img_path)
    if img is None:
        print(f"Failed to load {img_path}")
        return
        
    img_float = img.astype(np.float32) / 255.0
    
    # We will process each color channel independently
    sharpened = np.zeros_like(img_float)
    filter_2d = unsharp_mask_filter(ksize, sigma, alpha)
    
    # Apply to each channel
    for c in range(3):
        sharpened[:, :, c] = convolve2d(img_float[:, :, c], filter_2d, mode='same')
        
    # Clip and convert back to 8-bit
    sharpened_vis = (np.clip(sharpened, 0, 1) * 255).astype(np.uint8)
    
    os.makedirs('output', exist_ok=True)
    out_name = f"output/2_1_{out_prefix}_sharpened_a{alpha}.jpg"
    cv2.imwrite(out_name, sharpened_vis)
    print(f"Saved {out_name}")

if __name__ == "__main__":
    # Taj Mahal sharpening (blurry -> sharp)
    sharpen_image('data/taj.jpg', alpha=2.0, ksize=15, sigma=3.0, out_prefix='taj')
    
    # Evaluation: Sharp -> Blur -> Sharpen
    # We'll use the selfie image if it exists, otherwise cameraman
    eval_path = 'data/selfie.jpg'
    if not os.path.exists(eval_path):
        eval_path = 'data/cameraman.png'
        
    print(f"Using {eval_path} for sharp->blur->sharpen evaluation")
    img = cv2.imread(eval_path)
    if img is not None:
        img_float = img.astype(np.float32) / 255.0
        
        # Step 1: Blur the originally sharp image
        g = get_gaussian_kernel(15, 3.0)
        blurred = np.zeros_like(img_float)
        for c in range(img_float.shape[2] if len(img_float.shape) == 3 else 1):
            if len(img_float.shape) == 3:
                blurred[:, :, c] = convolve2d(img_float[:, :, c], g, mode='same')
            else:
                blurred = convolve2d(img_float, g, mode='same')
                
        blur_vis = (np.clip(blurred, 0, 1) * 255).astype(np.uint8)
        cv2.imwrite('output/2_1_eval_blurred.jpg', blur_vis)
        
        # Step 2: Sharpen the blurred image
        sharpened = np.zeros_like(img_float)
        unsharp_filter = unsharp_mask_filter(15, 3.0, alpha=3.0)
        
        for c in range(img_float.shape[2] if len(img_float.shape) == 3 else 1):
            if len(img_float.shape) == 3:
                sharpened[:, :, c] = convolve2d(blurred[:, :, c], unsharp_filter, mode='same')
            else:
                sharpened = convolve2d(blurred, unsharp_filter, mode='same')
                
        sharp_vis = (np.clip(sharpened, 0, 1) * 255).astype(np.uint8)
        cv2.imwrite('output/2_1_eval_resharpened.jpg', sharp_vis)
        
        print("Saved sharp->blur->sharpen evaluation images.")
    
    print("Success! Completed Part 2.1")
