# Standard library imports
import random

# PyQt5 imports
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QListWidget, QFormLayout,
                             QFrame, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtGui import QFont, QIntValidator, QRegExpValidator
from PyQt5.QtCore import QRegExp, Qt

# Local application imports
from special_classes import EnterLineEdit


class ClientWindow(QMainWindow):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager

        # Initialize all instance attributes
        self.client_id_entry = None
        self.client_name_entry = None
        self.client_address1_entry = None
        self.client_address2_entry = None
        self.client_phone_entry = None
        self.client_emailfax_entry = None
        self.contact_name_entry = None
        self.contact_address1_entry = None
        self.contact_address2_entry = None
        self.contact_phone_entry = None
        self.contact_emailfax_entry = None
        self.submit_button = None
        self.load_button = None
        self.delete_button = None
        self.clear_button = None
        self.client_table = None
        self.contact_table = None
        self.search_bar = None

        self.client_table = QTableWidget()

        self.initializeUI()
        self.search_clients("")

    def initializeUI(self):
        """Initializes the main UI components of the window."""
        self.setWindowTitle("Client Information")
        self.setGeometry(100, 100, 800, 500)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        self.setupIDFrame(main_layout)
        self.setupInputFields(main_layout)
        self.setupButtons(main_layout)
        self.setupClientLayout(main_layout)

    def setupIDFrame(self, layout):
        """Sets up the ID frame in the UI."""
        id_frame = QFrame()
        id_frame.setFrameShape(QFrame.StyledPanel)
        id_layout = QHBoxLayout(id_frame)
        layout.addWidget(id_frame)

        font = QFont("Arial", 12)
        label_font = QFont("Arial", 10, QFont.Bold)

        self.client_id_entry = QLineEdit()
        self.client_id_entry.setValidator(QIntValidator())
        self.client_id_entry.setFont(font)
        self.client_id_entry.setReadOnly(True)

        id_label = QLabel("ID:")
        id_label.setFont(label_font)

        id_layout.addWidget(id_label)
        id_layout.addWidget(self.client_id_entry)

    def setupInputFields(self, layout):
        """Sets up input fields for client and contact information."""
        input_layout = QHBoxLayout()
        layout.addLayout(input_layout)

        self.setupClientInfo(input_layout)
        self.setupContacts(input_layout)

    def setupClientInfo(self, layout):
        """Sets up client information input fields."""
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
        """Sets up contact information input fields."""
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

    def setupButtons(self, layout):
        """Sets up buttons in the UI."""
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

    def setupClientLayout(self, layout):
        """Sets up the client and contact table UI components."""

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search clients...")
        self.search_bar.textChanged.connect(self.search_clients)
        layout.addWidget(self.search_bar)

        # Layout for tables
        tables_layout = QHBoxLayout()

        # Client table setup
        self.setupClientTable()
        tables_layout.addWidget(self.client_table, 1)  # The second parameter '1' is the stretch factor

        # Contact table setup
        self.setupContactTable()
        tables_layout.addWidget(self.contact_table, 1)  # The second parameter '1' is the stretch factor

        # Adding the tables layout to the main layout
        layout.addLayout(tables_layout)

    def setupClientTable(self):

        # Client table
        self.client_table = QTableWidget()
        self.client_table.setAlternatingRowColors(True)
        self.client_table.setColumnCount(4)
        self.client_table.setHorizontalHeaderLabels(["ID", "Client Name", "Address 1", "Address 2"])

        self.client_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.client_table.setSelectionMode(QTableWidget.SingleSelection)
        self.client_table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.client_table.itemDoubleClicked.connect(self.load_client_data)

        self.client_table.setSortingEnabled(True)
        self.client_table.sortByColumn(1, Qt.AscendingOrder)

        client_header = self.client_table.horizontalHeader()
        client_header.setSectionResizeMode(0, QHeaderView.Interactive)
        client_header.setSectionResizeMode(1, QHeaderView.Stretch)
        client_header.setSectionResizeMode(2, QHeaderView.Stretch)
        client_header.setSectionResizeMode(3, QHeaderView.Stretch)

        self.client_table.setColumnWidth(0, 50)
        self.client_table.setColumnWidth(1, 200)
        self.client_table.setColumnWidth(2, 150)
        self.client_table.setColumnWidth(3, 150)

    def setupContactTable(self):

        # Contact table
        self.contact_table = QTableWidget()
        self.contact_table.setAlternatingRowColors(True)
        self.contact_table.setColumnCount(3)
        self.contact_table.setHorizontalHeaderLabels(["Contact Name", "Contact Type", "Contact Phone Number"])

        self.contact_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.contact_table.setSelectionMode(QTableWidget.SingleSelection)
        self.contact_table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.contact_table.setSortingEnabled(True)
        self.contact_table.sortByColumn(1, Qt.AscendingOrder)

        contact_header = self.contact_table.horizontalHeader()
        contact_header.setSectionResizeMode(0, QHeaderView.Interactive)
        contact_header.setSectionResizeMode(1, QHeaderView.Stretch)
        contact_header.setSectionResizeMode(2, QHeaderView.Stretch)

        self.contact_table.setColumnWidth(0, 100)
        self.contact_table.setColumnWidth(1, 100)
        self.contact_table.setColumnWidth(2, 100)

    def search_clients(self, text):
        """Searches for clients based on the provided text."""
        if not text.strip():
            query = """
                SELECT client_id, client_name, client_address1, client_address2 
                FROM clients 
                ORDER BY client_name
            """
            parameters = ()
        else:
            query = """
                SELECT client_id, client_name, client_address1, client_address2 
                FROM clients 
                WHERE client_name LIKE ? OR client_address1 LIKE ? OR client_address2 LIKE ?
                ORDER BY client_name
            """
            search_text = f"%{text}%"
            parameters = (search_text, search_text, search_text)

        results = self.db_manager.fetch_data('Clients.db', query, parameters)

        self.client_table.setRowCount(len(results))
        for row_number, row_data in enumerate(results):
            for column_number, data in enumerate(row_data):
                cell = QTableWidgetItem(str(data))
                self.client_table.setItem(row_number, column_number, cell)

    def load_client_data(self, item):
        """Loads client data from the database."""
        row = item.row()
        client_id = int(self.client_table.item(row, 0).text())  # Assuming ID is in the first column
        query = """
            SELECT client_id, client_name, client_address1, client_address2, 
                   client_phone, client_emailfax 
            FROM clients 
            WHERE client_id = ?
        """
        client_data = self.db_manager.fetch_data('Clients.db', query, (client_id,))

        if client_data:
            self.clear_fields()
            client = client_data[0]
            self.client_id_entry.setText(str(client[0]))
            self.client_name_entry.setText(client[1])
            self.client_address1_entry.setText(client[2])
            self.client_address2_entry.setText(client[3])
            self.client_phone_entry.setText(client[4])
            self.client_emailfax_entry.setText(client[5])

    def clear_fields(self):
        """Clears all input fields in the window."""
        self.client_id_entry.clear()
        self.client_name_entry.clear()
        self.client_address1_entry.clear()
        self.client_address2_entry.clear()
        self.client_phone_entry.clear()
        self.client_emailfax_entry.clear()
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
                client_data['client_id'] = client_id
            except ValueError:
                QMessageBox.warning(self, "Warning", "Invalid Client ID.")
                return

            query = "SELECT * FROM clients WHERE client_id = ?"
            existing_client = self.db_manager.fetch_data('Clients.db', query, (client_id,))
            if existing_client:
                self.db_manager.write_data('Clients.db', 'clients', 'client_id', client_data)
            else:
                QMessageBox.information(self, "Information", "Client ID not found.")
        else:
            new_id = self.generate_unique_client_id()
            client_data['client_id'] = new_id
            self.db_manager.add_new_entry('Clients.db', 'clients', client_data)
            self.client_id_entry.setText(str(new_id))

        current_search_text = self.search_bar.text()
        self.search_clients(current_search_text)

    def generate_unique_client_id(self):
        while True:
            new_id = random.randint(100000, 999999)
            query = "SELECT * FROM clients WHERE client_id = ?"
            if not self.db_manager.fetch_data('Clients.db', query, (new_id,)):
                return new_id
