import sqlite3
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

DB_FILE = "sticker_bot.db"

def db_connect():
    """Create a database connection to the SQLite database."""
    try:
        conn = sqlite3.connect(DB_FILE)
        return conn
    except sqlite3.Error as e:
        logger.error(f"Error connecting to database: {e}")
        return None

def setup_database():
    """
    Set up the database. Creates the 'users' table if it doesn't exist
    and adds new columns if they are missing.
    This function should be called once when the bot starts.
    """
    conn = db_connect()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        # Explanation for Samir:
        # This SQL command creates the table that will store all the user information.
        # - real_name: The user's actual first/last name for verification.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                telegram_username TEXT,
                language TEXT,
                nickname TEXT,
                stage TEXT,
                tribe TEXT,
                chosen_logo TEXT,
                real_name TEXT,
                registration_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                bonus_claimed INTEGER DEFAULT 0
            )
        """)
        conn.commit()

        # --- Migration: Add real_name column if it doesn't exist (for existing databases) ---
        cursor.execute("PRAGMA table_info(users)")
        columns = [info[1] for info in cursor.fetchall()]
        if 'real_name' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN real_name TEXT")
            conn.commit()
            logger.info("Added 'real_name' column to existing 'users' table.")

        # --- Migration: Add bonus_claimed column if it doesn't exist ---
        if 'bonus_claimed' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN bonus_claimed INTEGER DEFAULT 0")
            conn.commit()
            logger.info("Added 'bonus_claimed' column to existing 'users' table.")
        # --- End of Migration ---

        logger.info("Database setup complete. 'users' table is ready.")
    except sqlite3.Error as e:
        logger.error(f"Error setting up database table: {e}")
    finally:
        if conn:
            conn.close()

def user_exists(user_id: int) -> bool:
    """
    Check if a user already exists in the database.
    This is crucial to prevent users from registering for the free sticker multiple times.
    """
    conn = db_connect()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
        return cursor.fetchone() is not None
    except sqlite3.Error as e:
        logger.error(f"Error checking if user {user_id} exists: {e}")
        return False
    finally:
        if conn:
            conn.close()

def add_user(user_id: int, username: str, lang: str, nickname: str, stage: str, tribe: str, real_name: str):
    """
    Add a new user to the database after they complete the initial registration.
    """
    conn = db_connect()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        # Explanation for Samir:
        # This command inserts a new row into the 'users' table.
        # We added the 'real_name' to store the user's actual name for verification.
        cursor.execute("""
            INSERT INTO users (user_id, telegram_username, language, nickname, stage, tribe, real_name)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, username, lang, nickname, stage, tribe, real_name))
        conn.commit()
        logger.info(f"Added new user {user_id} ({nickname}) with real name {real_name} to the database.")
    except sqlite3.Error as e:
        logger.error(f"Error adding user {user_id}: {e}")
    finally:
        if conn:
            conn.close()

def update_user_logo_choice(user_id: int, chosen_logo: str):
    """
    Update a user's record with the tribe logo they chose for their free sticker.
    """
    conn = db_connect()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        # Explanation for Samir:
        # This command updates an existing row. It finds the user by their 'user_id'
        # and sets the 'chosen_logo' field to their selection.
        cursor.execute("""
            UPDATE users
            SET chosen_logo = ?
            WHERE user_id = ?
        """, (chosen_logo, user_id))
        conn.commit()
        logger.info(f"Updated logo choice for user {user_id} to {chosen_logo}.")
    except sqlite3.Error as e:
        logger.error(f"Error updating logo choice for user {user_id}: {e}")
    finally:
        if conn:
            conn.close()

def get_user_details(user_id: int) -> dict:
    """
    Retrieve all details for a specific user.
    Useful for sending the complete order information to the admin.
    """
    conn = db_connect()
    if conn is None:
        return {}

    try:
        conn.row_factory = sqlite3.Row  # This allows accessing columns by name
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user_data = cursor.fetchone()
        return dict(user_data) if user_data else {}
    except sqlite3.Error as e:
        logger.error(f"Error getting details for user {user_id}: {e}")
        return {}
    finally:
        if conn:
            conn.close()

def set_bonus_claimed(user_id: int):
    """
    Sets the bonus_claimed flag to 1 for a given user.
    """
    conn = db_connect()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users
            SET bonus_claimed = 1
            WHERE user_id = ?
        """, (user_id,))
        conn.commit()
        logger.info(f"User {user_id} has claimed their bonus sticker.")
    except sqlite3.Error as e:
        logger.error(f"Error setting bonus_claimed for user {user_id}: {e}")
    finally:
        if conn:
            conn.close()

def delete_user(user_id: int):
    """
    Deletes a user from the database. Used by the admin for testing.
    """
    conn = db_connect()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        logger.info(f"Deleted user {user_id} from the database.")
    except sqlite3.Error as e:
        logger.error(f"Error deleting user {user_id}: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    # Explanation for Samir:
    # This part of the script runs only when you execute `python database.py` directly.
    # It's a good way to initialize the database for the first time.
    print("Setting up the database...")
    setup_database()
    print("Database setup is done.")
