from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from yeni_soru_ekle_penceresi import YeniSoruEklePenceresi
from soru_sec_penceresi import SoruSecPenceresi

class AnaPencere(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Soru Bankası Uygulaması")
        self.setGeometry(100, 100, 300, 200)  # Başlangıç boyutları

        self.layout = QVBoxLayout()

        self.baslik = QLabel("Yapmak istediğiniz işlemi seçin:")
        self.layout.addWidget(self.baslik)

        self.yeni_soru_ekle_btn = QPushButton("Yeni Soru Ekle")
        self.yeni_soru_ekle_btn.clicked.connect(self.yeni_soru_ekle_sayfasini_ac)
        self.layout.addWidget(self.yeni_soru_ekle_btn)

        self.soru_sec_btn = QPushButton("Soru Seç")
        self.soru_sec_btn.clicked.connect(self.soru_sec_sayfasini_ac)
        self.layout.addWidget(self.soru_sec_btn)

        self.setLayout(self.layout)

        self.yeni_soru_penceresi = None
        self.soru_sec_penceresi = None

    def yeni_soru_ekle_sayfasini_ac(self):
        self.yeni_soru_penceresi = YeniSoruEklePenceresi()
        self.yeni_soru_penceresi.show()

    def soru_sec_sayfasini_ac(self):
        self.soru_sec_penceresi = SoruSecPenceresi()
        self.soru_sec_penceresi.show()