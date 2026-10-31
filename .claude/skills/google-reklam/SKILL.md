---
name: google-reklam
description: Google Ads arama kampanyası ve Google İşletme Profili (Haritalar) yönetimi — anahtar kelime, negatif kelime, duyarlı arama reklamı (RSA) başlık/açıklama, Google Ads Editor CSV, arama terimleri temizliği, dönüşüm takibi, yerel SEO, Google yorumları. Kullanıcı "Google reklam", "Google Ads", "anahtar kelime", "aramada çıkmak", "haritada çıkmak", "Google yorum", "işletme profili" dediğinde kullan. Use for Google Ads search campaigns, keywords, RSA copy, negatives and Google Business Profile for the tattoo studio.
---

# Google Reklam + İşletme Profili

## Kaynak dosyalar
- `ads/google/kampanya.yaml`: G1 kampanya ayarları, reklam grupları (AG1 Bölge, AG2 Minimal, AG3 Kapatma, AG4 Piercing), anahtar kelimeler, başlıklar, açıklamalar, öğeler
- `ads/google/negatif-kelimeler.txt`: negatif liste
- `docs/04-google-kurulum.md`: kurulum + İşletme Profili kontrol listesi

## İş akışları

### A) Kampanyayı hazırla / güncelle
1. `ads/google/kampanya.yaml` dosyasını düzenle.
2. `python3 tools/kontrol.py` → başlık **≤30**, açıklama **≤90**, yol **≤15** karakter; tekrar yok; riskli ifade yok.
3. `python3 tools/google_disa_aktar.py` → `cikti/google/*.csv`
4. Kullanıcıya Google Ads Editor yükleme adımlarını ver (docs/04, adım 5).

### B) Yeni başlık/açıklama yazma
- Her reklam grubunda **15 başlık, 4 açıklama** hedefle. Başlıklar birbirinden farklı açılardan yazılsın:
  konum (Bahçeşehir/Başakşehir) · stil · güven (steril, tek kullanımlık iğne) · teklif (ücretsiz tasarım görüşmesi) · fiyat ("X TL'den") · CTA (WhatsApp'tan yaz)
- En az 2 başlıkta anahtar kelime birebir geçsin ("Bahçeşehir Dövme Stüdyosu").
- Türkçe karakter sayımı: `ç ğ ı ö ş ü` birer karakterdir. Emin olmak için kontrol aracını çalıştır.

### C) Haftalık arama terimleri temizliği
1. Google Ads MCP bağlıysa `search_term_view` sorgula (son 7 gün, maliyete göre sırala). Bağlı değilse kullanıcıdan "Arama terimleri" raporunun CSV'sini iste.
2. Alakasız terimleri sınıflandır: malzeme/ürün, geçici dövme, silme/lazer, eğitim/iş, bilgi/eğlence, başka şehir.
3. Önerilen negatifleri listele → onay → `negatif-kelimeler.txt` dosyasına ekle → yeniden dışa aktar.
4. İyi dönüşen yeni terimleri **[tam eşleme]** olarak ilgili reklam grubuna ekle.

### D) Google Ads MCP ile okuma (googleads/google-ads-mcp)
Örnek GAQL sorguları:
```sql
SELECT campaign.name, metrics.cost_micros, metrics.clicks, metrics.conversions
FROM campaign WHERE segments.date DURING LAST_7_DAYS

SELECT search_term_view.search_term, metrics.cost_micros, metrics.clicks, metrics.conversions
FROM search_term_view WHERE segments.date DURING LAST_7_DAYS ORDER BY metrics.cost_micros DESC LIMIT 50
```
`cost_micros / 1.000.000 = TL`. Resmi MCP salt okunurdur; değişiklikleri Editor CSV'si veya arayüz üzerinden yaptır.

### E) İşletme Profili ve yorumlar
- docs/04'teki kontrol listesini kullanıcıyla tek tek geç.
- Yorum cevabı yazarken: teşekkür + stil adı + "Bahçeşehir" doğal geçsin, 2–3 cümle, her cevap farklı olsun. Olumsuz yoruma savunmacı değil, çözüm odaklı cevap ver, detayı özelden konuşmayı öner.
- ❌ Profil adına anahtar kelime ekleme. ❌ Yorum satın alma veya karşılığında indirim verme.

## Sabit ayarlar
Sadece Arama Ağı (Görüntülü Reklam Ağı ve arama ortakları KAPALI) · 12 km yarıçap · konum seçeneği "Varlık" · Performance Max / Akıllı kampanya YOK · tek kelime "dövme" geniş eşleme YOK.
