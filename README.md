# 🎯 AUTOMATION HUB - 통합 자동화 시스템

> 모든 웹 자동화를 한 곳에서 관리하는 중앙 허브

## 🚀 빠른 시작

### 더블클릭으로 시작하기:
```
quick_start.bat 실행
```

### 명령어로 시작하기:
```bash
cd C:\Users\8899y\Documents\AUTOMATION_HUB
python universal_automation_teacher.py
```

## 📁 폴더 구조

- **01_CAFE24**: 카페24 쇼핑몰 자동화
- **02_NAVER**: 네이버 관련 자동화
- **03_COUPANG**: 쿠팡 관련 자동화
- **SHARED**: 모든 사이트에서 공유하는 공통 모듈
- **KNOWLEDGE_BASE**: 학습된 지식 통합 저장소
- **GENERATED_SCRIPTS**: 자동 생성된 스크립트
- **WORKFLOWS**: 작업 순서 템플릿
- **TOOLS**: 유틸리티 도구

## 💡 주요 기능

### 1. 범용 학습 시스템
- 어떤 웹사이트든 학습 가능
- 대화형 인터페이스
- 학습 내용 자동 저장

### 2. 사이트별 자동화
- 카페24: 상품 가격 업데이트, 재고 관리
- 네이버: 블로그 포스팅, 스마트스토어 관리
- 쿠팡: 주문 확인, 상품 등록

### 3. 통합 실행
- 여러 사이트 동시 자동화
- 스케줄링 지원
- 실행 로그 관리

## 🔧 설정

### 의존성 설치:
```bash
pip install -r requirements.txt
```

### 환경 설정:
`config.yaml` 파일에서 기본 설정 변경 가능

## 📝 사용 예시

### 새로운 사이트 학습:
```python
# 1. universal_automation_teacher.py 실행
# 2. "새로운 사이트" 선택
# 3. 사이트 이름과 URL 입력
# 4. 요소를 하나씩 학습
```

### 기존 자동화 실행:
```python
# quick_start.bat 실행 후 원하는 사이트 선택
```

## 🛠️ 문제 해결

- **ChromeDriver 오류**: webdriver-manager가 자동으로 업데이트
- **요소를 찾을 수 없음**: 다른 선택자 방법 시도
- **로그인 실패**: credentials.json 확인

## 📞 지원

문제가 있으면 logs 폴더의 로그 파일을 확인하세요.

---

Made with ❤️ by 8899y & Claude
Last Updated: 2025-08-05