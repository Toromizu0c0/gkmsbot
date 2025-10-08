from niacalc_main import nia_caluculation  # 関数名を適切に変更してください
from niacalc_config import CONFIG
import math
import numpy as np

def allo_score(total_score, idol_name):
    idol_info = CONFIG["IDOL_SETTINGS"][idol_name]
    idol_type = idol_info["type"]
    trend_order = idol_info["trends"]
    score_limits = CONFIG["status_limit_score"][idol_type]
    score_decay = CONFIG["status_decay_score"][idol_type]
    
    remaining_score = total_score
    trend_scores = {"Vocal":0, "Dance":0, "Visual":0}
    
    #各流行の減衰店までスコアを充填
    for i, trend_attr in enumerate(trend_order):
        fill_amount = min(remaining_score, score_decay[i])
        trend_scores[trend_attr] += fill_amount
        remaining_score -= fill_amount
        if remaining_score <= 0:
            return [trend_scores["Vocal"], trend_scores["Dance"], trend_scores["Visual"]]
    
    #各流行の上限点までスコアを補充
    for i, trend_attr in enumerate(trend_order):
        gap_to_limit = score_limits[i] - score_decay[i]
        fill_amount = min(remaining_score, gap_to_limit)
        trend_scores[trend_attr] += fill_amount
        remaining_score -= fill_amount
        if remaining_score <= 0:
            return [trend_scores["Vocal"], trend_scores["Dance"], trend_scores["Visual"]]
        
    #上限を超えてもスコアが残っている　第一りゅこうにのこりぜんつっぱ
    if remaining_score > 0:
        trend_scores[trend_order[0]] += remaining_score
        
    return [trend_scores["Vocal"], trend_scores["Dance"], trend_scores["Visual"]]

def run_function_500_times(s1, s2, s3, b1, b2, b3, fans, name):
    result = []#結果を格納
    num_division = 500#分割数500
    under_limit = 100000
    over_limit = 1200582
    step = round((over_limit - under_limit) / (num_division - 1), -1)
    total_scores = [under_limit + step * i for i in range(num_division)]
    scores = [allo_score(total_score, name) for total_score in  total_scores]
    # for i in range(100):
    #     print(scores[i])
    
    for i in range(500):
        result.append(nia_caluculation(s1, s2, s3, b1, b2, b3, fans, name, scores[i]))
    return result

if __name__ == "__main__":
    results = run_function_500_times(976, 1428, 1342, 18.0, 33.5, 33.7, 78474, '葛城リーリヤ')
    
    # for result in results:
    #     print(f"{result["nia_score"]}   {result["scores"]}")
    # idx = np.argmin(np.abs(np.array(results) - 21000))
    # print(idx)
    scores_ary = np.array([d["nia_score"] for d in results])
    idx = np.argmin(np.abs(scores_ary - 21000))
    print(idx)
    print(results[idx])