# Minecraft Server Ngrok IP Puller Bot

This bot fetches the current Ngrok TCP address for a Minecraft server and sends it to a designated Discord channel every morning.

## Features

- Retrieves the Ngrok public URL for a Minecraft server using the __Ngrok API__.
- Sends the address to a __Discord channel__ through a bot.
- Automatically runs on __startup and every hour__, sending the IP address only if it changes.
- Spam reduction with a __persistent cache__
- Runs in a __Docker container__ as an option

## Docker Setup

You can run this bot with Docker and provide configuration via a `config.yaml` file mounted as a volume:

1. Create a `config.yaml` file with the following structure:

```yaml
ngrok_api_token: "your_ngrok_api_token"
discord_bot_token: "your_discord_bot_token"
discord_channel_id: your_discord_channel_id  # numeric, no quotes
```

Pull the image from GitHub Container Registry:
```bash
docker pull ghcr.io/michalovsky2112/minecraftserverngrokippuller:latest
```
Run the container mounting your config file:
```bash
docker run -d \
  --name msnipp-bot \
  -v /path/to/your/config.yaml:/app/config.yaml:ro \
  ghcr.io/michalovsky2112/minecraftserverngrokippuller:latest
```
Replace `/path/to/your/config.yaml` with the full path to your config file on the host.

(Optional) To keep the container running after reboot:
```bash
docker update --restart unless-stopped msnipp-bot
```
### Prerequisites

Before running this bot, you need to set up the following:

1. **Python 3.x**: Ensure you have Python 3 installed.
2. **Ngrok Account**: You will need an Ngrok account and an API token. You can get one by signing up at [Ngrok](https://ngrok.com/).
3. **Discord Account**: You will need to create a Discord bot and get a token from the [Discord Developer Portal](https://discord.com/developers/applications).

   
## Setup (Non-Docker)

1. Clone this repository:

    ```bash
    git clone https://github.com/Michalovsky2112/MinecraftServerNgrokIPPuller.git
    cd MinecraftServerNgrokIPPuller
    ```

2. Create and activate a virtual environment:

    ```bash
    python3 -m venv MSNIPP
    source MSNIPP/bin/activate  # For Linux/macOS
    MSNIPP\Scripts\activate  # For Windows
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `config.yaml` file to store your sensitive information:

    ```yaml
    NGROK_API_TOKEN: 'your_ngrok_api_token'
    TOKEN: 'your_discord_bot_token'
    CHANNEL_ID: 'your_discord_channel_id'
    ```

    Replace the placeholders with your actual values.

5. Run the bot:

    ```bash
    python bot.py
    ```

The bot will now send the Minecraft server's Ngrok address to the specified Discord channel at startup.

### Bonus

If you run linux, you can run the bot in a ```screen``` - if installed.
```bash
screen -dmS bot ./MSNIPP/bin/python3 bot.py
```
This will run the bot in a detached screen. To access it, execute: ```screen -r bot```. To exit while leaving running in background, press ```Ctrl + A``` and then ```Ctrl + D```.

## Contributing

If you want to contribute to this project, feel free to fork the repository, create a new branch, and submit a pull request with your changes. All contributions are welcome!

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
