from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QFormLayout, QListWidgetItem, QFrame, QMessageBox
from PyQt5.QtGui import QFont, QIntValidator, QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp
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
        self.view_clients()

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

        self.client_name_entry = QLineEdit()
        self.client_address1_entry = QLineEdit()
        self.client_address2_entry = QLineEdit()
        self.client_phone_entry = QLineEdit()
        self.client_emailfax_entry = QLineEdit()

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

        self.clear_button.clicked.connect(self.clear_fields)

    def setupClientList(self, layout):
        self.client_list = QListWidget()
        self.client_list.setAlternatingRowColors(True)
        self.client_list.itemDoubleClicked.connect(self.load_client_data)
        layout.addWidget(self.client_list)

    def view_clients(self):
        query = "SELECT client_id, client_name, client_address1 FROM clients"
        client_id = 2
        all_clients = self.db_manager.fetch_data('Clients.db', query)

        self.client_list.clear()
        for client in all_clients:
            self.client_list.addItem(f"{client[0]}: {client[1]}: {client[2]}")

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