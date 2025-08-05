"""
간단한 카페24 가격 수정 테스트
사용자와 함께 단계별로 진행
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def main():
    print("=== 카페24 가격 수정 단계별 테스트 ===")
    
    # 1. 브라우저 설정
    print("1. 브라우저 시작...")
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    
    try:
        # 2. 카페24 관리자 페이지 이동
        print("2. 카페24 관리자 페이지로 이동...")
        driver.get("https://manwonyori.cafe24.com/admin")
        time.sleep(2)
        
        # 알림창 처리 (페이지 정보보다 먼저)
        try:
            alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
            print(f"알림창 메시지: {alert.text}")
            alert.accept()
            print("알림창 확인 완료")
            time.sleep(3)
        except:
            print("알림창 없음")
        
        # 현재 페이지 정보 출력
        print(f"현재 URL: {driver.current_url}")
        print(f"페이지 제목: {driver.title}")
        
        print("\n사용자 확인이 필요합니다:")
        print("- 현재 브라우저에서 로그인 페이지가 보이나요?")
        print("- 아이디/비밀번호 입력 필드가 보이나요?")
        input("계속하려면 Enter를 누르세요...")
        
        # 3. 로그인 정보 입력
        print("3. 로그인 정보 입력...")
        
        # 아이디 입력 필드 찾기
        id_field = None
        id_selectors = [
            By.NAME, "admin_id",
            By.ID, "admin_id", 
            By.NAME, "id",
            By.XPATH, "//input[@type='text']"
        ]
        
        for selector_type, selector_value in [id_selectors[i:i+2] for i in range(0, len(id_selectors), 2)]:
            try:
                id_field = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((selector_type, selector_value))
                )
                if id_field.is_displayed():
                    print(f"아이디 필드 찾음: {selector_type} = {selector_value}")
                    break
            except:
                continue
        
        if id_field:
            id_field.clear()
            id_field.send_keys("manwonyori")
            print("아이디 입력 완료")
        else:
            print("아이디 필드를 찾을 수 없습니다. 수동으로 입력해주세요.")
            input("아이디를 수동으로 입력한 후 Enter를 누르세요...")
        
        # 비밀번호 입력
        try:
            password_field = driver.find_element(By.XPATH, "//input[@type='password']")
            password_field.clear()
            password_field.send_keys("happy8263!")
            print("비밀번호 입력 완료")
        except:
            print("비밀번호 필드를 찾을 수 없습니다. 수동으로 입력해주세요.")
            input("비밀번호를 수동으로 입력한 후 Enter를 누르세요...")
        
        print("로그인 버튼을 클릭하거나 Enter를 눌러주세요.")
        input("로그인 완료 후 Enter를 누르세요...")
        
        # 4. 관리자 페이지 진입 확인
        print("4. 관리자 페이지 진입 확인...")
        time.sleep(3)
        print(f"현재 URL: {driver.current_url}")
        
        if "admin" in driver.current_url and "login" not in driver.current_url:
            print("✅ 로그인 성공!")
        else:
            print("❌ 로그인 실패 또는 미완료")
            input("수동으로 로그인을 완료한 후 Enter를 누르세요...")
        
        # 5. 상품 관리 페이지 이동
        print("5. 상품 관리 페이지로 이동...")
        product_url = "https://manwonyori.cafe24.com/admin/php/shop1/p/product_list.php"
        driver.get(product_url)
        time.sleep(5)
        
        print(f"현재 URL: {driver.current_url}")
        print("상품 목록 페이지가 보이나요?")
        input("페이지 로딩 완료 후 Enter를 누르세요...")
        
        # 6. 상품 검색
        print("6. 상품 P00000IB 검색...")
        
        # 검색 필드 찾기
        search_field = None
        search_selectors = ["keyword", "search", "q"]
        for selector in search_selectors:
            try:
                search_field = driver.find_element(By.NAME, selector)
                if search_field.is_displayed():
                    print(f"검색 필드 찾음: {selector}")
                    break
            except:
                continue
        
        if search_field:
            search_field.clear()
            search_field.send_keys("P00000IB")
            print("검색어 입력 완료")
            
            # 검색 버튼 또는 Enter
            try:
                search_button = driver.find_element(By.XPATH, "//input[@type='submit']")
                search_button.click()
                print("검색 버튼 클릭")
            except:
                from selenium.webdriver.common.keys import Keys
                search_field.send_keys(Keys.RETURN)
                print("Enter 키로 검색")
            
            time.sleep(3)
        else:
            print("검색 필드를 찾을 수 없습니다.")
            print("수동으로 P00000IB를 검색해주세요.")
            input("검색 완료 후 Enter를 누르세요...")
        
        # 7. 상품 편집
        print("7. 상품 편집 버튼 클릭...")
        print("화면에서 P00000IB 상품의 '수정' 또는 '편집' 버튼을 찾아 클릭해주세요.")
        input("편집 페이지 진입 후 Enter를 누르세요...")
        
        # 8. 가격 수정
        print("8. 가격을 13500으로 수정...")
        print("판매가격 필드를 찾아 13500으로 변경해주세요.")
        
        # 가격 필드 자동 찾기 시도
        try:
            price_selectors = ["selling_price", "price", "product_price"]
            price_field = None
            for selector in price_selectors:
                try:
                    price_field = driver.find_element(By.NAME, selector)
                    if price_field.is_displayed():
                        print(f"가격 필드 찾음: {selector}")
                        break
                except:
                    continue
            
            if price_field:
                current_price = price_field.get_attribute("value")
                print(f"현재 가격: {current_price}")
                price_field.clear()
                price_field.send_keys("13500")
                print("새 가격 입력 완료: 13500")
            else:
                print("가격 필드를 찾을 수 없습니다. 수동으로 입력해주세요.")
        except Exception as e:
            print(f"가격 필드 처리 중 오류: {e}")
            print("수동으로 가격을 13500으로 변경해주세요.")
        
        input("가격 변경 완료 후 Enter를 누르세요...")
        
        # 9. 저장
        print("9. 변경사항 저장...")
        print("저장 버튼을 클릭해주세요.")
        input("저장 완료 후 Enter를 누르세요...")
        
        print("✅ 가격 수정 완료!")
        print("브라우저를 5초 후 닫습니다...")
        time.sleep(5)
        
    except Exception as e:
        print(f"오류 발생: {e}")
        input("문제 확인 후 Enter를 누르세요...")
    
    finally:
        driver.quit()
        print("브라우저 종료")

if __name__ == "__main__":
    main()