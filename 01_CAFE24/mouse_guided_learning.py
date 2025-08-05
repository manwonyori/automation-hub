"""
카페24 마우스 가이드 학습 모드
사용자가 마우스로 클릭 위치를 지정하면서 학습
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
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

class MouseGuidedLearning:
    def __init__(self):
        self.driver = None
        self.learned_elements = {}
        self.learning_file = "cafe24_learned_elements.json"
        self.load_learned_elements()
    
    def load_learned_elements(self):
        """이전에 학습한 요소들 로드"""
        if os.path.exists(self.learning_file):
            with open(self.learning_file, 'r', encoding='utf-8') as f:
                self.learned_elements = json.load(f)
    
    def save_learned_elements(self):
        """학습한 요소들 저장"""
        with open(self.learning_file, 'w', encoding='utf-8') as f:
            json.dump(self.learned_elements, f, ensure_ascii=False, indent=2)
    
    def setup_driver(self):
        """브라우저 설정"""
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.maximize_window()
        
        # JavaScript로 클릭 이벤트 리스너 추가
        self.driver.execute_script("""
            window.lastClickedElement = null;
            document.addEventListener('click', function(e) {
                window.lastClickedElement = e.target;
                e.target.style.border = '3px solid blue';
                console.log('Clicked:', e.target);
            }, true);
        """)
    
    def get_element_info(self, element):
        """요소의 정보 추출"""
        info = {
            'tag': element.tag_name,
            'text': element.text[:50] if element.text else '',
            'id': element.get_attribute('id'),
            'class': element.get_attribute('class'),
            'name': element.get_attribute('name'),
            'href': element.get_attribute('href'),
            'type': element.get_attribute('type'),
            'value': element.get_attribute('value'),
        }
        
        # XPath 생성
        xpath_options = []
        
        if info['id']:
            xpath_options.append(f"//{info['tag']}[@id='{info['id']}']")
        
        if info['name']:
            xpath_options.append(f"//{info['tag']}[@name='{info['name']}']")
        
        if info['text']:
            xpath_options.append(f"//{info['tag']}[contains(text(), '{info['text'][:20]}')]")
        
        if info['class']:
            classes = info['class'].split()[0]  # 첫 번째 클래스만
            xpath_options.append(f"//{info['tag']}[contains(@class, '{classes}')]")
        
        info['xpath_options'] = xpath_options
        return info
    
    def wait_for_user_click(self, prompt):
        """사용자의 클릭 대기"""
        print(f"\n{prompt}")
        print("클릭한 후 Enter를 눌러주세요...")
        
        # 콘솔에서 대기 (실제로는 브라우저에서 클릭)
        input()
        
        # 마지막으로 클릭한 요소 가져오기
        clicked_element = self.driver.execute_script("return window.lastClickedElement;")
        
        if clicked_element:
            # Selenium WebElement로 변환
            element_id = self.driver.execute_script("return arguments[0].id || Math.random().toString(36);", clicked_element)
            self.driver.execute_script("arguments[0].id = arguments[1];", clicked_element, element_id)
            element = self.driver.find_element(By.ID, element_id)
            
            info = self.get_element_info(element)
            print(f"클릭한 요소: {info['tag']} - {info['text']}")
            print(f"가능한 XPath: {info['xpath_options']}")
            
            return element, info
        
        return None, None
    
    def login(self):
        """로그인 프로세스"""
        print("=== 로그인 ===")
        self.driver.get("https://manwonyori.cafe24.com/admin")
        
        # 알림창 처리
        try:
            alert = WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            alert.accept()
        except:
            pass
        
        # 자동 로그인
        try:
            id_field = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='text']"))
            )
            id_field.send_keys("manwonyori")
            
            password_field = self.driver.find_element(By.XPATH, "//input[@type='password']")
            password_field.send_keys("happy8263!")
            password_field.send_keys(Keys.RETURN)
            
            WebDriverWait(self.driver, 10).until(
                lambda d: "admin" in d.current_url and "login" not in d.current_url
            )
            print("로그인 완료")
            return True
        except:
            print("자동 로그인 실패")
            return False
    
    def learn_search_process(self):
        """검색 프로세스 학습"""
        print("\n=== 검색 프로세스 학습 ===")
        
        # 상품관리 페이지로 이동
        self.driver.get("https://manwonyori.cafe24.com/disp/admin/shop1/product/productmanage")
        time.sleep(3)
        
        # 팝업 닫기
        for i in range(3):
            try:
                close_btn = self.driver.find_element(By.XPATH, "//button[contains(@class, 'close')] | //span[text()='×']")
                close_btn.click()
                time.sleep(0.3)
            except:
                break
        
        # 1. 검색분류 드롭다운
        element, info = self.wait_for_user_click("1. 검색분류 드롭다운을 클릭해주세요")
        if element:
            self.learned_elements['search_type_dropdown'] = info
            
            # 상품명 옵션 선택
            element, info = self.wait_for_user_click("2. '상품명' 옵션을 클릭해주세요")
            if element:
                self.learned_elements['product_name_option'] = info
        
        # 2. 검색어 입력 필드
        element, info = self.wait_for_user_click("3. 검색어 입력란을 클릭해주세요")
        if element:
            self.learned_elements['search_input'] = info
            element.clear()
            element.send_keys("[인생]점보떡볶이1490g")
            print("검색어 입력 완료")
        
        # 3. 검색 버튼
        element, info = self.wait_for_user_click("4. 검색 버튼을 클릭해주세요")
        if element:
            self.learned_elements['search_button'] = info
            # 실제 클릭은 이미 사용자가 함
            time.sleep(3)
        
        # 4. 체크박스
        element, info = self.wait_for_user_click("5. 상품의 체크박스를 클릭해주세요")
        if element:
            self.learned_elements['product_checkbox'] = info
        
        # 5. 엑셀다운로드 버튼
        element, info = self.wait_for_user_click("6. 엑셀다운로드 버튼을 클릭해주세요")
        if element:
            self.learned_elements['excel_download_button'] = info
            time.sleep(2)
        
        # 새 창 처리
        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            print("새 창으로 전환")
            
            # 6. 엑셀파일요청 버튼
            element, info = self.wait_for_user_click("7. 엑셀파일요청 버튼을 클릭해주세요")
            if element:
                self.learned_elements['excel_request_button'] = info
                
                # 알림창 처리
                try:
                    alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
                    alert.accept()
                except:
                    pass
                
                time.sleep(3)
            
            # 7. 다운로드 링크
            element, info = self.wait_for_user_click("8. 다운로드 링크를 클릭해주세요")
            if element:
                self.learned_elements['download_link'] = info
        
        # 학습 내용 저장
        self.save_learned_elements()
        print("\n=== 학습 완료! ===")
        print(f"학습한 요소들이 {self.learning_file}에 저장되었습니다.")
    
    def run_automated(self):
        """학습한 내용으로 자동 실행"""
        print("\n=== 자동 실행 모드 ===")
        
        if not self.learned_elements:
            print("학습된 요소가 없습니다. 먼저 학습 모드를 실행하세요.")
            return
        
        # 로그인
        if not self.login():
            return
        
        # 상품관리 페이지
        self.driver.get("https://manwonyori.cafe24.com/disp/admin/shop1/product/productmanage")
        time.sleep(3)
        
        # 학습한 요소들로 자동화
        try:
            # 검색분류 선택
            if 'search_type_dropdown' in self.learned_elements:
                xpath = self.learned_elements['search_type_dropdown']['xpath_options'][0]
                element = self.driver.find_element(By.XPATH, xpath)
                element.click()
                print("검색분류 드롭다운 클릭")
                
                # 상품명 선택
                if 'product_name_option' in self.learned_elements:
                    xpath = self.learned_elements['product_name_option']['xpath_options'][0]
                    element = self.driver.find_element(By.XPATH, xpath)
                    element.click()
                    print("상품명 옵션 선택")
            
            # 검색어 입력
            if 'search_input' in self.learned_elements:
                xpath = self.learned_elements['search_input']['xpath_options'][0]
                element = self.driver.find_element(By.XPATH, xpath)
                element.clear()
                element.send_keys("[인생]점보떡볶이1490g")
                print("검색어 입력")
            
            # 검색 실행
            if 'search_button' in self.learned_elements:
                xpath = self.learned_elements['search_button']['xpath_options'][0]
                element = self.driver.find_element(By.XPATH, xpath)
                element.click()
                print("검색 실행")
                time.sleep(3)
            
            print("자동 실행 완료!")
            
        except Exception as e:
            print(f"자동 실행 중 오류: {e}")
    
    def run(self):
        """메인 실행"""
        self.setup_driver()
        
        try:
            print("=== 카페24 마우스 가이드 학습 ===")
            print("1. 학습 모드 - 클릭 위치를 학습합니다")
            print("2. 자동 실행 - 학습한 내용으로 자동 실행합니다")
            
            mode = input("\n모드 선택 (1 또는 2): ").strip()
            
            if mode == "1":
                self.login()
                self.learn_search_process()
            elif mode == "2":
                self.run_automated()
            else:
                print("잘못된 선택입니다.")
                
        except Exception as e:
            print(f"오류: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            input("\nEnter를 눌러 종료...")
            self.driver.quit()

if __name__ == "__main__":
    learner = MouseGuidedLearning()
    learner.run()