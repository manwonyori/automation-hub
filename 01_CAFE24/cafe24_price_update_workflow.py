"""
카페24 가격 업데이트 완전 자동화 워크플로우
이전에 학습한 내용을 기반으로 한 완전 자동화
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
import pandas as pd
import glob

class Cafe24PriceUpdateWorkflow:
    def __init__(self):
        self.driver = None
        self.knowledge_base = {
            "manwonyori.cafe24.com:아이디 입력란": {
                "method": "xpath",
                "value": "//input[@type='text']",
                "element_type": "2",
                "success_rate": 100
            },
            "manwonyori.cafe24.com:비밀번호 입력란": {
                "method": "xpath", 
                "value": "//input[@type='password']",
                "element_type": "2",
                "success_rate": 100
            },
            "manwonyori.cafe24.com:검색분류 드롭다운": {
                "method": "xpath",
                "value": "//th[contains(text(), '검색분류')]/following-sibling::td//select",
                "element_type": "3",
                "success_rate": 100
            },
            "manwonyori.cafe24.com:검색어 입력란": {
                "method": "xpath",
                "value": "//th[contains(text(), '검색분류')]/following-sibling::td//input[@type='text']",
                "element_type": "2", 
                "success_rate": 100
            },
            "manwonyori.cafe24.com:체크박스": {
                "method": "xpath",
                "value": "//tbody//input[@type='checkbox'][@name='product_no[]'][1]",
                "element_type": "4",
                "success_rate": 100
            },
            "manwonyori.cafe24.com:엑셀다운로드 버튼": {
                "method": "xpath",
                "value": "//a[contains(text(), '엑셀다운로드')]",
                "element_type": "1",
                "success_rate": 100
            }
        }
        self.workflow_steps = []
        self.download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        
    def setup_driver(self):
        """브라우저 설정"""
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.maximize_window()
        print("브라우저를 시작했습니다.")
        
    def log_step(self, step_name, status="시작", screenshot=False):
        """단계 로깅"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"[{timestamp}] {step_name} - {status}"
        print(message)
        self.workflow_steps.append(message)
        
        # 스크린샷 저장 옵션
        if screenshot and self.driver:
            try:
                screenshot_name = f"cafe24_{timestamp.replace(':', '-').replace(' ', '_')}_{step_name.replace(' ', '_')}.png"
                self.driver.save_screenshot(screenshot_name)
                print(f"스크린샷 저장: {screenshot_name}")
            except:
                pass
        
    def save_workflow_log(self):
        """워크플로우 로그 저장"""
        log_file = f"cafe24_workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(self.workflow_steps))
        print(f"\n워크플로우 로그 저장: {log_file}")
        
    def login(self):
        """카페24 로그인"""
        self.log_step("로그인")
        
        try:
            self.driver.get("https://manwonyori.cafe24.com/admin")
            time.sleep(2)
            
            # 알림창 처리
            try:
                alert = WebDriverWait(self.driver, 2).until(EC.alert_is_present())
                alert.accept()
                self.log_step("알림창 처리", "완료")
            except:
                pass
            
            # 아이디 입력
            id_field = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, self.knowledge_base["manwonyori.cafe24.com:아이디 입력란"]["value"]))
            )
            id_field.clear()
            id_field.send_keys("manwonyori")
            self.log_step("아이디 입력", "완료")
            
            # 비밀번호 입력
            pwd_field = self.driver.find_element(By.XPATH, self.knowledge_base["manwonyori.cafe24.com:비밀번호 입력란"]["value"])
            pwd_field.clear()
            pwd_field.send_keys("happy8263!")
            pwd_field.send_keys(Keys.RETURN)
            self.log_step("비밀번호 입력", "완료")
            
            # 로그인 완료 대기
            WebDriverWait(self.driver, 10).until(
                lambda d: "admin" in d.current_url and "login" not in d.current_url
            )
            self.log_step("로그인", "성공")
            return True
            
        except Exception as e:
            self.log_step("로그인", f"실패: {e}")
            return False
            
    def search_product(self, product_name="[인생]점보떡볶이1490g"):
        """상품 검색"""
        self.log_step(f"상품 검색: {product_name}")
        
        try:
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
            self.log_step("팝업 처리", "완료")
            
            # 검색분류 선택
            search_type_select = self.driver.find_element(By.XPATH, self.knowledge_base["manwonyori.cafe24.com:검색분류 드롭다운"]["value"])
            select = Select(search_type_select)
            
            for option in select.options:
                if "상품명" in option.text:
                    select.select_by_visible_text(option.text)
                    self.log_step("검색분류 선택", "상품명")
                    break
                    
            # 검색어 입력
            search_field = self.driver.find_element(By.XPATH, self.knowledge_base["manwonyori.cafe24.com:검색어 입력란"]["value"])
            search_field.clear()
            search_field.send_keys(product_name)
            self.log_step("검색어 입력", product_name)
            
            # 검색 실행
            self.driver.execute_script("document.querySelector('form').submit();")
            self.log_step("검색 실행", "완료")
            time.sleep(5)  # 검색 결과 로딩 대기 시간 증가
            
            # 검색 결과 확인
            try:
                results = self.driver.find_elements(By.XPATH, "//tbody//tr")
                self.log_step("검색 결과", f"{len(results)}개 항목", screenshot=True)
            except:
                self.log_step("검색 결과", "확인 실패", screenshot=True)
            
            return True
            
        except Exception as e:
            self.log_step("상품 검색", f"실패: {e}")
            return False
            
    def download_excel(self):
        """엑셀 다운로드"""
        self.log_step("엑셀 다운로드")
        
        # 다운로드 전 파일 목록 (CSV와 XLS 모두 확인)
        before_csv = set(glob.glob(os.path.join(self.download_path, "*.csv")))
        before_xls = set(glob.glob(os.path.join(self.download_path, "*.xls")))
        before_xlsx = set(glob.glob(os.path.join(self.download_path, "*.xlsx")))
        before_files = before_csv | before_xls | before_xlsx
        
        try:
            # 체크박스 선택 - 더 유연한 방법으로 시도
            checkbox_selectors = [
                "//tbody//input[@type='checkbox'][@name='product_no[]'][1]",
                "//input[@type='checkbox'][contains(@name, 'product')]",
                "//tbody//input[@type='checkbox'][1]",
                "//table//input[@type='checkbox'][1]"
            ]
            
            checkbox = None
            for selector in checkbox_selectors:
                try:
                    checkbox = self.driver.find_element(By.XPATH, selector)
                    if checkbox.is_displayed():
                        self.log_step("체크박스 찾기", f"성공: {selector}")
                        break
                except:
                    continue
                    
            if checkbox and not checkbox.is_selected():
                checkbox.click()
                self.log_step("체크박스 선택", "완료")
            elif not checkbox:
                self.log_step("체크박스", "찾을 수 없음 - 계속 진행")
                
            # 엑셀다운로드 버튼 클릭 - 다양한 선택자 시도
            excel_selectors = [
                "//a[contains(text(), '엑셀다운로드')]",
                "//a[@class='btnNormal'][contains(., '엑셀다운로드')]",
                "//button[contains(text(), '엑셀다운로드')]",
                "//a[contains(@onclick, 'excel')]",
                "//a[contains(@href, 'excel')]",
                "//img[@alt='엑셀다운로드']/..",
                "//span[contains(text(), '엑셀다운로드')]/..",
                "//a[@class='btnNormal']"
            ]
            
            excel_button = None
            for selector in excel_selectors:
                try:
                    buttons = self.driver.find_elements(By.XPATH, selector)
                    for button in buttons:
                        button_text = button.text or button.get_attribute('title') or button.get_attribute('alt') or ""
                        # 엑셀 관련 텍스트 확인 (인코딩 문제 대응)
                        if button.is_displayed() and any(keyword in button_text.lower() for keyword in ['excel', 'xls', '엑셀', '다운']):
                            excel_button = button
                            self.log_step("엑셀다운로드 버튼 찾기", f"성공: {selector}")
                            break
                    if excel_button:
                        break
                except:
                    continue
                    
            # 못 찾았으면 모든 btnNormal 클래스 버튼 확인
            if not excel_button:
                try:
                    all_buttons = self.driver.find_elements(By.XPATH, "//a[@class='btnNormal']")
                    self.log_step("btnNormal 버튼 개수", f"{len(all_buttons)}개")
                    for i, button in enumerate(all_buttons):
                        if button.is_displayed():
                            onclick = button.get_attribute('onclick') or ""
                            href = button.get_attribute('href') or ""
                            if 'excel' in onclick.lower() or 'excel' in href.lower():
                                excel_button = button
                                self.log_step("엑셀다운로드 버튼 찾기", f"성공: btnNormal[{i}]")
                                break
                except:
                    pass
                    
            if excel_button:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", excel_button)
                time.sleep(1)
                self.driver.execute_script("arguments[0].click();", excel_button)
                self.log_step("엑셀다운로드 버튼 클릭", "완료")
            else:
                # JavaScript 함수 직접 호출
                try:
                    self.driver.execute_script("product_excel_download();")
                    self.log_step("JavaScript로 엑셀다운로드 실행", "완료")
                except:
                    self.log_step("엑셀다운로드 버튼", "찾을 수 없음", screenshot=True)
                    return None
            
            # 새 창 처리
            time.sleep(2)
            if len(self.driver.window_handles) > 1:
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.log_step("새 창 전환", "완료")
                
                # 엑셀파일요청
                request_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., '엑셀파일요청')] | //a[contains(., '엑셀파일요청')]"))
                )
                request_btn.click()
                self.log_step("엑셀파일요청", "완료")
                
                # 알림창 처리
                try:
                    alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
                    alert.accept()
                except:
                    pass
                    
                # 다운로드 링크 대기
                time.sleep(5)
                self.driver.refresh()
                time.sleep(3)
                
                # 현재 페이지 확인
                self.log_step("새 창 URL", self.driver.current_url)
                
                # 다운로드 링크 찾기 - 더 다양한 방법
                download_selectors = [
                    "//a[contains(@href, 'download')]",
                    "//a[contains(text(), '다운로드')]",
                    "//img[@alt='다운로드']/..",
                    "//a[contains(@onclick, 'download')]",
                    "//td[@class='center']//a",
                    "//table//a"
                ]
                
                download_found = False
                for selector in download_selectors:
                    try:
                        links = self.driver.find_elements(By.XPATH, selector)
                        self.log_step(f"링크 확인 ({selector})", f"{len(links)}개 발견")
                        for link in links:
                            if link.is_displayed():
                                href = link.get_attribute('href') or ""
                                text = link.text or ""
                                onclick = link.get_attribute('onclick') or ""
                                
                                # 다운로드 관련 링크인지 확인
                                if any(keyword in href.lower() + text.lower() + onclick.lower() 
                                      for keyword in ['download', 'xls', 'csv', '다운']):
                                    self.log_step("다운로드 링크 정보", f"href: {href}, text: {text}")
                                    link.click()
                                    self.log_step("다운로드 링크 클릭", "완료")
                                    download_found = True
                                    break
                        if download_found:
                            break
                    except Exception as e:
                        self.log_step(f"링크 확인 오류 ({selector})", str(e))
                        
                if not download_found:
                    self.log_step("다운로드 링크", "찾을 수 없음", screenshot=True)
                        
                time.sleep(5)
                
                # 메인 창으로 돌아가기
                self.driver.switch_to.window(self.driver.window_handles[0])
                
            # 다운로드 파일 확인 (CSV와 XLS 모두 확인)
            after_csv = set(glob.glob(os.path.join(self.download_path, "*.csv")))
            after_xls = set(glob.glob(os.path.join(self.download_path, "*.xls")))
            after_xlsx = set(glob.glob(os.path.join(self.download_path, "*.xlsx")))
            after_files = after_csv | after_xls | after_xlsx
            new_files = after_files - before_files
            
            if new_files:
                downloaded_file = list(new_files)[0]
                self.log_step("파일 다운로드", f"성공: {os.path.basename(downloaded_file)}")
                return downloaded_file
            else:
                self.log_step("파일 다운로드", "실패: 파일을 찾을 수 없음")
                return None
                
        except Exception as e:
            self.log_step("엑셀 다운로드", f"실패: {e}")
            return None
            
    def modify_price(self, excel_file, new_price=13500):
        """가격 수정"""
        self.log_step(f"가격 수정: {new_price}원")
        
        try:
            # 파일 확장자에 따라 다르게 읽기
            if excel_file.endswith('.csv'):
                df = pd.read_csv(excel_file, encoding='utf-8-sig')
            elif excel_file.endswith('.xls'):
                df = pd.read_excel(excel_file, engine='xlrd')
            else:  # xlsx
                df = pd.read_excel(excel_file)
                
            self.log_step("파일 읽기", f"성공: {len(df)}개 상품")
            
            if '판매가' in df.columns:
                current_price = df.loc[0, '판매가']
                self.log_step("현재 가격", f"{current_price}원")
                
                df.loc[0, '판매가'] = new_price
                
                # 수정된 파일 저장
                modified_file = os.path.join(self.download_path, f"price_modified_{int(time.time())}.csv")
                df.to_csv(modified_file, index=False, encoding='utf-8-sig')
                self.log_step("수정된 파일 저장", modified_file)
                
                return modified_file
            else:
                self.log_step("가격 수정", "실패: '판매가' 컬럼을 찾을 수 없음")
                return None
                
        except Exception as e:
            self.log_step("가격 수정", f"실패: {e}")
            return None
            
    def run_workflow(self):
        """전체 워크플로우 실행"""
        print("\n=== 카페24 가격 업데이트 워크플로우 시작 ===")
        print(f"목표: [인생]점보떡볶이1490g 가격을 13,500원으로 변경")
        print("-" * 50)
        
        self.setup_driver()
        
        try:
            # 1. 로그인
            if not self.login():
                print("로그인 실패로 워크플로우를 중단합니다.")
                return
                
            # 2. 상품 검색
            if not self.search_product("[인생]점보떡볶이1490g"):
                print("상품 검색 실패로 워크플로우를 중단합니다.")
                return
                
            # 3. 엑셀 다운로드
            downloaded_file = self.download_excel()
            if not downloaded_file:
                print("엑셀 다운로드 실패로 워크플로우를 중단합니다.")
                return
                
            # 4. 가격 수정
            modified_file = self.modify_price(downloaded_file, 13500)
            if not modified_file:
                print("가격 수정 실패로 워크플로우를 중단합니다.")
                return
                
            # 5. 완료 메시지
            print("\n" + "=" * 50)
            print("워크플로우 완료!")
            print("=" * 50)
            print(f"\n수정된 파일: {modified_file}")
            print("\n다음 단계:")
            print("1. 카페24 관리자에서 '상품 > 상품 엑셀 관리 > 엑셀 업로드' 메뉴로 이동")
            print("2. 위 파일을 업로드하여 가격을 일괄 변경")
            print("\n주의: 업로드 전 파일 내용을 한 번 더 확인하세요!")
            
            # 워크플로우 로그 저장
            self.save_workflow_log()
            
        except Exception as e:
            print(f"\n워크플로우 실행 중 오류: {e}")
            import traceback
            traceback.print_exc()
            
        finally:
            time.sleep(10)  # 10초 대기 후 자동 종료
            self.driver.quit()
            print("\n브라우저를 닫고 종료합니다.")
            
if __name__ == "__main__":
    workflow = Cafe24PriceUpdateWorkflow()
    workflow.run_workflow()