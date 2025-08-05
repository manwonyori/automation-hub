@echo off
cls
echo ================================================
echo    일일 커밋 도구
echo ================================================
echo.
echo 오늘의 작업 내용을 GitHub에 저장합니다.
echo.

REM 현재 상태 확인
git status

echo.
echo ------------------------------------------------
set /p message="커밋 메시지를 입력하세요: "

REM 모든 변경사항 추가
git add .

REM 커밋
git commit -m "%message%

Co-Authored-By: Claude <noreply@anthropic.com>"

REM 푸시
echo.
echo GitHub에 푸시 중...
git push

echo.
echo ✅ 커밋 완료!
echo.
echo 커밋 내역:
git log --oneline -5

pause