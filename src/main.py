"""
Discord Town - Infrastructure Hub
Main bot entry point
"""

import os
import json
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = '!'

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Load server configuration
def load_config():
    """Load server configuration from config.json"""
    try:
        with open('config/config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Config file not found. Please create config/config.json")
        return None

@bot.event
async def on_ready():
    """Called when the bot is ready"""
    print(f'{bot.user} has connected to Discord!')
    print('------')

@bot.event
async def on_message(message):
    """Handle incoming messages"""
    if message.author == bot.user:
        return
    
    await bot.process_commands(message)

@bot.command(name='ping')
async def ping(ctx):
    """Simple ping command"""
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

@bot.command(name='info')
async def info(ctx):
    """Bot information command"""
    embed = discord.Embed(
        title="Discord Town - Infrastructure Hub",
        description="Official community infrastructure bot",
        color=discord.Color.blue()
    )
    embed.add_field(name="Author", value="Jace (luna.sys)", inline=False)
    embed.add_field(name="Status", value="🟢 Online", inline=False)
    await ctx.send(embed=embed)

def main():
    """Main function"""
    if not TOKEN:
        print("Error: DISCORD_TOKEN not found in .env file")
        return
    
    config = load_config()
    if config:
        print(f"Loaded configuration for: {config.get('server', {}).get('name', 'Discord Town')}")
    
    print("Starting Discord Town bot...")
    bot.run(TOKEN)

if __name__ == '__main__':
    main()
