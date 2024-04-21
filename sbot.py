from telethon import TelegramClient, events
from datetime import datetime, timedelta
import asyncio
import json

api_id = '27653293'
api_hash = 'ef7e1abf5219cb91597e8aadcba42824'
bot_token = '7051338088:AAG1_8ZNoz5_oVHbng79kgz8dQXNXdRxqDQ'

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

settings_file = 'bot_settings.json'

def save_settings():
    data = {
        'user_timelines': user_timelines,
        'user_channel_preferences': user_channel_preferences,
        'user_next_timestamps': user_next_timestamps
    }
    with open(settings_file, 'w') as f:
        json.dump(data, f, indent=4)

def load_settings():
    try:
        with open(settings_file, 'r') as f:
            data = json.load(f)
            # Convert string keys back to integers (for user IDs)
            data['user_timelines'] = {int(k): v for k, v in data['user_timelines'].items()}
            data['user_channel_preferences'] = {int(k): v for k, v in data['user_channel_preferences'].items()}
            data['user_next_timestamps'] = {int(k): v for k, v in data['user_next_timestamps'].items()}
            return data
    except FileNotFoundError:
        return {'user_timelines': {}, 'user_channel_preferences': {}, 'user_next_timestamps': {}}

settings = load_settings()
user_timelines = settings['user_timelines']
user_channel_preferences = settings['user_channel_preferences']
user_next_timestamps = settings['user_next_timestamps']

#Starting the Bot

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    welcome_message = (
        "Welcome! Here's how to get started:\n"
        "1. Use the /setchannel command to set the target channel for your messages. Example: /setchannel @yourchannelname\n"
        "2. Use the /set_timeline command to set up your posting schedule. Provide a series of times in the format HH:MM:SS, separated by commas. Example: /set_timeline 08:00:00, 12:00:00, 18:00:00\n"
        "3. Once your timeline and channel are set, simply send me any message, and it will be scheduled according to your timeline.\n\n"
        "If you wish to reset your channel or timeline, just use the /setchannel and /set_timeline commands again with the new settings."
    )
    await event.respond(welcome_message)


user_timelines = {}  # Stores user timelines
user_next_timestamps = {}  # Tracks the next timestamp index for each user

#Code that sets the timeline for the user

@client.on(events.NewMessage(pattern='/set_timeline'))
async def set_timeline(event):
    raw_timeline = event.raw_text.split(maxsplit=1)[1] if len(event.raw_text.split(maxsplit=1)) > 1 else ""
    timeline = [time.strip() for time in raw_timeline.split(',')]
    
    # Validate and store the timeline
    try:
        # Convert times to datetime objects to validate format, but store strings for flexibility
        [datetime.strptime(time, '%H:%M:%S') for time in timeline]
        user_timelines[event.sender_id] = timeline
        user_next_timestamps[event.sender_id] = 0  # Reset the next timestamp index
        
        await event.respond(f"Here's your current timeline: {', '.join(timeline)}. Each message you send next will be scheduled to these times in order.")
    except ValueError:
        await event.respond("Please make sure to use the correct format for the timeline: HH:MM:SS, HH:MM:SS, ...")
    save_settings()  # Save after updating the preference
    # Global dictionary to store user preferences
user_channel_preferences = {}

#Code that sets the channel for the user

@client.on(events.NewMessage(pattern='/setchannel'))
async def set_channel(event):
    try:
        # Extract the channel username or ID from the message, stripping the command part
        target_channel = event.raw_text.split(' ', 1)[1].strip()
        
        # Save the target channel for the user
        user_channel_preferences[event.sender_id] = target_channel
        
        await event.respond(f"Your messages will now be sent to '{target_channel}'.")
        
    except IndexError:
        await event.respond("Please specify the channel username or ID after the command. Example: /setchannel @channelusername")
    save_settings()  # Save after updating the preference

@client.on(events.NewMessage)
async def schedule_message(event):
    # Skip command processing
    if event.raw_text.startswith('/'):
        return
    
    # Ensure the user has set a target channel
    if event.sender_id not in user_channel_preferences:
        await event.respond("Please set a target channel first using the /setchannel command.")
        return
    
    # Ensure the user has set a timeline
    if event.sender_id not in user_timelines or not user_timelines[event.sender_id]:
        await event.respond("Please set your post scheduling timeline first using the /set_timeline command.")
        return

    target_channel = user_channel_preferences[event.sender_id]
    current_timeline = user_timelines[event.sender_id]
    next_index = user_next_timestamps.get(event.sender_id, 0)

    # Calculate how many days in the future we need to schedule this message
    days_ahead = next_index // len(current_timeline)
    next_index %= len(current_timeline)  # This gets the next index in the timeline

    next_timestamp = current_timeline[next_index]
    schedule_date = datetime.now() + timedelta(days=days_ahead)
    schedule_time_str = f"{schedule_date.strftime('%Y-%m-%d')} {next_timestamp}"
    schedule_time = datetime.strptime(schedule_time_str, '%Y-%m-%d %H:%M:%S')

    user_next_timestamps[event.sender_id] = user_next_timestamps.get(event.sender_id, 0) + 1

    # Feedback to the user about the scheduling
    await event.respond(f"Your message has been scheduled for {schedule_time} to be sent to '{target_channel}'.")

    # Scheduling logic (asyncio.sleep to delay until the scheduled time)
    delta_seconds = (schedule_time - datetime.now()).total_seconds()
    await asyncio.sleep(delta_seconds)

    # Forward the message with media
    await event.message.forward_to(target_channel)


def main():
    print("SBot is running...")
    client.run_until_disconnected()

if __name__ == '__main__':
    main()
