#!/bin/bash
# ============================================================
# Instagram Bot API - Çalıştır (Mac/Linux)
# ============================================================

echo ""
echo "============================================================"
echo "  Instagram Bot API Başlatılıyor..."
echo "============================================================"
echo ""

# .env dosyası var mı kontrol et
if [ ! -f .env ]; then
    echo "[HATA] .env dosyası bulunamadı!"
    echo ""
    echo "Lütfen .env dosyası oluşturun:"
    echo "  IG_USERNAME=instagram_kullanici_adiniz"
    echo "  IG_PASSWORD=instagram_sifreniz"
    echo ""
    exit 1
fi

# Virtual environment var mı kontrol et
if [ ! -f venv/bin/activate ]; then
    echo "[HATA] Virtual environment bulunamadı!"
    echo ""
    echo "Lütfen önce SETUP.sh dosyasını çalıştırın:"
    echo "  chmod +x SETUP.sh"
    echo "  ./SETUP.sh"
    echo ""
    exit 1
fi

# Virtual environment aktif et
source venv/bin/activate

# Uygulamayı başlat
echo ""
echo "Uygulama başlatılıyor..."
echo "Public URL oluşturulacak ve otomatik kopyalanacak!"
echo ""
echo "Kapatmak için Ctrl+C yapın."
echo ""
python start.py
