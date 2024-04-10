# SchedulerBot for Telegram

SchedulerBot is an advanced Telegram bot built to simplify the scheduling of messages to channels or groups. With a user-friendly setup, it allows for precise scheduling, ensuring your messages are sent out on time, every time. Ideal for community managers, content creators, and anyone looking to automate their Telegram messaging.

## Features

- **Easy Scheduling**: Set up a timeline once, and SchedulerBot takes care of the rest.
- **Flexible Timelines**: Specify exact times for message delivery. Supports multiple timestamps for daily scheduling.
- **Channel Management**: Easily manage which channel your scheduled messages are sent to.
- **Persistence**: Your settings (channel preferences and timelines) are saved and remembered across bot restarts.
- **User-friendly**: Simple commands and instructions guide you through setting up and managing your schedules.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- A Telegram account
- `api_id` and `api_hash` from [Telegram's My Telegram](https://my.telegram.org/apps)
- A bot token from BotFather on Telegram

# Installation Instructions

-  Step 1: Clone the repository
git clone <repository-url>
cd <repository-directory>

-  Step 2: Install required Python package
pip install telethon

-  Step 3: Configure the bot
 Open the scheduler_bot.py file in a text editor of your choice
and insert your 'api_id', 'api_hash', and 'bot_token' in the designated placeholders.

## Usage Instructions

- To run the bot, execute
python scheduler_bot.py

## Interacting with the Bot in Telegram:

-  1. Start the bot in Telegram by sending '/start' to receive instructions

-  2. Set the target channel where messages will be scheduled
/setchannel @channelusername

- 3. Define your message scheduling timeline with specific times
/set_timeline 08:00:00, 12:00:00, 16:00:00

### Now, simply send your messages to the bot, and they will be scheduled according to the timeline you've set.

## Available Commands:

- ** /start** - Begin interaction with the bot and receive instructions.
- ** /setchannel** - Set or change the target channel for your scheduled messages.
-** /set_timeline** - Set up or adjust your message scheduling timeline.
-** /help** - Get a list of commands and instructions for use.
