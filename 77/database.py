import sqlite3
import psycopg2

import config


def setup_database_logging():
    global db_connection
    if config['db_type'] == 'sqlite':
        db_connection = sqlite3.connect(config['db_path'])
    elif config['db_type'] == 'postgresql':
        db_connection = psycopg2.connect(
            host=config['db_host'],
            port=config['db_port'],
            user=config['db_user'],
            password=config['db_password']
        )
    create_table_if_not_exists()

def create_table_if_not_exists():
    if config['db_type'] == 'sqlite':
        with db_connection:
            db_connection.execute(f"""
                CREATE TABLE IF NOT EXISTS {config['db_table']} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entry TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
    elif config['db_type'] == 'postgresql':
        with db_connection.cursor() as cursor:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {config['db_table']} (
                    id SERIAL PRIMARY KEY,
                    entry TEXT,
                    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                )
            """)
            db_connection.commit()

def log_to_database(entry):
    if config.get('db_logging'):
        if config['db_type'] == 'sqlite':
            with db_connection:
                db_connection.execute(f"INSERT INTO {config['db_table']} (entry) VALUES (?)", (entry,))
        elif config['db_type'] == 'postgresql':
            with db_connection.cursor() as cursor:
                cursor.execute(f"INSERT INTO {config['db_table']} (entry) VALUES (%s)", (entry,))
                db_connection.commit()
