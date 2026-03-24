# Future Talent Program-201 Yapay-Zeka-Bitirme-Projesi
# SQL Asistanı: AI Destekli SQL Sorgu ÜretiM Uygulaması
Bu projede, karmaşık SQL sorgularını sql kullanmada temel seviyede bilgi sahibi olan kişiler için  doğal dil kullanarak oluşturmalarına ve öğrenmelerine yardımcı olan yapay zeka destekli bir web uygulaması geliştirdim. Bu uygulama, **Google Gemini 1.5 Flash** altyapısını kullanır.

## Öne Çıkan Özellikler

* **Doğal Dil İşleme:** "Geçen ay en çok satış yapan 5 ürünü getir" gibi cümleleri SQL koduna dönüştürür.
* **Öğrenme Modu:** Üretilen sorguları seviyenize göre (Başlangıç, Orta, İleri) adım adım açıklar.
* **Hazır Senaryolar:** E-Ticaret, İK ve Kütüphane gibi hazır veritabanı şemalarıyla anında deneme yapabilirsiniz.
* **Çoklu Veritabanı Desteği:** Sorguları PostgreSQL, MySQL veya SQLite formatında üretir.
* **Güvenli Tasarım:** API anahtarınız arayüzde görünmez, `.env` dosyasından güvenli bir şekilde okunur.

## 🛠️ Kurulum

1.  **Gereksinimleri yükleyin:**
    ```bash
    pip install streamlit google-generativeai python-dotenv
    ```

2.  **API Anahtarını Hazırlayın:**
    Klasörünüzde `sql.env` isimli bir dosya oluşturun ve içine anahtarınızı yazın:
    ```text
    GEMINI_API_KEY=KENDI_API_ANAHTARINIZ
    ```

3.  **Uygulamayı Çalıştırın:**
    ```bash
    streamlit run sql_app.py
    ```

## 📂 Dosya Yapısı

*   `sql_app.py`: Ana uygulama kodu.
*   `sql.env`: API anahtarının saklandığı gizli dosya (GitHub'a yüklenmez).
*   `sql.gitignore`: Gizli dosyaların Git'e yüklenmesini engelleyen kurallar.


### Bu proje **Future Talent** programı kapsamında geliştirilmiştir. Her türlü öneri ve katkıya açıktır!

---
