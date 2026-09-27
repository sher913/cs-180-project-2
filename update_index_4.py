import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

replacement = '''
    <p><strong>Example 2: SY & Lord Farquaad (Lord FUHHH)</strong></p>
    
    <div style="display: flex; flex-direction: column; align-items: center; gap: 30px; background-color: #1a1a1a; padding: 30px; border-radius: 12px; border: 1px solid #333; margin-bottom: 40px;">
        <div style="display: flex; flex-direction: row; justify-content: center; gap: 20px; flex-wrap: wrap; width: 100%;">
            <div style="text-align: center; flex: 1; min-width: 150px; max-width: 250px;">
                <img src="output/high_aligned.jpg" alt="SY Aligned" style="width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.4);">
                <p style="color: #bbb; margin-top: 10px; font-size: 0.95rem;">SY (Aligned)</p>
            </div>
            <div style="text-align: center; flex: 1; min-width: 150px; max-width: 250px;">
                <img src="output/high_pass.jpg" alt="SY High Pass" style="width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.4);">
                <p style="color: #bbb; margin-top: 10px; font-size: 0.95rem;">High Pass Filter</p>
            </div>
            <div style="text-align: center; flex: 1; min-width: 150px; max-width: 250px;">
                <img src="output/low_aligned.jpg" alt="Farquaad Aligned" style="width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.4);">
                <p style="color: #bbb; margin-top: 10px; font-size: 0.95rem;">Farquaad (Aligned)</p>
            </div>
            <div style="text-align: center; flex: 1; min-width: 150px; max-width: 250px;">
                <img src="output/low_pass.jpg" alt="Farquaad Low Pass" style="width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.4);">
                <p style="color: #bbb; margin-top: 10px; font-size: 0.95rem;">Low Pass Filter</p>
            </div>
        </div>

        <div style="text-align: center; width: 100%; max-width: 600px; margin-top: 10px;">
            <img src="output/hybrid_result_lord%20fuhhh.jpg" alt="Lord FUHHH Hybrid" style="width: 100%; border-radius: 8px; border: 2px solid #555; box-shadow: 0 8px 24px rgba(0,0,0,0.8);">
            <p style="margin-top: 15px; font-size: 1.15rem; color: #fff;"><em><strong>Final Hybrid:</strong> Up close SY | Far away Farquaad</em></p>
        </div>
    </div>
'''

html = re.sub(r'<p><strong>Example 2: SY & Lord Farquaad \(Lord FUHHH\)</strong></p>.*?(?=<p><strong>Example 3: Earth & Mars \(Change over time/planets\)</strong></p>)', replacement + '\n\n', html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
