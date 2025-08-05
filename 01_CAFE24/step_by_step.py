"""
카페24 가격 수정 - 단계별 협력 방식
자동 로그인 후 사용자가 수동으로 진행
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
    print("=== 카페24 가격 수정 (단계별 협력) ===")
    print("자동으로 로그인한 후, 사용자가 수동으로 가격을 수정합니다.")
    
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
                    
                    print("=" * 60)
                    print("자동 로그인이 완료되었습니다!")
                    print("이제 수동으로 다음 단계를 진행해주세요:")
                    print("")
                    print("【단계별 가이드】")
                    print("1. 상품 검색창에 'P00000IB' 입력")
                    print("2. 검색 버튼 클릭 또는 Enter")
                    print("3. '[인생]점보떡볶이1490g' 상품 찾기")
                    print("4. '수정' 버튼 클릭")
                    print("5. 판매가격을 '13500'으로 변경")
                    print("6. '저장' 버튼 클릭")
                    print("")
                    print("목표: 12,600원 → 13,500원 가격 변경")
                    print("=" * 60)
                    
                    # 10분 대기 (충분한 작업 시간)
                    wait_time = 600  # 10분
                    print(f"수동 작업을 위해 {wait_time//60}분 대기합니다...")
                    
                    # 1분마다 상태 출력
                    for i in range(wait_time, 0, -60):
                        print(f"남은 시간: {i//60}분 {i%60}초")
                        time.sleep(60)
                    
                    print("시간이 종료되었습니다.")
                    
                else:
                    print("ERROR: 로그인 실패")
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