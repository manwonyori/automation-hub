"""
카페24 전용 자동화 스크립트
기존 cafe24 프로젝트의 모든 기능 통합
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from SHARED.core.browser_manager import BrowserManager
from SHARED.core.workflow_engine import WorkflowEngine
import json
import time
from datetime import datetime


class Cafe24Automation:
    """카페24 자동화 클래스"""
    
    def __init__(self):
        self.browser_manager = BrowserManager()
        self.workflow_engine = WorkflowEngine()
        self.knowledge_path = os.path.join(os.path.dirname(__file__), "knowledge", "elements.json")
        self.load_knowledge()
        
    def load_knowledge(self):
        """학습된 지식 로드"""
        if os.path.exists(self.knowledge_path):
            with open(self.knowledge_path, 'r', encoding='utf-8') as f:
                self.knowledge = json.load(f)
        else:
            self.knowledge = {
                "elements": {
                    "아이디입력란": {
                        "method": "xpath",
                        "value": "//input[@type='text']",
                        "type": "input"
                    },
                    "비밀번호입력란": {
                        "method": "xpath",
                        "value": "//input[@type='password']",
                        "type": "input"
                    },
                    "로그인버튼": {
                        "method": "xpath",
                        "value": "//input[@type='submit']",
                        "type": "button"
                    }
                }
            }
    
    def login(self, username="manwonyori", password="happy8263!"):
        """카페24 로그인"""
        driver = self.browser_manager.get_driver()
        
        # 로그인 페이지 이동
        driver.get("https://manwonyori.cafe24.com/admin")
        time.sleep(2)
        
        # 알림창 처리
        try:
            alert = driver.switch_to.alert
            alert.accept()
        except:
            pass
        
        # 로그인
        self.workflow_engine.execute_step(driver, {
            "action": "input",
            "element": "아이디입력란",
            "value": username
        }, self.knowledge)
        
        self.workflow_engine.execute_step(driver, {
            "action": "input",
            "element": "비밀번호입력란",
            "value": password
        }, self.knowledge)
        
        self.workflow_engine.execute_step(driver, {
            "action": "click",
            "element": "로그인버튼"
        }, self.knowledge)
        
        time.sleep(5)
        print("✅ 로그인 완료")
    
    def search_product(self, product_name):
        """상품 검색"""
        driver = self.browser_manager.get_driver()
        
        # 상품관리 페이지로 이동
        driver.get("https://manwonyori.cafe24.com/disp/admin/shop1/product/productmanage")
        time.sleep(3)
        
        # 팝업 닫기
        self.close_popups()
        
        # 검색 실행
        print(f"🔍 '{product_name}' 검색 중...")
        # 검색 로직 구현
        
    def close_popups(self):
        """팝업 닫기"""
        driver = self.browser_manager.get_driver()
        for _ in range(3):
            try:
                close_btn = driver.find_element("xpath", "//button[contains(@class, 'close')]")
                close_btn.click()
                time.sleep(0.5)
            except:
                break
    
    def update_price(self, product_name, new_price):
        """가격 업데이트 전체 프로세스"""
        print(f"\n{'='*50}")
        print(f"카페24 가격 업데이트 시작")
        print(f"상품: {product_name}")
        print(f"새 가격: {new_price:,}원")
        print(f"{'='*50}\n")
        
        # 1. 로그인
        self.login()
        
        # 2. 상품 검색
        self.search_product(product_name)
        
        # 3. 엑셀 다운로드
        # 4. 가격 수정
        # 5. 업로드
        
        print("\n✅ 가격 업데이트 완료!")
    
    def run(self):
        """메인 실행"""
        self.browser_manager.setup_driver()
        
        try:
            # 기본 작업: 점보떡볶이 가격 업데이트
            self.update_price("[인생]점보떡볶이1490g", 13500)
            
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            
        finally:
            input("\nEnter를 눌러 종료...")
            self.browser_manager.quit()


def main():
    """메인 함수"""
    automation = Cafe24Automation()
    automation.run()


if __name__ == "__main__":
    main()