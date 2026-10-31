#!/usr/bin/env python3
"""Reklam kreatiflerini üretir (fotoğraf + video).

    python3 tools/kreatif_uret.py              # hepsi
    python3 tools/kreatif_uret.py --sadece foto
    python3 tools/kreatif_uret.py --sadece video

Girdi : kreatif/kaynak/  (orijinal foto/video)   +  kreatif/kreatif.yaml (yazılar, sıra)
Çıktı : kreatif/cikti/
          akis_4x5/    Instagram/Facebook akış (1080x1350)
          hikaye_9x16/ Story / Reels görseli (1080x1920)
          carousel/    Kaydırmalı reklam kartları (1080x1350)
          video/       Reels videoları (1080x1920, H.264, 30 fps)

Kural: Dövmenin kendisine rötuş yapılmaz. Sadece kadraj, hafif ışık/netlik,
arka plan temizliği, format ve yazı. (Gerçekte olmayan bir sonucu göstermek yanıltıcı reklamdır.)
Gereken: Pillow, numpy, PyYAML, ffmpeg.
"""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

import numpy as np
import yaml
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

KOK = Path(__file__).resolve().parent.parent
KAYNAK = KOK / "kreatif" / "kaynak"
CIKTI = KOK / "kreatif" / "cikti"
FONT_DIR = Path("/usr/share/fonts/opentype/inter")
FPS = 30
KEMIK = (237, 231, 221)   # ana yazı rengi (kemik beyazı)
GRI = (160, 154, 146)
SIYAH = (6, 6, 7)


def font(ad: str, boy: int) -> ImageFont.FreeTypeFont:
    yol = FONT_DIR / ad
    try:
        return ImageFont.truetype(str(yol), boy)
    except OSError:
        return ImageFont.truetype("DejaVuSans-Bold.ttf" if "Bold" in ad or "Black" in ad else "DejaVuSans.ttf", boy)


def tr_buyuk(s: str) -> str:
    return s.replace("i", "İ").replace("ı", "I").upper()


# ---------------------------------------------------------------- metin
def aralikli_genislik(metin, f, aralik):
    return sum(f.getlength(c) for c in metin) + aralik * max(0, len(metin) - 1)


def aralikli_yaz(d: ImageDraw.ImageDraw, merkez_x, y, metin, f, renk, aralik=0):
    x = merkez_x - aralikli_genislik(metin, f, aralik) / 2
    for c in metin:
        d.text((x, y), c, font=f, fill=renk)
        x += f.getlength(c) + aralik


def satir_bol(metin, f, max_g):
    kelimeler, satirlar, s = metin.split(), [], ""
    for k in kelimeler:
        dene = (s + " " + k).strip()
        if f.getlength(dene) <= max_g:
            s = dene
        else:
            satirlar.append(s)
            s = k
    satirlar.append(s)
    return satirlar


def golgeli_katman(boyut, ciz):
    """Metni gölgeli çizer: ciz(draw) fonksiyonu katmana yazar."""
    katman = Image.new("RGBA", boyut, (0, 0, 0, 0))
    ciz(ImageDraw.Draw(katman))
    golge = Image.new("RGBA", boyut, (0, 0, 0, 0))
    golge.putalpha(katman.getchannel("A").filter(ImageFilter.GaussianBlur(10)).point(lambda a: int(a * 0.85)))
    return Image.alpha_composite(golge, katman)


def scrim(boyut, ust: bool, yukseklik, guc=0.85):
    w, h = boyut
    a = np.zeros((h, w), dtype=np.uint8)
    ramp = (np.linspace(1, 0, yukseklik) ** 1.6 * 255 * guc).astype(np.uint8)
    if ust:
        a[:yukseklik] = ramp[:, None]
    else:
        a[h - yukseklik:] = ramp[::-1][:, None]
    s = Image.new("RGBA", boyut, (0, 0, 0, 255))
    s.putalpha(Image.fromarray(a))
    return s


# ---------------------------------------------------------------- foto hazırlama
def foto_yukle(oge: dict) -> Image.Image:
    im = Image.open(KAYNAK / oge["dosya"]).convert("RGB")
    for x1, y1, x2, y2 in oge.get("temizle", []):
        # Kutuyu çevresindeki arka plan rengiyle doldur, kenarları yumuşat
        a = np.asarray(im).copy()
        pad = 30
        cev = np.concatenate([
            a[max(0, y1 - pad):y1, x1:x2].reshape(-1, 3), a[y2:y2 + pad, x1:x2].reshape(-1, 3),
            a[y1:y2, max(0, x1 - pad):x1].reshape(-1, 3), a[y1:y2, x2:x2 + pad].reshape(-1, 3)])
        a[y1:y2, x1:x2] = np.median(cev, axis=0).astype(np.uint8)
        yama = Image.fromarray(a)
        maske = Image.new("L", im.size, 0)
        ImageDraw.Draw(maske).rectangle([x1 - 6, y1 - 6, x2 + 6, y2 + 6], fill=255)
        im = Image.composite(yama, im, maske.filter(ImageFilter.GaussianBlur(5)))
    if oge.get("kirp"):
        im = im.crop(tuple(oge["kirp"]))
    # Hafif profesyonel bitiş: netlik + çok az kontrast. Dövme detayı DEĞİŞTİRİLMEZ.
    im = im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=30, threshold=3))
    im = ImageEnhance.Contrast(im).enhance(1.04)
    return im


def bulanik_zemin(im: Image.Image, boyut) -> Image.Image:
    """Fotoğrafın kendisinden karartılmış bulanık zemin (siyah zeminli fotoğraflarda neredeyse siyah)."""
    w, h = boyut
    o = max(w / im.width, h / im.height)
    z = im.resize((int(im.width * o) + 2, int(im.height * o) + 2), Image.BICUBIC)
    z = z.crop(((z.width - w) // 2, (z.height - h) // 2, (z.width - w) // 2 + w, (z.height - h) // 2 + h))
    z = z.filter(ImageFilter.GaussianBlur(45))
    return ImageEnhance.Brightness(z).enhance(0.22)


def yerlestir(im, kutu_w, kutu_h):
    o = min(kutu_w / im.width, kutu_h / im.height)
    return im.resize((round(im.width * o), round(im.height * o)), Image.LANCZOS)


def yumusak_yapistir(c: Image.Image, p: Image.Image, x: int, y: int, kenar=70):
    """Fotoğrafı zemine kenarları yumuşatarak yapıştırır (sert dikdörtgen çizgisi kalmaz)."""
    m = np.ones((p.height, p.width), dtype=np.float32)
    r = np.linspace(0, 1, kenar, dtype=np.float32)
    if y > 0:
        m[:kenar] *= r[:, None]
    if y + p.height < c.height:
        m[-kenar:] *= r[::-1][:, None]
    if x > 0:
        m[:, :kenar] *= r[None, :]
    if x + p.width < c.width:
        m[:, -kenar:] *= r[None, ::-1]
    c.paste(p, (x, y), Image.fromarray((m * 255).astype(np.uint8)))


def imza(d, W, y, kucuk=False):
    f1 = font("InterDisplay-Bold.otf", 30 if kucuk else 36)
    f2 = font("Inter-Medium.otf", 16 if kucuk else 18)
    aralikli_yaz(d, W / 2, y, tr_buyuk(M["ust"]), f1, KEMIK, 9)
    aralikli_yaz(d, W / 2, y + (40 if kucuk else 48), M["alt"], f2, GRI, 8)


def akis_4x5(kod, im) -> Image.Image:
    W, H = 1080, 1350
    c = bulanik_zemin(im, (W, H))
    p = yerlestir(im, W, H - 150)
    ust = max(0, (H - 150 - p.height) // 2)
    yumusak_yapistir(c, p, (W - p.width) // 2, ust)
    c = c.convert("RGBA")
    c = Image.alpha_composite(c, scrim((W, H), False, 300))
    c = Image.alpha_composite(c, golgeli_katman((W, H), lambda d: imza(d, W, H - 112)))
    return c.convert("RGB")


def hikaye_9x16(kod, im, yazi) -> Image.Image:
    W, H = 1080, 1920
    c = bulanik_zemin(im, (W, H))
    p = yerlestir(im, W, 1060)
    yumusak_yapistir(c, p, (W - p.width) // 2, 460 + (1060 - p.height) // 2)
    c = c.convert("RGBA")
    c = Image.alpha_composite(c, scrim((W, H), True, 520, 0.75))
    c = Image.alpha_composite(c, scrim((W, H), False, 520, 0.8))

    def ciz(d):
        f = font("InterDisplay-Bold.otf", 66)
        for i, s in enumerate(satir_bol(yazi, f, 940)):
            aralikli_yaz(d, W / 2, 290 + i * 80, s, f, KEMIK, 0)
        imza(d, W, 1545, kucuk=True)
    c = Image.alpha_composite(c, golgeli_katman((W, H), ciz))
    return c.convert("RGB")


def kapanis_karti(W, H, baslik=None, alt=None, uzmanlik=None) -> Image.Image:
    c = Image.new("RGB", (W, H), SIYAH)
    d = ImageDraw.Draw(c)
    orta = H / 2 - (60 if H > 1500 else 40)
    if baslik:
        fb = font("InterDisplay-Bold.otf", 64)
        satirlar = satir_bol(baslik, fb, W - 160)
        for i, s in enumerate(satirlar):
            aralikli_yaz(d, W / 2, orta - 330 + i * 76, s, fb, KEMIK)
        if alt:
            fa = font("Inter-Regular.otf", 32)
            for i, s in enumerate(satir_bol(alt, fa, W - 200)):
                aralikli_yaz(d, W / 2, orta - 330 + len(satirlar) * 76 + 24 + i * 44, s, fa, GRI)
    d.line([(W / 2 - 40, orta - 70), (W / 2 + 40, orta - 70)], fill=GRI, width=2)
    aralikli_yaz(d, W / 2, orta - 30, tr_buyuk(M["ust"]), font("InterDisplay-Bold.otf", 84), KEMIK, 14)
    aralikli_yaz(d, W / 2, orta + 78, M["alt"], font("Inter-Medium.otf", 28), GRI, 14)
    aralikli_yaz(d, W / 2, orta + 160, uzmanlik or M["uzmanlik"], font("Inter-Regular.otf", 38), KEMIK)
    # CTA kapsülü
    fc = font("Inter-SemiBold.otf", 36)
    cw = fc.getlength(M["cta"]) + 80
    y = orta + 260
    d.rounded_rectangle([W / 2 - cw / 2, y, W / 2 + cw / 2, y + 84], radius=42, fill=KEMIK)
    aralikli_yaz(d, W / 2, y + 20, M["cta"], fc, SIYAH)
    aralikli_yaz(d, W / 2, y + 130, f"{M['konum']}   ·   {M['hesap']}", font("Inter-Medium.otf", 28), GRI)
    return c


# ---------------------------------------------------------------- video
class Yazici:
    def __init__(self, yol: Path, ses: Path | None = None, ses_sure: float | None = None):
        komut = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920",
                 "-r", str(FPS), "-i", "-"]
        if ses:
            komut += ["-i", str(ses), "-map", "0:v", "-map", "1:a", "-af", "apad"]
        else:
            komut += ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-map", "0:v", "-map", "1:a"]
        komut += ["-shortest", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                  "-profile:v", "high", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(yol)]
        self.p = subprocess.Popen(komut, stdin=subprocess.PIPE)
        self.n = 0

    def yaz(self, im: Image.Image):
        self.p.stdin.write(im.convert("RGB").tobytes())
        self.n += 1

    def kapat(self):
        self.p.stdin.close()
        if self.p.wait() != 0:
            raise SystemExit("ffmpeg hatası")


def video_kareleri(yol: Path):
    """Videoyu 1080x1920 / 30fps kare kare okur (hafif kontrast ve netlik)."""
    vf = ("fps=30,scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,"
          "eq=contrast=1.04:saturation=1.03,unsharp=5:5:0.4")
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(yol), "-vf", vf, "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    boy = 1080 * 1920 * 3
    try:
        while True:
            b = p.stdout.read(boy)
            if len(b) < boy:
                break
            yield Image.frombytes("RGB", (1080, 1920), b)
    finally:
        p.kill()
        p.wait()


def zoom_kareleri(c: Image.Image, n: int, z1=1.0, z2=1.07):
    W, H = c.size
    for i in range(n):
        z = z1 + (z2 - z1) * (i / max(1, n - 1))
        w, h = W / z, H / z
        x, y = (W - w) / 2, (H - h) / 2
        yield c.resize((W, H), Image.BICUBIC, box=(x, y, x + w, y + h))


def sabit_kareler(c, n):
    for _ in range(n):
        yield c


def birlestir(yazici: Yazici, parcalar, gecis=12, ustune=None):
    """parcalar: [(kare_üreteci, kare_sayısı)]; aralarında 'gecis' karelik çapraz geçiş.
    ustune(i, kare) -> kare : zaman çizelgesindeki i. kareye yazı bindirmek için."""
    i = 0
    kuyruk = []                      # önceki parçanın sona saklanan kareleri
    for pi, (gen, n) in enumerate(parcalar):
        tut = gecis if pi < len(parcalar) - 1 else 0
        yeni = []
        for j, k in enumerate(gen):
            if j >= n:
                break
            if j < len(kuyruk):
                k = Image.blend(kuyruk[j], k, (j + 1) / (len(kuyruk) + 1))
            if j >= n - tut:
                yeni.append(k)
                continue
            yazici.yaz(ustune(i, k) if ustune else k)
            i += 1
        kuyruk = yeni
    return i


def kanca_bindir(baslangic_metin, alt_metin=None, sure_kare=78, imza_bitis=10**9):
    W, H = 1080, 1920
    ust = Image.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 0)), scrim((W, H), True, 620, 0.8))

    def ciz(d):
        f = font("InterDisplay-Black.otf", 84)
        satirlar = satir_bol(baslangic_metin, f, 960)
        for k, s in enumerate(satirlar):
            aralikli_yaz(d, W / 2, 300 + k * 96, s, f, KEMIK)
        if alt_metin:
            aralikli_yaz(d, W / 2, 300 + len(satirlar) * 96 + 18, alt_metin, font("Inter-Medium.otf", 36), GRI, 3)
    yazi = Image.alpha_composite(ust, golgeli_katman((W, H), ciz))
    alt = Image.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 0)), scrim((W, H), False, 420, 0.7))
    alt = Image.alpha_composite(alt, golgeli_katman((W, H), lambda d: imza(d, W, 1545, kucuk=True)))

    def uygula(i, k):
        k = k.convert("RGBA")
        if i < imza_bitis:
            k = Image.alpha_composite(k, alt)
        if i < sure_kare:
            a = 1.0 if i < sure_kare - 8 else (sure_kare - i) / 8
            katman = yazi.copy()
            katman.putalpha(yazi.getchannel("A").point(lambda v: int(v * a)))
            k = Image.alpha_composite(k, katman)
        return k.convert("RGB")
    return uygula


def video_sayisi(yol):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(yol)],
                         capture_output=True, text=True).stdout
    return int(float(out) * FPS)


# ---------------------------------------------------------------- ana akış
def main():
    global M
    ap = argparse.ArgumentParser()
    ap.add_argument("--sadece", choices=["foto", "video"])
    a = ap.parse_args()
    K = yaml.safe_load((KOK / "kreatif" / "kreatif.yaml").read_text(encoding="utf-8"))
    M = K["marka"]
    fotolar = {o["kod"]: foto_yukle(o) for o in K["fotograflar"] if o.get("reklam", True)}
    for alt in ("akis_4x5", "hikaye_9x16", "carousel", "video"):
        (CIKTI / alt).mkdir(parents=True, exist_ok=True)

    if a.sadece in (None, "foto"):
        for kod, im in fotolar.items():
            akis_4x5(kod, im).save(CIKTI / "akis_4x5" / f"{kod}.jpg", quality=92, subsampling=0)
            hikaye_9x16(kod, im, K["hikaye_yazilari"][kod]).save(CIKTI / "hikaye_9x16" / f"{kod}.jpg", quality=92, subsampling=0)
        car = K["carousel"]
        for i, kod in enumerate(car["sira"], 1):
            akis_4x5(kod, fotolar[kod]).save(CIKTI / "carousel" / f"kart{i:02d}-{kod}.jpg", quality=92, subsampling=0)
        kapanis_karti(1080, 1350, car["kapanis_baslik"], car["kapanis_alt"]).save(
            CIKTI / "carousel" / f"kart{len(car['sira']) + 1:02d}-kapanis.jpg", quality=92, subsampling=0)
        print(f"✔ {len(fotolar)} fotoğraf → akış 4:5, hikâye 9:16, carousel {len(car['sira']) + 1} kart")

    if a.sadece in (None, "video"):
        V = K["videolar"]
        hikaye = lambda kod: hikaye_zemini(fotolar[kod])  # noqa: E731

        # R1 — slayt: "Bu bir fotoğraf değil"
        s = V["slayt_realizm"]
        n = int(s["kare_suresi"] * FPS)
        parcalar = [(zoom_kareleri(hikaye(k), n + 12), n + 12) for k in s["sira"]]
        parcalar.append((sabit_kareler(kapanis_karti(1080, 1920), 80), 80))
        y = Yazici(CIKTI / "video" / s["cikti"])
        bitis = len(s["sira"]) * (n + 12 - 12)
        birlestir(y, parcalar, ustune=kanca_bindir(s["kanca"], s.get("kanca_alt"), 72, bitis))
        y.kapat()
        print(f"✔ {s['cikti']}  ({y.n / FPS:.1f} sn)")

        # R2 — süreç → sonuç
        s = V["surec_sonuc"]
        kay = KAYNAK / s["kaynak"]
        nv = video_sayisi(kay)
        sonuc = hikaye(s["sonuc_foto"])
        ds = ImageDraw.Draw(sonuc)
        aralikli_yaz(ds, 540, 300, s["sonuc_yazi"], font("InterDisplay-Black.otf", 84), KEMIK)
        parcalar = [(video_kareleri(kay), nv - 2), (zoom_kareleri(sonuc, 96), 96),
                    (sabit_kareler(kapanis_karti(1080, 1920, uzmanlik="Realizm dövme"), 80), 80)]
        y = Yazici(CIKTI / "video" / s["cikti"])
        bitis = (nv - 2 - 12) + (96 - 12)
        birlestir(y, parcalar, ustune=kanca_bindir(s["kanca"], None, 78, bitis))
        y.kapat()
        print(f"✔ {s['cikti']}  ({y.n / FPS:.1f} sn)")

        # Organik — Mario (ücretli reklamda kullanılmaz)
        s = V["organik_mario"]
        kay = KAYNAK / s["kaynak"]
        nv = video_sayisi(kay)
        alt = imza_katmani()
        parcalar = [(video_kareleri(kay), nv - 2),
                    (sabit_kareler(kapanis_karti(1080, 1920), 75), 75)]
        y = Yazici(CIKTI / "video" / s["cikti"], ses=kay)
        birlestir(y, parcalar, ustune=lambda i, k: Image.alpha_composite(k.convert("RGBA"), alt).convert("RGB")
                  if i < nv - 14 else k)
        y.kapat()
        print(f"✔ {s['cikti']}  ({y.n / FPS:.1f} sn)  ← SADECE ORGANİK")

        # Kapak görselleri (video küçük resmi)
        for ad in (V["slayt_realizm"]["cikti"], V["surec_sonuc"]["cikti"]):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "0.8", "-i", str(CIKTI / "video" / ad),
                            "-frames:v", "1", "-q:v", "2", str(CIKTI / "video" / ad.replace(".mp4", "-kapak.jpg"))],
                           check=True)


def hikaye_zemini(im):
    """Video için 9:16 zemin + fotoğraf (yazısız; yazı videoda bindirilir)."""
    W, H = 1080, 1920
    c = bulanik_zemin(im, (W, H))
    p = yerlestir(im, W, 1180)
    yumusak_yapistir(c, p, (W - p.width) // 2, 440 + (1180 - p.height) // 2)
    return c


def imza_katmani():
    W, H = 1080, 1920
    alt = Image.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 0)), scrim((W, H), False, 420, 0.6))
    return Image.alpha_composite(alt, golgeli_katman((W, H), lambda d: imza(d, W, 1545, kucuk=True)))


M: dict = {}

if __name__ == "__main__":
    main()
