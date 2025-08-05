@echo off
echo ========================================
echo   카페24 프로젝트 마이그레이션 도구
echo ========================================
echo.
echo 기존 카페24 프로젝트를 통합 허브로 이동합니다.
echo.
set /p confirm="계속하시겠습니까? (Y/N): "

if /i "%confirm%"=="Y" (
    echo.
    echo 파일 복사 중...
    
    REM 카페24 selenium-method 폴더의 파일들 복사
    xcopy /Y "C:\Users\8899y\Documents\cafe24\selenium-method\*.py" "C:\Users\8899y\Documents\AUTOMATION_HUB\01_CAFE24\" >nul 2>&1
    
    REM 지식 파일 복사
    xcopy /Y "C:\Users\8899y\Documents\cafe24\selenium-method\*.json" "C:\Users\8899y\Documents\AUTOMATION_HUB\01_CAFE24\knowledge\" >nul 2>&1
    
    REM universal_web_learner.py를 메인으로
    copy /Y "C:\Users\8899y\Documents\cafe24\selenium-method\universal_web_learner.py" "C:\Users\8899y\Documents\AUTOMATION_HUB\universal_automation_teacher.py" >nul 2>&1
    
    echo.
    echo ✅ 마이그레이션 완료!
    echo.
    echo 이동된 파일:
    echo - 카페24 자동화 스크립트들 → 01_CAFE24 폴더
    echo - 학습된 지식 → 01_CAFE24\knowledge 폴더
    echo - 범용 학습 시스템 → 메인 폴더
    echo.
) else (
    echo.
    echo 마이그레이션이 취소되었습니다.
)

pause