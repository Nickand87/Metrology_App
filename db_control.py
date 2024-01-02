import sqlite3
import os
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import QMessageBox
import sys


class DatabaseManager:
    """Handles database operations including initialization."""
    def __init__(self):
        self.db_folder = self.ensure_db_directory_exists()
        self.databases = self.load_database_names()
        self.connections = self.initialize_databases()

    def read_db_path_from_settings(self):
        """Read the database path from the XML settings file."""
        try:
            tree = ET.parse('settings.xml')
            root = tree.getroot()
            db_path = root.find('database/path').text
            return db_path
        except ET.ParseError:
            QMessageBox.critical(None, "Error", "Error parsing settings.xml.")
            sys.exit(1)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error reading settings: {str(e)}")
            sys.exit(1)

    def load_database_names(self):
        """Load the names of all databases from settings or a predefined list."""
        # Example: reading from a predefined list
        return ['Clients.db', 'Orders.db']

    def ensure_db_directory_exists(self):
        """Ensure the directory for the databases exists."""
        db_directory = self.read_db_path_from_settings()
        if not os.path.exists(db_directory):
            os.makedirs(db_directory)
        return db_directory

    def initialize_databases(self):
        """Initialize multiple databases and return their connections."""
        connections = {}
        db_initialization_mapping = {
            'Clients.db': self.initialize_clients_db,
            'Orders.db': self.initialize_orders_db,
        }

        for db_name in self.databases:
            db_path = os.path.join(self.db_folder, db_name)
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                # Call the specific initialization function for each database
                if db_name in db_initialization_mapping:
                    db_initialization_mapping[db_name](cursor)
                else:
                    print(f"No initialization function defined for {db_name}")

                connections[db_name] = conn
            except sqlite3.Error as e:
                print(f"Database Error with {db_name}: {str(e)}")
                QMessageBox.critical(None, "Database Error", f"{db_name}: {str(e)}")
                sys.exit(1)
        return connections

    def fetch_data(self, db_name, query, params=None):
        """Fetch data from the specified database using a SQL query."""
        if db_name in self.connections:
            conn = self.connections[db_name]
            try:
                cursor = conn.cursor()
                cursor.execute(query, params or ())
                return cursor.fetchall()
            except sqlite3.Error as e:
                print(f"Error fetching data from {db_name}: {str(e)}")
                QMessageBox.critical(None, "Database Error", f"Error fetching data from {db_name}: {str(e)}")
                return []
        else:
            QMessageBox.critical(None, "Database Error", f"Database {db_name} not found.")
            return []

    def write_data(self, db_name, table_name, key_field, data):
        """Write data to a specified table in a specified database."""
        if db_name not in self.connections:
            print(f"Database {db_name} not found.")
            return

        conn = self.connections[db_name]
        try:
            cursor = conn.cursor()

            # Check if a record with the key already exists
            select_query = f"SELECT * FROM {table_name} WHERE {key_field} = ?"
            cursor.execute(select_query, (data[key_field],))
            exists = cursor.fetchone()

            if exists:
                # Update existing record
                fields = ", ".join([f"{k} = ?" for k in data if k != key_field])
                values = [v for k, v in data.items() if k != key_field]
                update_query = f"UPDATE {table_name} SET {fields} WHERE {key_field} = ?"
                cursor.execute(update_query, values + [data[key_field]])
            else:
                # Insert new record
                placeholders = ", ".join(["?" for _ in data])
                fields = ", ".join(data.keys())
                values = list(data.values())
                insert_query = f"INSERT INTO {table_name} ({fields}) VALUES ({placeholders})"
                cursor.execute(insert_query, values)

            conn.commit()
        except sqlite3.Error as e:
            print(f"Error writing data to {db_name}: {str(e)}")
            conn.rollback()

    def initialize_clients_db(self, cursor):
        try:
            cursor.execute('''CREATE TABLE IF NOT EXISTS clients 
                               (id INTEGER PRIMARY KEY, client_id INTEGER, client_name TEXT, 
                                client_address1 TEXT, client_address2 TEXT, 
                                client_phone TEXT, client_emailfax TEXT)''')
        except sqlite3.Error as e:
            print(f"Database Error: {str(e)}")
            QMessageBox.critical(None, "Database Error", str(e))
            sys.exit(1)

    def initialize_orders_db(self, cursor):
        try:
            cursor.execute('''CREATE TABLE IF NOT EXISTS orders 
                               (id INTEGER PRIMARY KEY, client_id INTEGER, client_name TEXT, 
                                client_address1 TEXT, client_address2 TEXT, 
                                client_phone TEXT, client_emailfax TEXT)''')
        except sqlite3.Error as e:
            print(f"Database Error: {str(e)}")
            QMessageBox.critical(None, "Database Error", str(e))
            sys.exit(1)














    def add_dummy_clients(self):
        """Add dummy data to the clients table in Clients.db."""
        dummy_clients = [
            (1, 'Alice', '123 Wonderland Lane', 'Suite 1', '555-0101', 'alice@example.com'),
            (2, 'Bob', '456 Nowhere Street', '', '555-0202', 'bob@example.com')
        ]
        query = '''INSERT INTO clients 
                   (client_id, client_name, client_address1, client_address2, 
                   client_phone, client_emailfax) VALUES (?, ?, ?, ?, ?, ?)'''
        db_name = 'Clients.db'
        conn = self.connections[db_name]
        try:
            cursor = conn.cursor()
            cursor.executemany(query, dummy_clients)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding dummy clients to {db_name}: {str(e)}")
            conn.rollback()

    def add_dummy_orders(self):
        """Add dummy data to the orders table in Orders.db."""
        dummy_orders = [
            (1, 1, '2024-01-10', 150.00),
            (2, 2, '2024-01-11', 200.00)
        ]
        query = '''INSERT INTO orders 
                   (order_id, client_id, order_date, order_total) VALUES (?, ?, ?, ?)'''
        db_name = 'Orders.db'
        conn = self.connections[db_name]
        try:
            cursor = conn.cursor()
            cursor.executemany(query, dummy_orders)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding dummy orders to {db_name}: {str(e)}")
            conn.rollback()
