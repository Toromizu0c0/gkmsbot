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
from importjson import get_json
from discord.ext import commands
CONFIG = get_json()
from discord import app_commands
from discord.ext import commands

NIA_GOOGLE_API_KEY = os.getenv("TOKEN_gkmsBot_Gemini_nia")
model_nia = genai.GenerativeModel("gemini-2.5-flash")
chat_nia = model_nia.start_chat(history=[])
prompt_nia="""この画像から以下に示す内容を探して出力してください
            ・Vo, Da, Viの各ステータス（スケジュール画面の上部にあります）
            ・総ファン数（62000ではありません）
            ・Vo, Da, Viのパラメータボーナス（"%"の左側の数字です．小数点以下まできちんと読み取ってください）
            ・アイドルの名前（苗字と名前はつなげて出力してください）
            これらを以上の順番でカンマ区切りで出力してください．
            他の文章は不要ですので，解析された文字列のみ出力してください．"""
load_dotenv()

class NiaCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name='nia', description="二枚の画像から必要情報を読み取り，各ランク到達に必要なスコア逆算")
    @app_commands.describe(image1="スケジュール画面の画像を添付", image2="ステータス画面の画像を添付", stage="ステージを選択(finale or quartet)")
    
    async def nia_command(self, interaction:discord.Interaction, image1:discord.Attachment, image2:discord.Attachment, stage:str):
        await interaction.response.defer()#計算中
        try:
            image_data1 = await image1.read()
            image1 = Image.open(io.BytesIO(image_data1))
            image_data2 = await image2.read()
            image2 = Image.open(io.BytesIO(image_data2))
            bufferd = io.BytesIO()
            contents = [prompt_nia, image1, image2]#Geminiに送信
            response = chat_nia.send_message(contents)
            analyze_result_nia = response.text.split(',')
            
            send_message = ["目標評価:各必要スコア(流行別)"]
            evals = CONFIG["eval"]
            
            for key, value in evals.items():
                results = run_function_500_times(float(analyze_result_nia[0]), float(analyze_result_nia[1]), float(analyze_result_nia[2]),
                                                float(analyze_result_nia[4]), float(analyze_result_nia[5]), float(analyze_result_nia[6]), 
                                                float(analyze_result_nia[3]), analyze_result_nia[7],stage)
                scores_ary = np.array([d["nia_score"] for d in results])
                idx = np.argmin(np.abs(scores_ary - value))
                final_score = scores_ary[idx]
                
                if final_score < value and final_score != max(scores_ary):
                    idx += 1
                    send_message.append(f"{key}:{results[idx]["scores"]}\n")  
                elif final_score < value and final_score == max(scores_ary):
                    send_message.append(f"{key}:達成不可\n")
                else:
                    send_message.append(f"{key}:{results[idx]["scores"]}\n")
            sum_send_message = "".join(send_message)
            await interaction.followup.send(sum_send_message)
        except Exception as e:
            await interaction.followup.send(f"エラーが発生しました: {e}")
            
"Bot本体がCogを読み込む"
async def setup(bot: commands.Bot):
    await bot.add_cog(NiaCog(bot))