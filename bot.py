# Explanation for Samir:
# This is the main file for your bot.
# It brings everything together: the conversation logic, the text from locales.py, and the database functions from database.py.
# I've added comments to explain each major part of the code.

import logging
import os
import httpx
import time
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

# --- Load Environment Variables ---
# This line loads the .env file so the bot can access the BOT_TOKEN.
load_dotenv()

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from telegram.constants import ParseMode

# --- Local Imports ---
# Import the functions and text we defined in our other files.
import database as db
from locales import TEXT, TRIBES

# --- Configuration ---
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
    print("IMPORTANT: Bot token is not set. Please set the BOT_TOKEN environment variable.")

ADMIN_ID = 1096327366
GROUP_CHAT_ID = -1003141015653
CHANNEL_USERNAME = "@sticky_online_store"  # Make sure to include the '@'
API_BASE_URL = "https://platform.21-school.ru/services/21-school/api/v1"
AUTH_URL = "https://auth.21-school.ru/auth/realms/EduPowerKeycloak/protocol/openid-connect/token"
CLIENT_ID = "s21-open-api"
SCHOOL_USERNAME = os.environ.get("SCHOOL_USERNAME")
SCHOOL_PASSWORD = os.environ.get("SCHOOL_PASSWORD")

if not SCHOOL_USERNAME or not SCHOOL_PASSWORD:
    print("IMPORTANT: SCHOOL_USERNAME or SCHOOL_PASSWORD not set in environment variables. API validation will fail.")


# --- Logging ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# --- Conversation States ---
# Explanation for Samir:
# We've updated the conversation steps. Now, after validating the nickname with the API,
# we directly ask for the real name, skipping the manual stage and tribe selection.
(
    SELECT_LANG,
    CHECK_SUB,
    GET_NICKNAME,
    GET_REAL_NAME,
    CHOOSE_LOGO_STAGE,
    CHOOSE_LOGO_TRIBE,
) = range(6)


# --- Helper Functions ---
def get_text(key: str, lang: str) -> str:
    """Gets text from the locales dictionary for the given language."""
    return TEXT.get(lang, TEXT['en']).get(key, f"Missing text for key: {key}")

_access_token = None
_token_expiry_time = 0 # Unix timestamp

async def get_access_token() -> str | None:
    global _access_token, _token_expiry_time
    current_time = time.time()

    # Check if token is still valid
    if _access_token and _token_expiry_time > current_time + 60: # Refresh 60 seconds before expiry
        return _access_token

    if not SCHOOL_USERNAME or not SCHOOL_PASSWORD:
        logger.error("SCHOOL_USERNAME or SCHOOL_PASSWORD not set in environment variables.")
        return None

    payload = {
        "client_id": CLIENT_ID,
        "username": SCHOOL_USERNAME,
        "password": SCHOOL_PASSWORD,
        "grant_type": "password",
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(AUTH_URL, data=payload, headers=headers)
            response.raise_for_status() # Raise an exception for 4xx or 5xx status codes
            token_data = response.json()
            _access_token = token_data.get("access_token")
            expires_in = token_data.get("expires_in", 300) # Default to 5 minutes if not provided
            _token_expiry_time = current_time + expires_in
            logger.info("Successfully obtained new access token.")
            return _access_token
        except httpx.RequestError as e:
            logger.error(f"Failed to get access token: {e}")
            return None
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error getting access token: {e.response.status_code} - {e.response.text}")
            return None


async def validate_nickname(nickname: str) -> dict | None:
    """
    Validates a nickname against the School 21 API using httpx.
    Returns user data if valid, None otherwise.
    """
    token = await get_access_token()
    if not token:
        logger.error("No access token available for nickname validation.")
        return None

    url = f"{API_BASE_URL}/participants/{nickname}"
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            if response.status_code == 200:
                logger.info(f"API validation successful for nickname: {nickname}")
                return response.json()
            elif response.status_code == 404:
                logger.info(f"API validation failed for nickname {nickname}: Not Found.")
                return None
            else:
                logger.error(f"API error for nickname {nickname}: Status {response.status_code}, Response: {response.text}")
                return None
        except httpx.RequestError as e:
            logger.error(f"API request failed for nickname {nickname}: {e}")
            return None


# --- Conversation Entry Point ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Starts the conversation when the user sends /start.
    Greets the user and asks for their language.
    """
    user = update.effective_user
    logger.info(f"User {user.id} ({user.username}) started the bot.")

    if db.user_exists(user.id):
        user_data = db.get_user_details(user.id)
        lang = user_data.get('language', 'en')
        await update.message.reply_text(get_text('already_registered', lang))
        return ConversationHandler.END

    keyboard = [
        [
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
            InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data="lang_uz"),
            InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        get_text('welcome', 'en'),
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return SELECT_LANG


async def select_lang(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Handles the language selection, saves it, and asks the user to subscribe.
    """
    query = update.callback_query
    await query.answer()

    lang = query.data.split("_")[1]
    context.user_data["lang"] = lang
    logger.info(f"User {update.effective_user.id} selected language: {lang}")

    await query.edit_message_text(text=get_text('lang_selected', lang), parse_mode='Markdown')

    keyboard = [
        [InlineKeyboardButton(get_text('channel_button', lang), url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}")],
        [InlineKeyboardButton(get_text('confirm_button', lang), callback_data="confirm_sub")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(
        text=get_text('ask_subscribe', lang),
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return CHECK_SUB


async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Verifies if the user has subscribed to the channel.
    """
    query = update.callback_query
    await query.answer()
    user = update.effective_user
    lang = context.user_data.get("lang", "en")

    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user.id)
        if member.status not in ["left", "kicked"]:
            logger.info(f"User {user.id} is subscribed to {CHANNEL_USERNAME}.")
            await query.edit_message_text(text=get_text('ask_nickname', lang), parse_mode='Markdown')
            return GET_NICKNAME
        else:
            logger.info(f"User {user.id} is NOT subscribed to {CHANNEL_USERNAME}.")
            await query.message.reply_text(text=get_text('not_subscribed', lang), parse_mode='Markdown')
            # We return to the same state to let them click the button again
            return CHECK_SUB
    except Exception as e:
        logger.error(f"Error checking subscription for user {user.id}: {e}")
        await query.message.reply_text("Sorry, I couldn't verify your subscription status right now. Please try again later.")
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"Error checking subscription for user {user.id}. Error: {e}")
        return CHECK_SUB


async def get_nickname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Gets the user's nickname, validates it via API.
    If valid, it saves the data and asks for their real name.
    If invalid, it asks for the nickname again.
    """
    user = update.effective_user
    lang = context.user_data.get("lang", "en")
    nickname = update.message.text.strip().lower()

    api_data = await validate_nickname(nickname)

    if api_data:
        context.user_data["nickname"] = api_data.get("login")
        context.user_data["stage"] = api_data.get("parallelName")
        context.user_data["tribe"] = api_data.get("className")
        logger.info(f"User {user.id} entered valid nickname: {nickname}. Stage: {api_data.get('parallelName')}, Tribe: {api_data.get('className')}")

        await update.message.reply_text(
            text=get_text('ask_real_name', lang).format(nickname=nickname),
            parse_mode='Markdown'
        )
        return GET_REAL_NAME
    else:
        logger.info(f"User {user.id} entered invalid nickname: {nickname}")
        await update.message.reply_text(
            text=get_text('invalid_nickname', lang).format(nickname=nickname),
            parse_mode='Markdown'
        )
        return GET_NICKNAME


async def get_real_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Gets the user's real name, saves all registration data to the DB,
    and proceeds to the logo selection phase.
    """
    user = update.effective_user
    lang = context.user_data.get("lang", "en")
    real_name = update.message.text.strip()
    context.user_data["real_name"] = real_name
    logger.info(f"User {user.id} entered real name: {real_name}")

    # --- Save user to database ---
    user_data = context.user_data
    db.add_user(
        user_id=user.id,
        username=user.username or "N/A",
        lang=lang,
        nickname=user_data.get("nickname"),
        stage=user_data.get("stage"),
        tribe=user_data.get("tribe"),
        real_name=real_name,
    )

    await update.message.reply_text(
        text=get_text('registration_complete', lang),
        parse_mode='Markdown'
    )

    # --- Proceed to Logo Selection ---
    keyboard = [
        [
            InlineKeyboardButton(get_text('intensive_button', lang), callback_data="logo_stage_intensive"),
            InlineKeyboardButton(get_text('core_button', lang), callback_data="logo_stage_core"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        text=get_text('ask_logo_stage', lang),
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return CHOOSE_LOGO_STAGE


async def choose_logo_stage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Gets the stage for the desired logo and shows the available tribe logos.
    """
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get("lang", "en")

    logo_stage = query.data.split("_")[2]
    logger.info(f"User {update.effective_user.id} chose to see logos from stage: {logo_stage}")

    tribes = TRIBES.get(logo_stage, [])
    keyboard = [
        [InlineKeyboardButton(tribe, callback_data=f"logo_tribe_{tribe}")] for tribe in tribes
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=get_text('ask_logo_tribe', lang),
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return CHOOSE_LOGO_TRIBE


async def choose_logo_tribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Gets the final logo choice, saves it, notifies admin and group, sends confirmation and ad to user.
    This is the final step in the conversation.
    """
    query = update.callback_query
    await query.answer()
    user = update.effective_user
    lang = context.user_data.get("lang", "en")

    chosen_logo = query.data.split("_")[2]
    logger.info(f"User {user.id} chose the logo: {chosen_logo}")

    db.update_user_logo_choice(user.id, chosen_logo)
    user_details = db.get_user_details(user.id)

    # Explanation for Samir:
    # We've changed the format to HTML (<b> for bold) and removed the language.
    admin_message = (
        f"🔔 <b>New Sticker Order</b> 🔔\n\n"
        f"<b>User ID:</b> <code>{user.id}</code>\n"
        f"<b>Username:</b> @{user_details.get('telegram_username', 'N/A')}\n\n"
        f"--- Registration ---\n"
        f"<b>Nickname:</b> {user_details.get('nickname', 'N/A')}\n"
        f"<b>Real Name:</b> {user_details.get('real_name', 'N/A')}\n"
        f"<b>Stage:</b> {user_details.get('stage', 'N/A')}\n"
        f"<b>Tribe:</b> {user_details.get('tribe', 'N/A')}\n\n"
        f"--- Order ---\n"
        f"<b>Chosen Logo:</b> {chosen_logo}"
    )

    # Send notification to admin and the group
    notification_chat_ids = [ADMIN_ID, GROUP_CHAT_ID]
    for chat_id in notification_chat_ids:
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=admin_message,
                parse_mode=ParseMode.HTML
            )
            logger.info(f"Sent notification to chat {chat_id} for user {user.id}")
        except Exception as e:
            logger.error(f"Failed to send notification to chat {chat_id} for user {user.id}. Error: {e}")


    await query.edit_message_text(text="...")

    logo_image_path = f"images/{chosen_logo}.png"
    try:
        with open(logo_image_path, "rb") as photo:
            await query.message.reply_photo(
                photo=photo,
                caption=get_text('order_complete', lang).format(chosen_logo=chosen_logo),
                parse_mode='Markdown'
            )
    except FileNotFoundError:
        logger.error(f"Logo image not found: {logo_image_path}")
        await query.message.reply_text(
            text=get_text('order_complete', lang).format(chosen_logo=chosen_logo),
            parse_mode='Markdown'
        )

    ad_keyboard = [
        [InlineKeyboardButton(get_text('contact_me_button', lang), url="https://t.me/JUST_Samir")]
    ]
    ad_markup = InlineKeyboardMarkup(ad_keyboard)

    ad_image_path = "images/ad_sample.png"
    try:
        with open(ad_image_path, "rb") as ad_photo:
            await query.message.reply_photo(
                photo=ad_photo,
                caption=get_text('advertisement', lang),
                reply_markup=ad_markup,
                parse_mode='Markdown'
            )
    except FileNotFoundError:
        logger.error(f"Advertisement image not found: {ad_image_path}")
        await query.message.reply_text(
            text=get_text('advertisement', lang),
            reply_markup=ad_markup,
            parse_mode='Markdown'
        )

    logger.info(f"Conversation with user {user.id} finished.")
    return ConversationHandler.END


async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Handles any message that is not part of the conversation flow.
    """
    lang = context.user_data.get("lang", "en")
    await update.message.reply_text(get_text('fallback_message', lang))
    # Returning the current state or END can be decided based on desired behavior
    return ConversationHandler.END


from threading import Thread
from flask import Flask

# --- Webserver Setup for Render ---
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)


# --- Main Application Setup ---
def main() -> None:
    """
    This is the main function that runs the bot.
    """
    web_thread = Thread(target=run_web_server)
    web_thread.daemon = True
    web_thread.start()

    logger.info("Setting up database...")
    db.setup_database()

    logger.info("Starting bot...")
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECT_LANG: [
                CallbackQueryHandler(select_lang, pattern="^lang_"),
            ],
            CHECK_SUB: [
                CallbackQueryHandler(check_subscription, pattern="^confirm_sub$"),
            ],
            GET_NICKNAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_nickname),
            ],
            GET_REAL_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_real_name),
            ],
            CHOOSE_LOGO_STAGE: [
                CallbackQueryHandler(choose_logo_stage, pattern="^logo_stage_"),
            ],
            CHOOSE_LOGO_TRIBE: [
                CallbackQueryHandler(choose_logo_tribe, pattern="^logo_tribe_"),
            ],
        },
        fallbacks=[
            MessageHandler(filters.TEXT | filters.COMMAND, fallback),
        ],
    )

    async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """A command for the admin to reset their own user data for testing."""
        user = update.effective_user
        if user.id == ADMIN_ID:
            db.delete_user(user.id)
            await update.message.reply_text("Your user data has been reset. You can now use /start again.")
            logger.info(f"Admin {user.id} has reset their data.")
        else:
            logger.warning(f"User {user.id} tried to use the /reset command without permission.")

    application.add_handler(CommandHandler("reset", reset_command))
    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == "__main__":
    main()
