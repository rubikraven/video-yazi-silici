# AI Watermark Remover & Video Restoration

Bu proje, CapCut veya benzeri AI video editörlerinin export sırasında zorunlu olarak eklediği "AI" etiketlerini ve filigranları (watermark) görüntü işleme teknikleri kullanarak temizlemek için geliştirilmiştir.

## Teknik Detaylar
- **OpenCV Inpainting:** Silinen alanın çevredeki dokularla (Telea algoritması) doğal bir şekilde doldurulması.
- **Dinamik Maskeleme:** Belirli koordinatlara göre otomatik maske oluşturma.
- **Pixelate & Blur:** İnatçı kalıntılar için çok katmanlı temizlik.

## Kurulum
```bash
pip install -r requirements.txt
