import numpy as np
import cv2
import os

def get_gaussian_kernel(ksize, sigma):
    g1d = cv2.getGaussianKernel(ksize, sigma)
    return g1d @ g1d.T

def apply_gaussian(img, ksize, sigma):
    kernel = get_gaussian_kernel(ksize, sigma)
    if len(img.shape) == 3:
        out = np.zeros_like(img)
        for c in range(3):
            out[:, :, c] = cv2.filter2D(img[:, :, c], -1, kernel)
        return out
    else:
        return cv2.filter2D(img, -1, kernel)

def build_gaussian_stack(img, depth=5):
    """Builds a Gaussian stack without downsampling."""
    stack = [img]
    # We progressively increase sigma and kernel size to simulate downsampling
    sigma = 2.0
    for i in range(1, depth):
        ksize = int(6 * sigma) | 1
        blurred = apply_gaussian(stack[-1], ksize, sigma)
        stack.append(blurred)
        sigma *= 2.0
    return stack

def build_laplacian_stack(gaussian_stack):
    """Builds a Laplacian stack from a Gaussian stack."""
    depth = len(gaussian_stack)
    laplacian_stack = []
    for i in range(depth - 1):
        # L_i = G_i - G_{i+1}
        laplacian_stack.append(gaussian_stack[i] - gaussian_stack[i+1])
    # The last level is just the last Gaussian
    laplacian_stack.append(gaussian_stack[-1])
    return laplacian_stack

def blend_images(im1, im2, mask, depth=5):
    """Blends im1 and im2 using multiresolution blending according to mask."""
    # 1. Build Laplacian stacks for images
    g_stack1 = build_gaussian_stack(im1, depth)
    l_stack1 = build_laplacian_stack(g_stack1)
    
    g_stack2 = build_gaussian_stack(im2, depth)
    l_stack2 = build_laplacian_stack(g_stack2)
    
    # 2. Build Gaussian stack for mask
    mask_stack = build_gaussian_stack(mask, depth)
    
    # 3. Blend at each level
    blended_l_stack = []
    for i in range(depth):
        # L_out = L1 * mask + L2 * (1 - mask)
        level_blend = l_stack1[i] * mask_stack[i] + l_stack2[i] * (1 - mask_stack[i])
        blended_l_stack.append(level_blend)
        
    # 4. Collapse the stack
    out = np.zeros_like(im1)
    for i in range(depth):
        out += blended_l_stack[i]
        
    return np.clip(out, 0, 1), blended_l_stack, mask_stack

if __name__ == "__main__":
    apple_path = 'data/apple.jpeg'
    orange_path = 'data/orange.jpeg'
    
    if not os.path.exists(apple_path) or not os.path.exists(orange_path):
        print("Could not find apple/orange. Falling back to cameraman and taj for testing...")
        apple_path = 'data/cameraman.png'
        orange_path = 'data/taj.jpg'
        
    apple = cv2.imread(apple_path)
    orange = cv2.imread(orange_path)
    
    # If they are grayscale, convert to BGR so we can process them uniformly
    if len(apple.shape) == 2:
        apple = cv2.cvtColor(apple, cv2.COLOR_GRAY2BGR)
    if len(orange.shape) == 2:
        orange = cv2.cvtColor(orange, cv2.COLOR_GRAY2BGR)
        
    apple = apple[:, :, ::-1].astype(np.float32) / 255.0
    orange = orange[:, :, ::-1].astype(np.float32) / 255.0
    
    # Make sure they are the same size
    h, w = apple.shape[:2]
    orange = cv2.resize(orange, (w, h))
    
    # Create vertical mask for Oraple
    mask = np.zeros_like(apple)
    mask[:, :w//2, :] = 1.0
    
    blended, l_stack, mask_stack = blend_images(apple, orange, mask, depth=6)
    
    os.makedirs('output', exist_ok=True)
    cv2.imwrite('output/2_4_oraple.jpg', (blended[:, :, ::-1] * 255).astype(np.uint8))
    
    # Visualize the Laplacian stack for the Oraple as requested in 2.3
    # We will save the different levels of the blended Laplacian stack
    for i in range(len(l_stack)):
        # Shift by 0.5 to visualize negative values, except for the last level which is a Gaussian
        vis = l_stack[i] if i == len(l_stack)-1 else np.clip(l_stack[i] + 0.5, 0, 1)
        cv2.imwrite(f'output/2_3_oraple_level_{i}.jpg', (vis[:, :, ::-1] * 255).astype(np.uint8))
        
    print("Success! Created the Oraple and saved Laplacian stack visualizations.")
