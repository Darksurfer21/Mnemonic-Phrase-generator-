import requests
from mnemonic import Mnemonic
import time
import os

# Replace 'YOUR_BOT_TOKEN' with your actual Telegram bot token
BOT_TOKEN = 'YOUR_BOT_TOKEN'
CHAT_ID = 'CHAT ID'  # Replace with your chat ID or get from updates

# Function to send a message to Telegram
def send_message(text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {'chat_id': CHAT_ID, 'text': text}
    requests.post(url, data=payload)

# Function to send a file to Telegram
def send_file(file_path):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendDocument'
    with open(file_path, 'rb') as file:
        files = {'document': file}
        payload = {'chat_id': CHAT_ID}
        requests.post(url, data=payload, files=files)

# Function to generate mnemonics
def generate_mnemonics(num_phrases=1000):
    mnemo = Mnemonic("english")
    phrases = []

    for _ in range(num_phrases):
        phrase = mnemo.generate(strength=128)  # 128 bits for 12-word phrases
        phrases.append(phrase)

    return phrases

# Function to handle the mnemonic generation
def generate_and_send_mnemonics():
    send_message("Generating 1,000 mnemonic phrases...")
    
    # Generate mnemonics
    phrases = generate_mnemonics(1000)
    
    # Save phrases to a text file
    file_path = 'mnemonics.txt'
    with open(file_path, 'w') as file:
        for phrase in phrases:
            file.write(f"{phrase}\n")

    # Send the file to the user
    send_file(file_path)
    send_message("1,000 mnemonic phrases generated and sent as mnemonics.txt.")

    # Optionally remove the file after sending

# Function to get updates from the bot
def get_updates():
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates'
    response = requests.get(url)
    return response.json()

# Main function to run the bot
def main():
    send_message("Bot is now running...")
    last_update_id = None

    while True:
        updates = get_updates()

        for update in updates['result']:
            update_id = update['update_id']
            if update_id != last_update_id:
                last_update_id = update_id
                
                # Check for the command /gen
                if 'message' in update and 'text' in update['message']:
                    text = update['message']['text']
                    if text == '/gen':
                        generate_and_send_mnemonics()

        time.sleep(1)  # Polling delay

# Run the bot
if __name__ == "__main__":
    main()

print('Made by - Mr Snow ❄️ ')
