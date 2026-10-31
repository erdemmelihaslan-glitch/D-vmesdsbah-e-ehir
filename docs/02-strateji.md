# 02 · Reklam Stratejisi

## Hedef
**Reklamdan her ay ölçülebilir randevu (kaporalı).** "Beğeni" ya da "takipçi" hedef değildir. Asıl hedef, WhatsApp'a gelen ve kapora veren müşteridir.

## Müşteri tipleri (personalar)

| Persona | Kim | Ne ister | Hangi reklam |
|---|---|---|---|
| **İlk Dövme (Ece, 22)** | Esenyurt/Avcılar, öğrenci veya yeni çalışan | Küçük, anlamlı, uygun fiyatlı; korkuyor | K2-02 Minimal fiyat, K1-03 sanatçıyla tanış |
| **Anlam Arayan (Mert, 30)** | Bahçeşehir, çalışan, ikinci-üçüncü dövme | Özel tasarım, kaliteli sanatçı | K2-01 Portfolyo, K1-01 Süreç |
| **Kapatmacı (Selin, 34)** | Eski dövmesinden memnun değil | Uzman ve yargılamayan biri | K2-03 Kapatma, Google AG3 |
| **Hediye Alan (Can, 28)** | Sevgilisi veya arkadaşı için | Kolay ve şık bir hediye | K2-05 Hediye kartı, K2-06 Çift dövmesi |

## Huni (funnel): üç katman, tek amaç

```
  KEŞİF  (K1 Reels, %20)     → Görmeyen kişiye işini göster, video izleyenler havuzu oluştur
     ↓
  MESAJ  (K2 WhatsApp, %50)  → Hazır kişi doğrudan WhatsApp'tan yazar     ← ANA KAYNAK
     ↓                          + Google Arama (G1, %20): "bahçeşehir dövme" arayan hazır kişi
  HATIRLATMA (K3, %10)       → Görmüş ama yazmamış kişiyi geri çağır
     ↓
  WHATSAPP SÜRECİ            → 5 dk'da cevap, fiyat, kapora, randevu (07-mesaj-scriptleri.md)
     ↓
  YORUM + İYİLEŞMİŞ FOTO     → Google yorumu ve yeni reklam içeriği (döngü)
```

**Neden "Mesaj" kampanyası, neden form değil?** Dövme kararı konuşarak verilir. Müşteri fotoğraf atar, soru sorar. Form ise soğuk bir işlem gibi hissettirir. Türkiye'de WhatsApp en doğal kanal.

**Neden Google Arama?** "Bahçeşehir dövme" yazan kişi zaten karar vermiş durumdadır. Bunlar en sıcak tıklamalardır. Bütçe küçük olsa da kaçırılmamalı.

**Neden TikTok yok?** İlk 90 gün **organik** TikTok var (aynı Reels'ları yükle). Ücretli TikTok, Meta oturduktan sonra ikinci faz olur.

## Bütçe seviyeleri

| Seviye | Aylık | Kime uygun | Beklenti (orta senaryo*) |
|---|---|---|---|
| **Başlangıç** | 7.500 TL | İlk ay, test | ~10 randevu |
| **Büyüme** ⭐ | 15.000 TL | Kreatifler hazırsa önerilen | ~20 randevu |
| **Agresif** | 30.000 TL | Takvim boşsa ve süreç oturduysa | ~40 randevu (azalan getiri) |

\* `python3 tools/butce.py --karsilastir` · Varsayımlar `config/studio.yaml` dosyasında. **Garanti değildir.** İlk 14 günden sonra gerçek verinle güncellenir.

Bütçeye **%5 Meta konum ücreti** ekle. KDV için muhasebecine danış.

## Başarı ölçütleri (KPI)

| Metrik | Hedef (başlangıç) | Nereden |
|---|---|---|
| Mesaj başı maliyet | ≤ 45 TL | Ads Manager → "Başlatılan mesajlaşma sohbetleri" |
| Mesajdan ciddi talebe | ≥ %40 | `takip/musteri-takip.csv` |
| Ciddi talepten kaporaya | ≥ %20 | `takip/musteri-takip.csv` |
| Randevu başı maliyet | ≤ 800 TL | `python3 tools/rapor.py` |
| ROAS | ≥ 5x | `python3 tools/rapor.py` |
| İlk cevap süresi | ≤ 5 dk | WhatsApp Business |
| Aylık yeni Google yorumu | ≥ 8 | İşletme Profili |

## İlk 30 gün: başlangıç planı

### Hafta 0 — Hazırlık (reklam yok)
- [ ] `config/studio.yaml` dosyasını doldur → `python3 tools/kontrol.py`
- [ ] **WhatsApp Business** kur: profil, katalog, karşılama ve uzakta mesajı, etiketler (bkz. 07)
- [ ] **Meta Business Suite:** Instagram ve Facebook sayfası + WhatsApp numarası tek hesapta bağlı olsun
- [ ] **Google İşletme Profili:** tam doldurulmuş, 20+ foto, kategori "Dövme salonu" (bkz. 04)
- [ ] Mevcut müşterilerden **10 Google yorumu** iste. Reklamdan önce sosyal kanıt şart.
- [ ] **Kreatif çekimi:** en az 4 Reels + 1 carousel (bkz. 05). En büyük darboğaz budur.

### Hafta 1 — Yayına al
- [ ] K1 + K2 aç (K3 için henüz kitle yok). Google G1 aç.
- [ ] Her talebi `takip/musteri-takip.csv` dosyasına yaz. **Kaynak kodu** mesajın sonundaki [K2-01] gibi koddur.
- [ ] **İlk 72 saat hiçbir şeye dokunma.** Meta'nın öğrenme süresi var.

### Hafta 2 — İlk karar
- [ ] `python3 tools/rapor.py` → en kötü reklamı kapat, yerine yeni kanca koy
- [ ] Google → "Arama terimleri" raporuna bak, alakasız aramaları negatif listeye ekle
- [ ] Özel kitleleri oluştur (Instagram etkileşimi 60 gün, video %50 izleme 30 gün) → **K3'ü aç**

### Hafta 3–4 — Ölçekle
- [ ] Mesaj başı maliyeti hedefin altında olan setin bütçesini **3 günde bir %20** artır
- [ ] Varsayımları gerçek verilerle güncelle (`studio.yaml` → `varsayimlar`)
- [ ] Ay sonu raporu: `python3 tools/rapor.py --gun 30`

## 90 günlük yol haritası
| Ay | Odak |
|---|---|
| **Kasım 2026** | Kurulum + "Kış dövme sezonu" mesajı · Efsane Cuma'da **indirim yok, hediye kartı bonusu** |
| **Aralık 2026** | Yılbaşı hediye kartı (K2-05) · yıl sonu "en sevdiğim 9 işim" carousel'i |
| **Ocak 2027** | Durgun ayı Flash Günü ile doldur (K2-04) · 25 Ocak'tan itibaren Sevgililer Günü (K2-06) |
| **Şubat 2027** | 14 Şubat çift dövmesi · TikTok ücretli testi (bütçenin %10'u) |
