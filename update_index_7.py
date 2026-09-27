import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

stacks_addition = '''
    <p>We also computed the Laplacian stacks for the original Apple and Orange images prior to blending them.</p>
    
    <div class="row-gallery">
        <div class="gallery-item"><img src="output/2_3_apple_laplacian_0.jpg"><p>Apple L0</p></div>
        <div class="gallery-item"><img src="output/2_3_apple_laplacian_1.jpg"><p>Apple L1</p></div>
        <div class="gallery-item"><img src="output/2_3_apple_laplacian_2.jpg"><p>Apple L2</p></div>
        <div class="gallery-item"><img src="output/2_3_apple_laplacian_3.jpg"><p>Apple L3</p></div>
        <div class="gallery-item"><img src="output/2_3_apple_laplacian_4.jpg"><p>Apple L4</p></div>
        <div class="gallery-item"><img src="output/2_3_apple_laplacian_5.jpg"><p>Apple L5</p></div>
    </div>
    
    <div class="row-gallery">
        <div class="gallery-item"><img src="output/2_3_orange_laplacian_0.jpg"><p>Orange L0</p></div>
        <div class="gallery-item"><img src="output/2_3_orange_laplacian_1.jpg"><p>Orange L1</p></div>
        <div class="gallery-item"><img src="output/2_3_orange_laplacian_2.jpg"><p>Orange L2</p></div>
        <div class="gallery-item"><img src="output/2_3_orange_laplacian_3.jpg"><p>Orange L3</p></div>
        <div class="gallery-item"><img src="output/2_3_orange_laplacian_4.jpg"><p>Orange L4</p></div>
        <div class="gallery-item"><img src="output/2_3_orange_laplacian_5.jpg"><p>Orange L5</p></div>
    </div>
'''

html = html.replace('        <div class="gallery-item"><img src="output/2_3_oraple_level_5.jpg"><p>Level 5 (Lowest Freq)</p></div>\n    </div>', '        <div class="gallery-item"><img src="output/2_3_oraple_level_5.jpg"><p>Level 5 (Lowest Freq)</p></div>\n    </div>\n' + stacks_addition)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
