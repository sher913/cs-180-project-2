import numpy as np
import cv2
import os
from part2_2 import create_hybrid_image, compute_fft
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

if __name__ == "__main__":
    skull = cv2.imread('data/skull.jpg')[:, :, ::-1].astype(np.float32) / 255.0
    face = cv2.imread('data/face.jpg')[:, :, ::-1].astype(np.float32) / 255.0
    
    # Resize skull to face exactly
    h, w = face.shape[:2]
    skull = cv2.resize(skull, (w, h))
    
    # We want skull as high frequency (so you only see it up close)
    # Face as low frequency (so you see it from far away)
    # Wait, usually skull is seen far away? No, we'll do:
    # High freq: Skull
    # Low freq: Face
    
    sigma1 = 7.0 # High freq cutoff
    sigma2 = 10.0 # Low freq cutoff
    
    high_freq, low_freq, hybrid = create_hybrid_image(skull, face, sigma1, sigma2)
    
    os.makedirs('output', exist_ok=True)
    
    cv2.imwrite('output/2_2_custom_hybrid.jpg', (hybrid[:, :, ::-1] * 255).astype(np.uint8))
    
    print("Successfully created custom Hybrid image!")
