# Sticky Online Store - Telegram Bot

Hello Samir! This is the Telegram bot we built for your sticker business, `sticky_online_store`.

This bot is designed to attract new customers from school 21 by offering them a free tribe sticker in exchange for subscribing to your channel. It handles the entire process from start to finish.

## Bot Features

- **Multi-Language Support:** Communicates in English, Uzbek, and Russian.
- **Subscription Gate:** Requires users to subscribe to your channel before they can claim a free sticker.
- **User Registration:** Collects and saves the user's nickname, stage, and tribe to a database to prevent duplicate orders.
- **Sticker Ordering:** Allows users to choose a tribe logo for their free sticker.
- **Admin Notifications:** Automatically sends you a message with all the details of a new order.
- **Advertisement:** Promotes your custom sticker service after a user completes their free order.

---

## How to Set Up and Run the Bot

Follow these steps carefully to get your bot running.

### Step 1: Install Dependencies

First, you need to install the `python-telegram-bot` library. I've already created a `requirements.txt` file for this.

Open your terminal in the project directory (`/home/gildaolg-samir/my bot/`) and run this command:

```bash
# Make sure you are in your virtual environment (.venv) first
source .venv/bin/activate

# Install the required library
pip install -r requirements.txt
```

### Step 2: Set Your Bot Token

Your bot's token is like a secret password. **Never share it or write it directly in the code.** We will use an environment variable for this.

1.  Create a new file in the project directory named `.env`.
2.  Open the `.env` file and add your bot token in the following format. (Replace `123...` with your actual token from BotFather).

    ```
    BOT_TOKEN="123456:ABC-DEF1234567890"
    ```
3. The bot is programmed to read from this file. You will need to install a library to help with that. Run this command:
    ```bash
    pip install python-dotenv
    ```

### Step 3: Prepare the Images

The bot needs to send images for the tribe logos and the advertisement.

1.  Go to the `images/` directory.
2.  Add your tribe logo images here. **The names must match the tribe names exactly** and they should be `.png` files. For example:
    - `Ayiq.png`
    - `Jayron.png`
    - `Pegasus.png`
    - `Dragon.png`
    - ...and so on for all 8 tribes.
3.  Add the image for your advertisement and name it `ad_sample.png`.

If an image is missing, the bot will send a text message instead, but it looks much more professional with the images!

### Step 4: Initialize the Database

The first time you run the bot, you need to create the database file (`sticker_bot.db`) and the `users` table inside it.

Run the `database.py` script directly to do this:

```bash
python database.py
```

You will see a message saying "Setting up the database..." and "Database setup is done.". You only need to do this once.

### Step 5: Run the Bot!

Now you are ready to start the bot. Run the `bot.py` script:

```bash
python bot.py
```

You will see a message like "Starting bot...". Your bot is now online and ready to receive messages!

To stop the bot, go to your terminal and press `Ctrl + C`.

---

That's it! If you have any questions or need to make changes, you can review the code. I've left many comments and explanations for you in `bot.py`, `database.py`, and `locales.py`. Good luck with your sticker business!

---

## Testing the Bot

The bot is designed to prevent a user from registering more than once. This is great for production, but it can make it difficult for you, the admin, to test the full conversation flow multiple times.

To solve this, I have added a special, admin-only command:

### `/reset`

- **What it does:** This command deletes your own user record from the database.
- **How to use it:** Simply send `/reset` to the bot.
- **Who can use it:** Only you (the `ADMIN_ID` set in the code). The bot will ignore this command if sent by anyone else.

After you use `/reset`, the bot will forget that you have registered, and you can use `/start` to go through the entire process again from the beginning.
