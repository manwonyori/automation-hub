"""
자동 가격 수정 스크립트 (단계별 로그 출력)
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
    print("=== 카페24 자동 가격 수정 시작 ===")
    
    # 브라우저 설정
    print("1. 브라우저 시작...")
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    
    try:
        # 카페24 로그인
        print("2. 카페24 로그인...")
        driver.get("https://manwonyori.cafe24.com/admin")
        time.sleep(2)
        
        # 알림창 처리
        try:
            alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
            print(f"알림창: {alert.text}")
            alert.accept()
            print("알림창 처리 완료")
            time.sleep(3)
        except:
            print("알림창 없음")
        
        print(f"현재 위치: {driver.current_url}")
        
        # 아이디 입력
        print("3. 로그인 정보 입력...")
        id_field = None
        
        # 다양한 방법으로 아이디 필드 찾기
        selectors = [
            (By.NAME, "admin_id"),
            (By.ID, "admin_id"),
            (By.NAME, "id"),
            (By.NAME, "userid"),
            (By.XPATH, "//input[@type='text']"),
            (By.CSS_SELECTOR, "input[type='text']:first-of-type")
        ]
        
        for by, selector in selectors:
            try:
                id_field = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((by, selector))
                )
                print(f"아이디 필드 찾음: {by} = {selector}")
                break
            except:
                continue
        
        if id_field:
            id_field.clear()
            id_field.send_keys("manwonyori")
            print("아이디 입력 완료")
        else:
            print("아이디 필드를 찾을 수 없습니다")
            return
        
        # 비밀번호 입력
        try:
            password_field = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))
            )
            password_field.clear()
            password_field.send_keys("happy8263!")
            print("✅ 비밀번호 입력 완료")
        except:
            print("❌ 비밀번호 필드를 찾을 수 없습니다")
            return
        
        # 로그인 버튼 클릭
        login_button = None
        button_selectors = [
            (By.XPATH, "//input[@type='submit']"),
            (By.XPATH, "//button[@type='submit']"),
            (By.XPATH, "//input[@value='로그인']"),
            (By.XPATH, "//button[contains(text(), '로그인')]")
        ]
        
        for by, selector in button_selectors:
            try:
                login_button = driver.find_element(by, selector)
                if login_button.is_displayed():
                    break
            except:
                continue
        
        if login_button:
            login_button.click()
            print("✅ 로그인 버튼 클릭")
        else:
            # Enter 키로 로그인 시도
            id_field.send_keys(Keys.RETURN)
            print("✅ Enter 키로 로그인 시도")
        
        time.sleep(5)
        
        # 로그인 확인
        if "admin" in driver.current_url and "login" not in driver.current_url:
            print("✅ 로그인 성공!")
            print(f"현재 위치: {driver.current_url}")
        else:
            print("❌ 로그인 실패")
            print(f"현재 위치: {driver.current_url}")
            return
        
        # 상품 관리 페이지로 이동
        print("4. 상품 관리 페이지로 이동...")
        product_url = "https://manwonyori.cafe24.com/admin/php/shop1/p/product_list.php"
        driver.get(product_url)
        time.sleep(5)
        
        print(f"현재 위치: {driver.current_url}")
        
        # 팝업 처리
        close_buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'close')] | //span[text()='×'] | //a[@class='close']")
        for button in close_buttons:
            try:
                if button.is_displayed():
                    button.click()
                    print("✅ 팝업 닫기")
                    time.sleep(1)
            except:
                continue
        
        # 상품 검색
        print("5. 상품 P00000IB 검색...")
        
        # 검색 필드 찾기
        search_field = None
        search_selectors = [
            (By.NAME, "keyword"),
            (By.NAME, "search"),
            (By.NAME, "q"),
            (By.ID, "keyword"),
            (By.XPATH, "//input[@type='text'][1]"),
            (By.CSS_SELECTOR, "input[type='text']:first-of-type")
        ]
        
        for by, selector in search_selectors:
            try:
                search_field = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((by, selector))
                )
                print(f"✅ 검색 필드 찾음: {by} = {selector}")
                break
            except:
                continue
        
        if search_field:
            search_field.clear()
            search_field.send_keys("P00000IB")
            print("✅ 검색어 입력: P00000IB")
            
            # 검색 실행
            try:
                search_button = driver.find_element(By.XPATH, "//input[@type='submit'] | //button[@type='submit']")
                search_button.click()
                print("✅ 검색 버튼 클릭")
            except:
                search_field.send_keys(Keys.RETURN)
                print("✅ Enter 키로 검색")
            
            time.sleep(3)
        else:
            print("❌ 검색 필드를 찾을 수 없습니다")
            print("URL 파라미터로 검색 시도...")
            search_url = f"{product_url}?keyword=P00000IB"
            driver.get(search_url)
            time.sleep(3)
        
        # 편집 버튼 찾기
        print("6. 상품 편집 버튼 찾기...")
        
        edit_button = None
        edit_selectors = [
            (By.XPATH, "//a[contains(text(), '수정')] | //a[contains(text(), '편집')]"),
            (By.XPATH, "//input[@value='수정'] | //input[@value='편집']"),
            (By.XPATH, f"//tr[contains(., 'P00000IB')]//a[contains(@href, 'modify')]"),
            (By.CSS_SELECTOR, "a[href*='product_modify']")
        ]
        
        for by, selector in edit_selectors:
            try:
                elements = driver.find_elements(by, selector)
                for element in elements:
                    if element.is_displayed():
                        edit_button = element
                        print(f"✅ 편집 버튼 찾음: {by}")
                        break
                if edit_button:
                    break
            except:
                continue
        
        if edit_button:
            driver.execute_script("arguments[0].scrollIntoView(true);", edit_button)
            time.sleep(1)
            edit_button.click()
            print("✅ 편집 버튼 클릭")
            time.sleep(5)
        else:
            print("❌ 편집 버튼을 찾을 수 없습니다")
            print("수동으로 편집 페이지에 진입해야 합니다")
            return
        
        # 가격 수정
        print("7. 가격을 13500으로 수정...")
        
        price_field = None
        price_selectors = [
            (By.NAME, "selling_price"),
            (By.NAME, "product_price"),
            (By.NAME, "price"),
            (By.XPATH, "//input[@type='text' and contains(@name, 'price')]"),
            (By.XPATH, "//td[contains(text(), '판매가')] | //td[contains(text(), '가격')]//following-sibling::td//input[@type='text']")
        ]
        
        for by, selector in price_selectors:
            try:
                price_field = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((by, selector))
                )
                current_price = price_field.get_attribute("value")
                print(f"✅ 가격 필드 찾음: {by} = {selector}")
                print(f"현재 가격: {current_price}")
                break
            except:
                continue
        
        if price_field:
            price_field.clear()
            price_field.send_keys("13500")
            print("✅ 새 가격 입력: 13500")
        else:
            print("❌ 가격 필드를 찾을 수 없습니다")
            return
        
        # 저장
        print("8. 변경사항 저장...")
        
        save_button = None
        save_selectors = [
            (By.XPATH, "//input[@type='submit' and (@value='저장' or @value='수정' or @value='확인')]"),
            (By.XPATH, "//button[contains(text(), '저장') or contains(text(), '수정')]"),
            (By.CSS_SELECTOR, "input[type='submit']"),
            (By.CSS_SELECTOR, "button[type='submit']")
        ]
        
        for by, selector in save_selectors:
            try:
                save_button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((by, selector))
                )
                print(f"✅ 저장 버튼 찾음: {by}")
                break
            except:
                continue
        
        if save_button:
            driver.execute_script("arguments[0].scrollIntoView(true);", save_button)
            time.sleep(1)
            save_button.click()
            print("✅ 저장 버튼 클릭")
            time.sleep(5)
        else:
            print("❌ 저장 버튼을 찾을 수 없습니다")
            return
        
        # 완료 확인
        current_url = driver.current_url
        if "product_list" in current_url or "success" in current_url:
            print("✅ 가격 수정 완료!")
        else:
            print("⚠️ 저장 결과 확인 필요")
            print(f"현재 위치: {current_url}")
        
        print("브라우저를 10초 후 닫습니다...")
        time.sleep(10)
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        
        print("오류 발생으로 브라우저를 20초 후 닫습니다...")
        time.sleep(20)
    
    finally:
        driver.quit()
        print("브라우저 종료")

if __name__ == "__main__":
    main()