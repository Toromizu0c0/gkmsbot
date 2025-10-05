CONFIG = {
    "IDOL_SETTINGS":{
        #"アイドル名":"２極かバランスか":"流行"
        "花海咲季": {"type": "balance", "trends": ["Visual", "Dance", "Vocal"]},
        "月村手毬": {"type": "specialized","trends": ["Vocal", "Dance", "Visual"]},
        "藤田ことね": {"type": "specialized","trends": ["Dance", "Visual", "Vocal"]},
        "有村麻央": {"type": "specialized","trends": ["Vocal", "Visual", "Dance"]},
        "葛城リーリヤ": {"type": "balance","trends": ["Visual", "Dance", "Vocal"]},
        "倉本千奈": {"type": "specialized","trends": ["Dance", "Visual", "Vocal"]},
        "紫雲清夏": {"type": "specialized","trends": ["Dance", "Visual", "Vocal"]},
        "篠澤広": {"type": "balance","trends": ["Vocal", "Dance", "Visual"]},
        "花海佑芽": {"type": "balance","trends": ["Dance", "Vocal", "Visual"]},
        "姫崎莉波": {"type": "balance","trends": ["Visual", "Dance", "Vocal"]},
        "十王星南": {"type": "balance","trends": ["Visual", "Vocal", "Dance"]},
        "秦谷 美鈴": {"type": "specialized","trends": ["Vocal", "Visual", "Dance"]}
    },
    
    #第二減衰スコアで，ステータス上昇は上限値に達する．
    #第一減衰スコア，第二減衰スコアの定義{第一流行，第二流行，第三流行}
    "status_decay_score":{'balance':[66600, 31350, 17600],
                                'specialized':[65350, 30900, 17800]},
    "status_limit_score":{'balance':[134210, 63750, 36500],
                                'specialized':[136070, 63250, 36100]},
    
    #必要スコア，一時減衰スコア，二次減衰スコア，上限スコア
    "needed_score":100000,
    "sum_decay_score":260417,
    "second_decay_score":640882,
    "max_score":1200582,
    
    #上限ファン数
    "limit_fan":32668,
    #基礎ファン数（補正ファン数）[第一流行，第二流行，第三流行]
    "base_fans":[3656.17, 23427.8, 30358.5],
    
    #ステータス上層関連
    "status_rise":{
        'balance':{
            'limit_rise':[172.0, 142.0, 116.0],#上限パラ
            'base':[0.5, 0.0, 0.0],#基礎パラ
            'limit_coeff':[0.000756, 0.001276, 0.00182],#第二減衰パラ
            'decay_coeff':[0.0018, 0.00325, 0.00465],#第一減衰パラ
            'decay_correct':[70.0, 61.0, 50.0]#補正パラ
        },
        'specialized':{
            'limit_rise':[215.0, 129.0, 86.0],
            'base':[0.0, 0.0, 0.0],
            'limit_coeff':[0.000915, 0.00117, 0.00136],
            'decay_coeff':[0.0023, 0.00295, 0.003465],
            'decay_correct':[90.5, 55.0, 37.0]
        }
    },
    
    #最終評価用補正値
    "status_multiplier":2.3,
    #ファン数に応じた補正値
    "fan_rank_rules": [
        (20001, 0, 0.100), (40001, 300, 0.085), (60001, 900, 0.070),
        (80001, 1200, 0.065), (100001, 1600, 0.060), (120001, 2600, 0.050),
        (140001, 3800, 0.040), (float('inf'), 5200, 0.030)
    ]
}