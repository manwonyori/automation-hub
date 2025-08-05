"""
범용 웹 자동화 학습 시스템
사용자가 가르친 내용을 학습하고 수정하며 발전하는 시스템
"""

import time
import os
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

class UniversalWebLearner:
    def __init__(self):
        self.driver = None
        self.knowledge_base = {}
        self.workflows = {}
        self.knowledge_file = "universal_web_knowledge.json"
        self.workflows_file = "web_workflows.json"
        self.learning_history = []
        self.load_all_knowledge()
    
    def load_all_knowledge(self):
        """모든 학습 데이터 로드"""
        # 요소 지식 로드
        if os.path.exists(self.knowledge_file):
            with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                self.knowledge_base = json.load(f)
            print(f"요소 지식 로드: {len(self.knowledge_base)}개")
        
        # 워크플로우 로드
        if os.path.exists(self.workflows_file):
            with open(self.workflows_file, 'r', encoding='utf-8') as f:
                self.workflows = json.load(f)
            print(f"워크플로우 로드: {len(self.workflows)}개")
    
    def save_all_knowledge(self):
        """모든 학습 데이터 저장"""
        with open(self.knowledge_file, 'w', encoding='utf-8') as f:
            json.dump(self.knowledge_base, f, ensure_ascii=False, indent=2)
        
        with open(self.workflows_file, 'w', encoding='utf-8') as f:
            json.dump(self.workflows, f, ensure_ascii=False, indent=2)
        
        print("모든 지식을 저장했습니다.")
    
    def setup_driver(self, headless=False):
        """브라우저 설정"""
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        if headless:
            options.add_argument("--headless")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.maximize_window()
        print("브라우저를 시작했습니다.")
    
    def create_element_key(self, url, element_name):
        """URL별로 요소를 구분하는 키 생성"""
        domain = url.split('/')[2] if '/' in url else url
        return f"{domain}:{element_name}"
    
    def teach_element(self, element_name, url=None, retry_count=0):
        """요소 학습 (수정 가능)"""
        if url is None:
            url = self.driver.current_url
        
        element_key = self.create_element_key(url, element_name)
        
        # 기존 지식 확인
        if element_key in self.knowledge_base and retry_count == 0:
            print(f"\n'{element_name}'에 대한 기존 지식:")
            existing = self.knowledge_base[element_key]
            print(f"  방법: {existing['method']}")
            print(f"  값: {existing['value']}")
            print(f"  성공률: {existing.get('success_rate', 100)}%")
            
            choice = input("1) 기존 사용  2) 수정  3) 새로 학습: ").strip()
            
            if choice == "1":
                element = self.find_element(element_key)
                if element:
                    return element
                else:
                    print("기존 방법이 실패했습니다. 수정이 필요합니다.")
                    return self.teach_element(element_name, url, retry_count + 1)
            elif choice == "2":
                # 기존 값을 보여주고 수정
                print(f"현재 값: {existing['value']}")
        
        # 학습 시작
        print(f"\n=== '{element_name}' 학습 ===")
        print("찾는 방법:")
        print("1) xpath    - 예: //input[@name='keyword']")
        print("2) id       - 예: search-input")
        print("3) name     - 예: keyword")
        print("4) class    - 예: search-box")
        print("5) text     - 예: 검색")
        print("6) css      - 예: input.search-box")
        print("7) contains - 부분 텍스트 포함")
        
        method = input("방법 선택: ").strip()
        
        method_map = {
            '1': 'xpath', '2': 'id', '3': 'name', '4': 'class',
            '5': 'text', '6': 'css', '7': 'contains'
        }
        
        if method not in method_map:
            print("잘못된 선택입니다.")
            return self.teach_element(element_name, url, retry_count + 1)
        
        method_type = method_map[method]
        
        # 값 입력
        value = input(f"{method_type} 값 입력: ").strip()
        
        # 요소 유형
        print("\n요소 유형:")
        print("1) 클릭 가능 (버튼, 링크)")
        print("2) 입력 가능 (텍스트 필드)")
        print("3) 선택 가능 (드롭다운)")
        print("4) 체크박스/라디오")
        element_type = input("유형 선택: ").strip()
        
        # 지식 저장
        self.knowledge_base[element_key] = {
            'method': method_type,
            'value': value,
            'element_type': element_type,
            'created': datetime.now().isoformat(),
            'success_count': 0,
            'fail_count': 0,
            'success_rate': 100
        }
        
        # 찾기 시도
        element = self.find_element(element_key)
        if element:
            # 하이라이트
            self.highlight_element(element)
            
            # 추가 정보 수집
            tag = element.tag_name
            text = element.text[:50] if element.text else ""
            
            self.knowledge_base[element_key].update({
                'tag': tag,
                'sample_text': text
            })
            
            confirm = input("이 요소가 맞습니까? (y/n): ").strip().lower()
            if confirm == 'y':
                self.knowledge_base[element_key]['success_count'] += 1
                self.save_all_knowledge()
                print("학습 완료!")
                return element
            else:
                del self.knowledge_base[element_key]
                return self.teach_element(element_name, url, retry_count + 1)
        else:
            print("요소를 찾을 수 없습니다.")
            del self.knowledge_base[element_key]
            if retry_count < 3:
                retry = input("다시 시도하시겠습니까? (y/n): ").strip().lower()
                if retry == 'y':
                    return self.teach_element(element_name, url, retry_count + 1)
            return None
    
    def find_element(self, element_key):
        """학습한 방법으로 요소 찾기"""
        if element_key not in self.knowledge_base:
            return None
        
        knowledge = self.knowledge_base[element_key]
        method = knowledge['method']
        value = knowledge['value']
        
        try:
            if method == 'xpath':
                element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, value))
                )
            elif method == 'id':
                element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.ID, value))
                )
            elif method == 'name':
                element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.NAME, value))
                )
            elif method == 'class':
                element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, value))
                )
            elif method == 'text':
                element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, f"//*[text()='{value}']"))
                )
            elif method == 'contains':
                element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{value}')]"))
                )
            elif method == 'css':
                element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, value))
                )
            
            # 성공 카운트 증가
            knowledge['success_count'] += 1
            self.update_success_rate(element_key)
            return element
            
        except Exception as e:
            # 실패 카운트 증가
            knowledge['fail_count'] += 1
            self.update_success_rate(element_key)
            print(f"요소 찾기 실패: {e}")
            return None
    
    def update_success_rate(self, element_key):
        """성공률 업데이트"""
        knowledge = self.knowledge_base[element_key]
        total = knowledge['success_count'] + knowledge['fail_count']
        if total > 0:
            knowledge['success_rate'] = round(knowledge['success_count'] / total * 100, 2)
    
    def highlight_element(self, element):
        """요소 하이라이트"""
        self.driver.execute_script("""
            arguments[0].style.border = '3px solid red';
            arguments[0].style.backgroundColor = 'yellow';
            setTimeout(function() {
                arguments[0].style.border = '';
                arguments[0].style.backgroundColor = '';
            }, 3000);
        """, element)
    
    def create_workflow(self, workflow_name):
        """워크플로우 생성"""
        print(f"\n=== 워크플로우 '{workflow_name}' 생성 ===")
        
        steps = []
        step_num = 1
        
        while True:
            print(f"\n[단계 {step_num}]")
            print("1) URL 이동")
            print("2) 요소 클릭")
            print("3) 텍스트 입력")
            print("4) 드롭다운 선택")
            print("5) 대기")
            print("6) 조건 확인")
            print("7) 완료")
            
            action = input("동작 선택: ").strip()
            
            if action == "7":
                break
            
            step = {'step': step_num, 'action': action}
            
            if action == "1":
                url = input("URL 입력: ").strip()
                step['url'] = url
            elif action in ["2", "3", "4"]:
                element_name = input("요소 이름: ").strip()
                element = self.teach_element(element_name)
                if element:
                    step['element'] = self.create_element_key(self.driver.current_url, element_name)
                    
                    if action == "3":
                        text = input("입력할 텍스트: ").strip()
                        step['text'] = text
                    elif action == "4":
                        print("드롭다운 옵션을 확인합니다...")
                        # 옵션 표시 로직
            elif action == "5":
                seconds = input("대기 시간(초): ").strip()
                step['seconds'] = int(seconds) if seconds.isdigit() else 3
            elif action == "6":
                condition = input("확인할 조건 (예: URL 포함 문자): ").strip()
                step['condition'] = condition
            
            steps.append(step)
            step_num += 1
        
        self.workflows[workflow_name] = {
            'steps': steps,
            'created': datetime.now().isoformat(),
            'run_count': 0,
            'success_count': 0
        }
        
        self.save_all_knowledge()
        print(f"워크플로우 '{workflow_name}' 생성 완료!")
    
    def run_workflow(self, workflow_name):
        """워크플로우 실행"""
        if workflow_name not in self.workflows:
            print(f"워크플로우 '{workflow_name}'을 찾을 수 없습니다.")
            return False
        
        workflow = self.workflows[workflow_name]
        workflow['run_count'] += 1
        
        print(f"\n=== 워크플로우 '{workflow_name}' 실행 ===")
        
        try:
            for step in workflow['steps']:
                print(f"\n[단계 {step['step']}] ", end="")
                
                if step['action'] == "1":  # URL 이동
                    print(f"URL 이동: {step['url']}")
                    self.driver.get(step['url'])
                    time.sleep(2)
                    
                elif step['action'] == "2":  # 클릭
                    element = self.find_element(step['element'])
                    if element:
                        print(f"클릭: {step['element'].split(':')[1]}")
                        element.click()
                    else:
                        print("요소를 찾을 수 없습니다. 재학습이 필요합니다.")
                        return False
                        
                elif step['action'] == "3":  # 텍스트 입력
                    element = self.find_element(step['element'])
                    if element:
                        print(f"텍스트 입력: {step['text']}")
                        element.clear()
                        element.send_keys(step['text'])
                    else:
                        print("요소를 찾을 수 없습니다.")
                        return False
                        
                elif step['action'] == "5":  # 대기
                    print(f"{step['seconds']}초 대기")
                    time.sleep(step['seconds'])
                
                time.sleep(1)  # 각 단계 후 잠시 대기
            
            workflow['success_count'] += 1
            self.save_all_knowledge()
            print("\n워크플로우 실행 완료!")
            return True
            
        except Exception as e:
            print(f"\n워크플로우 실행 중 오류: {e}")
            return False
    
    def show_statistics(self):
        """학습 통계 표시"""
        print("\n=== 학습 통계 ===")
        
        print(f"\n요소 지식: {len(self.knowledge_base)}개")
        for key, knowledge in self.knowledge_base.items():
            domain, element = key.split(':', 1)
            print(f"\n[{domain}] {element}")
            print(f"  방법: {knowledge['method']} = {knowledge['value']}")
            print(f"  성공률: {knowledge['success_rate']}% ({knowledge['success_count']}/{knowledge['success_count'] + knowledge['fail_count']})")
        
        print(f"\n워크플로우: {len(self.workflows)}개")
        for name, workflow in self.workflows.items():
            print(f"\n{name}")
            print(f"  단계 수: {len(workflow['steps'])}")
            print(f"  실행 횟수: {workflow['run_count']}")
            print(f"  성공률: {workflow['success_count']}/{workflow['run_count'] if workflow['run_count'] > 0 else 0}")
    
    def export_knowledge(self, filename):
        """지식 내보내기"""
        export_data = {
            'knowledge_base': self.knowledge_base,
            'workflows': self.workflows,
            'exported_at': datetime.now().isoformat()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        print(f"지식을 {filename}으로 내보냈습니다.")
    
    def import_knowledge(self, filename):
        """지식 가져오기"""
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 병합 또는 덮어쓰기 선택
            choice = input("1) 병합  2) 덮어쓰기: ").strip()
            
            if choice == "2":
                self.knowledge_base = data['knowledge_base']
                self.workflows = data['workflows']
            else:
                self.knowledge_base.update(data['knowledge_base'])
                self.workflows.update(data['workflows'])
            
            self.save_all_knowledge()
            print("지식을 가져왔습니다.")
    
    def main_menu(self):
        """메인 메뉴"""
        while True:
            print("\n=== 범용 웹 자동화 학습 시스템 ===")
            print("1. 새 워크플로우 생성")
            print("2. 워크플로우 실행")
            print("3. 요소 학습/수정")
            print("4. 통계 보기")
            print("5. 지식 내보내기/가져오기")
            print("6. 카페24 빠른 실행")
            print("0. 종료")
            
            choice = input("\n선택: ").strip()
            
            if choice == "1":
                name = input("워크플로우 이름: ").strip()
                self.create_workflow(name)
                
            elif choice == "2":
                print("\n저장된 워크플로우:")
                for i, name in enumerate(self.workflows.keys(), 1):
                    print(f"{i}. {name}")
                
                idx = input("번호 선택: ").strip()
                if idx.isdigit() and 1 <= int(idx) <= len(self.workflows):
                    workflow_name = list(self.workflows.keys())[int(idx)-1]
                    self.run_workflow(workflow_name)
                    
            elif choice == "3":
                url = input("URL (현재 페이지는 Enter): ").strip()
                if url:
                    self.driver.get(url)
                    time.sleep(2)
                
                element_name = input("요소 이름: ").strip()
                self.teach_element(element_name)
                
            elif choice == "4":
                self.show_statistics()
                
            elif choice == "5":
                sub_choice = input("1) 내보내기  2) 가져오기: ").strip()
                if sub_choice == "1":
                    filename = input("파일명 (기본: export.json): ").strip() or "export.json"
                    self.export_knowledge(filename)
                elif sub_choice == "2":
                    filename = input("파일명: ").strip()
                    self.import_knowledge(filename)
                    
            elif choice == "6":
                # 카페24 전용 빠른 실행
                if "카페24 가격수정" in self.workflows:
                    self.run_workflow("카페24 가격수정")
                else:
                    print("카페24 워크플로우가 없습니다. 먼저 생성하세요.")
                    
            elif choice == "0":
                break
            
            else:
                print("잘못된 선택입니다.")
    
    def run(self):
        """실행"""
        self.setup_driver()
        
        try:
            self.main_menu()
        except Exception as e:
            print(f"오류 발생: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.driver.quit()
            print("프로그램을 종료합니다.")

if __name__ == "__main__":
    learner = UniversalWebLearner()
    learner.run()