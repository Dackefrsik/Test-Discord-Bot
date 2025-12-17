import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
import os
from dotenv import load_dotenv

Setup och Token
load_dotenv()
token = os.getenv("Token")

# Definiera botten med alla rättigheter (Intents)
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

Start-händelse (Synkar slash-kommandon)
@bot.event
async def on_ready():
    print(f'Inloggad som {bot.user.name} (ID: {bot.user.id})')
    try:
        # Denna rad är magisk - den skickar dina kommandon till Discord
        synced = await bot.tree.sync()
        print(f"✅ Synkade {len(synced)} slash-kommandon!")
    except Exception as e:
        print(f"❌ Kunde inte synka kommandon: {e}")
    print('------ Botten är nu online! ------')

Vanliga !-kommandon
@bot.command()
async def hello(ctx):
        await ctx.send("Hello!")

# Det vanliga !send kommandot
@bot.command()
async def send(ctx, channel: Optional[discord.TextChannel], *, message: str):
    # Om man inte skriver en kanal används den man är i
    target_channel = channel or ctx.channel
    await target_channel.send(message)

#Vanligt !info kommando
@bot.command()
async def info(ctx):
    embed = discord.Embed(
        title="Instruktion: Hur du använder !send",
        description="Använd kommandot för att skicka meddelanden till specifika kanaler.",
        color=discord.Color.blue()
    )
    embed.add_field(name="gör så här:", value="`!send #kanalnamn Ditt meddelande` ", inline=False)
    embed.set_footer(text="Tips: Skriv /send för att få upp en automatisk lista på kanaler!")
    await ctx.send(embed=embed)

#Slash kommandon 
#/hello
@bot.tree.command(name="hello", description="Let me say hello")
async def slash_hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello!")

#/info
@bot.tree.command(name="info", description="Info about commands")
async def info(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Instruktion: Hur du använder !send",
        description="Använd kommandot för att skicka meddelanden till specifika kanaler.",
        color=discord.Color.blue()
    )
    embed.add_field(name="gör så här:", value="`!send #kanalnamn Ditt meddelande` ", inline=False)
    embed.set_footer(text="Tips: Skriv /send för att få upp en automatisk lista på kanaler!")
    await interaction.response.send_message(embed=embed)

#/send
@bot.tree.command(name="send", description="Välj en kanal och skriv ett meddelande")
@app_commands.describe(channel="Vilken kanal ska meddelandet till?", message="Vad ska jag skriva?")
async def slash_send(interaction: discord.Interaction, channel: discord.TextChannel, message: str):
    # Skicka meddelandet till kanalen du valde
    await channel.send(message)
    # Svara användaren (ephemeral=True betyder att bara du ser svaret)
    await interaction.response.send_message(f"Klart! Skickade meddelandet till {channel.mention}", ephemeral=True)

#Kör botten på token från .env-filen 
bot.run(token)