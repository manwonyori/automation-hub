"""
카페24 엑셀 업로드 방식으로 가격 수정
상품 > 상품 엑셀 관리 > 엑셀 업로드
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

def main():
    print("=== 카페24 엑셀 업로드 가격 수정 ===")
    
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
                    
                    # 팝업 닫기
                    print("3. 팝업 닫기...")
                    close_buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'close')] | //span[text()='×'] | //a[@class='close']")
                    for button in close_buttons:
                        try:
                            if button.is_displayed():
                                button.click()
                                print("팝업 닫기")
                                time.sleep(1)
                        except:
                            continue
                    
                    # 상품 메뉴 클릭
                    print("4. 상품 메뉴로 이동...")
                    try:
                        # 상품 메뉴 찾기
                        product_menu = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '상품')] | //span[contains(text(), '상품')]"))
                        )
                        product_menu.click()
                        time.sleep(2)
                        print("상품 메뉴 클릭 완료")
                    except Exception as e:
                        print(f"상품 메뉴 클릭 실패: {e}")
                        # URL로 직접 이동 시도
                        print("URL로 직접 이동 시도...")
                    
                    # 상품 엑셀 관리 메뉴 찾기
                    print("5. 상품 엑셀 관리 메뉴로 이동...")
                    try:
                        excel_menu = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '상품 엑셀 관리')] | //span[contains(text(), '상품 엑셀 관리')]"))
                        )
                        excel_menu.click()
                        time.sleep(2)
                        print("상품 엑셀 관리 메뉴 클릭 완료")
                    except Exception as e:
                        print(f"상품 엑셀 관리 메뉴 클릭 실패: {e}")
                    
                    # 엑셀 업로드 메뉴 찾기
                    print("6. 엑셀 업로드 메뉴로 이동...")
                    try:
                        upload_menu = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '엑셀 업로드')] | //span[contains(text(), '엑셀 업로드')]"))
                        )
                        upload_menu.click()
                        time.sleep(3)
                        print("엑셀 업로드 페이지 진입 완료")
                    except Exception as e:
                        print(f"엑셀 업로드 메뉴 클릭 실패: {e}")
                    
                    print("=" * 60)
                    print("엑셀 업로드 페이지에 도착했습니다!")
                    print("")
                    print("【수동 작업 가이드】")
                    print("1. '파일 선택' 버튼을 클릭")
                    print("2. 가격 수정 엑셀 파일 선택")
                    print("   - 상품코드: P00000IB")
                    print("   - 판매가: 13500")
                    print("3. '업로드' 버튼 클릭")
                    print("4. 업로드 완료 확인")
                    print("")
                    print("CSV 파일 위치:")
                    print("C:\\Users\\8899y\\Documents\\cafe24\\price_update_sample_jumbo.csv")
                    print("=" * 60)
                    
                    # CSV 파일 확인
                    csv_path = "C:\\Users\\8899y\\Documents\\cafe24\\price_update_sample_jumbo.csv"
                    if os.path.exists(csv_path):
                        print(f"CSV 파일 확인됨: {csv_path}")
                    else:
                        print("CSV 파일이 없습니다. 생성 중...")
                        # CSV 파일 생성
                        with open(csv_path, 'w', encoding='utf-8-sig') as f:
                            f.write("상품코드,판매가\n")
                            f.write("P00000IB,13500\n")
                        print("CSV 파일 생성 완료")
                    
                    # 파일 업로드 필드 찾기
                    print("7. 파일 업로드 시도...")
                    try:
                        file_input = driver.find_element(By.XPATH, "//input[@type='file']")
                        file_input.send_keys(csv_path)
                        print("파일 선택 완료")
                        
                        # 업로드 버튼 찾기
                        upload_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//input[@value='업로드'] | //button[contains(text(), '업로드')]"))
                        )
                        upload_button.click()
                        print("업로드 버튼 클릭")
                        time.sleep(5)
                        
                        print("SUCCESS: 엑셀 업로드 완료!")
                    except Exception as e:
                        print(f"자동 업로드 실패: {e}")
                        print("수동으로 파일을 업로드해주세요.")
                    
                    # 10분 대기
                    wait_time = 600
                    print(f"작업 확인을 위해 {wait_time//60}분 대기합니다...")
                    
                    for i in range(wait_time, 0, -60):
                        print(f"남은 시간: {i//60}분")
                        time.sleep(60)
                    
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
        import traceback
        traceback.print_exc()
        time.sleep(60)
    
    finally:
        try:
            driver.quit()
            print("브라우저 종료")
        except:
            pass

if __name__ == "__main__":
    main()