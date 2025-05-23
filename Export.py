import os
import csv
from db_config import get_connection

def export_all():
    """
    Connects to the Jellies database, exports each table
    to a CSV file under an 'exports' folder.
    """
    tables = ['CustomerData', 'Inventory', 'BusinessIndex']
    export_dir = os.path.join(os.path.dirname(__file__), 'exports')
    os.makedirs(export_dir, exist_ok=True)

    cnx = get_connection()
    cursor = cnx.cursor()

    for table in tables:
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

        csv_path = os.path.join(export_dir, f"{table}.csv")
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(rows)

    cursor.close()
    cnx.close()
