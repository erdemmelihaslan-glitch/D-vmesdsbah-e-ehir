# Erdem Melih Tattoo Studio: Reklam Planı v2 (kurul tur 1 sonrası)

> Tarih: 31 Ekim 2026 · Durum: **YAYINA ALINMADI** · Tur 1 puanları: Meta 6 · Kreatif 6 · Politika 6 · Müşteri paneli 6 · Finans 6
> Tur 1 raporları: `kurul/tur1/` · v1: `kurul/plan-v1.md` · Kreatif önizlemeleri (v2): `kurul/gorseller/`

## 1. Ne değişti? (özet)
1. **Tek kampanya, tek set:** A1, günde 313 TL. Bu tutar 10.000 TL/ay'a %5 ücret dahil sığıyor. A2 yeniden hedefleme Faz 2'ye ertelendi.
2. **Hedefleme:** Yarıçap 25 km'den **18 km**'ye indi. Tutku ilgileri (Katman 2) silindi; kurulumda Ads Manager'da gerçekten bulunan en fazla 6 dövme ilgisi kalıyor. Kesin minimum yaş 21. Dil kontrolü yok.
3. **Kreatifler v2:**
   - "Doldur" kadrajı uygulandı: dövme genişliğin ~%60'ı, en fazla 1,5x büyütme. Gamma 1,2, zemin parlaklığı 0,30.
   - 9:16'da tüm yazılar **%14–65 bandında**.
   - R1 yeniden kurgulandı ("Önce gözlere bak → Bu bir dövme"; sert kesmeler, 7,1 sn).
   - Teklif ("Ücretsiz tasarım görüşmesi") artık görselin üstünde. Kapanış kartında ince çerçeveli etiket var.
4. **Faz 1'de yayına girecek görseller:** Sadece F02, F03, F05, F06 (R1, C1, F3, F5 reklamları) ve sahibinden gelince V1 konuşma videosu. F01, F04 ve R2 6. gün sonrası ayrı tekli reklam olarak. F07 sadece organik.
5. **Metin:** Güven satırı ilk 125 karakter içinde: "Tek kullanımlık iğne · sterilize ekipman · iyileşme takibi." "Steril ortam" ifadesi kalktı. "Ücretsiz rötuş" süre ve şart belli olana kadar metinde yok (kontrol aracı yakalıyor). "Portre" vaadi F05'ten kaldırıldı.
6. **Kod sistemi:** Hazır mesajın sonunda kısa kod "(R1)". 4 hızlı sorunun her birinin sonunda da kod var.
7. **Tek KPI seti, durdurma merdiveni, kapasite freni, Faz 2 geçiş kriterleri:** `config/studio.yaml > kpi, kapasite`. Rapor aracı artık kapora başı maliyeti, tahsil edilen ve rezerve ciroyu ayrı gösteriyor.
8. **Uyum:** Müşteri onam formu ve kayıt (`docs/13`, `kreatif/onaylar.csv`), KVKK aydınlatma sayfası (`landing/kvkk.html`), WhatsApp karşılama mesajında KVKK linki. Faz 1'de müşteri listesi yüklenmiyor. Advantage+ kreatif iyileştirmelerinin hepsi kapalı.
9. **Konuşma videosu senaryosu** hazır (`docs/12`: tanışma, yarım kalan proje ve portre videoları; B-roll listesi; black & grey süreç videosu).

## 2. Karar tablosu (her zorunlu maddeye cevap)
K = kabul · D = değiştirilerek kabul · R = gerekçeli red · S = sahibine bağlı, **yayın kapısına** eklendi

### Meta Ads Medya Uzmanı
| # | Talep | Karar |
|---|---|---|
| 1 | A2 kaldırılsın, bütçenin tamamı A1'e; IG etkileşimi kitle önerisi | **K.** A1 313 TL/gün. Öneriler: IG etkileşimi 365 gün, video %50 izleme 30 gün |
| 2 | WhatsApp'a yazanları müşteri listesiyle hariç tut | **R (Faz 1).** Politika üyesi KVKK ve yurt dışı aktarım riski nedeniyle liste yüklemeyi yasakladı; hukuki risk verimlilikten ağır basar. Açık kalan risk: WhatsApp'a yazan biri reklamı tekrar görebilir. Önlem: frekans > 3 izlenir. Faz 2'de açık rıza toplanırsa yeniden değerlendirilir. |
| 3 | 18 km + müşteriye semt sorulsun | **K.** Karşılama mesajında 4. soru "Hangi semttesin?" |
| 4 | Katman 2 silinsin, en fazla 6 ilgi | **K** |
| 5 | Reels güvenli alanı %14–65 | **K.** `kurul/gorseller/2-hikaye-9x16-guvenli-bolge.jpg` (kırmızı çizgiler) |
| 6 | Müzik dosyaya gömülsün | **K.** `--muzik` seçeneği eklendi. Meta Ses Koleksiyonu'ndan parça → **yayın kapısı** |
| 7 | Erdem'in konuşma Reels'i | **S.** Senaryo hazır (docs/12 Video A) → **yayın kapısı** |
| 8 | Set düzeyinde karar, 150 TL / 0 sohbet kuralı, tek eşik, "ciddi talep" tanımı | **K.** kpi.hedef_mesaj_basi_tl = 45 · reklam_kapat_harcama_tl = 150 · tanım: §5 |
| 9 | Kod hızlı sorulara da | **K** |
| 10 | config plana uydurulsun | **K.** Dağılım A1 = 1,00 · yas_max 65 · diller [] |
| — | "Öğrenmeyi karşılar" iddiası yanlış | **K.** Düzeltildi: 313 TL/gün ve sohbet başı 45 TL'de haftada ~49 sohbet; "öğrenme sınırlı" kabul. Kural: 7. gün sohbet başı 40–50 TL ise sahibin ön onayıyla ("öğrenme minimumuna çıkabiliriz") günde 340 TL'ye çıkılır. |

### Kreatif Direktör
| # | Talep | Karar |
|---|---|---|
| 1 | Doldur kadrajı, ≥ %55, ≤ 1,5x, gamma 1,2, zemin 0,30, orijinaller | **K.** F02, F03 ve F07 kaynakları 1,5x sınırında yetersiz → orijinal dosya istendi (**S**, engelleyici değil) |
| 2 | Güvenli alan; kapanış kartı ortası 760 | **K.** Kapanış içeriği y = 470–1060 arasında |
| 3 | TATTOO STUDIO 24 px, alt satır 44 px kemik beyazı | **K** |
| 4 | R1: gözler 1,8x → 1,2 sn geri çekil → 2,0 sn'ye kadar tut, sert kesmeler, kapanış 1,5 sn | **D.** Uygulandı, ancak Politika kararıyla F01 ve F07 çıktı: F05 → F03 → F06 → F02, 7,1 sn |
| 5 | R2'de sert kesme, netleştirme kapalı | **K** |
| 6 | Renkli R2 ana sette olmasın, black & grey süreç videosu çekilsin | **D.** R2 Faz 2'ye (6. gün, ayrı reklam). R3 black & grey süreç senaryosu docs/12'de (**S**, 7. gün) |
| 7 | Meta Ses Koleksiyonu, ~100 BPM, makine sesi –18 dB | **K.** 1,2 sn = 100 BPM'de 2 vuruş. Makine sesi kaydı B-roll listesinde |
| 8 | Teklif görselde olsun | **K.** Hikâyede y = 1160 ve kapanış kartında |
| 9 | Görsel ve metin eşleşsin; carousel sırası | **K.** Carousel: F05, F03, F02, F06, kapanış. A1 tekli reklamlar: F3 ve F5. Güven reklamı (eski A2-F01) kaldırıldı |
| 10 | Yenileme takvimi | **K.** §6 (14. güne kadar) |
| öneri | "Tüm işler Erdem Melih'in kendi çalışması" | **S.** C1 metninde var; sahibin özgünlük beyanı → **yayın kapısı** |

### Politika ve Hukuk Denetçisi
| # | Talep | Karar |
|---|---|---|
| 1 | Yazılı müşteri rızası, 24 saatte durdurma, repoda sadece baş harf | **K.** docs/13 + kreatif/onaylar.csv → **yayın kapısı** (F02, F03, F05, F06) |
| 2 | Advantage+ kreatif iyileştirmelerinin hepsi kapalı + ekran görüntüsü | **K.** Kurulum kontrol listesinde |
| 3 | F07 Faz 1'den çıksın | **K.** F07 sadece organik |
| 4 | İlk 3–5 gün sadece F02/F03/F05/F06; F01/F04 sonra ayrı reklam | **K.** 6. gün |
| 5 | Rötuş koşulu | **K.** Süre ve şart gelene kadar reklam metninde yok; kontrol aracı hata veriyor |
| 6 | "Steril ortam" → "sterilize ekipman" | **K.** Kontrol aracı yakalıyor |
| 7 | Özgünlük ve gerçek kişi portresi onayı | **S** → **yayın kapısı** (docs/13 D) |
| 8 | Müzik sadece Meta Ses Koleksiyonu ya da sessiz | **K** |
| 9 | Faz 1'de müşteri listesi yok | **K** |
| 10 | Karşılama mesajında KVKK linki, İYS | **K.** landing/kvkk.html + docs/07. **Yayın kapısı:** sayfa yayında olmalı |
| 11 | Mario: çağrı kartı yok, asla öne çıkarılmaz | **K.** Kapanış "organik" modda (çağrı yok) |

### Hedef Müşteri Paneli
| # | Talep | Karar |
|---|---|---|
| 1 | Portre örneği ya da "portre" vaadinin kaldırılması | **D.** F05'ten "portre" vaadi çıktı. "Portre dövme" hızlı sorusu kaldı (hizmet var, iddia yok). V3 portre videosu ancak onaylı bir örnek gelirse |
| 2 | Taze ve iyileşmiş hali yan yana | **S.** 14. güne kadar (§6). Faz 2 yeniden hedeflemenin ön şartı |
| 3 | Sanatçının yüzü ve sesi; videolar sessiz olmasın | **K/S.** V1 → **yayın kapısı**; müzik → **yayın kapısı** |
| 4 | İlk saniyede hareket; dövme ≥ %60 | **K.** R1 gözlere yakından açılıyor; doldur kadrajı |
| 5 | Güven ilk ~125 karakterde | **K.** Her reklamın 2. satırı (ilk satır kanca). Güven reklamındaki kurukafa görseli kaldırıldı |
| 6 | Yayından önce ≥ 10 Google yorumu; profil öne çıkanları | **D.** Instagram öne çıkanları (Süreç · Stüdyo · Yorumlar · İşler) → **yayın kapısı**, çünkü reklamdan gelen kişi Instagram profiline bakar. Google yorumu ≥ 10: 14. gün hedefi ve **Google fazının kapısı**. CTWA reklamında Google yorumu görünmediği için Meta'yı bekletmek değer kaybettirir. |
| 7 | Yarım kalan proje sorusu; R2'de gerçek süre | **K.** Hızlı soru 1 ve F5 metni. R2'de süre iddiası kaldırıldı |
| 8 | Kısa kod, konuya özel mesaj, hızlı soruda kod | **K** |
| 9 | Otomatik ilk cevap + mesai dışı | **K.** docs/07 (Erdem'in ağzından, 4 eleme sorusu) |
| 10 | "Fiyat boyuta göre değişir" satırı | **K.** R1 metninde; ayrıca "Fiyat ve seans süresi" hızlı sorusu |

### Finans ve Büyüme Stratejisti
| # | Talep | Karar |
|---|---|---|
| 1 | Toplam 313 TL/gün, ücret dahil | **K.** `ucret_dahil: true` → butce.py ayda 9.523 TL harcama + 476 TL ücret = 10.000 TL |
| 2 | "Öğrenme sınırlı" kabulü; 360'a çıkış sadece kriterle | **D.** Kabul. Sahibin "öğrenme minimumuna çıkabiliriz" ön onayıyla tek istisna: 7. gün sohbet başı 40–50 TL ise 340 TL/gün |
| 3 | Durdurma merdiveni, 20.000 TL kayıp tavanı | **K.** config > kpi. 20.000 TL tavanı **sahip onayına** sunuluyor |
| 4 | Faz 2 geçişi veriye bağlı; 450 TL/gün sınırı; Google ek mi? | **K.** Google = **EK** bütçe + sahip onayı |
| 5 | Kapasite freni; haftada en fazla 8 görüşme | **K.** config > kapasite |
| 6 | Otomatik karşılama + eleme; insan ≤ 60 dk | **D.** Panel 10 dk, Finans 60 dk istedi. Hedef **≤ 30 dk** (11:00–21:00), seans sırasında karşılama mesajı bunu dürüstçe söyler |
| 7 | Tek KPI seti; ana ölçüt kapora başı maliyet | **K.** Hedef ≤ 3.000 TL, durdurma > 6.000 TL (ortalama proje 12.000 TL tahminine göre; sahip verisiyle güncellenecek) |
| 8 | Araçlar plana uyumlu | **K.** butce.py, rapor.py (kod→kampanya eşlemesi A/A1/R1…), kontrol.py |
| 9 | Her soruya kod; CSV'ye sadece ciddi talepler | **K** |
| 10 | Tahsil edilen ve rezerve ayrı; ilk ay net çıkışın kabulü | **K.** Rapor ayırıyor. İlk ay 5.000–8.000 TL net çıkış riski sahibe yazılı bildirilecek |

## 3. Kampanya yapısı v2 (kesin)
**Kampanya A: `EM | Mesaj | WhatsApp | Realizm`** · Etkileşim → WhatsApp → sohbet · set bütçesi · limitsiz teklif

**A1: `A1 | Adv+ | 21+ | 18km | Dövme sinyali` → 313 TL/gün**
- Konum: Güvercin Sk. pini (41.0629, 28.6965), **18 km**, "yaşayan veya yakın zamanda bulunan"
- Advantage+ kitle AÇIK · **kesin minimum yaş 21** · dil kontrolü yok
- Öneriler: yaş 24–44 · özel kitleler (IG etkileşimi 365 gün; video %50 izleme 30 gün, oluşunca) · en fazla 6 ilgi: Dövmeler, Vücut sanatı, Ink Master, Inked, Miami Ink, Dövme sanatçısı (kurulum günü bulunanlar)
- Hariç: IG'den son 30 günde mesaj gönderenler
- Yerleşim: Advantage+ (Audience Network KAPALI) · **Advantage+ kreatif iyileştirmelerinin hepsi KAPALI**
- **Faz 1 reklamları (gün 1):** R1 (Reels) · C1 (carousel 5 kart) · F3 (tekli) · F5 (tekli) · **V1 (konuşma videosu, gelince)**
- **Faz 2 reklamları (gün 6+, ret yoksa, ayrı tekli):** R2 · F1 · F4
- Metinler ve hazır mesajlar: `ads/meta/kampanyalar.yaml` · Linkler: `cikti/linkler.csv`

**B1 (Faz 2):** Yeniden hedefleme, kriterler sağlanınca ve günlük ≥ 450 TL olunca. Kitle < 3.000 kişiyse açılmaz.
**G1 (Faz 2):** Google Arama, EK bütçe, landing + İşletme Profili + ≥ 10 Google yorumu şartıyla. `ads/google/kampanya.yaml` (fiyatsız, realizm odaklı).

**Lüks hedefleme (sahibin önerisi): bilinçli olarak YOK.** Advantage+ önerileri "VEYA" ile birleşir; lüks ilgileri dövme niyetini daraltmaz, sulandırır. Türkiye'de gelir hedeflemesi yok. Ayda ~5–10 kapora ile A/B testi istatistiksel olarak anlamsız. Premium sinyal **kreatifle** (karanlık, sinematik, büyük proje) ve **eleme sorularıyla** veriliyor. Ayda ≥ 10 kapora olunca Faz 3'te yeniden değerlendirilir.

## 4. Bütçe ve öğrenme
- 10.000 TL/ay = 9.523 TL harcama + %5 ücret ≈ 476 TL → **313 TL/gün**
- Sohbet başı 45 TL'de haftada ~49 sohbet. Öğrenme eşiğinin sınırında; "öğrenme sınırlı" kabul edilebilir
- KDV ve stopaj durumu muhasebeciye sorulacak (doğrulanmadı)

## 5. KPI ve kurallar (tek set)
- **Ciddi talep:** bölgesini, yaklaşık boyutunu ve fikrini/referansını paylaşan VE tasarım görüşmesi ya da fiyat aşamasına gelen kişi
- **Ana ölçüt:** kapora başı maliyet ≤ 3.000 TL (durdurma > 6.000 TL)
- **Ara ölçüt:** sohbet başı 45 TL (hedef)
- 72 saat dokunma · bir reklam 150 TL harcayıp 0 sohbet getirirse kapat · kararlar set düzeyinde
- **Gün 7:** sohbet başı > 100 TL ise en kötü 2 reklamı kapat
- **Gün 14:** ciddi talep < 10 ise A1 durur, revize edilir
- **Gün 30:** kapora < 2 ise 2. aya geçilmez
- **Gün 45:** rezerve ciro < harcama × 1,5 ise tamamen dur
- Test kaybı tavanı 20.000 TL (sahip onayı)
- **Faz 2 geçişi:** ≥ 60 sohbet · ≤ 50 TL · ciddi ≥ %30 · ≥ 2 kapora · 30 gün içinde ≥ 6 boş seans · cevap medyanı ≤ 30 dk. Sonra 3 günde bir %20 artış, 450 TL/gün'de dur.
- **Kapasite freni:** ilk boş tam gün > 4 hafta → A1 %50 kısılır · > 6 hafta → dur · tasarım görüşmesi ≤ 8/hafta
- **Cevap:** otomatik karşılama anında · insan cevabı ≤ 30 dk (11:00–21:00)

## 6. Yenileme takvimi
| Gün | Ne eklenir |
|---|---|
| 1 | R1, C1, F3, F5, V1 |
| 6 | Ret yoksa R2, F1, F4 (ayrı tekli reklamlar) |
| 7 | R3 black & grey süreç videosu (sahip çekerse) |
| 14 | 2 adet taze ve iyileşmiş yan yana · 1 isimsiz müşteri yorumu görseli · ≥ 10 Google yorumu |
| 21 | En iyi reklamın yeni kancalı versiyonu · frekans > 3 ise kreatif yenileme |

## 7. YAYIN KAPISI (hepsi ✔ olmadan reklam açılmaz)
- [ ] Kurul oybirliğiyle 10/10
- [ ] Müşteri reklam onayları: F02, F03, F05, F06 (`kreatif/onaylar.csv`)
- [ ] Sahibin özgünlük beyanı (docs/13 D)
- [ ] **V1 konuşma videosu** çekildi ve kurgulandı (docs/12 Video A)
- [ ] Meta Ses Koleksiyonu'ndan müzik videolara gömüldü
- [ ] Meta İşletme hesabı + IG + FB sayfası + **WhatsApp Business** bağlı · reklam hesabı TRY / İstanbul · ödeme yöntemi
- [ ] AdsAgent Meta yetkisi (docs/11) → kurulum PAUSED · **Advantage+ kreatif iyileştirmeleri kapalı** (ekran görüntüsü)
- [ ] WhatsApp Business: karşılama ve uzakta mesajı, etiketler, hızlı yanıtlar · KVKK sayfası yayında
- [ ] Instagram öne çıkanları: İşler · Süreç · Stüdyo · Yorumlar
- [ ] Sahibin yazılı kabulü: 20.000 TL test kaybı tavanı, ilk ay 5.000–8.000 TL net çıkış riski
- [ ] `python3 tools/kontrol.py` → hata yok

**Engelleyici olmayanlar (14 gün içinde):** orijinal fotoğraf dosyaları (4K ve F02/F03 netliği için), iyileşmiş fotoğraflar, Google yorumları, R3, rötuş süresi.

## 8. Sahipten istenen bilgiler
1. Realizm projelerinde ortalama toplam tutar ve seans sayısı (KPI eşikleri buna göre güncellenecek)
2. Önümüzdeki 8 haftada boş tam günler ve ayda alınabilecek yeni proje sayısı
3. Son 3 ayda organik olarak gelen aylık mesaj ve kapora sayısı (karşılaştırma için)
4. Seans sırasında mesajlara kim bakıyor?
5. Ücretsiz rötuş: kaç ay geçerli, şartı ne? · Kapora tutarı ve iade koşulu
6. Instagram hesabının yaklaşık etkileşim kitlesi (son 365 gün)
7. Fotoğraflardaki dövmeler gerçek bir kişinin portresi mi? (F03, F05)
