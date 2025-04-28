import discord
import requests
import asyncio
import secretss

# Set up intents for the bot
intents = discord.Intents.default()
client = discord.Client(intents=intents)

def get_minecraft_ngrok_address():
    try:
        headers = {
            "Authorization": f"Bearer {secretss.NGROK_API_TOKEN}",
            "Ngrok-Version": "2"
        }
        response = requests.get("https://api.ngrok.com/endpoints", headers=headers)
        response.raise_for_status()  # Raise error for bad HTTP status codes
        endpoints = response.json()['endpoints']
        for endpoint in endpoints:
            if endpoint['proto'] == 'tcp':
                hostport = endpoint['hostport']
                return f"Minecraft server address: `{hostport}`"
    except Exception as e:
        print(f"Failed to get ngrok address: {e}")
    return "No ngrok TCP endpoint found."

async def send_ngrok_address():
    await client.wait_until_ready()
    channel = client.get_channel(secretss.CHANNEL_ID)  # Ensure CHANNEL_ID is a valid int
    if channel:
        msg = get_minecraft_ngrok_address()
        await channel.send(msg)
    else:
        print("Failed to find channel.")

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    # Send ngrok address right after bot logs in
    await send_ngrok_address()
    # Optionally, close the bot after sending the message
    await client.close()

client.run(secretss.TOKEN)

# This code is a Discord bot that retrieves the ngrok address for a Minecraft server and sends it to a specified channel.
# It uses the discord.py library to interact with Discord and the requests library to make HTTP requests to the ngrok API.
# The bot logs in using a token and sends the ngrok address to a channel specified by its ID.
# The bot uses the ngrok API to get the current TCP endpoint for the Minecraft server and formats it into a message.
# The bot is designed to run indefinitely, but in this case, it closes itself after sending the message.
