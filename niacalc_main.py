import math
import numpy as np  
from importjson import get_json 
# import json
# from niacalc_config import CONFIG


# status = input("ステータスを入力:")
# bonus = input("ボーナスを入力(無ければ0):")
# fans = int(input("ファン数を入力:"))
# score = input("スコアを入力:")

#アイドル情報
# status = "1045 1127 1208"
# bonus = "28.1 30.0 36.9"
# fans = 85519.0
# score = "190536 94503 37542"
# idol_name = "姫崎莉波"
# #入力情報から各流行ごとのステータスを読み取る
# status = list(map(float, status.split()))
# sum_score = sum(score)

# #パラボバージョン
# bonus = list(map(float, bonus.split()))
# bonus = [ x /100 for x in bonus]

# #オーディションスコアバージョン
# score = list(map(float, score.split()))
# sum_score = sum(score)
# idol_info = CONFIG["IDOL_SETTINGS"][idol_name]
CONFIG = get_json()

def nia_caluculation(s1, s2, s3, b1, b2, b3, fans, name, scores, stage):
    status = [s1, s2, s3]#流行別試験前ステータス
    bonus = [b1/100, b2/100, b3/100]#パラメータボーナス
    score = scores#流行別最終スコアのリスト
    idol_info = CONFIG["common"]["IDOL_SETTINGS"][name]#アイドル名
    fans = fans#ファン数
    sum_score = sum(score)#最終合計スコア    
    item_bonus = 40.0/100#アイテムボーナス

    #ファン数の計算
    base_fans = CONFIG[stage]["base_fans"]
    max_score = CONFIG[stage]["max_score"]
    limit_fan = CONFIG[stage]["limit_fan"]
    secand_d_score = CONFIG[stage]["second_decay_score"]
    d_score = CONFIG[stage]["sum_decay_score"]
    needed_score = CONFIG[stage]["needed_score"]
    fan_coeff = CONFIG[stage]["fan_coeff"]

    if sum_score >= max_score:
        final_fans = fans + limit_fan*1.5
    elif sum_score >= secand_d_score:
        final_fans = fans + 1.5 * ((sum_score - secand_d_score) * fan_coeff[2] + base_fans[2])
    elif sum_score >= d_score:
        final_fans = fans + 1.5 * ((sum_score - d_score) * fan_coeff[1]  + base_fans[1])
    elif sum_score > needed_score:
        final_fans = fans + 1.5 * ((sum_score - 0) * fan_coeff[0] + base_fans[0])
    else:
        final_fans = fans


    #ステータスの計算
    limit_rise_status = CONFIG[stage]['status_rise'][idol_info['type']]['limit_rise']
    base_status = CONFIG[stage]["status_rise"][idol_info['type']]['base']
    limit_status_coefficient = CONFIG[stage]["status_rise"][idol_info['type']]['limit_coeff']
    decay_status_coefficient = CONFIG[stage]["status_rise"][idol_info['type']]['decay_coeff']
    decay_correct = CONFIG[stage]["status_rise"][idol_info['type']]['decay_correct']

    status_decay_score = CONFIG[stage]["status_decay_score"][idol_info['type']]
    status_limit_score = CONFIG[stage]["status_limit_score"][idol_info['type']]

    # rise_status = np.array([0.0, 0.0, 0.0])
    final_status = np.array([0.0, 0.0, 0.0])

    status_dict = {'Vocal': status[0], 'Dance': status[1], 'Visual': status[2]}
    bonus_dict = {'Vocal': bonus[0], 'Dance': bonus[1], 'Visual': bonus[2]}
    # score_dict = {idol_trends[i]: score[i] for i in range(3)}
    score_dict = {'Vocal': score[0], 'Dance': score[1], 'Visual': score[2]}
    rise_status_dict = {'Vocal': 0.0, 'Dance': 0.0, 'Visual': 0.0}
    final_status_dict = {'Vocal': 0.0, 'Dance': 0.0, 'Visual': 0.0}

    #第一流行から計算
    for i, attr in enumerate(idol_info['trends']):
        current_score = score_dict[attr]
        # print(attr, current_score)

        calculated_rise = 0.0
        if current_score >= status_limit_score[i]:
            calculated_rise = math.floor(limit_rise_status[i]*item_bonus) + math.floor(limit_rise_status[i]*bonus_dict[attr])

            total_rise = math.floor(limit_rise_status[i]) + calculated_rise
            # print(limit_rise_status[i], calculated_rise)
        elif current_score > status_decay_score[i]:

            calculated_rise = math.floor(decay_correct[i] + current_score * limit_status_coefficient[i])
            bonus_from_personal = math.floor(calculated_rise * (bonus_dict[attr]))
            bonus_from_item = math.floor(calculated_rise * (item_bonus))
            total_rise = calculated_rise + bonus_from_personal + bonus_from_item
        else:
            calculated_rise = math.floor(base_status[i] + current_score * decay_status_coefficient[i])
            bonus_from_personal = math.floor(calculated_rise * (bonus_dict[attr]))
            bonus_from_item = math.floor(calculated_rise * (item_bonus))
            total_rise = calculated_rise + bonus_from_personal + bonus_from_item
            # print(1)


        rise_status_dict[attr] = total_rise
        final_status_dict[attr] = status_dict[attr] + total_rise

    #総ファン数による係数を取得
    c, ratio = 0, 0
    for limit, const_c, const_ratio in CONFIG["common"]['fan_rank_rules']:
        if final_fans < limit:
            c, ratio = const_c, const_ratio
            break



    final_status = [min(float(value), 2300) for value in final_status_dict.values()]#上限は2300なので
    sum_final_status = sum(final_status)
    status_result = math.floor(sum_final_status * 2.3)
    fan_result = (math.floor(final_fans) * ratio + c)


    #NIA評価点　=パラメータ文 + ファン投票数換算文
    final_result = math.floor(fan_result + status_result)

    # print(f"アイドル: {name} ({idol_info['type']})")
    # print(f"流行順: {idol_info['trends']}")

    # print(f"item_bonus: {item_bonus*100}%")
    # print(f"Vo:{status_dict['Vocal']}, Da:{status_dict['Dance']}, Vi:{status_dict['Visual']}")
    # print(f"Vo_bonus:{bonus_dict['Vocal']*100:.1f}%, Da_bonus:{bonus_dict['Dance']*100:.1f}%, Vi_bonus:{bonus_dict['Visual']*100:.1f}%")
    # print(f"fans:{fans}")
    # print(f"score Vo:{score_dict['Vocal']}, Da:{score_dict['Dance']}, Vi:{score_dict['Visual']}")

    # print(f"rise_status Vo:{rise_status_dict['Vocal']:.0f}, Da:{rise_status_dict['Dance']:.0f}, Vi:{rise_status_dict['Visual']:.0f}")
    # print(f"final_status Vo:{final_status_dict['Vocal']:.0f}, Da:{final_status_dict['Dance']:.0f}, Vi:{final_status_dict['Visual']:.0f}")
    # print(f"final_fans:{final_fans:.0f}")
    # print(f"NIA評価点:{final_result}")
    
    result_data = {
        "idol_name": name,
        "idol_type": idol_info['type'],
        "trends": idol_info['trends'],
        "item_bonus_percent": item_bonus * 100,
        "status": status_dict,
        "bonus_percent": {
            'Vocal': bonus_dict['Vocal'] * 100,
            'Dance': bonus_dict['Dance'] * 100,
            'Visual': bonus_dict['Visual'] * 100
        },
        "fans": fans,
        "scores": score_dict,
        "rise_status": rise_status_dict,
        "final_status": final_status_dict,
        "final_fans": final_fans,
        "nia_score": final_result
    }

    return result_data