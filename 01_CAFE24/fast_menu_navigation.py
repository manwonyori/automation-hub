"""
카페24 메뉴 네비게이션으로 엑셀 업로드
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
    print("=== 카페24 메뉴 네비게이션 ===")
    
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
        
        # 팝업 빠르게 닫기
        for i in range(3):
            try:
                close_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'close')] | //span[text()='×']")
                close_btn.click()
                time.sleep(0.3)
            except:
                break
        
        # 메뉴 네비게이션
        print("메뉴 네비게이션 시작...")
        
        # 1. 상품 메뉴 클릭
        try:
            # 여러 선택자 시도
            selectors = [
                "//a[contains(., '상품') and not(contains(., '상품 엑셀'))]",
                "//span[contains(., '상품') and not(contains(., '상품 엑셀'))]",
                "//div[contains(., '상품') and not(contains(., '상품 엑셀'))]",
                "//*[@class='menu' and contains(., '상품')]"
            ]
            
            for selector in selectors:
                try:
                    product_menu = driver.find_element(By.XPATH, selector)
                    if product_menu.is_displayed():
                        product_menu.click()
                        print("상품 메뉴 클릭")
                        time.sleep(1)
                        break
                except:
                    continue
        except:
            print("상품 메뉴 찾기 실패")
        
        # 2. 상품 엑셀 관리 클릭
        try:
            excel_menu = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(., '상품 엑셀 관리')] | //span[contains(., '상품 엑셀 관리')]"))
            )
            excel_menu.click()
            print("상품 엑셀 관리 클릭")
            time.sleep(1)
        except:
            print("상품 엑셀 관리 찾기 실패")
        
        # 3. 엑셀 업로드 클릭
        try:
            upload_menu = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(., '엑셀 업로드')] | //span[contains(., '엑셀 업로드')]"))
            )
            upload_menu.click()
            print("엑셀 업로드 클릭")
            time.sleep(2)
        except:
            print("엑셀 업로드 찾기 실패")
        
        print(f"현재 URL: {driver.current_url}")
        
        # CSV 파일 생성
        csv_path = "C:\\Users\\8899y\\Documents\\cafe24\\price_update_jumbo.csv"
        with open(csv_path, 'w', encoding='utf-8-sig') as f:
            f.write("상품코드,판매가\n")
            f.write("P00000IB,13500\n")
        print(f"CSV 파일 생성: {csv_path}")
        
        # 파일 업로드 시도
        try:
            file_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
            )
            file_input.send_keys(csv_path)
            print("파일 선택 완료")
            
            # 업로드 버튼
            upload_btn = driver.find_element(By.XPATH, "//input[@value='업로드'] | //button[contains(., '업로드')]")
            upload_btn.click()
            print("업로드 클릭")
            
            time.sleep(3)
            print("업로드 완료!")
        except Exception as e:
            print(f"업로드 실패: {e}")
            print("수동으로 진행해주세요")
        
        # 결과 확인용 10초 대기
        print("결과 확인중...")
        time.sleep(10)
        
    except Exception as e:
        print(f"오류: {e}")
        time.sleep(10)
    
    finally:
        driver.quit()
        print("완료")

if __name__ == "__main__":
    main()