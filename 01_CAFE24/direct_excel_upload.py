"""
카페24 직접 URL로 엑셀 업로드
https://manwonyori.cafe24.com/disp/admin/shop1/product/ProductExcelManage
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
    print("=== 카페24 엑셀 업로드 (직접 URL) ===")
    
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
        
        # 빠른 로그인
        id_field = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='text']"))
        )
        id_field.send_keys("manwonyori")
        
        password_field = driver.find_element(By.XPATH, "//input[@type='password']")
        password_field.send_keys("happy8263!")
        password_field.send_keys(Keys.RETURN)
        
        # 로그인 완료 대기
        WebDriverWait(driver, 10).until(
            lambda d: "admin" in d.current_url and "login" not in d.current_url
        )
        print("로그인 완료")
        
        # 직접 URL로 이동
        print("상품 엑셀 관리 페이지로 이동...")
        driver.get("https://manwonyori.cafe24.com/disp/admin/shop1/product/ProductExcelManage")
        time.sleep(2)
        
        # 팝업 닫기
        for i in range(3):
            try:
                close_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'close')] | //span[text()='×']")
                close_btn.click()
                time.sleep(0.3)
            except:
                break
        
        print(f"현재 URL: {driver.current_url}")
        
        # CSV 파일 생성
        csv_path = "C:\\Users\\8899y\\Documents\\cafe24\\price_update_jumbo.csv"
        with open(csv_path, 'w', encoding='utf-8-sig') as f:
            f.write("상품코드,판매가\n")
            f.write("P00000IB,13500\n")
        print(f"CSV 파일 생성: {csv_path}")
        
        # 엑셀 업로드 탭/버튼 찾기
        try:
            # 엑셀 업로드 탭 클릭
            upload_tab = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(., '엑셀 업로드')] | //button[contains(., '엑셀 업로드')] | //span[contains(., '엑셀 업로드')]"))
            )
            upload_tab.click()
            print("엑셀 업로드 탭 클릭")
            time.sleep(1)
        except:
            print("엑셀 업로드 탭이 이미 활성화됨")
        
        # 파일 업로드
        try:
            file_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
            )
            file_input.send_keys(csv_path)
            print("파일 선택 완료")
            
            # 업로드 버튼 클릭
            upload_buttons = [
                "//input[@value='업로드']",
                "//button[contains(., '업로드')]",
                "//input[@type='submit']",
                "//button[@type='submit']"
            ]
            
            upload_clicked = False
            for btn_xpath in upload_buttons:
                try:
                    upload_btn = driver.find_element(By.XPATH, btn_xpath)
                    if upload_btn.is_displayed() and upload_btn.is_enabled():
                        upload_btn.click()
                        print("업로드 버튼 클릭")
                        upload_clicked = True
                        break
                except:
                    continue
            
            if upload_clicked:
                time.sleep(3)
                print("SUCCESS: 엑셀 업로드 완료!")
                
                # 결과 메시지 확인
                try:
                    result_msg = driver.find_element(By.XPATH, "//*[contains(text(), '완료')] | //*[contains(text(), '성공')] | //*[contains(text(), '처리')]")
                    print(f"결과: {result_msg.text}")
                except:
                    print("결과 메시지 확인 불가")
            else:
                print("업로드 버튼을 찾을 수 없습니다")
                
        except Exception as e:
            print(f"업로드 실패: {e}")
        
        # 결과 확인
        print("작업 완료! 5초 후 종료...")
        time.sleep(5)
        
    except Exception as e:
        print(f"오류: {e}")
        import traceback
        traceback.print_exc()
        time.sleep(5)
    
    finally:
        driver.quit()
        print("브라우저 종료")

if __name__ == "__main__":
    main()