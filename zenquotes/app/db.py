from app import config
import psycopg2
from psycopg2 import sql
import logging
from contextlib import contextmanager


# Context manager to establish connection to the PostgreSQL database
@contextmanager
def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=config.DB_PORT
        )
        yield conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise
    finally:
        if conn:
            conn.close()


# Create tables in database
def create_table():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            create_users_table = sql.SQL('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                name VARCHAR(100) NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                frequency VARCHAR(10) CHECK (frequency IN ('daily', 'weekly')) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
            ''')
            
            create_email_sends_table = sql.SQL('''
            CREATE TABLE IF NOT EXISTS email_sends (
                id SERIAL PRIMARY KEY,
                user_id INT REFERENCES users(id),
                send_date DATE DEFAULT CURRENT_DATE,
                status VARCHAR(20) CHECK (status IN ('sent', 'failed')) NOT NULL,
                error_message TEXT,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
            ''')
            
            cursor.execute(create_users_table)
            cursor.execute(create_email_sends_table)
        conn.commit()


# Insert a new user into the database
def insert_user(email, name, frequency):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:   
            insert_query = sql.SQL('''
                INSERT INTO users (email,name,frequency)
                VALUES (%s, %s, %s)
                ON CONFLICT (email) DO NOTHING;
            ''')
            cursor.execute(insert_query, (email, name, frequency))
            conn.commit()


# Fetch active users with their email frequency
def fetch_active_users(frequency):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            fetch_query = sql.SQL('''
                SELECT id, email, name FROM users
                WHERE is_active = TRUE AND frequency = %s;
            ''')
            cursor.execute(fetch_query, (frequency,))
            users = cursor.fetchall()
            return users


# Log email sent status into email_sends table
def log_email_status(user_id, success, error_message=None):
    with get_db_connection() as conn:
        try:
            with conn.cursor() as cursor:
                status = "sent" if success else "failed"

                insert_query = sql.SQL("""
                    INSERT INTO email_sends (user_id, status, error_message)
                    VALUES (%s, %s, %s);
                """)
        
                cursor.execute(insert_query, (user_id, status, error_message))
                conn.commit()

                logging.info(f"Email log inserted for user_id={user_id} with status={status}")

        except Exception as e:
            logging.error(f"Error logging email status for user_id={user_id}: {e}")
            conn.rollback()

    

# Get daily summary of sent/failed emails
def get_daily_summary():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            query = sql.SQL("""
                SELECT status, COUNT(*)
                FROM email_sends
                WHERE send_date = CURRENT_DATE
                GROUP BY status;
            """)
            cursor.execute(query)
            results = cursor.fetchall()

    summary = {"sent": 0, "failed": 0}
    for status, count in results:
        summary[status] = count
    return summary