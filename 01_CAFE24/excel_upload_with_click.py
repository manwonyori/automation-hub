"""
카페24 엑셀 업로드 - 선택 버튼 클릭 방식
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
    print("=== 카페24 엑셀 업로드 (선택 버튼 클릭) ===")
    
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
        
        # 엑셀 업로드 탭 클릭
        try:
            upload_tab = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(., '엑셀 업로드')] | //button[contains(., '엑셀 업로드')] | //span[contains(., '엑셀 업로드')]"))
            )
            upload_tab.click()
            print("엑셀 업로드 탭 클릭")
            time.sleep(1)
        except:
            print("엑셀 업로드 탭 찾기 실패 또는 이미 활성화")
        
        # "선택" 버튼 찾기
        try:
            select_buttons = [
                "//button[contains(., '선택')]",
                "//input[@value='선택']",
                "//a[contains(., '선택')]",
                "//span[contains(., '선택')]",
                "//button[contains(., '파일 선택')]",
                "//input[@value='파일 선택']",
                "//label[contains(., '선택')]"
            ]
            
            select_clicked = False
            for btn_xpath in select_buttons:
                try:
                    select_btn = driver.find_element(By.XPATH, btn_xpath)
                    if select_btn.is_displayed():
                        # JavaScript로 클릭 (더 안정적)
                        driver.execute_script("arguments[0].click();", select_btn)
                        print("선택 버튼 클릭")
                        select_clicked = True
                        time.sleep(1)
                        break
                except:
                    continue
            
            if not select_clicked:
                print("선택 버튼을 찾을 수 없음, file input 직접 찾기")
        except:
            pass
        
        # 파일 input 찾기
        try:
            # 여러 방법으로 file input 찾기
            file_inputs = driver.find_elements(By.XPATH, "//input[@type='file']")
            
            if file_inputs:
                for file_input in file_inputs:
                    try:
                        # 숨겨진 input일 수 있으므로 JavaScript로 처리
                        driver.execute_script("arguments[0].style.display = 'block';", file_input)
                        file_input.send_keys(csv_path)
                        print("파일 선택 완료")
                        break
                    except:
                        continue
            else:
                print("파일 input을 찾을 수 없습니다")
        except Exception as e:
            print(f"파일 선택 실패: {e}")
        
        # 엑셀 업로드 버튼 클릭
        try:
            upload_buttons = [
                "//button[contains(., '엑셀업로드')]",
                "//button[contains(., '엑셀 업로드')]",
                "//input[@value='엑셀업로드']",
                "//input[@value='엑셀 업로드']",
                "//button[contains(., '업로드')]",
                "//input[@value='업로드']",
                "//input[@type='submit']",
                "//button[@type='submit']"
            ]
            
            for btn_xpath in upload_buttons:
                try:
                    upload_btn = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.XPATH, btn_xpath))
                    )
                    upload_btn.click()
                    print("엑셀 업로드 버튼 클릭")
                    break
                except:
                    continue
            
            time.sleep(3)
            print("업로드 처리 중...")
            
            # 결과 확인
            try:
                result_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '완료')] | //*[contains(text(), '성공')] | //*[contains(text(), '처리')]")
                for elem in result_elements:
                    if elem.is_displayed():
                        print(f"결과: {elem.text}")
                        break
            except:
                pass
                
        except Exception as e:
            print(f"업로드 버튼 클릭 실패: {e}")
        
        print("작업 완료! 10초 후 종료...")
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