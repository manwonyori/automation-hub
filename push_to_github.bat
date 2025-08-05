@echo off
cls
echo ================================================
echo    GitHub 업로드 도구
echo ================================================
echo.
echo 저장소: https://github.com/manwonyorl/automation-hub
echo.
echo GitHub에서 저장소를 먼저 생성하셨나요?
echo (빈 저장소로 생성, README 추가 X)
echo.
set /p confirm="저장소를 생성했습니다 (Y/N): "

if /i "%confirm%"=="Y" (
    echo.
    echo GitHub에 업로드 중...
    
    git push -u origin main
    
    if %errorlevel% == 0 (
        echo.
        echo ================================================
        echo    ✅ 업로드 성공!
        echo ================================================
        echo.
        echo 저장소 주소: https://github.com/manwonyorl/automation-hub
        echo.
        echo 브라우저에서 확인하시려면:
        start https://github.com/manwonyorl/automation-hub
    ) else (
        echo.
        echo ❌ 업로드 실패!
        echo.
        echo 가능한 원인:
        echo 1. GitHub에 저장소가 없음
        echo 2. 저장소 이름이 다름
        echo 3. 인증 문제 (Personal Access Token 필요)
        echo.
        echo CREATE_GITHUB_REPO.md 파일을 참고하세요!
    )
) else (
    echo.
    echo GitHub에서 먼저 저장소를 생성하세요:
    echo.
    echo 1. https://github.com/new 접속
    echo 2. Repository name: automation-hub
    echo 3. 빈 저장소로 생성 (README 추가 X)
    echo.
    start https://github.com/new
)

echo.
pause