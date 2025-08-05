"""
카페24 엑셀 업로드 빠른 실행 버전
대기 시간 최소화
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
    print("=== 카페24 엑셀 업로드 (빠른 실행) ===")
    
    # 브라우저 설정
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    
    try:
        # 카페24 로그인
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
        id_field.clear()
        id_field.send_keys("manwonyori")
        
        password_field = driver.find_element(By.XPATH, "//input[@type='password']")
        password_field.clear()
        password_field.send_keys("happy8263!")
        password_field.send_keys(Keys.RETURN)
        
        # 로그인 대기
        WebDriverWait(driver, 10).until(
            lambda d: "admin" in d.current_url and "login" not in d.current_url
        )
        print("로그인 완료")
        
        # 팝업 닫기
        close_buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'close')] | //span[text()='×']")
        for button in close_buttons[:3]:  # 최대 3개만 닫기
            try:
                if button.is_displayed():
                    button.click()
                    time.sleep(0.5)
            except:
                continue
        
        # 직접 URL로 이동 (더 빠름)
        print("엑셀 업로드 페이지로 이동...")
        excel_upload_url = "https://manwonyori.cafe24.com/admin/php/shop1/p/excel_product_upload.php"
        driver.get(excel_upload_url)
        
        # 페이지 로드 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
        
        # CSV 파일 준비
        csv_path = "C:\\Users\\8899y\\Documents\\cafe24\\price_update_jumbo.csv"
        if not os.path.exists(csv_path):
            with open(csv_path, 'w', encoding='utf-8-sig') as f:
                f.write("상품코드,판매가\n")
                f.write("P00000IB,13500\n")
            print("CSV 파일 생성")
        
        # 파일 업로드
        file_input = driver.find_element(By.XPATH, "//input[@type='file']")
        file_input.send_keys(csv_path)
        print("파일 선택 완료")
        
        # 업로드 버튼 클릭
        upload_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@value='업로드'] | //button[contains(text(), '업로드')]"))
        )
        upload_button.click()
        print("업로드 실행")
        
        # 결과 확인 (5초만 대기)
        time.sleep(5)
        
        # 완료 메시지 확인
        try:
            success_msg = driver.find_element(By.XPATH, "//*[contains(text(), '완료')] | //*[contains(text(), '성공')]")
            if success_msg.is_displayed():
                print("SUCCESS: 가격 수정 완료!")
            else:
                print("업로드 완료 (결과 확인 필요)")
        except:
            print("업로드 완료 (결과 확인 필요)")
        
        print(f"최종 URL: {driver.current_url}")
        
    except Exception as e:
        print(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 브라우저는 바로 닫지 않고 10초만 대기
        time.sleep(10)
        driver.quit()
        print("완료")

if __name__ == "__main__":
    main()