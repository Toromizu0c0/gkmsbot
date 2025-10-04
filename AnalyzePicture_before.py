import easyocr
from PIL import Image
import numpy as np
import os


#日本語と英語を読み取る

reader = easyocr.Reader(['en', 'ja'], gpu=False)

def analyze_picture(target_path: str):
    
    img = Image.open(target_path)
    img = img.convert('L')
    
    img_np = np.array(img)#imgをnumpy配列に変換
    img_width, img_height = img.size
    
    # 画像全体をスキャン(信頼度の基準を下げる)
    full_scan_results = reader.readtext(img_np, detail=1, paragraph=False)
    # print(full_scan_results)
    base_bbox_np = None
    
    for(bbox_np, text, prob_np) in full_scan_results:
        if "審" in text:
            base_bbox_np = bbox_np
            # print(f"信頼度:{prob_np})")
            # print(base_bbox_np)
            break
    
    if base_bbox_np is None:
        print("基準となるテキストが見つかりません")
        return []
    
    # bboxは [[x_left_top, y_left_top], [x_right_top, y_right_top], [x_right_bottom, y_right_bottom], [x_left_bottom, y_left_bottom]]
    base_y_bottom = int(base_bbox_np[3][1]) # 左下隅のY座標を基準
    
    #目的の3行の数字エリアの切り抜き範囲を動的に計算
    ratio_offset_y_from_base = 0.10 # 基準Yからの1行目上端まで (画像の高さに対する割合)
    ratio_height_of_numbers_area = 0.23 # 3行の数字エリアの高さ 
    ratio_left_x = 0.1 # 数字エリアの左端X座標 
    ratio_right_x = 0.4 # 数字エリアの右端X座標 
    
    # 切り抜きエリアのY座標を計算
    cropped_top = int(base_y_bottom + (img_height * ratio_offset_y_from_base))
    cropped_bottom = int(cropped_top + (img_height * ratio_height_of_numbers_area))

    # 切り抜きエリアのX座標を計算
    cropped_left = int(img_width * ratio_left_x)
    cropped_right = int(img_width * ratio_right_x)

    # 座標が画像範囲内に収まるように調整
    cropped_top = max(0, cropped_top)
    cropped_bottom = min(img_height, cropped_bottom)
    cropped_left = max(0, cropped_left)
    cropped_right = min(img_width, cropped_right)   
    
    # 切り抜き範囲が妥当かチェック
    if cropped_top >= cropped_bottom or cropped_left >= cropped_right:
        print(f"エラー: 無効な切り抜き範囲が計算されました: top={cropped_top}, bottom={cropped_bottom}, left={cropped_left}, right={cropped_right}")
        print("  - 基準テキストからのオフセット値または画像のサイズが極端に異なる可能性があります。")
        return []
    
    # 切り抜いた画像を保存
    # cropped_img_path = f"cropped_{os.path.basename(target_path)}"
    # img_cropped = img.crop((cropped_left, cropped_top, cropped_right, cropped_bottom))
    # img_cropped.save(cropped_img_path)   
    
    #切り抜いた画像を解析
    # img_cropped_np = np.array(img.crop((cropped_left, cropped_top, cropped_right, cropped_bottom)))
    # cropped_results = reader.readtext(img_cropped_np, detail=1, paragraph=False)

    cropped_results = full_scan_results
    
    #結果の処理
    extracted_numbers_with_coords = []
    for (bbox_np, text, prob_np) in cropped_results:
        prob = float(prob_np) # 信頼度をPythonのfloatに変換
        
        cleaned_text = ''.join(filter(lambda c: c.isdigit(), text))
        if cleaned_text: # 空文字でないことを確認
            # 検出された文字のY座標（切り抜き画像内での相対座標）
            # bbox_npの左上Y座標がそのテキストの開始Y座標となる
            y_coord_in_cropped = int(bbox_np[0][1])
            extracted_numbers_with_coords.append(
                {'text': cleaned_text, 'score': prob, 'y_coord_relative': y_coord_in_cropped}
            )
    
    # Y座標が上から順になるようにソート
    extracted_numbers_with_coords.sort(key=lambda x: x['y_coord_relative'])
    
    final_numbers = [item['text'] for item in extracted_numbers_with_coords]
    # print(f"  - 抽出された数字: {final_numbers}")

    return final_numbers
# target_path1 = "C:/Users/stst1/discord/testOCR/lilija.jpg"
# out1 = analyze_picture(target_path1)
# print(out1)



# target_path2 = "C:/Users/stst1/discord/testOCR/lilija_ipad.jpg"
# out2 = analyze_picture(target_path2)
# print(out2)

# texts = []
# for coords, text, score in out1:
#     texts.append(text)
#     print(f"text:{text}, score:{score}, coords:{coords[0]}")

# print()

# for coords, text, score in out2:
#     texts.append(text)
#     print(f"text:{text}, score:{score}, coords:{coords[0]}")
# # print(texts)