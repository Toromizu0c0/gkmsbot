# インストールした discord.py を読み込む
import discord
from hajime_calc import calc_score
import requests 
import io       
import asyncio
import os
from dotenv import load_dotenv
import google.generativeai as genai
import discord
from PIL import Image
import os
from dotenv import load_dotenv
from niacalc_main import nia_caluculation
from nia_reverse_calc import run_function_500_times
import numpy as np
load_dotenv()

# 自分のBotのアクセストークンに置き換えてください
TOKEN = os.getenv("TOKEN_gkmsBot")
HAJIME_GOOGLE_API_KEY = os.getenv("TOKEN_gkmsBot_Gemini_hajime")
NIA_GOOGLE_API_KEY = os.getenv("TOKEN_gkmsBot_Gemini_nia")

intents = discord.Intents.default()
#メッセージを読む権限を付与
intents.message_content=True

# 接続に必要なオブジェクトを生成
client = discord.Client(intents=intents)

load_dotenv()
genai.configure(api_key=HAJIME_GOOGLE_API_KEY)

model_hajime = genai.GenerativeModel("gemini-2.5-flash")
chat_hajime = model_hajime.start_chat(history=[])
prompt_hajime= """この画像は，各パラメータのステータスと，その右にスコア倍率が書かれています．
            Vo，Da，Viのそれぞれのステータスを読み取って，半角スペース区切りで出力してください．
            他の文章はいらないので，リストだけ出力してください．"""

model_nia = genai.GenerativeModel("gemini-2.5-flash")
chat_nia = model_nia.start_chat(history=[])
prompt_nia="""この画像から以下に示す内容を探して出力してください
            ・Vo, Da, Viの各ステータス（スケジュール画面の上部にあります）
            ・総ファン数（62000ではありません）
            ・Vo, Da, Viのパラメータボーナス（"%"の左側の数字です．小数点以下まできちんと読み取ってください）
            ・アイドルの名前（苗字と名前はつなげて出力してください）
            これらを以上の順番でカンマ区切りで出力してください．
            他の文章は不要ですので，解析された文字列のみ出力してください．"""
# prompt_nia = "こんにちはと出力して"


# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # if message.content == '/neko':
    if message.content.startswith("/hajime"):#もしコマンドが/hajimeで始まったら
        async with message.channel.typing():
            # calc_message = await message.channel.send("計算中...")
            
            try:
                parts = message.content.split()[1:]#コマンドあとの数字を取得し
                nums = list(map(int, parts))#int変換
                if(len(nums) != 3):
                    await message.channel.send("入力は /hajime (Voステ) (Daステ) (Viステ)")
                    return

                Vo, Da, Vi = nums
                result = calc_score(Vo, Da, Vi)
                await message.channel.send(result)

            except ValueError:
                await message.channel.send("数字を正しく入力")
                

    #メッセージに添付ファイルはありますか
    if message.attachments and message.content.startswith("/pichajime"):
        async with message.channel.typing():
            #添付ファイルを一つずつチェック
            for attachment in message.attachments:
                #添付ファイルは画像形式ですか
                if attachment.content_type.startswith('image/'):
                    try:
                        image_data = await attachment.read()
                        image = Image.open(io.BytesIO(image_data))
                        contents = [prompt_hajime, image]
                        response = chat_hajime.send_message(contents)
                        analyze_result = response.text.split()
                        await message.channel.send(f"Vo: {analyze_result[0]}, Da: {analyze_result[1]}, Vi: {analyze_result[2]}")
                    except Exception as e:
                        await message.channel.send("画像の解析に失敗しました")

                    result = calc_score(int(analyze_result[0]), int(analyze_result[1]), int(analyze_result[2]))
                    await message.channel.send(result)
                    
    if message.attachments and message.content.startswith("/nia"):
            # Geminiに渡すためのリストを準備。最初にプロンプト（指示文）を入れる。
            prompt_parts = [prompt_nia]

            async with message.channel.typing():
                # 添付ファイルを一つずつチェック
                for attachment in message.attachments:
                    # 添付ファイルが画像形式かを確認
                    if attachment.content_type.startswith('image/'):
                        try:
                            image_data = await attachment.read()
                            img = Image.open(io.BytesIO(image_data))

                            # 画像の上半分を切り取る
                            width, height = img.size
                            crop_area = (0, 0, width, height // 2)
                            cropped_img = img.crop(crop_area)

                            # Geminiに送信するために画像をバイトデータに変換
                            img_byte_arr = io.BytesIO()
                            cropped_img.save(img_byte_arr, format='JPEG')

                            image_part = {
                                "mime_type": 'image/jpeg', 
                                "data": img_byte_arr.getvalue()
                            }

                            prompt_parts.append(image_part)

                        except Exception as e:
                            await message.channel.send(f"画像の処理中にエラーが発生しました: {e}")
                            print(e) # エラーをコンソールに表示
                            return # エラーが起きたら処理を中断

                # 添付された画像が1枚でもあれば、Geminiにリクエストを送る
                if len(prompt_parts) > 1: # 最初のプロンプト以外に画像データがあるかチェック
                    try:
                        response = model_nia.generate_content(prompt_parts)
                        analyze_result = response.text.split(',') # プロンプトでカンマ区切りを指定したので、カンマで分割
                        score_parts = message.content.split()[1:]#コマンドあとの数字を取得し
                        score = list(map(float, score_parts))#int変換
                        print(analyze_result)
                        # result = nia_caluculation(float(analyze_result[0]), float(analyze_result[1]), float(analyze_result[2]), float(analyze_result[4]),
                                                    # float(analyze_result[5]), float(analyze_result[6]), float(analyze_result[3]), analyze_result[7], score)
                        results = run_function_500_times(float(analyze_result[0]), float(analyze_result[1]), float(analyze_result[2]), float(analyze_result[4]),
                                                            float(analyze_result[5]), float(analyze_result[6]), float(analyze_result[3]), analyze_result[7])
                        scores_ary = np.array([d["nia_score"] for d in results])
                        idx = np.argmin(np.abs(scores_ary - score))
                        final_result = results[idx]
                        send_message = f"アイドル名:{final_result["idol_name"]}\n\入力ステータス:{[analyze_result[0], analyze_result[1], analyze_result[2]]}\n\目標評価値:{score}\n\最終ステータス:{final_result["final_status"]}\n\最終オデ必要スコア:{final_result["scores"]}\n\最終評価値:{final_result["nia_score"]}"
                        await message.channel.send(send_message)
                    except Exception as e:
                        # await message.channel.send(f"Gemini APIとの通信でエラーが発生しました: {e}")
                        print(e)
                else:
                    await message.channel.send("処理できる画像が添付されていませんでした。")                    
    
        

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)