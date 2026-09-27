import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

filter_snippet = '''
    <pre><code># 1. 9x9 Box Filter
box_filter = np.ones((9, 9), dtype=np.float32) / 81.0
img_box = conv2d_2loops(img, box_filter)

# 2. Finite Difference Operators
Dx = np.array([[1, -1]], dtype=np.float32)
Dy = np.array([[1], [-1]], dtype=np.float32)

img_dx = conv2d_2loops(img, Dx)
img_dy = conv2d_2loops(img, Dy)</code></pre>
'''

html = html.replace('<p>Using our custom engine, we ran a 9x9 box filter and the `Dx`/`Dy` finite difference operators over a custom selfie.</p>', '<p>Using our custom engine, we ran a 9x9 box filter and the `Dx`/`Dy` finite difference operators over a custom selfie using the following filters:</p>\n' + filter_snippet)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
