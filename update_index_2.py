import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

p24_addition = '''
        <div class="gallery-item">
            <img src="output/2_4_winter_summer.jpg" alt="Winter Summer Blend">
            <p><strong>Winter & Summer</strong><br>Diagonal Mask</p>
        </div>
'''

html = html.replace('<div class="gallery-item">\n            <img src="output/2_4_real_sun_moon.jpg" alt="Sun Moon Blend">\n            <p><strong>The Sun & Moon</strong><br>Irregular Circular Mask</p>\n        </div>', '<div class="gallery-item">\n            <img src="output/2_4_real_sun_moon.jpg" alt="Sun Moon Blend">\n            <p><strong>The Sun & Moon</strong><br>Irregular Circular Mask</p>\n        </div>' + p24_addition)

bw_24_learned = '''
    <h3>Bells & Whistles: Colorful Multiresolution Blending</h3>
    <p>For the multiresolution blending, we extended the 1D Gaussian and Laplacian stacks to operate across all 3 color channels (RGB) independently. By building identical masks for each channel, we successfully preserved the vibrant colors of the Apple, Orange, Sun, Moon, and Seasons without any color fringing at the boundaries. Blending in RGB space turned out to be extremely effective because the low-frequency color bleeds match the high-frequency texture seams perfectly, creating a highly realistic fusion.</p>

    <h2>What I Learned</h2>
    <p>The most important thing I learned from this project is the sheer power of frequency decomposition in human visual perception. I never realized that our eyes naturally filter images by distance - prioritizing high-frequency edges up close, but relying entirely on low-frequency blobs and color gradients from afar. Being able to mathematically pull apart an image into its frequency bands using simple Gaussian convolutions, and then recombine them to trick the human brain (like in the Hybrid Images) or seamlessly stitch two un-alike objects (like the Oraple) was mind-blowing to see in practice!</p>
</div>
</body>
</html>
'''

html = re.sub(r'</div>\s*<br><br>\s*</body>\s*</html>', bw_24_learned, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
