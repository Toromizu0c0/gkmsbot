import math

def calc_score(Vo_status, Da_status, Vi_status, junni = 1):
    Vo_status = min(Vo_status +  30, 1800)
    Da_status = min(Da_status +  30, 1800)
    Vi_status = min(Vi_status +  30, 1800)
    status_hyoka = (Vo_status+Da_status+Vi_status) * 2.3
    results = []

    # junni = int(input("最終順位を入力"))
    if junni == 1:
        junni_hyoka = 1700
    elif junni == 2:
        junni_hyoka = 900
    elif junni == 3:
        junni_hyoka = 500

    # mokuhyou = int(input("目標評価値を入力"))
    mokuhyou = {"C":3000, "C+":4500, "B":6000, "B+":8000, "A":10000, 
                "A+":11500, "S":13000, "S+":14500, "SS":16000, 
                "SS+":18000}#, "SSS":20000, "SSS+":23000}

    for hyoka_key, hyoka_value in mokuhyou.items():
        score_hyoka = hyoka_value - status_hyoka - junni_hyoka

        if score_hyoka >= 3650.01:
            target_score = (score_hyoka - 3250)/0.01    
        elif score_hyoka >= 3450.02:
            target_score = (score_hyoka - 2850)/0.02
        elif score_hyoka >= 3050.04:
            target_score = (score_hyoka - 2250)/0.04
        elif score_hyoka >= 2250.08:
            target_score = (score_hyoka - 1450)/0.08
        elif score_hyoka >= 1500.15:
            target_score = (score_hyoka - 750)/0.15
        else:
            target_score = (score_hyoka)/0.3

        if target_score > 0:
            results.append("必要スコア（" + hyoka_key +":" + str(hyoka_value) + "）" + str(math.floor(target_score)))
        else:
            results.append("必要スコア（" + hyoka_key +": 0）")

    return "\n".join(results)        