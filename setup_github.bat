@echo off
cls
echo ================================================
echo    GitHub 저장소 연결 도구
echo ================================================
echo.
echo 이 도구는 AUTOMATION_HUB를 GitHub에 연결합니다.
echo.
echo 사전 준비사항:
echo 1. GitHub 계정이 있어야 합니다
echo 2. GitHub에서 'automation-hub' 저장소를 만드세요
echo    (비어있는 저장소로 생성)
echo.
pause

echo.
echo GitHub 사용자 정보 설정...
set /p username="GitHub 사용자명: "
set /p email="GitHub 이메일: "

git config user.name "%username%"
git config user.email "%email%"

echo.
echo 원격 저장소 연결...
echo.
echo GitHub 저장소 URL 형식:
echo https://github.com/사용자명/저장소명.git
echo 예: https://github.com/8899y/automation-hub.git
echo.
set /p repo_url="GitHub 저장소 URL 입력: "

git remote add origin %repo_url%

echo.
echo 브랜치 이름을 main으로 변경...
git branch -M main

echo.
echo GitHub에 푸시 중...
git push -u origin main

echo.
echo ================================================
echo    ✅ GitHub 연결 완료!
echo ================================================
echo.
echo 앞으로 변경사항을 저장하려면:
echo 1. git add .
echo 2. git commit -m "변경 내용 설명"
echo 3. git push
echo.
pause