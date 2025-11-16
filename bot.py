# Explanation for Samir:
# This is the main file for your bot.
# It brings everything together: the conversation logic, the text from locales.py, and the database functions from database.py.
# I've added comments to explain each major part of the code.

import logging
import os
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

# --- Local Imports ---
# Import the functions and text we defined in our other files.
import database as db
from locales import TEXT, TRIBES

# --- Configuration ---
# Explanation for Samir:
# It's very important to keep your token secret.
# We will get it from an environment variable so you don't have to write it directly in the code.
# You will need to create a file named '.env' and put your token there like this:
# BOT_TOKEN="123456:ABC-DEF1234567890"
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
    print("IMPORTANT: Bot token is not set. Please set the BOT_TOKEN environment variable.")

ADMIN_ID = 1096327366
CHANNEL_USERNAME = "@sticky_online_store" # Make sure to include the '@'

# --- Logging ---
# This helps us see errors and information about what the bot is doing.
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# --- Conversation States ---
# Explanation for Samir:
# These are like "steps" or "stages" in the conversation.
# The bot uses these to remember where it is in the process with each user.
(
    SELECT_LANG,
    CHECK_SUB,
    GET_NICKNAME,
    GET_STAGE,
    GET_TRIBE,
    CHOOSE_LOGO_STAGE,
    CHOOSE_LOGO_TRIBE,
) = range(7)


# --- Helper Functions ---
def get_text(key: str, lang: str) -> str:
    """Gets text from the locales dictionary for the given language."""
    return TEXT.get(lang, TEXT['en']).get(key, f"Missing text for key: {key}")


# --- Conversation Entry Point ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Starts the conversation when the user sends /start.
    Greets the user and asks for their language.
    """
    user = update.effective_user
    logger.info(f"User {user.id} ({user.username}) started the bot.")

    # Check if user is already registered
    if db.user_exists(user.id):
        # Since we don't know their language yet, we'll have to guess or send in a default.
        # A better approach would be to save lang on first contact, even before registration.
        # For now, we'll just send in English. We can refine this later.
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

    # Using the English 'welcome' text as it's the first interaction.
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
        # The user's status can be 'creator', 'administrator', 'member', 'restricted', 'left', or 'kicked'.
        # We accept anyone who is not 'left' or 'kicked'.
        if member.status not in ["left", "kicked"]:
            logger.info(f"User {user.id} is subscribed to {CHANNEL_USERNAME}.")
            await query.edit_message_text(text=get_text('ask_nickname', lang), parse_mode='Markdown')
            return GET_NICKNAME
        else:
            logger.info(f"User {user.id} is NOT subscribed to {CHANNEL_USERNAME}.")
            await query.message.reply_text(text=get_text('not_subscribed', lang), parse_mode='Markdown')
            return CHECK_SUB
    except Exception as e:
        logger.error(f"Error checking subscription for user {user.id}: {e}")
        # Maybe the bot doesn't have permissions, or the channel username is wrong.
        # We should inform the user and the admin.
        await query.message.reply_text("Sorry, I couldn't verify your subscription status right now. Please try again later.")
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"Error checking subscription for user {user.id}. Error: {e}")
        return CHECK_SUB


async def get_nickname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Gets the user's nickname, saves it, and asks for their stage.
    """
    user = update.effective_user
    lang = context.user_data.get("lang", "en")
    nickname = update.message.text
    context.user_data["nickname"] = nickname
    logger.info(f"User {user.id} entered nickname: {nickname}")

    keyboard = [
        [
            InlineKeyboardButton(get_text('intensive_button', lang), callback_data="stage_intensive"),
            InlineKeyboardButton(get_text('core_button', lang), callback_data="stage_core"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        text=get_text('ask_stage', lang).format(nickname=nickname),
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return GET_STAGE


async def get_stage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Gets the user's stage, saves it, and asks for their tribe.
    """
    query = update.callback_query
    await query.answer()
    user = update.effective_user
    lang = context.user_data.get("lang", "en")

    stage = query.data.split("_")[1]
    context.user_data["stage"] = stage
    logger.info(f"User {user.id} selected stage: {stage}")

    # Create buttons for the tribes based on the selected stage
    tribes = TRIBES.get(stage, [])
    keyboard = [
        [InlineKeyboardButton(tribe, callback_data=f"tribe_{tribe}")] for tribe in tribes
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=get_text('ask_tribe', lang),
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return GET_TRIBE


async def get_tribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Gets the user's tribe, saves all registration data to the DB,
    and proceeds to the logo selection phase.
    """
    query = update.callback_query
    await query.answer()
    user = update.effective_user
    lang = context.user_data.get("lang", "en")

    tribe = query.data.split("_")[1]
    context.user_data["tribe"] = tribe
    logger.info(f"User {user.id} selected tribe: {tribe}")

    # --- Save user to database ---
    user_data = context.user_data
    db.add_user(
        user_id=user.id,
        username=user.username or "N/A",
        lang=lang,
        nickname=user_data.get("nickname"),
        stage=user_data.get("stage"),
        tribe=tribe,
    )

    await query.edit_message_text(
        text=get_text('registration_complete', lang),
        parse_mode='Markdown'
    )

    # Explanation for Samir:
    # This is the placeholder where you can send a fun sticker after registration.
    # You'll need to get the 'file_id' of the sticker you want to send.
    # To get a sticker's file_id, you can send the sticker to a bot like @RawDataBot.
    # Then, you can uncomment the line below and replace 'YOUR_STICKER_FILE_ID'
    # await query.message.reply_sticker(sticker='YOUR_STICKER_FILE_ID')


    # --- Proceed to Logo Selection ---
    keyboard = [
        [
            InlineKeyboardButton(get_text('intensive_button', lang), callback_data="logo_stage_intensive"),
            InlineKeyboardButton(get_text('core_button', lang), callback_data="logo_stage_core"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(
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
    Gets the final logo choice, saves it, notifies admin, sends confirmation and ad to user.
    This is the final step in the conversation.
    """
    query = update.callback_query
    await query.answer()
    user = update.effective_user
    lang = context.user_data.get("lang", "en")

    chosen_logo = query.data.split("_")[2]
    logger.info(f"User {user.id} chose the logo: {chosen_logo}")

    # --- Update DB and Notify Admin ---
    db.update_user_logo_choice(user.id, chosen_logo)
    user_details = db.get_user_details(user.id)

    admin_message = get_text('admin_notification', 'en').format(
        user_id=user.id,
        username=user_details.get('telegram_username', 'N/A'),
        lang=user_details.get('language', 'N/A'),
        nickname=user_details.get('nickname', 'N/A'),
        stage=user_details.get('stage', 'N/A'),
        tribe=user_details.get('tribe', 'N/A'),
        chosen_logo=chosen_logo
    )
    await context.bot.send_message(chat_id=ADMIN_ID, text=admin_message)
    logger.info(f"Sent notification to admin for user {user.id}")

    # --- Send Confirmation to User ---
    await query.edit_message_text(text="...") # Clear the buttons

    # Explanation for Samir:
    # This is where you send the image of the tribe logo the user chose.
    # Make sure you have images in the 'images' folder with names like 'Ayiq.png', 'Pegasus.png', etc.
    # The code will look for a file with the exact name of the chosen logo.
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
        # If the image is missing, send a text confirmation instead.
        await query.message.reply_text(
            text=get_text('order_complete', lang).format(chosen_logo=chosen_logo),
            parse_mode='Markdown'
        )


    # --- Send Advertisement ---
    ad_keyboard = [
        [InlineKeyboardButton(get_text('contact_me_button', lang), url="https://t.me/JUST_Samir")]
    ]
    ad_markup = InlineKeyboardMarkup(ad_keyboard)

    # Explanation for Samir:
    # This is for the advertisement. Place an attractive image for your ad
    # in the 'images' folder and name it 'ad_sample.png'.
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
        # If the ad image is missing, just send the text.
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
    return ConversationHandler.END


# --- Main Application Setup ---
def main() -> None:
    """
    This is the main function that runs the bot.
    """
    # Explanation for Samir:
    # First, we make sure the database table is created and ready.
    logger.info("Setting up database...")
    db.setup_database()

    logger.info("Starting bot...")
    # The Application object connects to the Telegram API.
    application = Application.builder().token(BOT_TOKEN).build()

    # Explanation for Samir:
    # This is the ConversationHandler. It's the heart of the bot's logic.
    # It manages the flow of the conversation from one step to the next.
    # - entry_points: This is how the conversation starts (with the /start command).
    # - states: This defines all the possible steps and which functions to call for each one.
    # - fallbacks: If the user sends something unexpected, this handles it.
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
            GET_STAGE: [
                CallbackQueryHandler(get_stage, pattern="^stage_"),
            ],
            GET_TRIBE: [
                CallbackQueryHandler(get_tribe, pattern="^tribe_"),
            ],
            CHOOSE_LOGO_STAGE: [
                CallbackQueryHandler(choose_logo_stage, pattern="^logo_stage_"),
            ],
            CHOOSE_LOGO_TRIBE: [
                CallbackQueryHandler(choose_logo_tribe, pattern="^logo_tribe_"),
            ],
            # Other states will be added here.
        },
        fallbacks=[
            MessageHandler(filters.TEXT | filters.COMMAND, fallback),
        ],
    )

    # --- Admin Reset Command ---
    async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """A command for the admin to reset their own user data for testing."""
        user = update.effective_user
        if user.id == ADMIN_ID:
            db.delete_user(user.id)
            await update.message.reply_text("Your user data has been reset. You can now use /start again.")
            logger.info(f"Admin {user.id} has reset their data.")
        else:
            logger.warning(f"User {user.id} tried to use the /reset command without permission.")
            # We don't need to tell the user they can't use it, just ignore.

    application.add_handler(CommandHandler("reset", reset_command))
    application.add_handler(conv_handler)

    # Start the Bot
    application.run_polling()


if __name__ == "__main__":
    main()
