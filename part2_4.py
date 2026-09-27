import numpy as np
import cv2
import os
from part2_3 import blend_images

def create_circular_mask(h, w, center, radius):
    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y - center[1])**2)
    mask = dist_from_center <= radius
    return mask.astype(np.float32)

if __name__ == "__main__":
    os.makedirs('output', exist_ok=True)
    
    # -------------------------------------------------------------
    # Custom Blend 1: Irregular Mask (Galaxy Coffee)
    # -------------------------------------------------------------
    coffee = cv2.imread('data/coffee.jpg')
    galaxy = cv2.imread('data/galaxy.jpg')
    
    if coffee is not None and galaxy is not None:
        coffee = coffee[:, :, ::-1].astype(np.float32) / 255.0
        galaxy = galaxy[:, :, ::-1].astype(np.float32) / 255.0
        
        # Resize galaxy to match coffee
        h, w = coffee.shape[:2]
        galaxy = cv2.resize(galaxy, (w, h))
        
        # Create a circular mask for the coffee cup liquid (approximate center and radius)
        # Assuming the generated coffee cup is centered
        center = (w // 2, h // 2)
        radius = int(min(h, w) * 0.3)
        
        mask_2d = create_circular_mask(h, w, center, radius)
        mask = np.stack([mask_2d]*3, axis=2)
        
        # Blend galaxy into coffee
        blended_coffee, _, _ = blend_images(galaxy, coffee, mask, depth=6)
        cv2.imwrite('output/2_4_custom_irregular_galaxy_coffee.jpg', (blended_coffee[:, :, ::-1] * 255).astype(np.uint8))
        print("Successfully created Galaxy Coffee with irregular mask!")
        
    # -------------------------------------------------------------
    # Custom Blend 2: Regular Mask (Summer / Winter transition)
    # -------------------------------------------------------------
    summer = cv2.imread('data/summer.jpg')
    winter = cv2.imread('data/winter.jpg')
    
    if summer is not None and winter is not None:
        summer = summer[:, :, ::-1].astype(np.float32) / 255.0
        winter = winter[:, :, ::-1].astype(np.float32) / 255.0
        
        h, w = summer.shape[:2]
        winter = cv2.resize(winter, (w, h))
        
        # Create a diagonal split mask
        Y, X = np.ogrid[:h, :w]
        mask_2d = (X > Y).astype(np.float32)
        mask = np.stack([mask_2d]*3, axis=2)
        
        blended_seasons, _, _ = blend_images(summer, winter, mask, depth=6)
        cv2.imwrite('output/2_4_custom_regular_seasons.jpg', (blended_seasons[:, :, ::-1] * 255).astype(np.uint8))
        print("Successfully created Summer/Winter with regular diagonal mask!")
        
