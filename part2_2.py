import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
import os

sys.path.append('cs180_proj2_hybrid_starter_code')
from align_image_code import align_image_centers, rescale_images, rotate_im1, match_img_size

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

def compute_fft(image):
    if len(image.shape) == 3:
        image = cv2.cvtColor((image*255).astype(np.uint8), cv2.COLOR_BGR2GRAY) / 255.0
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = np.log(np.abs(fshift) + 1e-8)
    return magnitude_spectrum

def create_hybrid_image(im1, im2, sigma1, sigma2):
    """
    im1: High frequency image
    im2: Low frequency image
    """
    # Low pass filter im2
    ksize2 = int(6 * sigma2) | 1
    low_frequencies = apply_gaussian(im2, ksize2, sigma2)
    
    # High pass filter im1
    ksize1 = int(6 * sigma1) | 1
    im1_blurred = apply_gaussian(im1, ksize1, sigma1)
    high_frequencies = im1 - im1_blurred
    
    # Combine
    hybrid = np.clip(low_frequencies + high_frequencies, 0, 1)
    
    return high_frequencies, low_frequencies, hybrid

def align_images_headless(im1, im2):
    # Hardcoded points derived from true visual verification
    # Nutmeg: Left eye (our left), Right eye
    p1, p2 = (610, 290), (740, 350)
    # Derek: Left eye (our left), Right eye
    p3, p4 = (305, 330), (445, 330)
    pts = (p1, p2, p3, p4)
    
    im1, im2 = align_image_centers(im1, im2, pts)
    im1, im2 = rescale_images(im1, im2, pts)
    im1, angle = rotate_im1(im1, pts)
    im1, im2 = match_img_size(im1, im2)
    return im1, im2

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--headless', action='store_true')
    args = parser.parse_args()

    # Load Derek and Nutmeg (Nutmeg is high freq, Derek is low freq)
    im1 = cv2.imread('data/nutmeg.jpg')[:, :, ::-1] / 255.0 # High freq
    im2 = cv2.imread('cs180_proj2_hybrid_starter_code/DerekPicture.jpg')[:, :, ::-1] / 255.0 # Low freq
    
    if args.headless:
        print("Running in headless mode with hardcoded points...")
        im1_aligned, im2_aligned = align_images_headless(im1, im2)
    else:
        print("Interactive mode: Please click 2 points on each image.")
        from align_image_code import align_images
        im1_aligned, im2_aligned = align_images(im1, im2)
        
    sigma1 = 5.0 # High freq cutoff
    sigma2 = 7.0 # Low freq cutoff
    
    high_freq, low_freq, hybrid = create_hybrid_image(im1_aligned, im2_aligned, sigma1, sigma2)
    
    os.makedirs('output', exist_ok=True)
    
    # Save images (convert RGB to BGR for cv2)
    cv2.imwrite('output/2_2_aligned_high_freq.jpg', (im1_aligned[:, :, ::-1] * 255).astype(np.uint8))
    cv2.imwrite('output/2_2_aligned_low_freq.jpg', (im2_aligned[:, :, ::-1] * 255).astype(np.uint8))
    cv2.imwrite('output/2_2_high_freq_component.jpg', ((high_freq[:, :, ::-1] + 0.5) * 255).clip(0, 255).astype(np.uint8))
    cv2.imwrite('output/2_2_low_freq_component.jpg', (low_freq[:, :, ::-1] * 255).astype(np.uint8))
    cv2.imwrite('output/2_2_hybrid.jpg', (hybrid[:, :, ::-1] * 255).astype(np.uint8))
    
    # Save FFTs
    fft_im1 = compute_fft(im1_aligned)
    fft_im2 = compute_fft(im2_aligned)
    fft_hf = compute_fft((high_freq + 0.5).clip(0, 1))
    fft_lf = compute_fft(low_freq)
    fft_hybrid = compute_fft(hybrid)
    
    fig, axes = plt.subplots(1, 5, figsize=(20, 4))
    axes[0].imshow(fft_im1, cmap='gray'); axes[0].set_title('Im1 (High) FFT')
    axes[1].imshow(fft_im2, cmap='gray'); axes[1].set_title('Im2 (Low) FFT')
    axes[2].imshow(fft_hf, cmap='gray'); axes[2].set_title('High-Freq Filtered FFT')
    axes[3].imshow(fft_lf, cmap='gray'); axes[3].set_title('Low-Freq Filtered FFT')
    axes[4].imshow(fft_hybrid, cmap='gray'); axes[4].set_title('Hybrid FFT')
    for ax in axes: ax.axis('off')
    plt.tight_layout()
    plt.savefig('output/2_2_fourier_analysis.jpg')
    
    print("Success! Saved hybrid images and Fourier transforms to 'output' folder.")
