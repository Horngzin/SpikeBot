import os
import discord
from discord.ext import commands
import yt_dlp
import static_ffmpeg
static_ffmpeg.add_paths()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

YTDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': True}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} - Bot is online!")

@bot.command()
async def play(ctx, url: str):
    if not ctx.author.voice:
        await ctx.send("You need to join a voice channel first!")
        return

    channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await channel.connect()

    async with ctx.typing():
        with yt_dlp.YoutubeDL(YTDL_OPTIONS) as ytdl:
            info = ytdl.extract_info(url, download=False)
            audio_url = info['url']
            title = info.get('title', 'Audio')

        source = discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS)
        ctx.voice_client.play(source)

    await ctx.send(f"🎶 Now playing: **{title}**")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected from voice channel.")

bot.run(os.getenv("DISCORD_TOKEN"))
