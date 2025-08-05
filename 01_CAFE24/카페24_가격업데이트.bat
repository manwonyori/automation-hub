@echo off
cls
echo ================================================
echo    카페24 가격 업데이트 자동화
echo ================================================
echo.
echo 상품: [인생]점보떡볶이1490g
echo 변경 가격: 13,500원
echo.
echo 이 프로그램은 다음 작업을 자동으로 수행합니다:
echo 1. 카페24 로그인
echo 2. 상품 검색
echo 3. 엑셀 다운로드
echo 4. 가격 수정
echo.
pause

cd /d "%~dp0"
python run_price_update.py

pause