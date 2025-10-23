# インストールした discord.py を読み込む
import discord
import os
from dotenv import load_dotenv
import discord
import os
from dotenv import load_dotenv
from importjson import get_json
from discord.ext import commands

CONFIG = get_json()
load_dotenv()

# 自分のBotのアクセストークンに置き換えてください
TOKEN = os.getenv("TOKEN_gkmsBot")

intents = discord.Intents.default()
#メッセージを読む権限を付与
intents.message_content=True

# 接続に必要なオブジェクトを生成
bot = commands.Bot(command_prefix='/', intents=intents)


# 起動時に動作する処理
@bot.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    try:
        await bot.load_extension('cogs.hajime_cog')
        await bot.load_extension('cogs.nia_cog')
    except Exception as e:
        print(f"Cogsの読み込みに失敗しました: {e}")
        
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} 個のコマンドを同期しました")
    except Exception as e:
        print(f"コマンドの同期に失敗しました: {e}")
        
bot.run(TOKEN)