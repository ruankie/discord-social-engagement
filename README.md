[![GitHub Repo stars](https://img.shields.io/github/stars/ruankie/discord-social-engagement)](https://github.com/ruankie/discord-social-engagement)

# 🗨️ discord-social-engagement
A Discord bot that tracks social engagement on specified channels. 

This bot includes slash commands with annotated arguments for easy use. An extra layer of security is added so that only selected users can trigger these commands. Some server side logging is also done to monitor the triggering of commands and the health of the bot.

## Demo
![discord-engagement-bot](https://user-images.githubusercontent.com/58558211/235516052-b38c5e2e-c16d-4eb9-a508-a3b71142ab86.gif)

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
4. Set the tracked channels and authorised bot users in `config.yml` (you can use `config.yml.example` as a template)

### Run Bot
1. Run the following command on your bot server (the bot will only respond while this is running):
```bash
python src/main.py
```
2. Once initialised, the bot will appear online and it will respond to slash commands. Type `/` and a list of available commands will appear if you have the correct permissions on the server.

## Useful Resources
- https://discordpy.readthedocs.io/en/stable/#
- https://www.linkedin.com/pulse/discord-bot-part-2-slash-commands-leandro-fumio-kino
- https://www.youtube.com/watch?v=jh1CtQW4DTo
- https://gifcap.dev

