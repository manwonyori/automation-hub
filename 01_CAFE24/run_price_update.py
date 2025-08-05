"""
카페24 가격 업데이트 실행 스크립트
[인생]점보떡볶이1490g 가격을 13,500원으로 변경
"""

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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


class Cafe24PriceUpdater:
    def __init__(self):
        self.driver = None
        self.download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        
    def setup_driver(self):
        """브라우저 설정"""
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.maximize_window()
        print("✅ 브라우저 시작")
        
    def login(self):
        """카페24 로그인"""
        print("\n1️⃣ 로그인 중...")
        self.driver.get("https://manwonyori.cafe24.com/admin")
        time.sleep(2)
        
        # 알림창 처리
        try:
            alert = WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            alert.accept()
        except:
            pass
            
        # 로그인
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
        print("✅ 로그인 성공")
        
    def search_product(self, product_name):
        """상품 검색"""
        print(f"\n2️⃣ '{product_name}' 검색 중...")
        
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
                
        # 검색분류 선택
        search_type_select = self.driver.find_element(By.XPATH, "//th[contains(text(), '검색분류')]/following-sibling::td//select")
        select = Select(search_type_select)
        
        for option in select.options:
            if "상품명" in option.text:
                select.select_by_visible_text(option.text)
                print("✅ 검색분류: 상품명")
                break
                
        # 검색어 입력
        parent_td = search_type_select.find_element(By.XPATH, "./ancestor::td")
        search_field = parent_td.find_element(By.XPATH, ".//input[@type='text']")
        search_field.clear()
        search_field.send_keys(product_name)
        
        # 검색 실행
        self.driver.execute_script("document.querySelector('form').submit();")
        time.sleep(5)
        
        print("✅ 검색 완료")
        
    def download_excel(self):
        """엑셀 다운로드"""
        print("\n3️⃣ 엑셀 다운로드 중...")
        
        # 다운로드 전 파일 목록
        before_files = set(glob.glob(os.path.join(self.download_path, "*.csv")))
        before_files.update(glob.glob(os.path.join(self.download_path, "*.xls")))
        
        # 체크박스 선택
        try:
            checkbox = self.driver.find_element(By.XPATH, "//tbody//input[@type='checkbox'][1]")
            if not checkbox.is_selected():
                checkbox.click()
                print("✅ 상품 선택")
        except:
            print("⚠️ 체크박스를 찾을 수 없습니다")
            
        # 엑셀다운로드 버튼 찾기
        excel_button = None
        selectors = [
            "//a[contains(text(), '엑셀다운로드')]",
            "//a[@class='btnNormal'][contains(., '엑셀')]",
            "//span[contains(text(), '엑셀다운로드')]/.."
        ]
        
        for selector in selectors:
            try:
                buttons = self.driver.find_elements(By.XPATH, selector)
                for button in buttons:
                    if button.is_displayed():
                        excel_button = button
                        break
                if excel_button:
                    break
            except:
                continue
                
        if excel_button:
            excel_button.click()
            print("✅ 엑셀다운로드 버튼 클릭")
        else:
            # JavaScript로 시도
            try:
                self.driver.execute_script("product_excel_download();")
                print("✅ JavaScript로 다운로드 실행")
            except:
                print("❌ 엑셀다운로드 버튼을 찾을 수 없습니다")
                return None
                
        # 새 창 처리
        time.sleep(2)
        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            print("✅ 새 창으로 전환")
            
            # 엑셀파일요청
            try:
                request_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., '엑셀파일요청')] | //a[contains(., '엑셀파일요청')]"))
                )
                request_btn.click()
                print("✅ 엑셀파일요청")
                
                # 알림창 처리
                try:
                    alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
                    alert.accept()
                except:
                    pass
                    
                # 다운로드 대기
                time.sleep(5)
                self.driver.refresh()
                time.sleep(3)
                
                # 다운로드 링크 클릭
                download_links = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'download')]")
                for link in download_links:
                    if link.is_displayed():
                        link.click()
                        print("✅ 다운로드 시작")
                        break
                        
                time.sleep(5)
                
            except Exception as e:
                print(f"❌ 다운로드 실패: {e}")
                
            # 메인 창으로 돌아가기
            self.driver.switch_to.window(self.driver.window_handles[0])
            
        # 다운로드된 파일 확인
        after_files = set(glob.glob(os.path.join(self.download_path, "*.csv")))
        after_files.update(glob.glob(os.path.join(self.download_path, "*.xls")))
        new_files = after_files - before_files
        
        if new_files:
            downloaded_file = list(new_files)[0]
            print(f"✅ 다운로드 완료: {os.path.basename(downloaded_file)}")
            return downloaded_file
        else:
            print("❌ 다운로드된 파일을 찾을 수 없습니다")
            return None
            
    def modify_price(self, file_path, new_price=13500):
        """가격 수정"""
        print(f"\n4️⃣ 가격을 {new_price:,}원으로 수정 중...")
        
        try:
            # 파일 읽기
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path, encoding='utf-8-sig')
            else:
                df = pd.read_excel(file_path)
                
            print(f"✅ 파일 읽기 성공: {len(df)}개 상품")
            
            # 판매가 컬럼 찾기
            price_column = None
            for col in df.columns:
                if '판매가' in col:
                    price_column = col
                    break
                    
            if price_column:
                # 현재 가격
                current_price = df.loc[0, price_column]
                print(f"📌 현재 가격: {current_price}원")
                
                # 새 가격 설정
                df.loc[0, price_column] = new_price
                print(f"📌 새 가격: {new_price}원")
                
                # 수정된 파일 저장
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                if file_path.endswith('.csv'):
                    modified_file = os.path.join(self.download_path, f"price_updated_{timestamp}.csv")
                    df.to_csv(modified_file, index=False, encoding='utf-8-sig')
                else:
                    modified_file = os.path.join(self.download_path, f"price_updated_{timestamp}.xlsx")
                    df.to_excel(modified_file, index=False)
                    
                print(f"✅ 수정된 파일 저장: {os.path.basename(modified_file)}")
                return modified_file
                
            else:
                print("❌ '판매가' 컬럼을 찾을 수 없습니다")
                print(f"사용 가능한 컬럼: {list(df.columns)}")
                return None
                
        except Exception as e:
            print(f"❌ 파일 수정 실패: {e}")
            return None
            
    def run(self):
        """메인 실행"""
        print("\n" + "="*50)
        print("🚀 카페24 가격 업데이트 자동화 시작")
        print("="*50)
        
        self.setup_driver()
        
        try:
            # 1. 로그인
            self.login()
            
            # 2. 상품 검색
            self.search_product("[인생]점보떡볶이1490g")
            
            # 3. 엑셀 다운로드
            downloaded_file = self.download_excel()
            
            if downloaded_file:
                # 4. 가격 수정
                modified_file = self.modify_price(downloaded_file, 13500)
                
                if modified_file:
                    print("\n" + "="*50)
                    print("✅ 가격 수정 완료!")
                    print("="*50)
                    print("\n📋 다음 단계:")
                    print("1. 카페24 관리자 페이지에서")
                    print("2. [상품 > 상품 엑셀 관리 > 엑셀 업로드] 메뉴로 이동")
                    print(f"3. 수정된 파일 업로드: {os.path.basename(modified_file)}")
                    print(f"4. 파일 위치: {modified_file}")
                    
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")
            import traceback
            traceback.print_exc()
            
        finally:
            print("\n브라우저는 10초 후 자동으로 닫힙니다...")
            time.sleep(10)
            self.driver.quit()


if __name__ == "__main__":
    updater = Cafe24PriceUpdater()
    updater.run()