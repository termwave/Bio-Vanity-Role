# Discord Role Assignment Bot

This bot automates the process of assigning roles in a Discord server based on user profile bio checks. Users can easily obtain roles by clicking a button and meeting the specified criteria.

## Features

- **Automatic Role Assignment**: Allows users to click a button to request a seller role if their bio matches a required vanity URL.
- **Custom Text Channel Creation**: Creates a private channel for each user where the bot verifies their profile and assigns the appropriate role.
- **Webhook Logging**: Sends logs to a specified webhook when users are assigned roles.
- **Dynamic Role Message**: Automatically posts a role assignment message with an embedded button.

## Requirements

- Python 3.x
- `discord.py` for Discord bot interaction
- `dhooks` for webhook integration
- `requests` for fetching user profiles

## Setup

1. Install the required dependencies.
   ```bash
   pip install -r requirements.txt
   ```

2. Configure the bot by modifying `config.json` with the following keys:
   - `bot-token`: Your Discord bot token.
   - `role-id`: The ID of the seller role.
   - `user-token`: A Discord user token to authenticate API calls.
   - `vanity`: The required vanity string in the user's bio.
   - `fixed-channel-id`: The ID of the channel where the role assignment message should be posted.
   - `role-webhook`: The webhook URL for logging.

3. Run the bot.
   ```bash
   python main.py
   ```

## How It Works

- The bot posts a message in the configured channel, allowing users to click a button to get a role.
- It creates a temporary text channel, verifies the user's profile for the specified vanity URL, and assigns them the seller role if they meet the criteria.
- After verification, the temporary channel is deleted.

## Contributing

Feel free to submit issues or pull requests to improve the functionality of the bot!
addy:ltc1qcuc2ufpvylaas7s6prdhsp97gc8dvp9rg5a28j
dc id termwave_
