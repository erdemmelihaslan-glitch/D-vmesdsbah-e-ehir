# Erdem Melih Tattoo Studio: Reklam Planı v3 (kurul tur 2 sonrası)

> Durum: **YAYINA ALINMADI** · Tur 2 puanları: Meta 8 · Kreatif 8 · Politika 8 · Panel 8 · Finans 8 (tur 1: hepsi 6)
> Bu belge `plan-v2.md`'nin üzerine yazılan değişikliklerdir. v2'nin geri kalanı geçerlidir. Tur 2 raporları: `kurul/tur2/`

## 1. Tur 2 karar tablosu
K = kabul · D = değiştirilerek kabul · S = sahibine bağlı, **yayın kapısına** eklendi

### Meta Ads Medya Uzmanı
| # | Talep | Karar |
|---|---|---|
| 1 | Yenileme takvimi öğrenmeyi sıfırlıyor → tek 7. gün düzenlemesi, sonra ≥ 7 gün ara | **K.** §2 |
| 2 | Video %50 izleyenler kitlesi kurulumda oluşturulsun, ilk günden öneri olarak eklensin | **K.** Kurulum kontrol listesi §4 |
| 3 | 450 TL onaysız olamaz; her artış sahip onaylı; istisna yazılı kabule | **K.** `kpi.max_gunluk_tl_sahip_onayli`; istisna formülü §3 |
| 4 | Yayından önce her reklamdan telefonla test mesajı | **K.** Yayın kapısı |
| itiraz | "Frekans > 3" yerine yeni kişi oranı ve tekrar yazan oranı | **K.** Takip CSV'sine `tekrar` sütunu eklendi. Rapor %15'i aşarsa uyarıyor. Ads Manager'da "yeni mesajlaşma kişileri" sütunu (varsa) haftalık izlenir. |

### Kreatif Direktör
| # | Talep | Karar |
|---|---|---|
| 1 | 9:16'da imza ve etiket dövmeyi kapatıyor | **K.** İmza kaldırıldı; teklif etiketi başlığın hemen altında (y ≈ 392). 480–1248 arası sadece dövme. `kurul/gorseller/2-…` |
| 2 | R1: 0–0,6 sn 1,8x sabit, 0,6–1,2 sn geri çekilme, "Bu bir dövme." 1,2–2,4 sn | **K.** `kurul/gorseller/4-video-R1-…-0.3sn.jpg` (zaman damgalı) |
| 3 | 100 BPM vuruş ızgarası; kesmeler 2,4 / 3,6 / 4,8 sn; kapanış 6,0 sn'de, 1,8 sn; ofset | **K.** Toplam 7,8 sn. `bpm` ayarı + `--muzik-ofset` |
| 4 | V1 kurgu şartnamesi | **K.** §5 |
| itiraz | R2/F4 renkli: R3 yoksa R2 girmesin, %40 / %30 frenleri | **K.** `kampanyalar.yaml > R2, F4 > kosul` |

### Politika ve Hukuk Denetçisi
| # | Talep | Karar |
|---|---|---|
| 1 | "Ücretsiz" ile "çizim" ayrılsın | **K.** C1 ve B1V'de "netleştirelim/netleştiririz". Carousel kapanışında "netleştirelim". Tanım: `reklam.tasarim_gorusmesi_tanim`. Karşılama mesajında "ücretsiz ve bağlayıcı değil", /kapora'da "çizim kaporayla başlar" |
| 2 | /fiyat düzeltilsin, kontrol.py şablonları tarasın | **K.** "sterilize", şartsız rötuş çıktı. kontrol.py docs/07 alıntı satırlarını tarıyor (ilk taramada kendi /portre notumdaki "garanti" kelimesini de yakaladı, düzeltildi) |
| 3 | Her kreatif için onay kontrolü (R2/F1/F4/V1 dahil) | **K.** Her reklamda `kreatif_kodlari` var. `kontrol.py --yayin` (gün 1) ve `--yayin 2` (gün 7): onaysız kreatif **HATA**. Normal modda uyarı |
| 4 | kvkk.html yer tutucuları; reklam kodu için meşru menfaat satırı | **K/S.** Satır eklendi. [2] yıl ve [E-posta] yayın kapısında |
| 5 | Onam formunda "isteğe bağlı" ibaresi | **K.** A ve B bölümlerinde |
| 6 | Kapora iade ve erteleme koşulu yazılmadan kapora alınmasın | **S.** /kapora şablonunda yer tutucu; yayın kapısında |

### Hedef Müşteri Paneli
| # | Talep | Karar |
|---|---|---|
| 1 | Profilde "İyileşmiş" öne çıkanı (≥ 3 iş) yayın kapısına | **S.** Yayın kapısında; "Yorumlar" öne çıkanı da isimsiz gerçek mesajlarla |
| 2 | /portre hazır cevabı | **K.** docs/07 (dürüst, kesin benzerlik sözü yok; gizlilik notu) |
| 3 | Fiyat çelişkisi | **K.** Reklam, karşılama ve /fiyat aynı şeyi söylüyor: "ilk cevapta yaklaşık aralık + seans sayısı; net fiyat tasarım netleşince." Reklamda rakam yok |
| 4 | Seans sırasında mesajlara kim bakıyor (yazılı) | **S.** Yayın kapısında |
| 5 | /fiyat'taki "steril" ve rötuş ifadeleri | **K.** (Politika 2 ile aynı) |

### Finans ve Büyüme Stratejisti
| # | Talep | Karar |
|---|---|---|
| 1 | 340 TL yerine formül: 45–50 TL ve ciddi ≥ %30 → 7,2 × sohbet başı, tavan 360 TL | **K.** `kpi.gun7_ogrenme_istisnasi`; rapor koşul sağlanınca öneriyor |
| 2 | 450 TL "sahip onaylı"; Faz 2 tavanı 14.400 TL/ay yazılı kabule | **K** |
| 3 | Faz 2 en erken 14. gün | **K.** `kpi.faz2_en_erken_gun` |
| 4 | rapor.py artış önerileri kapıyı atlıyor; kapora 0 iken 6.000 TL uyarısı; 30 dk | **K.** "%20 artır" ve "para basıyor" önerileri kaldırıldı, yerine Faz 2 kontrol listesi (✔/✘) geldi. Kapora yokken > 6.000 TL uyarısı eklendi. Durdurma en erken 30. gün |
| 5 | Tanımlar (kayıp, rezerve, ücret dahil harcama, cevap medyanı) | **K.** config > kpi yorumları ve §3 |

## 2. Yenileme takvimi v3 (öğrenmeyi koruyan)
| Gün | Düzenleme |
|---|---|
| 0 (kurulum) | A1: R1, C1, F3, F5, V1. Kitle önerileri: IG etkileşimi 365 gün + **video %50 izleyenler (boş da olsa şimdi oluşturulur)** |
| 1–6 | **Dokunma.** Sadece 150 TL / 0 sohbet kuralıyla kapatma |
| **7** | **Tek düzenleme:** en kötü 2 reklamı kapat + F1 ekle + (R3 hazırsa) R3 + R2 + F4. R3 yoksa R2 ve F4 girmez. Öğrenme istisnası koşulu sağlanıyorsa bütçe aynı düzenlemede ayarlanır. `kontrol.py --yayin 2` |
| 14+ | Faz 2 kontrol listesi (rapor). Sonraki eklemeler (iyileşmiş yan yana, yorum görseli) en az 7 gün arayla, tek düzenlemede |

## 3. Bütçe kuralları v3
- **Taban:** 313 TL/gün (10.000 TL/ay, %5 ücret dahil)
- **Tek ön onaylı istisna (gün 7):** sohbet başı 45–50 TL **ve** ciddi talep ≥ %30 → günlük = 7,2 × sohbet başı, **en fazla 360 TL** (≈ 11.500 TL/ay)
- **Diğer her artış sahibin açık onayıyla.** Faz 2 (en erken 14. gün, kontrol listesinin tamamı ✔) → 3 günde bir %20, tavan 450 TL/gün (≈ 14.400 TL/ay)
- **Tanımlar:** kayıp = kümülatif reklam çıkışı (ücret dahil) − reklamdan tahsil edilen · rezerve ciro = tahsil edilen + kaporalı işlerin kalanı · `harcama.csv` ücret dahil girilir (Ads Manager × 1,05) · cevap medyanı = haftada 10 sohbetten örnek

## 4. Kurulum kontrol listesi (AdsAgent ile, hepsi PAUSED)
1. Özel kitleler: IG etkileşimi 365 gün · **Video %50 izleyenler 30 gün (R1, V1 videoları)**. Boş olsa da şimdi oluşturulur.
2. A kampanyası → A1 seti (plan-v2 §3) · kesin min. yaş 21 · 18 km · Audience Network kapalı
3. Her reklamda: **Advantage+ kreatif iyileştirmeleri tek tek KAPALI** (ekran görüntüsü `kurul/kurulum/`) · hazır mesaj + 4 hızlı soru, sonlarında kod
4. Her reklamın önizlemesinden **telefonla test mesajı**: kod, karşılama mesajı ve KVKK linki geliyor mu?
5. `python3 tools/kontrol.py --yayin` → hata yok
6. Sahibe son "başlatıyorum" bildirimi → yayın

## 5. V1 konuşma videosu kurgu şartnamesi
- 9:16, 1080×1920, 30 fps, H.264. Kaynak 4K dikey (docs/12)
- **Altyazı:** en fazla 2 satır, 48 px, Inter SemiBold, kemik beyazı (#EDE7DD), gölgeli, **y = 1000–1200**
- **Konuşma sırasında imza yok.** Ekran yazıları docs/12'deki gibi, y = 300 bandında (kanca 84 px)
- B-roll'lar sert kesmeyle, vuruşa otururken. Makine sesi –18 dB
- **Kapanış kartı R1 ile aynı** (1,8 sn). Müzik: Meta Ses Koleksiyonu, konuşmanın altında –20 dB
- Müşteri görünen B-roll'larda o müşterinin onayı `kreatif/onaylar.csv`'ye **V1** koduyla girilir

## 6. YAYIN KAPISI v3 (hepsi ✔ olmadan reklam açılmaz)
- [ ] Kurul oybirliğiyle 10/10
- [ ] `python3 tools/kontrol.py --yayin` → **hata yok** (F02, F03, F05, F06 ve V1 müşteri onayları `kreatif/onaylar.csv`'de)
- [ ] Sahibin özgünlük beyanı (docs/13 D) · F03/F05 gerçek kişi portresi mi?
- [ ] V1 konuşma videosu çekildi ve §5'e göre kurgulandı
- [ ] Meta Ses Koleksiyonu müziği gömüldü (`--muzik`, `--muzik-ofset`)
- [ ] Meta İşletme + IG + FB sayfası + WhatsApp Business bağlı · reklam hesabı TRY / İstanbul · ödeme yöntemi
- [ ] AdsAgent Meta yetkisi → §4 kurulum listesi (Advantage+ kreatif kapalı, ekran görüntüsü)
- [ ] Her reklamdan test mesajı: kod + karşılama + KVKK linki doğrulandı
- [ ] WhatsApp Business: karşılama ve uzakta mesajı, etiketler, hızlı yanıtlar (/fiyat, /portre, /kapora, /bakim, /yorum)
- [ ] **Seans sırasında mesajlara kimin bakacağı yazılı** (kişi ya da mola saatleri)
- [ ] **/kapora iade ve erteleme koşulu yazıldı**
- [ ] KVKK sayfası yayında: saklama süresi ve e-posta dolduruldu
- [ ] Instagram öne çıkanları: **İyileşmiş (≥ 3 iş, gün ışığında, filtresiz)** · Süreç · Stüdyo · Yorumlar (isimsiz gerçek mesajlar)
- [ ] Sahibin yazılı kabulü: 20.000 TL test kaybı tavanı · ilk ay 5.000–8.000 TL net çıkış riski · gün 7 istisnası (≤ 360 TL/gün) · Faz 2 tavanı 14.400 TL/ay (her adım ayrıca onaylı)
