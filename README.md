# Dövme Reklam Seti: Bahçeşehir

Bahçeşehir'deki dövme stüdyosu için **uçtan uca reklam sistemi**: pazar araştırması, strateji, hazır Meta ve Google kampanyaları, reklam metinleri, WhatsApp mesaj şablonları, ölçüm araçları, landing sayfası ve Claude skill'leri.

```
Reklam (Meta + Google) → WhatsApp'ta [KOD]'lu mesaj → Kapora → Randevu → Yorum + iyileşmiş foto → yeni reklam
```

## 🚀 Hızlı başlangıç

1. **`config/studio.yaml` dosyasını doldur.** `DOLDUR` yazan her yeri değiştir: stüdyo adı, sanatçı, telefon, Instagram, fiyatlar, bütçe, stiller.
2. Kontrol et:
   ```bash
   pip install -r tools/requirements.txt
   python3 tools/kontrol.py          # hata/uyarı listesi
   python3 tools/butce.py            # aylık plan + beklenen sonuç
   python3 tools/linkler.py          # her reklam için takip linkleri
   python3 tools/google_disa_aktar.py
   ```
3. Okuma sırası: **`docs/02-strateji.md`** → `03-meta-kurulum.md` → `04-google-kurulum.md` → `07-mesaj-scriptleri.md`
4. Kreatifleri çek (`docs/05-kreatif-rehberi.md`), reklamları aç, her müşteriyi `takip/musteri-takip.csv` dosyasına yaz.
5. Her pazartesi: `python3 tools/rapor.py`, ya da Claude'a **"haftalık raporu çıkar"** de.

## 📁 Klasörler

| Yol | İçerik |
|---|---|
| `config/studio.yaml` | **Tek ayar dosyası**: stüdyo, fiyat, bütçe, hedefleme, varsayımlar |
| `docs/01-pazar-arastirmasi.md` | Rakipler (Cleopatra Ink, SOIL, Mia), fiyatlar, reklam maliyetleri, mevzuat |
| `docs/02-strateji.md` | Konumlanma, personalar, huni, bütçe seviyeleri, KPI, 30/90 günlük plan |
| `docs/03-meta-kurulum.md` | Instagram ve Facebook reklam kurulumu adım adım |
| `docs/04-google-kurulum.md` | Google İşletme Profili + Google Ads arama kampanyası |
| `docs/05-kreatif-rehberi.md` | Reels kuralları, kanca bankası, çekim listesi |
| `docs/06-icerik-takvimi.md` | Haftalık ritim + Kasım 2026 – Ekim 2027 kampanya takvimi |
| `docs/07-mesaj-scriptleri.md` | WhatsApp şablonları: fiyat, itiraz, kapora, yorum, takip |
| `docs/08-olcum-ve-optimizasyon.md` | Hangi reklam randevu getiriyor + karar kuralları |
| `docs/09-acik-kaynak-araclar.md` | GitHub'dan seçilmiş araçlar (MCP, SDK, Postiz, n8n, Umami, Chatwoot…) |
| `docs/10-mevzuat-ve-kurallar.md` | 18 yaş, Meta politikası, reklam hukuku, KVKK, İYS, vergi |
| `ads/meta/kampanyalar.yaml` | K1 Keşif · K2 WhatsApp Mesaj · K3 Yeniden Hedefleme: 12 reklam |
| `ads/google/` | Arama kampanyası: 4 reklam grubu, anahtar kelimeler, negatifler |
| `tools/` | Python araçları (aşağıda) |
| `takip/` | Müşteri ve harcama takip tabloları (`ornek/` klasöründe örnek veri) |
| `landing/index.html` | Mobil uyumlu, WhatsApp butonlu tek sayfalık site (reklam kodunu taşır) |
| `cikti/` | Araçların ürettiği dosyalar (Google Ads Editor CSV'leri, linkler) |
| `kurulum/` | Claude'u reklam hesaplarına bağlama (MCP) + n8n/Umami docker |
| `.claude/skills/` | **Claude skill'leri** (aşağıda) |

## 🧠 Claude skill'leri (Meta + Google)
Bu repo Claude Code ile açıldığında otomatik yüklenir. Türkçe konuşman yeterli:

| Skill | Ne zaman | Örnek |
|---|---|---|
| `reklam-yoneticisi` | Genel sorular, yönlendirme | "Bu ay ne yapmalıyız?" |
| `meta-reklam` | Instagram/Facebook kampanya kurulum, bütçe, teşhis, ret | "K2 bütçesini artıralım mı?" |
| `google-reklam` | Google Ads, anahtar kelime, negatif, İşletme Profili, yorumlar | "Arama terimlerini temizle" |
| `reklam-metni` | Yeni kanca, metin, başlık (kurallara uygun) | "Kapatma için 3 yeni reklam yaz" |
| `haftalik-rapor` | Performans raporu + aksiyonlar | "Reklamlar nasıl gidiyor?" |
| `icerik-takvimi` | Reels senaryoları, aylık plan | "Aralık için 12 Reels fikri" |
| `musteri-mesaji` | WhatsApp/DM cevabı, itiraz | "Müşteri 'pahalı' dedi, ne yazayım?" |
| `rakip-analizi` | Rakiplerin reklamları ve yorumları | "SOIL şu an ne reklam veriyor?" |

**Reklam hesabını Claude'a bağlarsan** (Meta/Google MCP, bkz. `kurulum/README.md`), skill'ler veriyi doğrudan hesaptan çeker, kampanyaları senin onayınla kurar ve günceller.

## 🛠 Araçlar

| Komut | Ne yapar |
|---|---|
| `python3 tools/kontrol.py` | Tüm metinleri denetler: karakter sınırları, "en iyi/garanti/acısız" gibi riskli ifadeler, 18+ kuralı, bütçe toplamı |
| `python3 tools/butce.py --karsilastir` | 7.500 / 15.000 / 30.000 TL planları ve beklenen randevu sayısı |
| `python3 tools/linkler.py` | UTM'li web linkleri + **kodlu WhatsApp linkleri** → hangi reklam randevu getirdi |
| `python3 tools/google_disa_aktar.py` | Google Ads Editor'e yüklenecek CSV'ler |
| `python3 tools/rapor.py --ornek` | Haftalık rapor + "ne yapmalı" önerileri |
| `python3 tools/meta_kur.py` | Meta kampanyalarını API ile PAUSED kurar (resmi Meta SDK) |

## ⚠️ Yayına almadan önce senden gerekenler
- Gerçek **fiyatların** ve **kapora** tutarın
- **"Ücretsiz rötuş"** ve **"ücretsiz tasarım görüşmesi"** vaatleri reklamlarda geçiyor. Gerçekten sunmuyorsan çıkar.
- 8 adet en iyi iş fotoğrafın + 2 süreç videosu
- Meta İşletme hesabı + WhatsApp Business numarası
- Vergi ve KDV için muhasebeci görüşü (bkz. `docs/10`)
