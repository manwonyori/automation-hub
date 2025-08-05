# 🔗 GitHub 설정 가이드

## 1️⃣ GitHub 저장소 생성

### 웹에서 생성:
1. https://github.com 로그인
2. 우측 상단 `+` → `New repository` 클릭
3. 저장소 정보 입력:
   - Repository name: `automation-hub`
   - Description: `통합 웹 자동화 플랫폼 - 모든 반복 작업을 자동화`
   - Public/Private 선택
   - ❌ "Initialize this repository with:" 체크 해제 (로컬에 이미 있으므로)

## 2️⃣ 로컬 저장소 연결

```bash
# AUTOMATION_HUB 폴더에서 실행
cd C:\Users\8899y\Documents\AUTOMATION_HUB

# Git 초기화 (이미 완료됨)
git init

# 사용자 정보 설정 (처음 한 번만)
git config user.name "8899y"
git config user.email "your-email@example.com"

# 파일 추가
git add .

# 첫 커밋
git commit -m "🚀 Initial commit: 통합 자동화 허브 구축

- 카페24, 네이버, 쿠팡 자동화 통합
- 범용 학습 시스템 구현
- 공통 모듈 구조화"

# GitHub 원격 저장소 연결
git remote add origin https://github.com/8899y/automation-hub.git

# 푸시
git push -u origin main
```

## 3️⃣ 자주 사용하는 Git 명령어

### 변경사항 확인:
```bash
git status
```

### 변경사항 저장:
```bash
git add .
git commit -m "✨ 새로운 기능: 네이버 자동화 추가"
git push
```

### 최신 버전 가져오기:
```bash
git pull
```

## 4️⃣ 커밋 메시지 규칙

- 🚀 `feat:` 새로운 기능
- 🐛 `fix:` 버그 수정
- 📝 `docs:` 문서 수정
- ✨ `style:` 코드 포맷팅
- ♻️ `refactor:` 코드 리팩토링
- 🧪 `test:` 테스트 추가
- 🔧 `chore:` 기타 변경사항

예시:
```bash
git commit -m "🚀 feat: 쿠팡 주문 확인 자동화 추가"
git commit -m "🐛 fix: 카페24 로그인 오류 수정"
git commit -m "📝 docs: README 사용법 업데이트"
```

## 5️⃣ 브랜치 전략

### 메인 브랜치:
- `main`: 안정된 버전
- `develop`: 개발 버전

### 기능 브랜치:
```bash
# 새 기능 개발
git checkout -b feature/naver-blog-automation

# 작업 후 병합
git checkout main
git merge feature/naver-blog-automation
```

## 6️⃣ 민감한 정보 보호

**.gitignore에 추가된 항목들:**
- credentials.json (로그인 정보)
- *.env (환경 변수)
- logs/ (로그 파일)
- 다운로드한 CSV/Excel 파일

⚠️ **절대 커밋하지 말아야 할 것들:**
- 비밀번호
- API 키
- 개인정보
- 실제 상품 데이터

## 7️⃣ 협업 시 주의사항

### Pull Request 사용:
1. Fork 후 작업
2. 기능 완성 후 PR 생성
3. 코드 리뷰
4. 병합

### 이슈 관리:
- 버그나 기능 요청은 Issues 탭 활용
- 라벨로 분류 (bug, enhancement, help wanted)

## 8️⃣ GitHub Actions (자동화)

`.github/workflows/test.yml` 예시:
```yaml
name: Test Automation Scripts

on: [push, pull_request]

jobs:
  test:
    runs-on: windows-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    - run: |
        pip install -r requirements.txt
        pytest tests/
```

## 9️⃣ README 배지 추가

```markdown
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Selenium](https://img.shields.io/badge/selenium-4.15.2-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
```

---

🎯 **목표**: 모든 자동화 코드를 GitHub에서 버전 관리하여 안전하게 보관하고 공유!

📅 작성일: 2025-08-05