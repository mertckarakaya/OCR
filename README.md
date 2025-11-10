# OCR Docker Batch Processor

Bu proje, **Tesseract OCR** kullanarak PDF dosyalarındaki metinleri otomatik olarak `.txt` dosyalarına dönüştürür.  
Hiçbir şeyi yerel makinene kurmana gerek yok — her şey Docker container içinde çalışır.

---

## Özellikler

- Tamamen **Docker tabanlı** (Python, Tesseract, Poppler içerir)  
- `data/in/` klasöründeki tüm **PDF dosyalarını otomatik tarar**  
- Çıktıları aynı klasör yapısıyla `data/out/` altına yazar  
- Çıktı dosyaları `*.OCR.txt` formatındadır  
- Türkçe + İngilizce OCR desteklidir (isteğe göre değiştirilebilir)

---

## Klasör Yapısı

```
ocr-docker/
├─ Dockerfile
├─ docker-compose.yml
├─ requirements.txt
├─ batch.py
└─ data/
   ├─ in/          # PDF dosyalarını buraya koy
   │   ├─ faturalar/
   │   │   └─ ocak.pdf
   │   └─ kimlikler/
   │       └─ pasaport.pdf
   └─ out/         # OCR çıktıları burada oluşur
       ├─ faturalar/
       │   └─ ocak.OCR.txt
       └─ kimlikler/
           └─ pasaport.OCR.txt
```

---

## Kurulum ve Kullanım

### 1. Build et
```bash
docker compose build
```

### 2. OCR işlemini başlat
```bash
docker compose up
```

> Container, `data/in/` içindeki tüm PDF’leri işler, `data/out/` içine sonuçları yazar ve sonra otomatik kapanır.

---

## Ortam Değişkenleri

| Değişken | Varsayılan | Açıklama |
|-----------|-------------|-----------|
| `OCR_LANG` | `tur+eng` | OCR dili (örnek: `eng`, `tur`, `eng+tur`) |
| `OCR_DPI` | `300` | PDF sayfa çözünürlüğü (OCR doğruluğunu etkiler) |
| `OCR_PSM` | `6` | Sayfa segmentasyon modu (tek sütun, tam sayfa vs.) |
| `OCR_FORCE` | `0` | `1` olursa mevcut `.OCR.txt` dosyaları yeniden yazılır |

Değerleri `docker-compose.yml` içinde düzenleyebilirsin veya çalıştırma sırasında geçici olarak verebilirsin:
```bash
docker compose run --rm -e OCR_FORCE=1 ocr
```

---

## Notlar

- Yalnızca `.pdf` dosyaları işlenir.  
  (İstersen `.png`, `.jpg` desteği eklenebilir.)  
- PDF içindeki sayfalar sırasıyla taranır ve her sayfanın başına `--- Page N ---` etiketi eklenir.  
- `Tesseract` içinde Türkçe ve İngilizce dilleri hazır kurulu gelir.  

---

## Örnek Kullanım

```
# PDF'leri koy
cp ./faturalar/*.pdf ./data/in/faturalar/

# İşlet
docker compose up

# Çıktıyı oku
cat ./data/out/faturalar/ocak.OCR.txt
```

---

## Temizlik
```bash
docker compose down
docker image rm my-ocr-batch
```

---

Hazırlayan: **Mert Can Karakaya**  
Basit, taşınabilir ve sıfır kurulumla çalışan OCR çözümü
