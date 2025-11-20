# Gemini's Notes for Samir's Sticker Bot

This file will track the development process, decisions made, and the overall plan for building the Telegram bot for the "sticky_online_store".

## Project Goals

- Create a Telegram bot to promote a custom sticker business.
- Offer a free sticker to users who subscribe to a Telegram channel.
- Register users to prevent abuse of the free offer.
- Collect user orders for the free sticker.
- Notify the admin (Samir) of new orders.
- Advertise the main sticker business.

## Bot Flow & Features

1.  **Start & Language Selection:**
    - User starts the bot with `/start`.
    - Bot replies with a welcome message and asks to select a language (ENG/UZB/RUS) via inline buttons.
    - The chosen language will be used for all subsequent communication with that user.

2.  **Channel Subscription:**
    - Bot asks the user to subscribe to the `@sticky_online_store` channel.
    - A button "✅ I have subscribed" is provided.
    - The bot will verify the user's membership in the channel. If not a member, it will prompt them again.

3.  **User Registration:**
    - Once subscription is confirmed, the registration process begins.
    - The bot checks if the user (by `user_id`) is already in the database. If so, it informs them they've already registered.
    - **Collect Nickname:** Bot asks for the user's unique school nickname.
    - **Collect Stage:** Bot asks for their stage (Intensive/Core) with buttons.
    - **Collect Tribe:** Based on the stage, the bot presents the corresponding tribe options (Ayiq, Jayron, etc.) with buttons.

4.  **Database:**
    - An SQLite database will be used.
    - A `users` table will store:
        - `user_id` (Primary Key)
        - `telegram_username`
        - `language`
        - `nickname`
        - `stage`
        - `tribe`
        - `chosen_logo`
        - `registration_timestamp`

5.  **Free Sticker Order:**
    - After registration, the user can choose the logo for their free sticker.
    - **Choose Stage for Logo:** Bot asks which stage's logos they want to see (Intensive/Core).
    - **Choose Tribe for Logo:** Bot shows the relevant tribe logos as buttons.
    - Upon selection, the bot sends a picture of the chosen tribe's logo.
    - The caption will confirm the order and provide a pickup date (placeholder).
    - The `chosen_logo` is saved to the database.

6.  **Admin Notification:**
    - A formatted message with all the user's details and their order is sent to the Admin ID (`1096327366`).

7.  **Advertisement:**
    - After the order confirmation, the bot sends a final message.
    - This message will be an advertisement for the paid sticker service, including the special offer for nickname stickers.
    - It will be sent with a sample image and a button linking to Samir's personal Telegram account (`t.me/JUST_Samir`).

## Technical Details

- **Language:** Python
- **Library:** `python-telegram-bot`
- **Database:** SQLite3
- **Key Feature:** `ConversationHandler` to manage the multi-step interaction flow.
- **File Structure:**
    - `bot.py`: Main application logic.
    - `database.py`: Database setup and functions.
    - `locales.py`: All bot text in ENG, UZB, RUS.
    - `GEMINI.md`: This file.
    - `README.md`: Instructions for setup and running the bot.
    - `requirements.txt`: Project dependencies.
    - `images/`: Directory for tribe logos and ad images.

## Development Plan

- **Step 1: Setup Project Structure:** Create all the necessary files and directories.
- **Step 2: Database:** Implement `database.py`.
- **Step 3: Locales:** Implement `locales.py` with all the text.
- **Step 4: Bot Core:** Set up the main `bot.py`, including constants and the `ConversationHandler` skeleton.
- **Step 5: Implement Conversation Flow:** Build out each step of the conversation from language selection to the final advertisement.
- **Step 6: Placeholders:** Add comments for sticker and image placeholders.
- **Step 7: Documentation:** Write the `README.md` file.
- **Step 8: Final Review:** Test the entire flow and ensure all requirements are met.

## Development Updates

### Session 2 (2025-11-19): API Integration & Flow Overhaul

In this session, we significantly changed the user registration flow to improve validation and user experience.

**1. Nickname Validation via API:**
-   The bot no longer accepts any nickname. It now validates the user's nickname against the official School 21 API (`https://platform.21-school.ru/services/21-school/api/v1/participants/{login}`).
-   This prevents users from registering with fake nicknames.
-   If a nickname is invalid, the user is prompted to try again.

**2. Automatic Stage & Tribe Detection:**
-   Upon successful API validation, the bot automatically retrieves the user's `stage` (from `parallelName`) and `tribe` (from `className`).
-   The manual steps for asking the user to select their stage and tribe have been removed, simplifying the conversation flow.

**3. Real Name Verification:**
-   A new step was added to the registration process: the bot now asks for the user's **full name**.
-   This name is stored in the database in a new `real_name` column.
-   **Purpose:** To help with identity verification when distributing the stickers at school.

**4. Enhanced Admin Notifications:**
-   The admin notification message format was changed to use HTML for more reliable bolding.
-   The user's selected `language` was removed from the notification to make it cleaner.
-   The user's `real_name` was added to the notification.
-   Notifications are now sent to a **support group chat** (`-1003141015653`) in addition to the primary admin, allowing a team to manage orders.

**Technical Changes:**
-   Added `requests` to `requirements.txt` and used the `httpx` library (an existing dependency) for making asynchronous API calls.
-   Modified `database.py` to add the `real_name` column to the `users` table and handle schema migration.
-   Updated `locales.py` with new text for the changed flow.
-   Overhauled the `ConversationHandler` logic in `bot.py`.

### Session 3 (2025-11-20): Terminology Updates & Bonus Flow Enhancement

This session focused on refining the bot's language based on user feedback and improving the bonus sticker acquisition flow.

**1. Terminology Changes:**
-   **Tribe -> Wave:** The term "Tribe" was replaced with "Wave" in the admin notification message for new orders to reflect the correct internal terminology.
-   **Nickname -> Nickname/Login:** To avoid confusion, the prompt for the user's nickname was changed to "**Nickname/Login**" in all user-facing messages and in the admin notifications.
-   **Full Name -> Name:** The request for a "full name" was simplified to just "name" to reduce friction during registration.

**2. Bonus Offer Enhancement:**
-   The bonus sticker offer, which appears after the main advertisement, was changed from a text-only message to a photo with a caption.
-   The bot now sends an image (`images/bonus_offer.png`) that can visually present the bonus choices, with the offer text as the caption.

**3. Code Deployment:**
-   All changes from this session were committed and pushed to the `main` branch of the remote GitHub repository.
