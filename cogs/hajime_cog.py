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
from discord import app_commands
from discord.ext import commands

HAJIME_GOOGLE_API_KEY = os.getenv("TOKEN_gkmsBot_Gemini_hajime")
genai.configure(api_key=HAJIME_GOOGLE_API_KEY)

model_hajime = genai.GenerativeModel("gemini-2.5-flash")
chat_hajime = model_hajime.start_chat(history=[])
prompt_hajime= """この画像は，各パラメータのステータスと，その右にスコア倍率が書かれています．
            Vo，Da，Viのそれぞれのステータスを読み取って，半角スペース区切りで出力してください．
            他の文章はいらないので，リストだけ出力してください．"""
load_dotenv()

# Cogクラス定義
class HajimeCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    #/hajimeコマンド
    @app_commands.command(name='hajime', description="ステータス(Vo,Da,Vi)から必要スコア逆算")
    #入力値の保証
    @app_commands.describe(vo="Voステ", da="Daステ", vi="Viステ")
    async def hajime_command(self, interaction:discord.Interaction, vo:int, da:int, vi:int):
        await interaction.response.defer()#計算中
        result = calc_score(vo, da, vi)
        await interaction.followup.send(result)
    
    #/pichajimeコマンド
    @app_commands.command(name='pichajime', description="画像からステータス(Vo,Da,Vi)を読み取り必要スコア逆算")
    #入力画像の保証
    @app_commands.describe(image="最終試験前の画像を添付")
    async def pichajime_command(self, interaction:discord.Interaction, image:discord.Attachment):
        await interaction.response.defer()#計算中
        try:#画像が添付されている
            image_data = await image.read()
            image = Image.open(io.BytesIO(image_data))
            buffered = io.BytesIO()
            contents = [prompt_hajime, image]#Geminiに送信
            response = chat_hajime.send_message(contents)
            analyze_result_hajime = response.text.strip()
            vo, da, vi = map(int, analyze_result_hajime.split())
            result = calc_score(vo, da, vi)
            await interaction.followup.send(result)
            
        except Exception as e:
            await interaction.followup.send(f"エラーが発生しました: {e}")

"Bot本体がCogを読み込む"
async def setup(bot: commands.Bot):
    await bot.add_cog(HajimeCog(bot))