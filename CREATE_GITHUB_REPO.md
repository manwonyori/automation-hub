# 🚀 GitHub 저장소 생성 가이드

## 1️⃣ GitHub에서 저장소 만들기

1. **GitHub 접속**: https://github.com/manwonyorl
2. **새 저장소 생성**:
   - 우측 상단 `+` 버튼 → `New repository` 클릭
   
3. **저장소 정보 입력**:
   ```
   Repository name: automation-hub
   Description: 통합 웹 자동화 플랫폼 - 카페24, 네이버, 쿠팡 자동화
   Public/Private: 선택
   
   ⚠️ 중요: 다음 옵션들은 체크하지 마세요!
   □ Add a README file (체크 X)
   □ Add .gitignore (체크 X)
   □ Choose a license (체크 X)
   ```

4. **Create repository** 클릭

## 2️⃣ 저장소 생성 후 업로드

저장소를 만든 후 아래 명령어를 실행하세요:

```bash
# PowerShell 또는 명령 프롬프트에서
cd C:\Users\8899y\Documents\AUTOMATION_HUB

# 이미 연결된 origin 제거 (있을 경우)
git remote remove origin

# 새로 연결
git remote add origin https://github.com/manwonyorl/automation-hub.git

# 푸시
git push -u origin main
```

## 3️⃣ 문제 해결

### 인증 오류가 발생하는 경우:

1. **Personal Access Token 생성**:
   - GitHub → Settings → Developer settings → Personal access tokens
   - Generate new token (classic)
   - 권한: repo 전체 체크
   - 토큰 복사 (한 번만 보여짐!)

2. **푸시할 때**:
   - Username: manwonyorl
   - Password: [복사한 토큰 붙여넣기]

### 다른 이름으로 만들었다면:

```bash
# 예: automation-platform으로 만든 경우
git remote add origin https://github.com/manwonyorl/automation-platform.git
git push -u origin main
```

## 4️⃣ 업로드 성공 확인

업로드가 완료되면:
- 🌐 https://github.com/manwonyorl/automation-hub 에서 확인
- 모든 파일이 표시되어야 함

---

💡 **팁**: Private 저장소로 만들면 본인만 볼 수 있습니다!