---
name: musteri-mesaji
description: Dövme müşterilerine WhatsApp/Instagram DM cevabı yazma — ilk cevap, fiyat verme, "pahalı" itirazı, "düşüneceğim", kapora, randevu hatırlatma, bakım, Google yorum isteği, takip mesajları; ayrıca mesajdan randevuya dönüşüm oranını artırma. Kullanıcı bir müşteri mesajını yapıştırıp "ne cevap vereyim", "nasıl yazayım", "müşteri pahalı dedi", "cevap vermedi", "yorum nasıl isterim" dediğinde kullan. Use for drafting replies to tattoo customer DMs/WhatsApp messages and improving lead-to-booking conversion.
---

# Müşteri Mesajları (WhatsApp / DM)

## Önce oku
- `docs/07-mesaj-scriptleri.md`: tüm şablonlar (/ilk, /fiyat, /pahali, /dusunecegim, /kapora, /hatirlatma, /bakim, /yorum, /takip1, /takip2)
- `config/studio.yaml`: fiyatlar, kapora, yorum linki, adres

## Müşteri mesajı yapıştırıldığında
1. **Aşamayı belirle:** ilk temas / fiyat sorusu / itiraz / kararsız / kapora / randevu sonrası
2. **Mesajın sonunda [KOD] var mı?** Varsa kullanıcıya hatırlat: "Bunu takip dosyasına `kaynak_kodu=K2-02` olarak yaz" (ya da onay alıp `takip/musteri-takip.csv` dosyasına baş harflerle sen ekle)
3. **Cevap taslağı yaz:** şablonu temel al ama müşterinin söylediğine **kişiselleştir** (stil, bölge, boyut).
4. **Her cevap bir soruyla ya da iki seçenekli bir teklifle bitsin** ("Salı mı Perşembe mi?").
5. Uzun yazma: WhatsApp'ta 3–5 satır. Gerekirse "sesli mesaj olarak şunu söyle" önerisi ver.

## Fiyat verme ilkeleri
- Fiyatı saklama. Kesin bilgi yoksa **aralık ver** ve netleştirici soru sor.
- Fiyatı **değerle birlikte** ver: özel çizim, steril ortam, iyileşme takibi, rötuş.
- İndirim yerine **seçenek** sun: boyutu küçültmek, detayı sadeleştirmek, flash tasarım.
- `config/studio.yaml` → `fiyatlar` dışında fiyat uydurma. Emin değilsen kullanıcıya sor.

## Kırmızı çizgiler
- 18 yaş altı olduğu anlaşılan biri → kibarca reddet: "18 yaşını doldurduğunda seni bekliyoruz 🖤". Veli onayıyla bile iş alma.
- Sağlık sorusu (alerji, ilaç, cilt hastalığı, hamilelik) → "Doktoruna danışmanı öneririz" de, tıbbi tavsiye verme.
- Toplu kampanya mesajı taslağı istenirse → önce **izin kuralını** hatırlat (6563 / İYS, docs/07 sonu).
- Müşterinin fotoğrafını paylaşmak için **yazılı onay** mesajı taslağı da öner.

## Dönüşüm sorunu teşhisi
Kullanıcı "çok mesaj geliyor ama randevu yok" derse sor:
- İlk cevap süresi ne kadar? (hedef ≤ 5 dk)
- Fiyatı ilk mesajda mı veriyorsun, yoksa "gelin konuşalım" mı diyorsun?
- Takip mesajı atıyor musun? (/takip1 2 gün sonra, /takip2 7 gün sonra)
- Kapora isteme anı net mi?
Sonra `takip/musteri-takip.csv` dosyasındaki `kayip` satırlarının `not` alanlarından ortak nedeni bul.
