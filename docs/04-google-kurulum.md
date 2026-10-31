# 04 · Google Kurulum: İşletme Profili + Arama Reklamları

## Önce ücretsiz olan: Google İşletme Profili (GBP)
"Dövmeci yakınımda" ve "bahçeşehir dövme" aramalarında **harita sonuçları** reklamlardan önce görünür, üstelik ücretsizdir. Reklama para vermeden önce bu adımı tamamla.

**Kontrol listesi** (business.google.com):
- [ ] Ana kategori: **Dövme salonu**. Ek kategori: Piercing stüdyosu (yapıyorsan)
- [ ] Ad: Gerçek tabela adın. ⚠️ Ada "Bahçeşehir En İyi Dövme" gibi anahtar kelime eklersen Google profili askıya alabilir.
- [ ] Adres, telefon (WhatsApp numarası), çalışma saatleri ve özel gün saatleri
- [ ] Web sitesi: `cikti/linkler.csv` dosyasındaki **ORG-GMB** linki (Google'dan geleni ayırt etmek için)
- [ ] **Hizmetler:** Minimal dövme, Fine line, Yazı dövmesi, Kapatma, Realistik… Her birine kısa açıklama ve "başlangıç fiyatı" yaz.
- [ ] **Fotoğraflar:** 20+ adet. Dış cephe (bulunabilirlik), iç mekan, sanatçı, işler, steril ekipman
- [ ] **Haftada 1 gönderi** (Güncellemeler): yeni bir iş + "WhatsApp'tan yaz"
- [ ] **Soru-Cevap:** Kendin sor ve cevapla ("Fiyatlar ne kadar?", "18 yaş altına yapıyor musunuz?", "Randevusuz geliniyor mu?")
- [ ] **Yorum linki** → `studio.yaml` → `google_yorum_linki`

### Yorum toplama sistemi (en önemli sıralama faktörlerinden biri)
1. Seans bitince: "Memnun kaldıysan yorumun bizim için çok değerli 🙏" + link (bkz. 07 → *Yorum İsteği*)
2. 4 hafta sonra iyileşme kontrolü: "İyileşmiş halinin fotoğrafını atar mısın?" Fotoğraf gelince yorum linkini tekrar gönder.
3. **Her yoruma cevap ver.** Cevapta "Bahçeşehir" ve stil adı geçsin, doğal bir dille.
4. ⚠️ Yorum **satın alma**, indirim karşılığı yorum isteme. Google bunu yasaklıyor, sahte yorum da yasal risk taşıyor.

---

## Google Ads: Arama kampanyası (G1)

Kampanyanın tüm içeriği `ads/google/kampanya.yaml` dosyasında: reklam grupları, anahtar kelimeler, 15 başlık ve 4 açıklama.

### Kurulum (Google Ads Editor ile hızlı yol)
1. `python3 tools/kontrol.py` → hata yok
2. `python3 tools/google_disa_aktar.py` → `cikti/google/` klasöründe 3 CSV oluşur
3. **ads.google.com** → yeni kampanya → **Uzman moduna geç**. ⚠️ "Akıllı kampanya" önerisini reddet.
4. Kampanya ayarları:
   - Hedef: **Potansiyel müşteri** → Tür: **Arama**
   - Ağlar: **Görüntülü Reklam Ağı KAPALI**, **Arama ortakları KAPALI**
   - Konum: stüdyonun çevresinde **12 km yarıçap**
   - Konum seçeneği: **"Varlık: Hedef konumlarınızdaki veya düzenli olarak orada bulunan kişiler"** (ilgi seçeneğini KAPAT, yoksa İzmir'den tıklayan olur)
   - Dil: Türkçe
   - Bütçe: `python3 tools/butce.py` çıktısındaki "G1 günlük" tutarı
   - Teklif: ilk 2 hafta **Tıklamaları en üst düzeye çıkar + TBM sınırı 15 TL**. 15+ dönüşüm sonrası → **Dönüşümleri en üst düzeye çıkar**.
   - Reklam zaman planlaması: çalışma saatlerin (mesaja dönebildiğin saatler)
5. **Google Ads Editor** (ücretsiz masaüstü uygulaması) → hesabı indir → **Hesap → İçe aktar → Dosyadan**:
   `anahtar-kelimeler.csv` → `reklamlar.csv` → `negatifler.csv` → **Yayınla**
6. **Öğeler** (reklam uzantıları): site bağlantıları, açıklama metinleri, yapılandırılmış snippet, **arama öğesi** (telefon), **konum öğesi** (İşletme Profilini bağla). Detaylar `kampanya.yaml` → `ogeler` bölümünde.

### Dönüşüm takibi (yoksa Google kör uçar)
- **Hedefler → Dönüşümler → Yeni:**
  - "Web sitesi → WhatsApp butonu tıklaması" (landing sayfasındaki `wa.me` linkleri)
  - "Reklamlardan gelen telefon aramaları" (arama öğesi, 30 sn+)
  - "Yerel işlemler → Yol tarifi" (İşletme Profili bağlıysa otomatik)
- Landing sayfası (`landing/index.html`) kullanıyorsan Google etiketini (gtag) `<head>` içine ekle. Sayfa WhatsApp tıklamasında `gtag('event','whatsapp_tiklama')` olayını tetikliyor.

### Haftalık bakım (15 dk)
1. **Arama terimleri** raporu → alakasız olanları `ads/google/negatif-kelimeler.txt` dosyasına ekle → yeniden dışa aktar
2. Reklam gücü "Zayıf" ise yeni başlık ekle (kontrol aracı ≤30 karakteri denetler)
3. TBM 15 TL'yi sürekli aşıyorsa: geniş kelimeleri durdur, sadece **[tam eşleme]** bırak

### Google'da yapılmaması gerekenler
- ❌ Performance Max veya Akıllı kampanya: küçük bütçede parayı Görüntülü Reklam Ağı ve YouTube'a dağıtır
- ❌ "Dövme" tek kelime geniş eşleme: dövme anlamları, rüyada dövme, oyunlar gibi alakasız aramalara para gider
- ❌ Başka şehirleri hedeflemek
