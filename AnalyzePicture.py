import easyocr
from PIL import Image
import numpy as np
import os


#日本語と英語を読み取る

reader = easyocr.Reader(['en', 'ja'], gpu=False)
texts = []
final_numbers = []

def analyze_picture(target_path: str):
    
    img = Image.open(target_path)
    img = img.convert('L')
    
    img_np = np.array(img)#imgをnumpy配列に変換
    img_width, img_height = img.size
    
    # 画像全体をスキャン(信頼度の基準を下げる)
    full_scan_results = reader.readtext(img_np, detail=1, paragraph=False)
    
    for(bbox_np, text, prob_np) in full_scan_results:
        texts.append(text)
    print(texts)
    final_numbers.append(texts[4])
    final_numbers.append(texts[8])
    final_numbers.append(texts[11])

    return final_numbers