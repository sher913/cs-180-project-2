import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

replacement = '''
    <p><strong>Example 2: SY & Lord Farquaad (Lord FUHHH)</strong></p>
    
    <div class="gallery">
        <div class="gallery-item">
            <img src="output/high_aligned.jpg" alt="SY Aligned">
            <p>SY (Aligned)</p>
        </div>
        <div class="gallery-item">
            <img src="output/high_pass.jpg" alt="SY High Pass">
            <p>High Pass Filter</p>
        </div>
        <div class="gallery-item">
            <img src="output/low_aligned.jpg" alt="Farquaad Aligned">
            <p>Lord Farquaad (Aligned)</p>
        </div>
        <div class="gallery-item">
            <img src="output/low_pass.jpg" alt="Farquaad Low Pass">
            <p>Low Pass Filter</p>
        </div>
    </div>

    <div class="large-img">
        <img src="output/hybrid_result_lord%20fuhhh.jpg" alt="Lord FUHHH Hybrid" style="max-width: 500px;">
        <p><em>Up close: SY | Far away: Lord Farquaad</em></p>
    </div>
'''

pattern = r'<p><strong>Example 2: SY & Lord Farquaad \(Lord FUHHH\)</strong></p>\s*<div class="large-img">\s*<img src="output/2_2_real_hybrid_lord_fuhhh\.jpg" alt="Lord FUHHH Hybrid" style="max-width: 500px;">\s*<p><em>Up close: SY \| Far away: Lord Farquaad</em></p>\s*</div>'

html = re.sub(pattern, replacement, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
