@echo off
setlocal

:: Always run from the folder this .bat file lives in, so it finds
:: youtube_downloader.py regardless of where you double-click it from.
cd /d "%~dp0"

echo ============================
echo   YouTube Video Downloader
echo ============================
echo.

set /p VIDEO_URL="Paste YouTube URL: "
if "%VIDEO_URL%"=="" (
    echo.
    echo No URL entered. Exiting.
    pause
    exit /b
)

set /p QUALITY="Max quality - e.g. 1080, 720 - or press Enter for best: "
if "%QUALITY%"=="" set QUALITY=best

echo.
echo Downloading...
echo.

python youtube_downloader.py "%VIDEO_URL%" -q %QUALITY%

echo.
echo ============================
echo Done. Press any key to close.
echo ============================
pause >nul