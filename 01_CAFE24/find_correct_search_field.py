"""
카페24 올바른 검색 필드 찾기
검색분류 드롭다운 바로 옆의 입력 필드 찾기
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

def main():
    print("=== 카페24 올바른 검색 필드 찾기 ===")
    
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
        
        # 1. 검색분류 드롭다운 찾기
        print("1. 검색분류 드롭다운 찾기...")
        search_type_select = None
        try:
            # 여러 방법으로 드롭다운 찾기
            selectors = [
                "//select[@name='search_type']",
                "//select[contains(@name, 'search')]",
                "//th[contains(text(), '검색분류')]/following-sibling::td//select",
                "//label[contains(text(), '검색분류')]/following-sibling::select"
            ]
            
            for selector in selectors:
                try:
                    search_type_select = driver.find_element(By.XPATH, selector)
                    if search_type_select.is_displayed():
                        print(f"검색분류 드롭다운 찾음: {selector}")
                        break
                except:
                    continue
            
            if search_type_select:
                # 상품명으로 변경
                select = Select(search_type_select)
                for option in select.options:
                    if "상품명" in option.text:
                        select.select_by_visible_text(option.text)
                        print("검색분류: 상품명으로 변경")
                        break
        except Exception as e:
            print(f"검색분류 변경 실패: {e}")
        
        # 2. 드롭다운 바로 옆의 입력 필드 찾기
        print("2. 검색 입력 필드 찾기...")
        search_field = None
        
        if search_type_select:
            try:
                # 방법 1: 같은 부모(td) 내의 input 찾기
                parent_td = search_type_select.find_element(By.XPATH, "./ancestor::td")
                search_field = parent_td.find_element(By.XPATH, ".//input[@type='text']")
                print("방법 1: 같은 td 내의 input 찾음")
            except:
                try:
                    # 방법 2: 드롭다운 다음 형제 요소
                    search_field = search_type_select.find_element(By.XPATH, "./following-sibling::input[@type='text']")
                    print("방법 2: following-sibling input 찾음")
                except:
                    try:
                        # 방법 3: 드롭다운 다음의 첫 번째 input
                        search_field = driver.find_element(By.XPATH, "//select[@name='search_type']/following::input[@type='text'][1]")
                        print("방법 3: following input 찾음")
                    except:
                        pass
        
        # 대체 방법들
        if not search_field:
            alternative_selectors = [
                "//input[@name='keyword']",
                "//input[@name='search_keyword']",
                "//input[@name='product_name']",
                "//th[contains(text(), '검색어')]/following-sibling::td//input",
                "//label[contains(text(), '검색어')]/following-sibling::input"
            ]
            
            for selector in alternative_selectors:
                try:
                    search_field = driver.find_element(By.XPATH, selector)
                    if search_field.is_displayed():
                        print(f"대체 방법으로 찾음: {selector}")
                        break
                except:
                    continue
        
        if search_field:
            # 검색어 입력
            search_field.clear()
            search_field.send_keys("[인생]점보떡볶이1490g")
            print("검색어 입력: [인생]점보떡볶이1490g")
            
            # 판매상태를 전체로 변경
            print("3. 판매상태를 전체로 변경...")
            try:
                selling_selects = [
                    "//select[@name='selling']",
                    "//select[@name='selling_status']",
                    "//th[contains(text(), '판매상태')]/following-sibling::td//select",
                    "//label[contains(text(), '판매상태')]/following-sibling::select"
                ]
                
                for selector in selling_selects:
                    try:
                        selling_status = driver.find_element(By.XPATH, selector)
                        if selling_status.is_displayed():
                            select_selling = Select(selling_status)
                            for option in select_selling.options:
                                if "전체" in option.text:
                                    select_selling.select_by_visible_text(option.text)
                                    print("판매상태: 전체로 변경")
                                    break
                            break
                    except:
                        continue
            except:
                print("판매상태 변경 실패")
            
            # 검색 실행
            print("4. 검색 실행...")
            # Enter 키로 검색
            search_field.send_keys(Keys.RETURN)
            time.sleep(3)
            
            print("검색 완료!")
            
            # 검색 결과 확인
            try:
                # 상품 테이블에서 점보떡볶이 찾기
                product_rows = driver.find_elements(By.XPATH, "//table[@class='boardList']//tr | //table//tr[contains(., '점보떡볶이')]")
                print(f"검색 결과: {len(product_rows)}개 상품 발견")
            except:
                print("검색 결과 확인 실패")
            
        else:
            print("ERROR: 검색 필드를 찾을 수 없습니다")
            print("페이지 구조를 확인해주세요")
        
        print("\n페이지 상태 확인을 위해 20초 대기...")
        time.sleep(20)
        
    except Exception as e:
        print(f"오류: {e}")
        import traceback
        traceback.print_exc()
        time.sleep(20)
    
    finally:
        driver.quit()
        print("브라우저 종료")

if __name__ == "__main__":
    main()