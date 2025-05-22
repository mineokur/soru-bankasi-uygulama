import sys
from PyQt6.QtWidgets import QApplication
from ana_pencere import AnaPencere

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ana_pencere = AnaPencere()
    ana_pencere.show()  # Bu satırı ekleyin
    sys.exit(app.exec())