# sudoku-sat-solver
A Python desktop app that uses Gemini API (OCR) and PySAT (Boolean Satisfiability) to extract and find all solutions for Sudoku puzzles. ✨
# Sudoku SAT Solver & OCR ✨

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-pink)
![PySAT](https://img.shields.io/badge/Solver-PySAT-orange)
![Gemini API](https://img.shields.io/badge/AI-Gemini%20API-brightgreen)

Bu proje, bir Sudoku bulmacasının çözülebilirliğini Önermeler Mantığı kullanarak bir Sağlanabilirlik (SAT) problemine kodlayan ve tüm geçerli çözümleri bulan, görüntü işleme destekli bir masaüstü uygulamasıdır. Karadeniz Teknik Üniversitesi (KTÜ) Yazılım Mühendisliği bölümü akademik projesi olarak geliştirilmiştir.

## 🌟 Özellikler

* **Yapay Zeka Destekli OCR:** Google Gemini 2.5 Flash modeli kullanılarak, yüklenen Sudoku bulmacası görselleri analiz edilir ve 9x9'luk dijital matrislere dönüştürülür.
* **SAT Kodlaması (Boolean Satisfiability):** Sudoku kuralları (satır, sütun, blok kısıtları) Konjonktif Normal Form (CNF) formatına dönüştürülerek mantıksal bir modele oturtulur.
* **Gelişmiş Çözümleme:** `python-sat` kütüphanesi ve endüstri standardı `glucose3` çözücüsü ile bulmacanın tüm olası çözümleri (maksimum 100 çözüme kadar) hesaplanır.
* **Asenkron Mimari:** Threading ve Queue mekanizmaları sayesinde, ağır çözümleme ve API bekleme süreleri boyunca kullanıcı arayüzü (GUI) donmaz ve akıcı bir deneyim sunar.
* **Modern ve Estetik Arayüz:** Çözümler arasında gezinmeyi sağlayan "Çözüm Gezgini", animasyonlu durum bildirimleri ve kişiselleştirilmiş renk paletiyle şık bir kullanıcı deneyimi sağlar.

## ⚙️ Sistem Mimarisi

1. **Girdi:** Kullanıcı bir Sudoku görseli yükler veya manuel olarak rakamları girer.
2. **OCR İşleyici:** Görsel, Base64 formatında Gemini API'ye gönderilir ve JSON formatında 9x9 bir matris olarak geri döner.
3. **SAT Kodlayıcı:** Matris, Sudoku'nun matematiksel kurallarına göre 729 boolean değişkeni üzerinden CNF formülüne dökülür.
4. **SAT Çözücü:** Oluşturulan formül çözülür. Tespit edilen her çözüm için, çözücüye *engelleme maddesi (blocking clause)* eklenerek alternatif çözümler aranmaya devam eder.

## 🚀 Kurulum ve Çalıştırma

### Gereksinimler
Projeyi yerel ortamınızda çalıştırmak için aşağıdaki adımları izleyin:

1. Repoyu bilgisayarınıza klonlayın:
   ```bash
   git clone [https://github.com/KULLANICI_ADIN/sudoku-sat-solver.git](https://github.com/KULLANICI_ADIN/sudoku-sat-solver.git)
   cd sudoku-sat-solver
