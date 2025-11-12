# ===============================================
# main.py — The Orchestrator
# Coordinates fetching quotes, users, and emails
# ===============================================

import time
import logging
from app import db, quote_fetcher, emailer
from datetime import datetime


# Setup logging 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)


# Log in sections for readability
def log_section_header(title):                                                  
    line = "=" * 80
    logging.info(f"\n{line}\n=== {title.upper()} ({datetime.now().date()}) ===\n{line}")


# Main job function
def main():
    logging.info("\n" + "="*80)
    logging.info("=== Mindfuel Daily Quotes Job Started ===")

    # Initialize the database and create or ensure tables exist
    db.create_tables()

    # Fetch daily quote
    quote_data = quote_fetcher.fetch_quote()
    if not quote_data:
        logging.error("Failed to fetch quote. Exiting job")
        return
    logging.info(f"Quote fetched: {quote_data['quote']} - {quote_data['author']}")

    # Fetch daily active users
    log_section_header("Daily Quotes")
    daily_users = db.fetch_active_users("daily")
    if not daily_users:
        logging.warning("No active daily users found.")
    else:
        logging.info(f"Found {len(daily_users)} active users.")
        send_to_users(daily_users, quote_data, "daily")

    # Fetch weekly active users
    # Assuming the system would send mail to weekly only on Mondays with 0 being Monday
    if datetime.now().weekday() == 0: 
        log_section_header("Weekly Quotes")
        weekly_users = db.fetch_active_users("weekly")
        if not weekly_users:
            logging.warning("No active weekly users found.")
        else:
            logging.info(f"Found {len(weekly_users)} active users.")
            send_to_users(weekly_users, quote_data, "weekly")
    
    logging.info("=== Mindfuel Daily Quotes Job Completed ===")
    logging.info("="*80 + "\n")


# Send email to each users based on their preferred frequency
def send_to_users(users, quote_data, frequency):
    for user in users:
        time.sleep(2)       # pause between sends
        user_id, email, name = user
        first_name = name.split()[0]

        success = emailer.send_email(
            quote=quote_data["quote"],
            author=quote_data["author"],
            name=first_name,
            to_email=email,
            frequency=frequency
        )
    
        # Log email status in DB
        db.log_email_status(
            user_id=user_id, 
            success=success,
            error_message=None if success else "Email failed to send"
)

# Run the job
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"Unexpected error occured: {e}")
    finally:
        # Send daily summary email to admin
        summary = db.get_daily_summary()
        emailer.send_summary_email(summary)







'''
# Testing
if __name__ == "__main__":
    # Initialize the database and create tables
    db.create_tables()

    # Insert test users
    db.insert_user("user1@example.com", "Alice", "daily")
    db.insert_user("user2@example.com", "Bob", "weekly")

    # Fetch and print active daily users
    daily_users = db.fetch_active_users("daily")
    for user in daily_users:
        print(f"User ID: {user[0]}, Email: {user[1]}, Name: {user[2]}")
    print("Database initialized and test users added.")
'''