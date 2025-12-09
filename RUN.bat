@echo off
REM ============================================================
REM Instagram Bot API - Calistir (Windows)
REM ============================================================

echo.
echo ============================================================
echo   Instagram Bot API Baslatiliyor...
echo ============================================================
echo.

REM .env dosyasi var mi kontrol et
if not exist .env (
    echo [HATA] .env dosyasi bulunamadi!
    echo.
    echo Lutfen .env dosyasi olusturun:
    echo   IG_USERNAME=instagram_kullanici_adiniz
    echo   IG_PASSWORD=instagram_sifreniz
    echo.
    pause
    exit /b 1
)

REM Virtual environment aktif et
if not exist venv\Scripts\activate.bat (
    echo [HATA] Virtual environment bulunamadi!
    echo.
    echo Lutfen once SETUP.bat dosyasini calistirin.
    echo.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

REM Uygulamayi baslat
echo.
echo Uygulama baslatiliyor...
echo Public URL olusturulacak ve otomatik kopyalanacak!
echo.
echo Kapatmak icin Ctrl+C yapin.
echo.
python start.py

pause
