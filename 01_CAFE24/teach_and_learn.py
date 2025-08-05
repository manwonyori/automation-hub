"""
카페24 티칭 모드 - 사용자가 직접 가르치는 자동화
"""

import time
import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

class TeachAndLearn:
    def __init__(self):
        self.driver = None
        self.knowledge_base = {}
        self.knowledge_file = "cafe24_knowledge.json"
        self.load_knowledge()
    
    def load_knowledge(self):
        """이전에 학습한 지식 로드"""
        if os.path.exists(self.knowledge_file):
            with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                self.knowledge_base = json.load(f)
            print(f"기존 지식을 로드했습니다: {len(self.knowledge_base)}개 항목")
    
    def save_knowledge(self):
        """학습한 지식 저장"""
        with open(self.knowledge_file, 'w', encoding='utf-8') as f:
            json.dump(self.knowledge_base, f, ensure_ascii=False, indent=2)
        print(f"지식을 저장했습니다: {self.knowledge_file}")
    
    def setup_driver(self):
        """브라우저 설정"""
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.maximize_window()
        print("브라우저를 시작했습니다.")
    
    def show_page_info(self):
        """현재 페이지 정보 표시"""
        print(f"\n현재 URL: {self.driver.current_url}")
        print(f"페이지 제목: {self.driver.title}")
    
    def find_element_by_teaching(self, element_name, action="click"):
        """사용자가 가르친 방법으로 요소 찾기"""
        
        # 이미 학습한 경우
        if element_name in self.knowledge_base:
            print(f"\n'{element_name}'에 대해 이미 학습한 내용이 있습니다.")
            knowledge = self.knowledge_base[element_name]
            print(f"방법: {knowledge['method']}")
            print(f"값: {knowledge['value']}")
            
            use_existing = input("기존 지식을 사용하시겠습니까? (y/n): ").strip().lower()
            if use_existing == 'y':
                return self.apply_knowledge(element_name)
        
        # 새로 학습
        print(f"\n=== '{element_name}' 찾는 방법을 가르쳐주세요 ===")
        print("1. xpath - XPath로 찾기")
        print("2. id - ID로 찾기")
        print("3. name - name 속성으로 찾기")
        print("4. class - class명으로 찾기")
        print("5. text - 텍스트로 찾기")
        print("6. css - CSS 선택자로 찾기")
        
        method = input("방법 선택 (1-6): ").strip()
        
        method_map = {
            '1': 'xpath',
            '2': 'id',
            '3': 'name',
            '4': 'class',
            '5': 'text',
            '6': 'css'
        }
        
        if method not in method_map:
            print("잘못된 선택입니다.")
            return None
        
        method_type = method_map[method]
        
        # 값 입력받기
        if method_type == 'xpath':
            print("\n예시: //input[@name='keyword']")
            print("예시: //button[contains(text(), '검색')]")
            value = input("XPath 입력: ").strip()
        elif method_type == 'id':
            value = input("ID 값 입력: ").strip()
        elif method_type == 'name':
            value = input("name 속성값 입력: ").strip()
        elif method_type == 'class':
            value = input("class명 입력: ").strip()
        elif method_type == 'text':
            value = input("텍스트 입력: ").strip()
        elif method_type == 'css':
            print("\n예시: input[name='keyword']")
            print("예시: button.btn-primary")
            value = input("CSS 선택자 입력: ").strip()
        
        # 추가 정보
        wait_time = input("대기 시간 (초, 기본값 3): ").strip()
        wait_time = int(wait_time) if wait_time else 3
        
        # 지식 저장
        self.knowledge_base[element_name] = {
            'method': method_type,
            'value': value,
            'action': action,
            'wait_time': wait_time
        }
        
        # 바로 적용해보기
        element = self.apply_knowledge(element_name)
        if element:
            print("요소를 찾았습니다!")
            
            # 하이라이트
            self.driver.execute_script("""
                arguments[0].style.border = '3px solid red';
                arguments[0].style.backgroundColor = 'yellow';
            """, element)
            
            confirm = input("이 요소가 맞습니까? (y/n): ").strip().lower()
            if confirm == 'y':
                self.save_knowledge()
                return element
            else:
                # 잘못된 경우 삭제
                del self.knowledge_base[element_name]
                print("다시 시도해주세요.")
                return self.find_element_by_teaching(element_name, action)
        else:
            print("요소를 찾을 수 없습니다.")
            del self.knowledge_base[element_name]
            retry = input("다시 시도하시겠습니까? (y/n): ").strip().lower()
            if retry == 'y':
                return self.find_element_by_teaching(element_name, action)
            return None
    
    def apply_knowledge(self, element_name):
        """저장된 지식으로 요소 찾기"""
        if element_name not in self.knowledge_base:
            return None
        
        knowledge = self.knowledge_base[element_name]
        method = knowledge['method']
        value = knowledge['value']
        wait_time = knowledge.get('wait_time', 3)
        
        try:
            if method == 'xpath':
                element = WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located((By.XPATH, value))
                )
            elif method == 'id':
                element = WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located((By.ID, value))
                )
            elif method == 'name':
                element = WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located((By.NAME, value))
                )
            elif method == 'class':
                element = WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located((By.CLASS_NAME, value))
                )
            elif method == 'text':
                element = WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{value}')]"))
                )
            elif method == 'css':
                element = WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, value))
                )
            
            return element
        except Exception as e:
            print(f"요소를 찾을 수 없습니다: {e}")
            return None
    
    def teach_mode(self):
        """티칭 모드 - 사용자가 하나씩 가르침"""
        print("\n=== 티칭 모드 시작 ===")
        print("각 단계마다 요소를 찾는 방법을 알려주세요.")
        
        # 1. 로그인
        print("\n[1단계: 로그인]")
        self.driver.get("https://manwonyori.cafe24.com/admin")
        time.sleep(2)
        
        # 알림창 처리
        try:
            alert = WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            alert.accept()
            print("알림창을 처리했습니다.")
        except:
            pass
        
        self.show_page_info()
        
        # 아이디 입력
        id_field = self.find_element_by_teaching("아이디 입력란", "input")
        if id_field:
            id_field.clear()
            id_field.send_keys("manwonyori")
            print("아이디를 입력했습니다.")
        
        # 비밀번호 입력
        pwd_field = self.find_element_by_teaching("비밀번호 입력란", "input")
        if pwd_field:
            pwd_field.clear()
            pwd_field.send_keys("happy8263!")
            print("비밀번호를 입력했습니다.")
        
        # 로그인 버튼
        login_btn = self.find_element_by_teaching("로그인 버튼", "click")
        if login_btn:
            login_btn.click()
            time.sleep(5)
            print("로그인 버튼을 클릭했습니다.")
        
        # 2. 상품 관리 페이지
        print("\n[2단계: 상품 검색]")
        self.driver.get("https://manwonyori.cafe24.com/disp/admin/shop1/product/productmanage")
        time.sleep(3)
        self.show_page_info()
        
        # 팝업 닫기
        close_popups = input("팝업을 닫아야 합니까? (y/n): ").strip().lower()
        if close_popups == 'y':
            popup_close = self.find_element_by_teaching("팝업 닫기 버튼", "click")
            if popup_close:
                popup_close.click()
                print("팝업을 닫았습니다.")
        
        # 검색분류 드롭다운
        search_type = self.find_element_by_teaching("검색분류 드롭다운", "select")
        if search_type:
            # Select 처리
            select = Select(search_type)
            print("옵션 목록:")
            for i, option in enumerate(select.options):
                print(f"{i}: {option.text}")
            
            option_idx = input("상품명 옵션의 번호를 입력하세요: ").strip()
            if option_idx.isdigit():
                select.select_by_index(int(option_idx))
                print("상품명 옵션을 선택했습니다.")
        
        # 검색어 입력
        search_input = self.find_element_by_teaching("검색어 입력란", "input")
        if search_input:
            search_input.clear()
            search_input.send_keys("[인생]점보떡볶이1490g")
            print("검색어를 입력했습니다.")
        
        # 검색 버튼
        search_btn = self.find_element_by_teaching("검색 버튼", "click")
        if search_btn:
            search_btn.click()
            time.sleep(3)
            print("검색을 실행했습니다.")
        
        # 체크박스
        checkbox = self.find_element_by_teaching("상품 체크박스", "click")
        if checkbox:
            if not checkbox.is_selected():
                checkbox.click()
            print("체크박스를 선택했습니다.")
        
        # 엑셀다운로드
        excel_btn = self.find_element_by_teaching("엑셀다운로드 버튼", "click")
        if excel_btn:
            excel_btn.click()
            time.sleep(2)
            print("엑셀다운로드 버튼을 클릭했습니다.")
        
        print("\n=== 티칭 완료! ===")
        print(f"학습한 내용이 {self.knowledge_file}에 저장되었습니다.")
    
    def auto_mode(self):
        """자동 실행 모드"""
        print("\n=== 자동 실행 모드 ===")
        
        if not self.knowledge_base:
            print("학습된 내용이 없습니다. 먼저 티칭 모드를 실행하세요.")
            return
        
        try:
            # 로그인
            self.driver.get("https://manwonyori.cafe24.com/admin")
            time.sleep(2)
            
            # 알림창 처리
            try:
                alert = WebDriverWait(self.driver, 2).until(EC.alert_is_present())
                alert.accept()
            except:
                pass
            
            # 학습한 요소들로 자동화
            elements_to_process = [
                ("아이디 입력란", lambda e: (e.clear(), e.send_keys("manwonyori"))),
                ("비밀번호 입력란", lambda e: (e.clear(), e.send_keys("happy8263!"))),
                ("로그인 버튼", lambda e: e.click()),
            ]
            
            for element_name, action in elements_to_process:
                element = self.apply_knowledge(element_name)
                if element:
                    action(element)
                    print(f"{element_name} 처리 완료")
                    time.sleep(1)
            
            # 로그인 대기
            time.sleep(5)
            
            # 상품 관리 페이지
            self.driver.get("https://manwonyori.cafe24.com/disp/admin/shop1/product/productmanage")
            time.sleep(3)
            
            # 나머지 자동화...
            print("자동 실행을 계속합니다...")
            
        except Exception as e:
            print(f"자동 실행 중 오류: {e}")
    
    def run(self):
        """메인 실행"""
        self.setup_driver()
        
        try:
            while True:
                print("\n=== 카페24 티칭 & 자동화 시스템 ===")
                print("1. 티칭 모드 - 처음부터 하나씩 가르치기")
                print("2. 자동 실행 - 학습한 내용으로 자동 실행")
                print("3. 지식 확인 - 학습한 내용 보기")
                print("4. 종료")
                
                choice = input("\n선택 (1-4): ").strip()
                
                if choice == "1":
                    self.teach_mode()
                elif choice == "2":
                    self.auto_mode()
                elif choice == "3":
                    print("\n=== 학습한 지식 ===")
                    for name, info in self.knowledge_base.items():
                        print(f"\n{name}:")
                        print(f"  방법: {info['method']}")
                        print(f"  값: {info['value']}")
                elif choice == "4":
                    break
                else:
                    print("잘못된 선택입니다.")
                
        except Exception as e:
            print(f"오류: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            self.driver.quit()
            print("프로그램을 종료합니다.")

if __name__ == "__main__":
    system = TeachAndLearn()
    system.run()