import qdarkstyle


def dark_style():
    # Load the default dark stylesheet from qdarkstyle
    stylesheet = qdarkstyle.load_stylesheet()

    # Add custom rules for QListWidget
    custom_rules = """
       QListWidget {
           alternate-background-color: #505050;
       }
       QTableWidget {
           background-color: #60798B;
       }
       QTableWidget::item {
           background-color: #9DA9B5; 
       }
       QTableWidget::item:alternate {
           background-color: #7D8B9C;
       }
       QTableWidget::item:selected {
           background-color: #506070;
       }
       QTableWidget QHeaderView::section {
           background-color: #60798B;
       }
       QTableWidget QTableCornerButton::section {
           background-color: #60798B;
       }
       """

    # Combine the default stylesheet with the custom rules
    return stylesheet + custom_rules


def light_style():
    # Define or load the light style here
    return ""
