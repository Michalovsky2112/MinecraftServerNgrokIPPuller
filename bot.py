import discord # type: ignore
import requests
import asyncio
import logging
import secretss
import logging
import os


# --- Logging Setup ---
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


# Set up intents for the bot
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# --- IP Cache ---
last_sent_ip = None

IP_STORE_FILE = "last_ip.txt"

def get_minecraft_ngrok_address():
    try:
        headers = {
            "Authorization": f"Bearer {secretss.NGROK_API_TOKEN}",
            "Ngrok-Version": "2"
        }
        response = requests.get("https://api.ngrok.com/endpoints", headers=headers)
        response.raise_for_status()
        for endpoint in response.json().get('endpoints', []):
            if endpoint['proto'] == 'tcp':
                return endpoint['hostport']
    except Exception as e:
        logging.error(f"Error getting ngrok address: {e}")
    return None

def load_last_ip():
    if os.path.exists(IP_STORE_FILE):
        with open(IP_STORE_FILE, 'r') as f:
            return f.read().strip()
    return None

def save_last_ip(ip):
    with open(IP_STORE_FILE, 'w') as f:
        f.write(ip)

async def send_if_ip_changed():
    await client.wait_until_ready()
    channel = client.get_channel(secretss.CHANNEL_ID)
    if not channel:
        logging.error("Failed to find channel.")
        return

    current_ip = get_minecraft_ngrok_address()
    if not current_ip:
        logging.warning("Could not fetch ngrok IP.")
        return

    last_ip = load_last_ip()
    if current_ip != last_ip:
        logging.info(f"IP changed: {last_ip} → {current_ip}")
        await channel.send(f"New Minecraft server address: `{current_ip}`")
        save_last_ip(current_ip)
    else:
        logging.info("IP unchanged. No message sent.")

async def hourly_loop():
    while True:
        await send_if_ip_changed()
        await asyncio.sleep(3600)  # wait 1 hour

@client.event
async def on_ready():
    logging.info(f"Logged in as {client.user}")
    client.loop.create_task(hourly_loop())
    await send_if_ip_changed()  # Send immediately on startup

client.run(secretss.TOKEN)

# This code is a Discord bot that retrieves the ngrok address for a Minecraft server and sends it to a specified channel.
# It uses the discord.py library to interact with Discord and the requests library to make HTTP requests to the ngrok API.
# The bot logs in using a token and sends the ngrok address to a channel specified by its ID.
# The bot uses the ngrok API to get the current TCP endpoint for the Minecraft server and formats it into a message.

