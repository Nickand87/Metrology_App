from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QFormLayout, QListWidgetItem, QFrame, QMessageBox
from PyQt5.QtGui import QFont, QIntValidator, QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp
from special_classes import EnterLineEdit
import xml.etree.ElementTree as ET
import qdarkstyle
from styles import dark_style, light_style
import sys
import random
from db_control import DatabaseManager


class ClientWindow(QMainWindow):

    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.initializeUI()
        self.search_clients("")

    def initializeUI(self):
        self.setWindowTitle("Client Information")
        self.setGeometry(100, 100, 800, 500)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.setupIDFrame(main_layout)
        self.setupInputFields(main_layout)
        self.setupButtons(main_layout)
        self.setupClientList(main_layout)

    def setupIDFrame(self, layout):
        id_frame = QFrame()
        id_frame.setFrameShape(QFrame.StyledPanel)
        id_layout = QHBoxLayout(id_frame)
        layout.addWidget(id_frame)

        font = QFont("Arial", 12)
        label_font = QFont("Arial", 10, QFont.Bold)

        self.client_id_entry = QLineEdit()
        self.client_id_entry.setValidator(QIntValidator())
        self.client_id_entry.setFont(font)
        self.client_id_entry.setReadOnly(True)  # Make the client_id field read-only

        id_label = QLabel("ID:")
        id_label.setFont(label_font)

        id_layout.addWidget(id_label)
        id_layout.addWidget(self.client_id_entry)

    def setupInputFields(self, layout):
        input_layout = QHBoxLayout()
        layout.addLayout(input_layout)

        self.setupClientInfo(input_layout)
        self.setupContacts(input_layout)

    def setupClientInfo(self, layout):
        clients_frame = QFrame()
        clients_frame.setFrameShape(QFrame.StyledPanel)
        clients_layout = QFormLayout(clients_frame)
        layout.addWidget(clients_frame)

        font = QFont("Arial", 12)
        label_font = QFont("Arial", 10, QFont.Bold)

        clients_title = QLabel("Company Info")
        clients_title.setFont(label_font)
        clients_layout.addRow(clients_title)

        self.client_name_entry = EnterLineEdit()
        self.client_address1_entry = EnterLineEdit()
        self.client_address2_entry = EnterLineEdit()
        self.client_phone_entry = EnterLineEdit()
        self.client_emailfax_entry = EnterLineEdit()

        phone_reg_exp = QRegExp("[0-9\-]+")
        self.client_phone_entry.setValidator(QRegExpValidator(phone_reg_exp))

        for label_text, widget in [
            ("Client Name:", self.client_name_entry),
            ("Address:", self.client_address1_entry),
            ("Address:", self.client_address2_entry),
            ("Phone #:", self.client_phone_entry),
            ("Email/Fax:", self.client_emailfax_entry)
        ]:
            label = QLabel(label_text)
            label.setFont(label_font)
            widget.setFont(font)
            clients_layout.addRow(label, widget)

    def setupContacts(self, layout):
        contacts_frame = QFrame()
        contacts_frame.setFrameShape(QFrame.StyledPanel)
        contacts_layout = QFormLayout(contacts_frame)
        layout.addWidget(contacts_frame)

        font = QFont("Arial", 12)
        label_font = QFont("Arial", 10, QFont.Bold)

        contacts_title = QLabel("Contacts")
        contacts_title.setFont(label_font)
        contacts_layout.addRow(contacts_title)

        self.contact_name_entry = QLineEdit()
        self.contact_address1_entry = QLineEdit()
        self.contact_address2_entry = QLineEdit()
        self.contact_phone_entry = QLineEdit()
        self.contact_emailfax_entry = QLineEdit()

        phone_reg_exp = QRegExp("[0-9\-]+")
        self.contact_phone_entry.setValidator(QRegExpValidator(phone_reg_exp))

        for label_text, widget in [
            ("Contact Name:", self.contact_name_entry),
            ("Address:", self.contact_address1_entry),
            ("Address:", self.contact_address2_entry),
            ("Phone #:", self.contact_phone_entry),
            ("Email/Fax:", self.contact_emailfax_entry)
        ]:
            label = QLabel(label_text)
            label.setFont(label_font)
            widget.setFont(font)
            contacts_layout.addRow(label, widget)

    def load_client_data(self, item):
        # Extract client_id from the clicked item
        client_id = int(item.text().split(':')[0])  # Assumes format "client_id: client_name: client_address1"

        # Fetch client data from database
        query = "SELECT client_id, client_name, client_address1, client_address2, client_phone, client_emailfax FROM clients WHERE client_id = ?"
        client_data = self.db_manager.fetch_data('Clients.db', query, (client_id,))

        if client_data:
            # Assuming client_data[0] contains the client data tuple
            self.clear_fields()
            client = client_data[0]
            self.client_id_entry.setText(str(client[0]))
            self.client_name_entry.setText(client[1])
            self.client_address1_entry.setText(client[2])
            self.client_address2_entry.setText(client[3])
            self.client_phone_entry.setText(client[4])
            self.client_emailfax_entry.setText(client[5])

    def setupButtons(self, layout):
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        font = QFont("Arial", 12)

        self.submit_button = QPushButton("Submit")
        self.load_button = QPushButton("Load Customer")
        self.delete_button = QPushButton("Delete Customer")
        self.clear_button = QPushButton("Clear Fields")

        self.submit_button.setFont(font)
        self.load_button.setFont(font)
        self.delete_button.setFont(font)
        self.clear_button.setFont(font)

        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.clear_button)

        self.submit_button.clicked.connect(self.amend_client)
        self.clear_button.clicked.connect(self.clear_fields)

    def setupClientList(self, layout):
        # Create a horizontal layout to hold the two list boxes
        hbox = QHBoxLayout()

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search clients...")
        self.search_bar.textChanged.connect(self.search_clients)
        layout.addWidget(self.search_bar)

        # client list
        self.client_list = QListWidget()
        self.client_list.setAlternatingRowColors(True)
        self.client_list.itemDoubleClicked.connect(self.load_client_data)
        hbox.addWidget(self.client_list)

        # contact list
        self.contact_list = QListWidget()
        self.contact_list.setAlternatingRowColors(True)
        hbox.addWidget(self.contact_list)

        layout.addLayout(hbox)

    def search_clients(self, text):
        if not text.strip():
            # If the search bar is empty, list all clients
            query = """
                SELECT client_id, client_name, client_address1, client_address2 
                FROM clients 
                ORDER BY client_name
            """
            parameters = ()
        else:
            # Perform a fuzzy search on client_name, client_address1, and client_address2
            query = """
                SELECT client_id, client_name, client_address1, client_address2 
                FROM clients 
                WHERE client_name LIKE ? OR client_address1 LIKE ? OR client_address2 LIKE ?
                ORDER BY client_name
            """
            search_text = f"%{text}%"
            parameters = (search_text, search_text, search_text)

        results = self.db_manager.fetch_data('Clients.db', query, parameters)

        # Update the client list with the results
        self.client_list.clear()
        for client in results:
            self.client_list.addItem(f"{client[0]}: {client[1]}: {client[2]}: {client[3]}")

    def clear_fields(self):
        """Clears all input fields in the window."""
        self.client_id_entry.clear()
        self.client_name_entry.clear()
        self.client_address1_entry.clear()
        self.client_address2_entry.clear()
        self.client_phone_entry.clear()
        self.client_emailfax_entry.clear()

        # Clearing contact fields if they exist
        self.contact_name_entry.clear()
        self.contact_address1_entry.clear()
        self.contact_address2_entry.clear()
        self.contact_phone_entry.clear()
        self.contact_emailfax_entry.clear()

    def amend_client(self):
        client_id_text = self.client_id_entry.text()
        client_data = {
            'client_name': self.client_name_entry.text(),
            'client_address1': self.client_address1_entry.text(),
            'client_address2': self.client_address2_entry.text(),
            'client_phone': self.client_phone_entry.text(),
            'client_emailfax': self.client_emailfax_entry.text()
        }

        if client_id_text:
            try:
                client_id = int(client_id_text)
                client_data['client_id'] = client_id  # Add this line
            except ValueError:
                QMessageBox.warning(self, "Warning", "Invalid Client ID.")
                return

            # Check if client_id exists in the database
            query = "SELECT * FROM clients WHERE client_id = ?"
            existing_client = self.db_manager.fetch_data('Clients.db', query, (client_id,))
            if existing_client:
                # Update existing client
                self.db_manager.write_data('Clients.db', 'clients', 'client_id', client_data)
            else:
                QMessageBox.information(self, "Information", "Client ID not found.")
        else:
            # Generate a new client ID and add as a new entry
            new_id = self.generate_unique_client_id()
            client_data['client_id'] = new_id  # Add this line
            self.db_manager.add_new_entry('Clients.db', 'clients', client_data)
            self.client_id_entry.setText(str(new_id))

        self.view_clients()

    def generate_unique_client_id(self):
        while True:
            new_id = random.randint(100000, 999999)
            query = "SELECT * FROM clients WHERE client_id = ?"
            if not self.db_manager.fetch_data('Clients.db', query, (new_id,)):
                return new_id