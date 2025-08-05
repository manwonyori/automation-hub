@echo off
cls
echo ========================================
echo    대화형 웹 자동화 학습 시스템
echo ========================================
echo.
echo 이 프로그램은 웹사이트를 보면서
echo 요소를 클릭하여 학습시킬 수 있습니다.
echo.
echo 주요 기능:
echo - 브라우저에서 요소 클릭하여 학습
echo - 학습한 내용 저장 및 재사용
echo - 즉시 자동화 실행
echo.
pause

cd /d "%~dp0"
python simple_interactive_teacher.py

pause