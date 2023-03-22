[![GitHub Repo stars](https://img.shields.io/github/stars/ruankie/discord-social-engagement)](https://github.com/ruankie/discord-social-engagement)

# discord-social-engagement
A Discord bot that track social engagement.

| Status: 🏗️ Under construction...

## Usage

### Setup
1. Set up and activate your conda virtual environment by running:
    ```bash
    conda env create -f conda.yml
    conda activate discord
    ```
2. Create a Discord bot with the correct permissions and invite it to your server (see [this page](https://discordpy.readthedocs.io/en/stable/discord.html#discord-intro) for details)
3. Set your Discord credentials
    - Enter your bot ID in `.env.example` and rename it to `.env`
    - Set the channels you want to monitor inside `src/bot_config.example.yml` and rename it to `src/bot_config.yml`

### Run bot
1. Navigate to the `src/` directory and run the main script:
```bash
cd src/
python main.py
```
