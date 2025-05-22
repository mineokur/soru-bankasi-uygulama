from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton, QFileDialog, QMessageBox
import pandas as pd
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl
import os

class SoruSecPenceresi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Soru Seç")
        self.setGeometry(100, 100, 600, 500)

        self.layout = QVBoxLayout()

        self.sorular_listesi_etiketi = QLabel("Mevcut Sorular:")
        self.sorular_listesi = QListWidget()
        self.sorular_listesi.itemClicked.connect(self.soru_detaylarini_goster)
        self.layout.addWidget(self.sorular_listesi_etiketi)
        self.layout.addWidget(self.sorular_listesi)

        self.soru_detay_etiketi = QLabel("Soru Detayları:")
        self.soru_detay_alani = QLabel()
        self.layout.addWidget(self.soru_detay_etiketi)
        self.layout.addWidget(self.soru_detay_alani)

        self.dosya_sec_dugmesi = QPushButton("Yazdırılacak Soru Bankası Dosyasını Seç")
        self.dosya_sec_dugmesi.clicked.connect(self.dosya_sec)
        self.layout.addWidget(self.dosya_sec_dugmesi)

        self.secilen_dosya_etiketi = QLabel("Seçilen Dosya:")
        self.secilen_dosya_yolu = QLabel("Henüz dosya seçilmedi.")
        self.layout.addWidget(self.secilen_dosya_etiketi)
        self.layout.addWidget(self.secilen_dosya_yolu)

        self.yazdir_dugmesi = QPushButton("Yazdır")
        self.yazdir_dugmesi.clicked.connect(self.yazdir)
        self.layout.addWidget(self.yazdir_dugmesi)

        self.setLayout(self.layout)

        self.soru_bankasi = self.excel_yukle()
        self.sorulari_listele()
        self.secilen_dosya = None

    def excel_yukle(self):
        try:
            df = pd.read_excel("soru_bankasi.xlsx")
            return df.to_dict('records')
        except FileNotFoundError:
            return []

    def sorulari_listele(self):
        self.sorular_listesi.clear()
        for soru in self.soru_bankasi:
            item_text = soru['Soru'][:50] + "..."
            item = QListWidgetItem(item_text)
            item.setData(1, soru) # Tüm soru detaylarını sakla
            self.sorular_listesi.addItem(item)

    def soru_detaylarini_goster(self, item):
        soru = item.data(1)
        detay_metni = f"**Soru:** {soru['Soru']}\n\n"
        detay_metni += f"A) {soru['A Şıkkı']}\n"
        detay_metni += f"B) {soru['B Şıkkı']}\n"
        detay_metni += f"C) {soru['C Şıkkı']}\n"
        detay_metni += f"D) {soru['D Şıkkı']}\n"
        detay_metni += f"E) {soru['E Şıkkı']}\n\n"
        detay_metni += f"**Doğru Cevap:** {soru['Cevap']}"
        self.soru_detay_alani.setText(detay_metni)

    def dosya_sec(self):
        dosya_adi, _ = QFileDialog.getOpenFileName(self, "Yazdırılacak Dosyayı Seçin", "", "Tüm Dosyalar (*.*);;PDF Dosyaları (*.pdf);;Word Dosyaları (*.docx)")
        if dosya_adi:
            self.secilen_dosya = dosya_adi
            self.secilen_dosya_yolu.setText(dosya_adi)

    def yazdir(self):
        if self.secilen_dosya:
            if os.path.exists(self.secilen_dosya):
                QDesktopServices.openUrl(QUrl.fromLocalFile(self.secilen_dosya))
                QMessageBox.information(self, "Başarılı", f"{self.secilen_dosya} dosyası yazdırılıyor.")
            else:
                QMessageBox.critical(self, "Hata", "Seçilen dosya bulunamadı.")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen öncelikle yazdırılacak bir dosya seçin.")