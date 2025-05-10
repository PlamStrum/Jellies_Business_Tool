# setup_db.py
import mysql.connector
from mysql.connector import errorcode
import os

# 1) Update these values with your MySQL settings
DB_CONFIG = {
    'user':     'root',
    'password': 'password',
    'host':     '127.0.0.1',        # or 'localhost'
    'port':     3306,
    # don't specify database here; the script will create it
}


def run_schema(sql_file_path: str):
    """Connects to MySQL and executes each statement in the given .sql file."""
    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        cursor = cnx.cursor()
        print("Connected to MySQL server.")

        # Read the full contents of schema.sql
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()

        # Split on semicolons and execute each non-empty statement
        for raw_stmt in schema_sql.split(';'):
            stmt = raw_stmt.strip()
            if not stmt:
                continue
            cursor.execute(stmt)
            first_line = stmt.splitlines()[0]
            print(f"→ Executed: {first_line[:50]}{'...' if len(first_line) > 50 else ''}")

        cnx.commit()
        print("Database schema created/updated successfully.")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Authentication error: check your username or password")
        else:
            print(f"Error: {err}")
    finally:
        cursor.close()
        cnx.close()


if __name__ == '__main__':
    # Determine absolute path to schema.sql
    base_dir = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(base_dir, 'schema.sql')
    print("Running schema from:", schema_path)
    run_schema(schema_path)