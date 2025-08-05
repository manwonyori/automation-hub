@echo off
cls
echo ================================================
echo    🎓 대화형 웹 자동화 학습 시스템
echo ================================================
echo.
echo 이 프로그램은 웹사이트의 요소를 직접 클릭하여
echo 학습시킬 수 있는 대화형 시스템입니다.
echo.
echo 선택하세요:
echo.
echo 1. 간단한 콘솔 버전 (권장)
echo 2. GUI 버전 (고급)
echo 0. 취소
echo.

set /p choice="선택 (0-2): "

if "%choice%"=="1" (
    echo.
    echo 간단한 대화형 학습을 시작합니다...
    echo.
    python simple_interactive_teacher.py
) else if "%choice%"=="2" (
    echo.
    echo GUI 학습 도구를 시작합니다...
    echo.
    python interactive_teacher.py
) else if "%choice%"=="0" (
    echo.
    echo 취소되었습니다.
    exit
)

pause