import os
import pandas as pd
from db_config import get_connection

# Configuration: output folder
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'exports')
os.makedirs(OUTPUT_DIR, exist_ok=True)

QUERY_TEMPLATES = {
    'CustomerData': 'SELECT * FROM CustomerData;',
    'Inventory': 'SELECT * FROM Inventory;',
    'BusinessIndex': 'SELECT * FROM BusinessIndex;',
}


def export_table(table_name: str, query: str):
    """Exports a SQL query result to a CSV file."""
    cnx = get_connection()
    try:
        df = pd.read_sql(query, cnx)
        output_path = os.path.join(OUTPUT_DIR, f"{table_name}.csv")
        df.to_csv(output_path, index=False)
        print(f"Exported {table_name} to {output_path}")
    except Exception as e:
        print(f"Error exporting {table_name}: {e}")
    finally:
        cnx.close()


def main():
    print("Starting data export...")
    for name, query in QUERY_TEMPLATES.items():
        export_table(name, query)
    print("All data exported successfully.")


if __name__ == '__main__':
    main()
