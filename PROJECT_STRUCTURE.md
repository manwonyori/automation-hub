# 🎯 통합 자동화 허브 (AUTOMATION_HUB)
> 모든 자동화 프로젝트를 한 곳에서 관리

## 📁 통합 폴더 구조
```
C:\Users\8899y\Documents\AUTOMATION_HUB\
│
├── 📄 README.md                          # 전체 프로젝트 가이드
├── 📄 universal_automation_teacher.py    # 🌟 메인 범용 학습 시스템
├── 📄 requirements.txt                   # 공통 의존성
├── 📄 config.yaml                        # 전역 설정
│
├── 📁 01_CAFE24\                         # 카페24 전용
│   ├── 📄 cafe24_automation.py           # 카페24 자동화 스크립트
│   ├── 📄 price_update_workflow.py       # 가격 업데이트 워크플로우
│   ├── 📁 knowledge\                     # 학습된 지식
│   │   ├── elements.json
│   │   └── workflows.json
│   └── 📁 logs\                          # 실행 로그
│
├── 📁 02_NAVER\                          # 네이버 전용
│   ├── 📄 naver_automation.py
│   ├── 📁 knowledge\
│   └── 📁 logs\
│
├── 📁 03_COUPANG\                        # 쿠팡 전용
│   ├── 📄 coupang_automation.py
│   ├── 📁 knowledge\
│   └── 📁 logs\
│
├── 📁 SHARED\                            # 🔄 공통 모듈
│   ├── 📁 core\                          # 핵심 엔진
│   │   ├── browser_manager.py
│   │   ├── element_learner.py
│   │   ├── workflow_engine.py
│   │   └── code_generator.py
│   ├── 📁 plugins\                       # 플러그인
│   │   ├── scheduler.py
│   │   ├── api_server.py
│   │   └── notification.py
│   └── 📁 templates\                     # 템플릿
│       ├── site_template.py
│       └── workflow_template.json
│
├── 📁 KNOWLEDGE_BASE\                    # 🧠 통합 지식 저장소
│   ├── cafe24_knowledge.json
│   ├── naver_knowledge.json
│   └── universal_patterns.json          # 공통 패턴
│
├── 📁 GENERATED_SCRIPTS\                 # 🤖 자동 생성 스크립트
│   ├── daily_cafe24_update.py
│   ├── naver_blog_poster.py
│   └── multi_site_sync.py
│
├── 📁 WORKFLOWS\                         # 📋 워크플로우 저장소
│   ├── login_workflows.json
│   ├── data_extraction_workflows.json
│   └── form_submission_workflows.json
│
└── 📁 TOOLS\                             # 🛠️ 유틸리티
    ├── quick_start.bat                   # 빠른 시작
    ├── backup_knowledge.py               # 지식 백업
    └── migrate_old_scripts.py            # 기존 스크립트 이전
```

## 🚀 빠른 실행 명령어

### 1. 범용 학습 시스템 실행
```bash
cd C:\Users\8899y\Documents\AUTOMATION_HUB
python universal_automation_teacher.py
```

### 2. 카페24 자동화 실행
```bash
cd C:\Users\8899y\Documents\AUTOMATION_HUB\01_CAFE24
python cafe24_automation.py
```

### 3. 멀티 사이트 동기화
```bash
cd C:\Users\8899y\Documents\AUTOMATION_HUB
python GENERATED_SCRIPTS\multi_site_sync.py
```

## 💡 핵심 장점

1. **중앙 집중식 관리** - 모든 자동화를 한 곳에서
2. **코드 재사용** - SHARED 폴더의 공통 모듈 활용
3. **지식 공유** - KNOWLEDGE_BASE에서 패턴 학습
4. **쉬운 확장** - 새 사이트는 폴더만 추가
5. **통합 실행** - 여러 사이트 동시 자동화

## 🔄 기존 프로젝트 통합 방법

```bash
# 1. 카페24 프로젝트 이동
xcopy /E /I "C:\Users\8899y\Documents\cafe24" "C:\Users\8899y\Documents\AUTOMATION_HUB\01_CAFE24"

# 2. 웹 자동화 플랫폼 통합
xcopy /E /I "C:\Users\8899y\web_automation_platform" "C:\Users\8899y\Documents\AUTOMATION_HUB\SHARED"

# 3. 통합 완료 후 기존 폴더 정리 (선택사항)
```

## 📝 다음 단계

1. AUTOMATION_HUB 폴더 생성
2. 기존 프로젝트들 통합
3. universal_automation_teacher.py를 메인으로 설정
4. 각 사이트별 폴더에 특화 스크립트 배치

---
생성일: 2025-08-05
제작: 8899y & Claude