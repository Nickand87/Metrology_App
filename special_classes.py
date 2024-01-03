from PyQt5.QtWidgets import QLineEdit, QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, QPoint


class EnterLineEdit(QLineEdit):

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.focusNextPrevChild(True)
        else:
            super().keyPressEvent(event)


class CustomTitleBar(QWidget):

    def __init__(self, parent=None, title_bar_height=30, button_width=30):
        super().__init__(parent)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.title_label = QLabel("Metrology Stuff")
        self.layout.addWidget(self.title_label)
        self.layout.addStretch()

        self.close_button = QPushButton("X")
        self.minimize_button = QPushButton("-")
        self.maximize_button = QPushButton("[]")

        for btn in [self.close_button, self.minimize_button, self.maximize_button]:
            btn.setFixedSize(button_width, title_bar_height)

        self.layout.addWidget(self.minimize_button)
        self.layout.addWidget(self.maximize_button)
        self.layout.addWidget(self.close_button)

        self.setFixedHeight(title_bar_height)

        self.close_button.clicked.connect(parent.close)
        self.minimize_button.clicked.connect(parent.showMinimized)
        self.maximize_button.clicked.connect(self.toggleMaximizeRestore)

        self.is_dragging = False
        self.drag_start_position = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = True
            self.drag_start_position = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.is_dragging:
            # Calculate the new window position
            delta = event.globalPos() - self.drag_start_position
            self.drag_start_position = event.globalPos()
            self.parent().move(self.parent().pos() + delta)

    def mouseReleaseEvent(self, event):
        self.is_dragging = False

    def toggleMaximizeRestore(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
            self.maximize_button.setText("[]")
        else:
            self.parent().showMaximized()
            self.maximize_button.setText("_")