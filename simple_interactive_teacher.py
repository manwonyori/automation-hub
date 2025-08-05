"""
간단한 대화형 학습 시스템
콘솔에서 실시간으로 요소를 가르치는 방식
"""

import os
import json
import time
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


class SimpleInteractiveTeacher:
    def __init__(self):
        self.driver = None
        self.knowledge = {}
        self.current_site = None
        self.learning_mode = False
        
    def setup_browser(self):
        """브라우저 설정"""
        print("\n브라우저를 시작합니다...")
        
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.maximize_window()
        
        print("[OK] 브라우저 시작 완료")
        
    def inject_click_detector(self):
        """클릭 감지 스크립트 주입"""
        script = """
        window.teacherMode = true;
        window.lastClicked = null;
        
        // 모든 클릭 이벤트 가로채기
        document.addEventListener('click', function(e) {
            if (window.teacherMode) {
                e.preventDefault();
                e.stopPropagation();
                
                // 요소 정보 저장
                window.lastClicked = {
                    tag: e.target.tagName,
                    id: e.target.id,
                    class: e.target.className,
                    name: e.target.name,
                    text: e.target.textContent.substring(0, 100),
                    type: e.target.type,
                    placeholder: e.target.placeholder
                };
                
                // 하이라이트
                e.target.style.border = '3px solid red';
                e.target.style.backgroundColor = 'yellow';
                
                console.log('요소 클릭됨:', window.lastClicked);
                
                return false;
            }
        }, true);
        
        console.log('학습 모드 활성화됨');
        """
        
        self.driver.execute_script(script)
        print("[OK] 학습 모드가 활성화되었습니다.")
        print("--> 이제 브라우저에서 학습할 요소를 클릭하세요!")
        
    def get_clicked_element(self):
        """클릭한 요소 정보 가져오기"""
        return self.driver.execute_script("return window.lastClicked;")
        
    def clear_clicked(self):
        """클릭 정보 초기화"""
        self.driver.execute_script("window.lastClicked = null;")
        
    def disable_learning_mode(self):
        """학습 모드 비활성화"""
        self.driver.execute_script("window.teacherMode = false;")
        print("[OK] 학습 모드가 비활성화되었습니다.")
        
    def find_element_smart(self, element_info):
        """여러 방법으로 요소 찾기 시도"""
        # ID로 시도
        if element_info.get('id'):
            try:
                return self.driver.find_element(By.ID, element_info['id'])
            except:
                pass
                
        # Name으로 시도
        if element_info.get('name'):
            try:
                return self.driver.find_element(By.NAME, element_info['name'])
            except:
                pass
                
        # Class로 시도
        if element_info.get('class'):
            try:
                classes = element_info['class'].split()[0]  # 첫 번째 클래스만
                return self.driver.find_element(By.CLASS_NAME, classes)
            except:
                pass
                
        # 텍스트로 시도
        if element_info.get('text'):
            try:
                return self.driver.find_element(By.XPATH, f"//*[contains(text(), '{element_info['text'][:20]}')]")
            except:
                pass
                
        return None
        
    def teach_element(self):
        """요소 학습"""
        print("\n" + "="*50)
        print("[학습] 요소 학습")
        print("="*50)
        
        # 학습 모드 활성화
        self.inject_click_detector()
        
        # 요소 이름 입력
        element_name = input("\n학습할 요소의 이름을 입력하세요 (예: 로그인버튼): ").strip()
        if not element_name:
            print("[X] 요소 이름이 필요합니다.")
            return
            
        print(f"\n--> 브라우저에서 '{element_name}'에 해당하는 요소를 클릭하세요...")
        print("(클릭한 요소는 노란색으로 표시됩니다)")
        
        # 클릭 대기
        for i in range(10):
            time.sleep(1)
            clicked = self.get_clicked_element()
            if clicked:
                break
            print(f"대기 중... {10-i}초")
        else:
            print("[X] 시간 초과. 요소를 클릭하지 않았습니다.")
            return
            
        print(f"\n[OK] 요소를 찾았습니다!")
        print(f"태그: {clicked['tag']}")
        print(f"ID: {clicked.get('id', 'N/A')}")
        print(f"Class: {clicked.get('class', 'N/A')}")
        print(f"텍스트: {clicked.get('text', 'N/A')[:50]}...")
        
        # 요소 타입 선택
        print("\n요소 타입을 선택하세요:")
        print("1. 버튼/링크 (클릭)")
        print("2. 입력 필드 (텍스트 입력)")
        print("3. 드롭다운 (선택)")
        print("4. 체크박스")
        
        element_type = input("선택 (1-4): ").strip()
        
        # 지식 저장
        if 'elements' not in self.knowledge:
            self.knowledge['elements'] = {}
            
        self.knowledge['elements'][element_name] = {
            'info': clicked,
            'type': element_type,
            'learned_at': datetime.now().isoformat()
        }
        
        print(f"\n[OK] '{element_name}' 학습 완료!")
        
        # 클릭 정보 초기화
        self.clear_clicked()
        
        # 추가 학습 여부
        more = input("\n다른 요소도 학습하시겠습니까? (y/n): ").strip().lower()
        if more == 'y':
            self.teach_element()
        else:
            self.disable_learning_mode()
            
    def test_element(self, element_name):
        """학습한 요소 테스트"""
        if element_name not in self.knowledge.get('elements', {}):
            print(f"[X] '{element_name}'는 학습되지 않았습니다.")
            return None
            
        element_info = self.knowledge['elements'][element_name]['info']
        element = self.find_element_smart(element_info)
        
        if element:
            # 하이라이트
            self.driver.execute_script("""
                arguments[0].style.border = '3px solid green';
                arguments[0].style.backgroundColor = 'lightgreen';
            """, element)
            
            print(f"[OK] '{element_name}' 요소를 찾았습니다!")
            time.sleep(2)
            
            # 하이라이트 제거
            self.driver.execute_script("""
                arguments[0].style.border = '';
                arguments[0].style.backgroundColor = '';
            """, element)
            
            return element
        else:
            print(f"[X] '{element_name}' 요소를 찾을 수 없습니다.")
            return None
            
    def save_knowledge(self):
        """학습 내용 저장"""
        if not self.current_site:
            self.current_site = input("사이트 이름 (예: cafe24): ").strip()
            
        # 저장 경로
        knowledge_dir = f"KNOWLEDGE_BASE/{self.current_site}"
        os.makedirs(knowledge_dir, exist_ok=True)
        
        knowledge_file = os.path.join(knowledge_dir, "interactive_elements.json")
        with open(knowledge_file, 'w', encoding='utf-8') as f:
            json.dump(self.knowledge, f, ensure_ascii=False, indent=2)
            
        print(f"\n[OK] 학습 내용 저장 완료: {knowledge_file}")
        
    def load_knowledge(self, site_name):
        """기존 지식 로드"""
        knowledge_file = f"KNOWLEDGE_BASE/{site_name}/interactive_elements.json"
        
        if os.path.exists(knowledge_file):
            with open(knowledge_file, 'r', encoding='utf-8') as f:
                self.knowledge = json.load(f)
            print(f"[OK] 기존 지식 로드: {len(self.knowledge.get('elements', {}))}개 요소")
        else:
            print("새로운 사이트입니다. 학습을 시작하세요.")
            
    def interactive_menu(self):
        """대화형 메뉴"""
        while True:
            print("\n" + "="*50)
            print("[학습 시스템] 대화형 학습 시스템")
            print("="*50)
            print("1. 웹사이트 열기")
            print("2. 요소 학습하기")
            print("3. 학습한 요소 테스트")
            print("4. 학습 내용 저장")
            print("5. 자동화 실행")
            print("6. 학습한 요소 목록")
            print("0. 종료")
            
            choice = input("\n선택: ").strip()
            
            if choice == "1":
                url = input("URL 입력: ").strip()
                self.driver.get(url)
                print("[OK] 페이지 로드 완료")
                
                # 알림창 처리
                try:
                    alert = WebDriverWait(self.driver, 2).until(EC.alert_is_present())
                    alert.accept()
                    print("[OK] 알림창 처리")
                except:
                    pass
                    
            elif choice == "2":
                self.teach_element()
                
            elif choice == "3":
                element_name = input("테스트할 요소 이름: ").strip()
                self.test_element(element_name)
                
            elif choice == "4":
                self.save_knowledge()
                
            elif choice == "5":
                self.run_automation()
                
            elif choice == "6":
                self.list_elements()
                
            elif choice == "0":
                break
                
    def list_elements(self):
        """학습한 요소 목록"""
        elements = self.knowledge.get('elements', {})
        
        if not elements:
            print("\n학습한 요소가 없습니다.")
            return
            
        print(f"\n[목록] 학습한 요소 ({len(elements)}개):")
        for name, data in elements.items():
            info = data['info']
            print(f"\n- {name}")
            print(f"  태그: {info['tag']}")
            print(f"  ID: {info.get('id', 'N/A')}")
            print(f"  타입: {data['type']}")
            
    def run_automation(self):
        """간단한 자동화 실행"""
        print("\n[자동화] 자동화 실행")
        
        # 카페24 로그인 예시
        if "아이디입력란" in self.knowledge.get('elements', {}):
            print("\n카페24 로그인을 시도합니다...")
            
            # 아이디 입력
            id_element = self.test_element("아이디입력란")
            if id_element:
                id_element.clear()
                id_element.send_keys("manwonyori")
                
            # 비밀번호 입력
            pwd_element = self.test_element("비밀번호입력란")
            if pwd_element:
                pwd_element.clear()
                pwd_element.send_keys("happy8263!")
                
            # 로그인 버튼 클릭
            login_element = self.test_element("로그인버튼")
            if login_element:
                login_element.click()
                print("[OK] 로그인 완료!")
        else:
            print("먼저 요소들을 학습하세요.")
            
    def run(self):
        """메인 실행"""
        print("\n간단한 대화형 학습 시스템")
        print("화면을 보면서 요소를 클릭하여 학습합니다.")
        
        # 브라우저 시작
        self.setup_browser()
        
        # 기존 지식 로드 여부
        load = input("\n기존 학습 데이터를 로드하시겠습니까? (y/n): ").strip().lower()
        if load == 'y':
            site = input("사이트 이름 (예: cafe24): ").strip()
            self.current_site = site
            self.load_knowledge(site)
            
        try:
            # 대화형 메뉴 실행
            self.interactive_menu()
            
        except Exception as e:
            print(f"\n[X] 오류 발생: {e}")
            
        finally:
            if self.driver:
                self.driver.quit()
            print("\n프로그램을 종료합니다.")


def main():
    teacher = SimpleInteractiveTeacher()
    teacher.run()


if __name__ == "__main__":
    main()