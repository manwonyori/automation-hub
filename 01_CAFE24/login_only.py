"""
카페24 로그인만 수행 후 사용자와 협의
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
    print("=== 카페24 로그인 후 협의 ===")
    
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
                    print("SUCCESS: 로그인 완료!")
                    print(f"현재 위치: {driver.current_url}")
                    
                    print("=" * 50)
                    print("로그인이 완료되었습니다!")
                    print("현재 관리자 대시보드에 있습니다.")
                    print("다음 단계를 위해 사용자의 지시를 기다립니다.")
                    print("=" * 50)
                    
                    # 사용자 협의를 위해 충분한 시간 대기
                    wait_time = 1800  # 30분
                    print(f"사용자 협의를 위해 {wait_time//60}분 대기합니다...")
                    
                    # 5분마다 상태 출력
                    for i in range(wait_time, 0, -300):
                        print(f"남은 시간: {i//60}분 - 현재 URL: {driver.current_url}")
                        time.sleep(300)
                    
                    print("대기 시간이 종료되었습니다.")
                    
                else:
                    print("ERROR: 로그인 실패")
                    print(f"현재 위치: {driver.current_url}")
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