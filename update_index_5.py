import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

p11_addition = '''
    <p><strong>Runtime & Boundaries:</strong> Comparing our implementation with <code>scipy.signal.convolve2d</code>, the runtime difference is staggering. Our nested loops in Python run in O(N*M*K*L) which takes several seconds per image, whereas Scipy relies on highly-optimized C code that finishes almost instantly. For boundary handling, our implementation uses zero-padding (<code>mode='constant'</code>), which artificially darkens the edges of the image. Scipy offers padding modes like <code>'symm'</code> or <code>'boundary'</code> which mirror or extend the edge pixels, preventing artificial dark borders.</p>
'''

html = html.replace('return output</code></pre>', 'return output</code></pre>\n' + p11_addition)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
