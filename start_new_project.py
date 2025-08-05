"""
새 프로젝트 시작 도구
기존 학습 내용을 활용하여 빠르게 시작
"""

import os
import json
import shutil
from datetime import datetime
from SHARED.core.pattern_manager import PatternManager


def create_new_project(project_name: str, similar_to: str = None):
    """새 프로젝트 생성"""
    print(f"\n=== {project_name} 프로젝트 생성 ===")
    
    # 1. 프로젝트 폴더 생성
    project_dir = f"{project_name.upper()}"
    if project_name.lower() == "naver":
        project_dir = "02_NAVER"
    elif project_name.lower() == "coupang":
        project_dir = "03_COUPANG"
    
    os.makedirs(project_dir, exist_ok=True)
    os.makedirs(f"{project_dir}/knowledge", exist_ok=True)
    os.makedirs(f"{project_dir}/logs", exist_ok=True)
    
    print(f"[OK] 프로젝트 폴더 생성: {project_dir}")
    
    # 2. 유사 프로젝트에서 패턴 복사
    if similar_to:
        pm = PatternManager()
        similar_patterns = pm.extract_pattern_from_site(similar_to)
        
        if similar_patterns:
            # 패턴 저장
            pattern_file = f"{project_dir}/knowledge/transferred_patterns.json"
            with open(pattern_file, 'w', encoding='utf-8') as f:
                json.dump(similar_patterns, f, ensure_ascii=False, indent=2)
            
            print(f"[OK] {similar_to}의 패턴을 복사했습니다")
            
            # 분석 결과
            print("\n전이된 패턴:")
            for pattern_type, pattern_data in similar_patterns.items():
                if pattern_data:
                    print(f"  - {pattern_type}: {len(pattern_data)} 요소")
    
    # 3. 기본 자동화 스크립트 생성
    automation_script = f"""'''
{project_name} 자동화 스크립트
생성일: {datetime.now().strftime('%Y-%m-%d')}
기반: {similar_to or '새로 시작'}
'''

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from SHARED.core.browser_manager import BrowserManager
from SHARED.core.workflow_engine import WorkflowEngine
from SHARED.core.pattern_manager import PatternManager


class {project_name.capitalize()}Automation:
    def __init__(self):
        self.browser_manager = BrowserManager()
        self.workflow_engine = WorkflowEngine()
        self.pattern_manager = PatternManager()
        self.driver = None
        
    def setup(self):
        '''브라우저 설정'''
        self.driver = self.browser_manager.setup_driver()
        
    def login(self):
        '''로그인 프로세스'''
        # 전이된 패턴 로드
        transferred = self.load_transferred_patterns()
        
        if transferred and 'login' in transferred:
            print("전이된 로그인 패턴 사용")
            # 패턴 적용
        else:
            print("새로운 로그인 방식 학습 필요")
            
    def load_transferred_patterns(self):
        '''전이된 패턴 로드'''
        pattern_file = "knowledge/transferred_patterns.json"
        if os.path.exists(pattern_file):
            with open(pattern_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
        
    def run(self):
        '''메인 실행'''
        self.setup()
        
        try:
            # 여기에 자동화 로직 추가
            print("{project_name} 자동화 시작")
            
        except Exception as e:
            print(f"오류 발생: {{e}}")
            
        finally:
            if self.driver:
                self.driver.quit()


if __name__ == "__main__":
    automation = {project_name.capitalize()}Automation()
    automation.run()
"""
    
    script_file = f"{project_dir}/{project_name}_automation.py"
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(automation_script)
    
    print(f"[OK] 자동화 스크립트 생성: {script_file}")
    
    # 4. 학습 가이드 생성
    guide_content = f"""# {project_name} 학습 가이드

## 1. 전이된 패턴 확인
- {similar_to}에서 전이된 패턴이 있습니다
- `knowledge/transferred_patterns.json` 확인

## 2. 패턴 검증
```python
python validate_patterns.py --site {project_name}
```

## 3. 추가 학습 필요 항목
- [ ] 사이트별 특수 요소
- [ ] 다른 UI 구조
- [ ] 추가 기능

## 4. 실행
```python
python {project_name}_automation.py
```
"""
    
    with open(f"{project_dir}/LEARNING_GUIDE.md", 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print(f"[OK] 학습 가이드 생성")
    
    print(f"\n=== {project_name} 프로젝트 생성 완료! ===")
    print(f"다음 단계:")
    print(f"1. cd {project_dir}")
    print(f"2. 패턴 검증 실행")
    print(f"3. 추가 학습 진행")


def main():
    print("새 자동화 프로젝트 생성")
    print("-" * 30)
    
    project_name = input("프로젝트 이름 (예: naver): ").strip().lower()
    
    # 기존 프로젝트 목록
    existing_projects = []
    for folder in os.listdir("."):
        if os.path.isdir(folder) and folder.startswith("0"):
            existing_projects.append(folder)
    
    if existing_projects:
        print("\n기존 프로젝트:")
        for i, proj in enumerate(existing_projects, 1):
            print(f"{i}. {proj}")
        
        similar = input("\n유사한 프로젝트 번호 (없으면 Enter): ").strip()
        if similar.isdigit() and 1 <= int(similar) <= len(existing_projects):
            similar_to = existing_projects[int(similar)-1].split("_")[1].lower()
        else:
            similar_to = None
    else:
        similar_to = None
    
    create_new_project(project_name, similar_to)


if __name__ == "__main__":
    main()