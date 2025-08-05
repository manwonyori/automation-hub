"""
수동 보조 가격 수정 스크립트
로그인 후 사용자가 수동으로 진행할 수 있도록 도움
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
    print("=== 카페24 수동 보조 가격 수정 ===")
    print("로그인을 자동으로 처리한 후, 수동으로 가격을 수정할 수 있습니다.")
    
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
        print("2. 카페24 자동 로그인...")
        driver.get("https://manwonyori.cafe24.com/admin")
        time.sleep(2)
        
        # 알림창 처리
        try:
            alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
            print(f"알림창 처리: {alert.text}")
            alert.accept()
            time.sleep(3)
        except:
            pass
        
        # 아이디 입력
        id_field = None
        selectors = [
            (By.NAME, "admin_id"),
            (By.ID, "admin_id"),
            (By.NAME, "id"),
            (By.XPATH, "//input[@type='text']")
        ]
        
        for by, selector in selectors:
            try:
                id_field = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((by, selector))
                )
                break
            except:
                continue
        
        if id_field:
            id_field.clear()
            id_field.send_keys("manwonyori")
            print("아이디 입력 완료")
            
            # 비밀번호 입력
            try:
                password_field = driver.find_element(By.XPATH, "//input[@type='password']")
                password_field.clear()
                password_field.send_keys("happy8263!")
                print("비밀번호 입력 완료")
                
                # 로그인
                try:
                    login_button = driver.find_element(By.XPATH, "//input[@type='submit'] | //button[@type='submit']")
                    login_button.click()
                except:
                    id_field.send_keys(Keys.RETURN)
                
                time.sleep(5)
                
                if "admin" in driver.current_url and "login" not in driver.current_url:
                    print("SUCCESS: 자동 로그인 완료!")
                    print(f"현재 위치: {driver.current_url}")
                    
                    # 상품 관리 페이지로 이동
                    print("3. 상품 관리 페이지로 이동...")
                    product_url = "https://manwonyori.cafe24.com/admin/php/shop1/p/product_list.php"
                    driver.get(product_url)
                    time.sleep(5)
                    
                    print("=" * 50)
                    print("자동 로그인이 완료되었습니다!")
                    print("이제 수동으로 다음 단계를 진행해주세요:")
                    print("")
                    print("1. 브라우저에서 상품 검색창에 'P00000IB' 입력")
                    print("2. 검색 실행")
                    print("3. '[인생]점보떡볶이1490g' 상품 찾기")
                    print("4. '수정' 또는 '편집' 버튼 클릭")
                    print("5. 판매가격을 '13500'으로 변경")
                    print("6. '저장' 버튼 클릭")
                    print("")
                    print("브라우저는 5분 후 자동으로 닫힙니다.")
                    print("=" * 50)
                    
                    # 5분 대기 (수동 작업 시간)
                    wait_time = 300  # 5분
                    print(f"수동 작업을 위해 {wait_time}초 대기합니다...")
                    
                    for i in range(wait_time, 0, -30):
                        print(f"남은 시간: {i}초")
                        time.sleep(30)
                    
                    print("시간이 종료되었습니다. 브라우저를 닫습니다.")
                    
                else:
                    print("ERROR: 로그인 실패")
                    print("브라우저에서 수동으로 로그인해주세요.")
                    time.sleep(60)
                    
            except Exception as e:
                print(f"비밀번호 입력 오류: {e}")
                time.sleep(60)
        else:
            print("ERROR: 로그인 필드를 찾을 수 없습니다")
            time.sleep(60)
    
    except Exception as e:
        print(f"오류 발생: {e}")
        time.sleep(60)
    
    finally:
        try:
            driver.quit()
            print("브라우저 종료")
        except:
            pass

if __name__ == "__main__":
    main()