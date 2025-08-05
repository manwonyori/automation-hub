@echo off
cls
echo ================================================
echo    AUTOMATION HUB - 통합 자동화 시스템
echo ================================================
echo.
echo 선택하세요:
echo.
echo 1. 범용 학습 시스템 (새 사이트 학습)
echo 2. 카페24 자동화
echo 3. 네이버 자동화
echo 4. 쿠팡 자동화
echo 5. 모든 사이트 동시 실행
echo 6. 스케줄러 관리
echo 0. 종료
echo.

set /p choice="선택 (0-6): "

if "%choice%"=="1" (
    echo.
    echo 범용 학습 시스템을 시작합니다...
    cd /d "%~dp0"
    python universal_automation_teacher.py
) else if "%choice%"=="2" (
    echo.
    echo 카페24 자동화를 시작합니다...
    cd /d "%~dp0\01_CAFE24"
    python cafe24_automation.py
) else if "%choice%"=="3" (
    echo.
    echo 네이버 자동화를 시작합니다...
    cd /d "%~dp0\02_NAVER"
    python naver_automation.py
) else if "%choice%"=="4" (
    echo.
    echo 쿠팡 자동화를 시작합니다...
    cd /d "%~dp0\03_COUPANG"
    python coupang_automation.py
) else if "%choice%"=="5" (
    echo.
    echo 모든 사이트 동시 실행...
    cd /d "%~dp0\GENERATED_SCRIPTS"
    python multi_site_sync.py
) else if "%choice%"=="6" (
    echo.
    echo 스케줄러 관리...
    cd /d "%~dp0\SHARED\plugins"
    python scheduler.py
) else if "%choice%"=="0" (
    echo.
    echo 프로그램을 종료합니다.
    exit
)

echo.
pause
goto :eof