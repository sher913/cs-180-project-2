import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

p21_addition = '''
    <div class="gallery">
        <div class="gallery-item">
            <img src="data/taj.jpg" alt="Original Taj">
            <p>Original Taj Mahal</p>
        </div>
        <div class="gallery-item">
            <img src="output/2_1_taj_blurred.jpg" alt="Blurred Taj">
            <p>Gaussian Blurred</p>
        </div>
        <div class="gallery-item">
            <img src="output/2_1_taj_highfreq.jpg" alt="High Freq Taj">
            <p>High Frequencies (Original - Blurred)</p>
        </div>
        <div class="gallery-item">
            <img src="output/2_1_taj_sharpened_a2.0.jpg" alt="Sharpened Taj">
            <p>Sharpened (Alpha = 2.0)</p>
        </div>
    </div>

    <p>We also tested varying amounts of sharpening on another image (Coffee).</p>
    <div class="gallery">
        <div class="gallery-item">
            <img src="data/coffee.jpg" alt="Original Coffee">
            <p>Original Coffee</p>
        </div>
        <div class="gallery-item">
            <img src="output/2_1_coffee_a1.0.jpg" alt="Coffee a1">
            <p>Sharpened (Alpha = 1.0)</p>
        </div>
        <div class="gallery-item">
            <img src="output/2_1_coffee_a3.0.jpg" alt="Coffee a3">
            <p>Sharpened (Alpha = 3.0)</p>
        </div>
        <div class="gallery-item">
            <img src="output/2_1_coffee_a5.0.jpg" alt="Coffee a5">
            <p>Sharpened (Alpha = 5.0)</p>
        </div>
    </div>
'''

pattern = r'<div class="gallery">\s*<div class="gallery-item">\s*<img src="data/taj\.jpg" alt="Original Taj">\s*<p>Original Taj Mahal</p>\s*</div>\s*<div class="gallery-item">\s*<img src="output/2_1_taj_sharpened_a2\.0\.jpg" alt="Sharpened Taj">\s*<p>Sharpened \(Alpha = 2\.0\)</p>\s*</div>\s*</div>'

html = re.sub(pattern, p21_addition, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
