"""
카페24 상품 직접 편집
P00000IB 상품을 찾아서 수정 페이지로 진입
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

def main():
    print("=== 카페24 P00000IB 상품 직접 수정 ===")
    
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    
    try:
        # 로그인
        driver.get("https://manwonyori.cafe24.com/admin")
        
        # 알림창 처리
        try:
            alert = WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert.accept()
        except:
            pass
        
        # 로그인
        id_field = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='text']"))
        )
        id_field.send_keys("manwonyori")
        
        password_field = driver.find_element(By.XPATH, "//input[@type='password']")
        password_field.send_keys("happy8263!")
        password_field.send_keys(Keys.RETURN)
        
        WebDriverWait(driver, 10).until(
            lambda d: "admin" in d.current_url and "login" not in d.current_url
        )
        print("로그인 완료")
        
        # 상품관리 페이지로 이동
        print("상품관리 페이지로 이동...")
        driver.get("https://manwonyori.cafe24.com/disp/admin/shop1/product/productmanage")
        time.sleep(3)
        
        # 팝업 닫기
        for i in range(3):
            try:
                close_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'close')] | //span[text()='×']")
                close_btn.click()
                time.sleep(0.3)
            except:
                break
        
        # P00000IB 검색
        print("P00000IB 상품 검색...")
        
        # 검색어 입력
        search_field = driver.find_element(By.XPATH, "//input[@name='keyword'] | //input[@type='text'][1]")
        search_field.clear()
        search_field.send_keys("P00000IB")
        search_field.send_keys(Keys.RETURN)
        time.sleep(3)
        
        print("상품 찾는 중...")
        
        # 상품 행 찾기 - 여러 방법 시도
        product_found = False
        
        # 방법 1: 상품코드로 직접 찾기
        try:
            product_row = driver.find_element(By.XPATH, "//tr[contains(., 'P00000IB')]")
            if product_row:
                print("상품 행 발견")
                
                # 수정 버튼 찾기
                edit_links = [
                    ".//a[contains(., '수정')]",
                    ".//a[contains(., '편집')]",
                    ".//a[contains(@href, 'product_modify')]",
                    ".//a[contains(@href, 'ProductRegister')]",
                    ".//button[contains(., '수정')]"
                ]
                
                for link_xpath in edit_links:
                    try:
                        edit_btn = product_row.find_element(By.XPATH, link_xpath)
                        edit_btn.click()
                        product_found = True
                        print("수정 버튼 클릭")
                        break
                    except:
                        continue
        except:
            print("상품 행을 찾을 수 없습니다")
        
        # 방법 2: 상품명으로 찾기
        if not product_found:
            try:
                # 점보떡볶이 텍스트로 찾기
                product_link = driver.find_element(By.XPATH, "//a[contains(., '점보떡볶이')] | //a[contains(., '점보')]")
                product_link.click()
                product_found = True
                print("상품명 클릭으로 진입")
            except:
                print("상품명 링크를 찾을 수 없습니다")
        
        if not product_found:
            print("상품을 찾을 수 없습니다")
            print("수동으로 진행해주세요")
            time.sleep(30)
            return
        
        # 수정 페이지 로드 대기
        time.sleep(5)
        print(f"현재 URL: {driver.current_url}")
        
        # 가격 필드 찾기
        print("가격 필드 찾는 중...")
        
        price_fields = [
            "//input[@name='product_price']",
            "//input[@name='selling_price']",
            "//input[@name='price']",
            "//input[contains(@name, 'price')][@type='text']",
            "//input[@id='product_price']",
            "//input[@id='selling_price']"
        ]
        
        price_field = None
        for field_xpath in price_fields:
            try:
                fields = driver.find_elements(By.XPATH, field_xpath)
                for field in fields:
                    if field.is_displayed() and field.get_attribute('value'):
                        price_field = field
                        current_price = field.get_attribute('value')
                        print(f"가격 필드 발견 - 현재 가격: {current_price}")
                        break
                if price_field:
                    break
            except:
                continue
        
        if price_field:
            # 가격 수정
            price_field.clear()
            price_field.send_keys("13500")
            print("새 가격 입력: 13500")
            
            # 저장 버튼 찾기
            print("저장 버튼 찾는 중...")
            
            save_buttons = [
                "//button[contains(., '저장')]",
                "//input[@value='저장']",
                "//button[contains(., '수정')]",
                "//input[@value='수정']",
                "//button[@type='submit']",
                "//input[@type='submit']"
            ]
            
            for btn_xpath in save_buttons:
                try:
                    save_btn = driver.find_element(By.XPATH, btn_xpath)
                    if save_btn.is_displayed():
                        # 스크롤해서 보이게 하기
                        driver.execute_script("arguments[0].scrollIntoView(true);", save_btn)
                        time.sleep(1)
                        save_btn.click()
                        print("저장 버튼 클릭")
                        break
                except:
                    continue
            
            time.sleep(5)
            print("SUCCESS: 가격 수정 완료!")
            
            # 확인 알림 처리
            try:
                alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
                alert_text = alert.text
                print(f"알림: {alert_text}")
                alert.accept()
            except:
                pass
                
        else:
            print("가격 필드를 찾을 수 없습니다")
            print("페이지 구조를 확인해주세요")
        
        print("\n10초 후 종료...")
        time.sleep(10)
        
    except Exception as e:
        print(f"오류: {e}")
        import traceback
        traceback.print_exc()
        time.sleep(10)
    
    finally:
        driver.quit()
        print("브라우저 종료")

if __name__ == "__main__":
    main()