# Bu repo: Bahçeşehir dövme stüdyosu reklam sistemi

- Kullanıcı stüdyo sahibi. **Türkçe**, sade ve teknik jargon olmadan konuş.
- Genel reklam istekleri için `.claude/skills/reklam-yoneticisi` skill'i ile başla. O skill doğru alt skill'e yönlendirir (meta-reklam, google-reklam, reklam-metni, haftalik-rapor, icerik-takvimi, musteri-mesaji, rakip-analizi).
- Tek doğruluk kaynağı: `config/studio.yaml` (stüdyo bilgileri, fiyat, bütçe) + `ads/` (kampanya ve metinler).
- `ads/` veya `config/` değiştikten sonra: `python3 tools/kontrol.py` → ardından `python3 tools/linkler.py` ve `python3 tools/google_disa_aktar.py` ile `cikti/` klasörünü yenile.
- Para harcayan veya reklamı yayına alan her işlemden önce açık onay al. Yeni kampanyalar PAUSED kurulur.
- 18 yaş altı hedefleme ve "en iyi / garanti / acısız" gibi iddialar yasak (bkz. `docs/10-mevzuat-ve-kurallar.md`).
- Müşteri tam adı ve telefonu repoya yazılmaz (KVKK).
