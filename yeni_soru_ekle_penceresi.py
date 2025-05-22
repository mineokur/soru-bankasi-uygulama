from PyQt6.QtWidgets import QWidget, QLabel, QTextEdit, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QFileDialog, QMessageBox
import pandas as pd

class YeniSoruEklePenceresi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yeni Soru Ekle")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QHBoxLayout()

        # Sol Taraf (Soru ve Cevap Girişleri)
        self.sol_layout = QVBoxLayout()

        self.soru_etiketi = QLabel("Soru:")
        self.soru_alani = QTextEdit()
        self.sol_layout.addWidget(self.soru_etiketi)
        self.sol_layout.addWidget(self.soru_alani)

        self.cevap_etiketleri = [QLabel(f"Cevap {i+1}:") for i in range(5)]
        self.cevap_alanlari = [QLineEdit() for _ in range(5)]
        self.dogru_cevap_etiketi = QLabel("Doğru Cevap:")
        self.dogru_cevap_secimi = QComboBox()
        self.dogru_cevap_secimi.addItems(['A', 'B', 'C', 'D', 'E'])

        for i in range(5):
            self.sol_layout.addWidget(self.cevap_etiketleri[i])
            self.sol_layout.addWidget(self.cevap_alanlari[i])
        self.sol_layout.addWidget(self.dogru_cevap_etiketi)
        self.sol_layout.addWidget(self.dogru_cevap_secimi)

        self.ekle_btn = QPushButton("Soru Bankasına Ekle")
        self.ekle_btn.clicked.connect(self.soru_ekle)
        self.sol_layout.addWidget(self.ekle_btn)

        self.layout.addLayout(self.sol_layout)

        # Sağ Taraf (Mevcut Sorular ve Excel Kaydetme)
        self.sag_layout = QVBoxLayout()

        self.mevcut_sorular_etiketi = QLabel("Mevcut Sorular:")
        self.mevcut_sorular_listesi = QListWidget()
        self.sag_layout.addWidget(self.mevcut_sorular_etiketi)
        self.sag_layout.addWidget(self.mevcut_sorular_listesi)

        self.excel_kaydet_btn = QPushButton("Soru Bankasını Excel Olarak Kaydet")
        self.excel_kaydet_btn.clicked.connect(self.excel_kaydet)
        self.sag_layout.addWidget(self.excel_kaydet_btn)

        self.layout.addLayout(self.sag_layout)

        self.setLayout(self.layout)

        self.soru_bankasi = self.excel_yukle()
        self.sorulari_listele()

    def excel_yukle(self):
        try:
            df = pd.read_excel("soru_bankasi.xlsx")
            return df.to_dict('records')
        except FileNotFoundError:
            return []

    def excel_kaydet(self):
        if not self.soru_bankasi:
            QMessageBox.warning(self, "Uyarı", "Kaydedilecek soru bulunmamaktadır.")
            return

        try:
            df = pd.DataFrame(self.soru_bankasi)
            df.to_excel("soru_bankasi.xlsx", index=False)
            QMessageBox.information(self, "Başarılı", "Soru bankası Excel'e kaydedildi.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Excel'e kaydetme sırasında bir hata oluştu: {e}")

    def soru_ekle(self):
        soru_metni = self.soru_alani.toPlainText()
        cevaplar = [alan.text() for alan in self.cevap_alanlari]
        dogru_cevap_index = self.dogru_cevap_secimi.currentIndex()
        dogru_cevap = chr(ord('A') + dogru_cevap_index)

        if not soru_metni or not all(cevaplar):
            QMessageBox.warning(self, "Uyarı", "Lütfen soruyu ve tüm cevap seçeneklerini doldurun.")
            return

        yeni_soru = {
            "Soru": soru_metni,
            "A Şıkkı": cevaplar[0],
            "B Şıkkı": cevaplar[1],
            "C Şıkkı": cevaplar[2],
            "D Şıkkı": cevaplar[3],
            "E Şıkkı": cevaplar[4],
            "Cevap": dogru_cevap
        }

        self.soru_bankasi.append(yeni_soru)
        self.sorulari_listele()

        # Alanları temizle
        self.soru_alani.clear()
        for alan in self.cevap_alanlari:
            alan.clear()
        self.dogru_cevap_secimi.setCurrentIndex(0)

    def sorulari_listele(self):
        self.mevcut_sorular_listesi.clear()
        for soru in self.soru_bankasi:
            item_text = f"{soru['Soru'][:50]}... (Cevap: {soru['Cevap']})" # İlk 50 karakteri göster
            item = QListWidgetItem(item_text)
            self.mevcut_sorular_listesi.addItem(item)