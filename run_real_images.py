import numpy as np
import cv2
import os
from part2_2 import create_hybrid_image, compute_fft
from part2_3 import blend_images

def center_crop_and_resize(img1, img2, size=(800, 800)):
    def crop_center(img):
        h, w = img.shape[:2]
        min_dim = min(h, w)
        start_x = w//2 - min_dim//2
        start_y = h//2 - min_dim//2
        return img[start_y:start_y+min_dim, start_x:start_x+min_dim]
        
    img1_c = cv2.resize(crop_center(img1), size)
    img2_c = cv2.resize(crop_center(img2), size)
    return img1_c, img2_c

def create_circular_mask(h, w, center, radius):
    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y - center[1])**2)
    mask = dist_from_center <= radius
    return mask.astype(np.float32)

if __name__ == "__main__":
    os.makedirs('output', exist_ok=True)
    
    # Tiger and Cat removed by user request
    import sys
    sys.path.append('cs180_proj2_hybrid_starter_code')
    from align_image_code import align_image_centers, rescale_images, rotate_im1, match_img_size
    
    # -------------------------------------------------------------
    # 2. Real Hybrid Pair 2: Earth (High Freq) + Mars (Low Freq)
    # -------------------------------------------------------------
    earth = cv2.imread('data/earth.jpg')[:, :, ::-1].astype(np.float32) / 255.0
    mars = cv2.imread('data/mars.jpg')[:, :, ::-1].astype(np.float32) / 255.0
    
    # Earth center and right edge
    p1, p2 = (600, 630), (1170, 630)
    # Mars center and right edge
    p3, p4 = (625, 625), (1180, 625)
    pts2 = (p1, p2, p3, p4)
    
    earth_a, mars_a = align_image_centers(earth, mars, pts2)
    earth_a, mars_a = rescale_images(earth_a, mars_a, pts2)
    earth_a, mars_a = match_img_size(earth_a, mars_a)
    
    high_freq, low_freq, hybrid = create_hybrid_image(earth_a, mars_a, sigma1=5.0, sigma2=10.0)
    cv2.imwrite('output/2_2_real_hybrid_earth_mars.jpg', (hybrid[:, :, ::-1] * 255).astype(np.uint8))
    print("Created Aligned Hybrid Earth/Mars")
    
    # -------------------------------------------------------------
    # 2.5 Real Hybrid Pair 3: Su Ying (High Freq) + Lord Farquaad (Low Freq)
    # -------------------------------------------------------------
    suying = cv2.imread('data/su ying.webp')[:, :, ::-1].astype(np.float32) / 255.0
    farquaad = cv2.imread('data/lord farquaad.webp')[:, :, ::-1].astype(np.float32) / 255.0
    
    # Su Ying eyes (im1)
    p1, p2 = (220, 250), (340, 250)
    # Farquaad eyes (im2)
    p3, p4 = (600, 335), (700, 335)
    pts3 = (p1, p2, p3, p4)
    
    suying_a, farquaad_a = align_image_centers(suying, farquaad, pts3)
    suying_a, farquaad_a = rescale_images(suying_a, farquaad_a, pts3)
    suying_a, angle = rotate_im1(suying_a, pts3)
    suying_a, farquaad_a = match_img_size(suying_a, farquaad_a)
    
    high_freq3, low_freq3, hybrid3 = create_hybrid_image(suying_a, farquaad_a, sigma1=3.0, sigma2=6.0)
    cv2.imwrite('output/2_2_real_hybrid_lord_fuhhh.jpg', (hybrid3[:, :, ::-1] * 255).astype(np.uint8))
    print("Created Aligned Hybrid Lord FUHHH")

    # -------------------------------------------------------------
    # 3. Real Blending 1: Apple + Orange (Oraple, Regular Mask)
    # -------------------------------------------------------------
    apple = cv2.imread('data/apple.jpeg')[:, :, ::-1].astype(np.float32) / 255.0
    orange = cv2.imread('data/orange.jpeg')[:, :, ::-1].astype(np.float32) / 255.0
    apple, orange = center_crop_and_resize(apple, orange, (600, 600))
    
    # Vertical mask
    mask_2d = np.zeros((600, 600), dtype=np.float32)
    mask_2d[:, :300] = 1.0
    mask = np.stack([mask_2d]*3, axis=2)
    
    blended, _, _ = blend_images(apple, orange, mask, depth=6)
    cv2.imwrite('output/2_4_real_oraple.jpg', (blended[:, :, ::-1] * 255).astype(np.uint8))
    print("Created real Oraple (Apple + Orange)")

    # -------------------------------------------------------------
    # 4. Real Blending 2: Sun + Moon (Irregular Circular Mask)
    # -------------------------------------------------------------
    sun = cv2.imread('data/sun.jpg')[:, :, ::-1].astype(np.float32) / 255.0
    moon = cv2.imread('data/moon.jpg')[:, :, ::-1].astype(np.float32) / 255.0
    sun, moon = center_crop_and_resize(sun, moon, (800, 800))
    
    # Circular mask
    mask_2d = create_circular_mask(800, 800, (400, 400), 200)
    mask = np.stack([mask_2d]*3, axis=2)
    
    blended, _, _ = blend_images(sun, moon, mask, depth=6)
    cv2.imwrite('output/2_4_real_sun_moon.jpg', (blended[:, :, ::-1] * 255).astype(np.uint8))
    print("Created real Sun/Moon blend with irregular mask")
