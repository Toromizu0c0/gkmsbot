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
load_dotenv()

# 自分のBotのアクセストークンに置き換えてください
TOKEN = os.getenv("TOKEN_gkmsBot")
GOOGLE_API_KEY = os.getenv("TOKEN_gkmsBot_Gemini")

intents = discord.Intents.default()
#メッセージを読む権限を付与
intents.message_content=True

# 接続に必要なオブジェクトを生成
client = discord.Client(intents=intents)

load_dotenv()
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")
chat = model.start_chat(history=[])
prompt = """この画像は，各パラメータのステータスと，その右にスコア倍率が書かれています．
            Vo，Da，Viのそれぞれのステータスを読み取って，半角スペース区切りで出力してください．
            他の文章はいらないので，リストだけ出力してください．"""


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
    if message.attachments and message.content.startswith("/pic"):
        async with message.channel.typing():
            #添付ファイルを一つずつチェック
            for attachment in message.attachments:
                #添付ファイルは画像形式ですか
                if attachment.content_type.startswith('image/'):
                    try:
                        image_data = await attachment.read()
                        image = Image.open(io.BytesIO(image_data))
                        contents = [prompt, image]
                        response = chat.send_message(contents)
                        analyze_result = response.text.split()
                        await message.channel.send(f"Vo: {analyze_result[0]}, Da: {analyze_result[1]}, Vi: {analyze_result[2]}")
                    except Exception as e:
                        await message.channel.send("画像の解析に失敗しました")

                    result = calc_score(int(analyze_result[0]), int(analyze_result[1]), int(analyze_result[2]))
                    await message.channel.send(result)
    
        

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)