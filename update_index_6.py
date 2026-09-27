import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

replacement = '''
    <p><strong>Example 1: Derek & Nutmeg</strong></p>
    <p>For this hybrid, we used a high-frequency cutoff of <code>sigma = 5.0</code> for Nutmeg and a low-frequency cutoff of <code>sigma = 7.0</code> for Derek. Below is the entire process from the aligned images, to the filtered results, and finally the Hybrid image.</p>
    
    <div style="display: flex; flex-direction: column; align-items: center; gap: 30px; background-color: #1a1a1a; padding: 30px; border-radius: 12px; border: 1px solid #333; margin-bottom: 20px;">
        <div style="display: flex; flex-direction: row; justify-content: center; gap: 20px; flex-wrap: wrap; width: 100%;">
            <div style="text-align: center; flex: 1; min-width: 150px; max-width: 250px;">
                <img src="output/2_2_aligned_high_freq.jpg" alt="Nutmeg Aligned" style="width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.4);">
                <p style="color: #bbb; margin-top: 10px; font-size: 0.95rem;">Nutmeg (Aligned)</p>
            </div>
            <div style="text-align: center; flex: 1; min-width: 150px; max-width: 250px;">
                <img src="output/2_2_high_freq_component.jpg" alt="Nutmeg High Pass" style="width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.4);">
                <p style="color: #bbb; margin-top: 10px; font-size: 0.95rem;">High Pass Filter</p>
            </div>
            <div style="text-align: center; flex: 1; min-width: 150px; max-width: 250px;">
                <img src="output/2_2_aligned_low_freq.jpg" alt="Derek Aligned" style="width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.4);">
                <p style="color: #bbb; margin-top: 10px; font-size: 0.95rem;">Derek (Aligned)</p>
            </div>
            <div style="text-align: center; flex: 1; min-width: 150px; max-width: 250px;">
                <img src="output/2_2_low_freq_component.jpg" alt="Derek Low Pass" style="width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.4);">
                <p style="color: #bbb; margin-top: 10px; font-size: 0.95rem;">Low Pass Filter</p>
            </div>
        </div>

        <div style="text-align: center; width: 100%; max-width: 400px; margin-top: 10px;">
            <img src="output/2_2_hybrid.jpg" alt="Derek Nutmeg Hybrid" style="width: 100%; border-radius: 8px; border: 2px solid #555; box-shadow: 0 8px 24px rgba(0,0,0,0.8);">
            <p style="margin-top: 15px; font-size: 1.15rem; color: #fff;"><em><strong>Final Hybrid:</strong> Up close Nutmeg | Far away Derek</em></p>
        </div>
    </div>

    <h4>Frequency Analysis (2D Fourier Transforms)</h4>
    <p>Here is the breakdown of the frequency domains during the creation of the Derek & Nutmeg hybrid.</p>
    <div class="large-img">
        <img src="output/2_2_fourier_analysis.jpg" alt="Fourier Transforms">
    </div>
'''

html = re.sub(r'<p><strong>Example 1: Derek & Nutmeg</strong></p>.*?(?=<p><strong>Example 2: SY & Lord Farquaad \(Lord FUHHH\)</strong></p>)', replacement + '\n\n', html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
