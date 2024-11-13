from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from ui.admin_profile import AdminProfileWindow  # Импортируем новое окно

class AdminDashboardWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Панель Администратора')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.profile_button = QPushButton('Профиль', self)
        self.profile_button.clicked.connect(self.open_admin_profile)

        layout.addWidget(self.profile_button)

        self.setLayout(layout)

    def open_admin_profile(self):
        """Открытие профиля администратора"""
        self.admin_profile_window = AdminProfileWindow()
        self.admin_profile_window.show()
        self.close()
