---
name: reklam-metni
description: Dövme stüdyosu için reklam metni, kanca (hook), başlık, Reels ekran yazısı, carousel metni, Google başlık/açıklama yazma ve mevcut metinleri iyileştirme — Türk reklam hukuku ve Meta politikasına uygun. Kullanıcı "reklam metni yaz", "yeni kanca", "başlık öner", "bu metni düzelt", "A/B testi", "yeni reklam" dediğinde kullan. Use for writing or rewriting compliant Turkish ad copy, hooks and headlines for Meta and Google.
---

# Reklam Metni Yazımı

## Önce oku
- `config/studio.yaml`: stüdyo adı, sanatçı, stiller (false olan stil için metin yazma), fiyatlar
- `ads/meta/kampanyalar.yaml`: mevcut metinlerin tonu ve formatı
- `docs/05-kreatif-rehberi.md`: kanca bankası

## Ses tonu
- **Samimi, sıcak, kendinden emin; asla yalvaran ya da agresif değil.** "Sen" diye hitap et.
- Sanatçı birinci tekil konuşur ("çizerim", "birlikte tasarlayalım"). Kurumsal "firmamız" dili kullanma.
- Kısa cümle. Emoji ölçülü: satır başına en fazla 1 tane, ✔️ 📍 ✍️ 🖤 gibi.
- Konumlanma: **sana özel tasarım · görünen güven · erişilebilirlik** (docs/01 §6)

## Formül
1. **Kanca** (ilk satır / ekran yazısı, ≤ 8 kelime): merak, somut sayı ya da tanıdık bir dert ("İlk dövmen mi?")
2. **Değer:** ne alacak (özel çizim, steril ortam, iyileşme takibi)
3. **Güven:** tek kullanımlık iğne, 18+ kimlik, gerçek yorum
4. **CTA:** tek ve net: "WhatsApp'tan yaz", "fikrini gönder"
5. **Konum:** 📍 Bahçeşehir

## Kurallar (kontrol aracı denetler)
- ❌ "en iyi", "bir numara", "lider", "garanti(li)", "%100", "acısız", "hiç acımaz", "bedava"
- ❌ Görünüşü aşağılayan dil ("çirkin", "utanıyor musun", "rezil")
- ❌ Kişiye özellik atfetme ("Sen de dövmeli biri misin?") → Meta reddediyor
- ❌ Sahte aciliyet ("son 2 kontenjan!"): sadece gerçekse yaz
- ✅ Fiyat yazıyorsan: "X TL'den başlar; fiyat boyut ve detaya göre değişir"
- Meta başlık ≤ 40 karakter, birincil metnin ilk satırı ≤ 125 karakter
- Google başlık ≤ 30, açıklama ≤ 90 karakter

## Çıktı
- Her istek için **3 farklı açı** öner (ör. süreç / güven / fiyat). Her biri: kanca, metin, başlık, CTA, hazır mesaj (karşılama).
- Kullanıcı seçince `ads/meta/kampanyalar.yaml` dosyasına **yeni kodla** ekle (K2-07, K2-08…). Eski reklamın kodunu değiştirme, raporlar bozulur.
- Ardından `python3 tools/kontrol.py` çalıştır ve sonucu göster.
- Mesaj reklamında `karsilama` alanını mutlaka doldur. Kod `tools/linkler.py` ile otomatik eklenir.
